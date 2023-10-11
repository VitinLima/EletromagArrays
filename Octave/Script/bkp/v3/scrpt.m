clear;
close all;
clc;

a=181; %resolução angular
thetaScanAngles = linspace(0,pi,a);
phiScanAngles = linspace(-pi/2,pi/2,a);
thetaSteerAngle = 90;
phiSteerAngle = 0;
elementWeights = [1,1,1];
theta=0:0.01:2*pi;
[THETA,PHI]= meshgrid(thetaScanAngles,phiScanAngles);
%matriz característica das antenas em cada uma de suas coordenadas
Xpos = [1,2,3];
Ypos = [0,0,0];
Zpos = [0,0,0];
%Número de onda
f = 4.33e8;
c = 299792458; % <= Correção na velocidade da luz
k = 2*pi*f/c;
dtheta=pi/a;
dphi=pi/a;
%Número de elementos do arranjo
P = length(Xpos);
%Considerando coordenadas esféricas temos que:
%O tamanho dos vetores que contem os ângulo de escaneamento
M = length(thetaScanAngles);
N = length(phiScanAngles);
%Calculando as coordenadas
u = sin(thetaScanAngles)'*cos(phiScanAngles);
v = sin(thetaScanAngles)'*sin(phiScanAngles);
w = repmat(cos(thetaScanAngles)', 1, N);
% Applicando a rotação
us = u - sin(thetaSteerAngle)*cos(phiSteerAngle);
vs = v - sin(thetaSteerAngle)*sin(phiSteerAngle);
ws = w - cos(thetaSteerAngle);
%Calculando o fator de arranjo
uu = bsxfun(@times, us, reshape(Xpos, 1, 1, P));
vv = bsxfun(@times, vs, reshape(Ypos, 1, 1, P));
ww = bsxfun(@times, ws, reshape(Zpos, 1, 1, P));
g = repmat(reshape(elementWeights, 1, 1, P), M, N);
AF = sum(g.*exp(1j*k*(uu + vv + ww)),3);

%Diretividade
figure;
hold on;
AFmag = abs(AF);
Utheta = AFmag.^2;
Prad=sum(sum(Utheta.*sin(THETA)*dtheta*dphi));
D = 4*pi*Utheta/Prad;
DdB = 20.*log10(D);
%plotar em ângulo
subplot(2,1,1),polar(thetaScanAngles,AFmag(:,phiScanAngles==0));
title('Eixo polar E do arranjo de antena normalizado');
AFdb = 20*log10(AFmag);
AFplot=(AFdb + abs(AFdb))/2;
subplot(2,1,2),polar(thetaScanAngles,AFplot(:,phiScanAngles==0));
title('Eixo polar E do arranjo de antena normalizado em db');
FNBW=(180/pi)*2*(pi/2-acos(D));
HPBW=(180/pi)*2*(pi/2-acos(1.391*D/pi));
FSLBW=(180/pi)*2*(pi/2-acos(1.5*D));

%visualizando
figure;
hold on;
surf(PHI,THETA,AFmag);
shading interp;
##colormap('padrão');
colormap( 'default');
xlabel( '\phi [deg]','fontsize',15);
set(gca,'XTicklabel',{'-90','-60','-30','0','30','60','90'},'fontsize',15,'fontweight','bold','box','on');
ylabel('\theta [deg]','fontsize',15);
set(gca,'YTicklabel',{'180','150','120','90','60','30','0'},'fontsize',15,'fontweight','bold','box','on');
axis([-pi/2,pi/2,0,pi,-Inf,Inf]);
zlabel( 'AFmag','FontSize',15);
title('AFmag');

%Gráfico 3d da diretividade
figure;
surf(PHI,THETA,D);
shading interp;
colormap( 'default');
xlabel( '\phi [deg]','fontsize',15);
set(gca,'XTicklabel',{'-90','-60','-30','0','30','60','90'},'fontsize',15,'fontweight','bold','box','on');
ylabel('\theta [deg]','fontsize',15);
set(gca,'YTicklabel',{'180','150','120','90','60','30','0'},'fontsize',15,'fontweight','bold','box','on');
axis([-pi/2,pi/2,0,pi,-Inf,Inf]);
zlabel( 'Diretividade','FontSize',15);
title('Diretividade em função de \theta e \phi','FontSize',20);
%Dois cortes para a visualização dos ângulos de diretividade máxima.
Domax=max(max(DdB));
[x,y] = find(DdB==Domax,1);
Do_theta = DdB(x,:);
Do_phi=DdB(:,y);

figure;
hold on;
subplot(2,1,1),line(thetaScanAngles,Do_theta, 'LineWidth',2.5);
axis([0,pi,-Inf,inf]);
txt = ['D for \phi = ', num2str(rad2deg(phiScanAngles(y)),3), ' [deg]'];
legend(txt);
text(.0,.8, ['Diretividade máxima ', num2str(Domax,3), ' [deg]']);
##t2=text(1,1,['D_0 =', num2str(Domax),'(dB)']);
##set(t2,'units','normalized','position',[ll.05],'HorizontalAlign','right','FontSize',15,'FontWeight','Bold');
set(gca,'XTick', 0:pi/6:pi);
set(gca,'XTickLabel',{'0','30','60','90','120','150','180'},'fontsize',15,'fontweight','bold');
grid on;
xlabel('\theta [deg]','fontsize',15);
ylabel('Diretividade (dB)','FontSize',15)
title('Diretividade em \theta', 'FontSize',20);
subplot(2,1,2),line(phiScanAngles,Do_phi, 'LineWidth',2.5);
axis([-pi/2,pi/2,-Inf,Inf]);
txt = ['D for \theta = ', num2str(rad2deg(thetaScanAngles(x)),3), ' [deg]'];
legend(txt);
##t3=text(1,1,['D_0 =', num2str(Domax),'(dB)']);
##set(t3,'units','normalized','position',[l l.05],'HorizontalAlign','right','FontSize',15,'FontWeight','Bold');
set(gca,'XTick',-pi/2:pi/6:pi/2);
set(gca,'XTickLabel',{'-90','-60','-30','0','30','60','90'},'fontsize',15,'fontweight','bold');
grid on;
xlabel('\phi [deg]','fontsize',15);
ylabel('Diretividade (dB)','FontSize',15);
title('Diretividade em \phi', 'FontSize',20);
