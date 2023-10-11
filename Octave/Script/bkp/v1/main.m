

return;

%Fator de fase
##stcp = sin(thetaScanAngles)'.*cos(phiScanAngles);
##stsp = sin(thetaScanAngles)'.*sin(phiScanAngles);
##ct = repmat(cos(thetaScanAngles)', 1, N);
##
##AF = zeros(M, N);
##for i = 1:rows(P)
##  FF = k*(P(i,1)*stcp + P(i,2)*stsp + P(i,3)*ct);
##  AF += modI(i)*cos(phaseI(i))*cos(FF);
##end

##%Calculando as coordenadas
##u = sin(thetaScanAngles)'*cos(phiScanAngles);
##v = sin(thetaScanAngles)'*sin(phiScanAngles);
##w = repmat(cos(thetaScanAngles)', 1, N);
##
##% Applicando a rotação
##us = u - sin(thetaSteerAngle)*cos(phiSteerAngle);
##vs = v - sin(thetaSteerAngle)*sin(phiSteerAngle);
##ws = w - cos(thetaSteerAngle);
##
##%Calculando o fator de arranjo
##uu = bsxfun(@times, us, reshape(Xpos, 1, 1, P));
##vv = bsxfun(@times, vs, reshape(Ypos, 1, 1, P));
##ww = bsxfun(@times, ws, reshape(Zpos, 1, 1, P));
##g = repmat(reshape(elementWeights, 1, 1, P), M, N);
##AF = sum(g.exp(1j*k(uu + vv + ww)),3); % "Fator de Arranjo"

## Resolução do eixo X para graficos (mude o valor para ver o que faz,
##  números ímpares tem melhores resultados)
Nx=7;

%Diretividade
figure('visible', showImages);
hold on;
AFmag = abs(AF);
Utheta = AFmag.^2;
Prad=sum(sum(Utheta.*sin(THETA)*dtheta*dphi));
D = 4*pi*Utheta/Prad;
DdB = 20.*log10(D);
%plotar em ?ngulo
subplot(2,1,1),polar(thetaScanAngles,AFmag(:,phiScanAngles==0));
grid on;
title('Eixo polar E do arranjo de antena normalizado');
AFdb = 20*log10(AFmag);
AFplot=(AFdb + abs(AFdb))/2;
subplot(2,1,2),polar(thetaScanAngles,AFplot(:,phiScanAngles==0));
grid on;
title('Eixo polar E do arranjo de antena normalizado em db');
##FNBW=(180/pi)2(pi/2-acos(D));
##HPBW=(180/pi)2(pi/2-acos(1.391*D/pi));
##FSLBW=(180/pi)2(pi/2-acos(1.5*D));

%visualizando
figure('visible', showImages);
hold on;
surf(PHI,THETA,AFmag);
shading interp;
##colormap('padr?o');
colormap( 'default');
xlabel( '\phi [deg]','fontsize',15);
set(gca,'XTicklabel',{'-90','-60','-30','0','30','60','90'},'fontsize',15,'fontweight','bold','box','on');
ylabel('\theta [deg]','fontsize',15);
set(gca,'YTicklabel',{'180','150','120','90','60','30','0'},'fontsize',15,'fontweight','bold','box','on');
axis([-pi/2,pi/2,0,pi,-Inf,Inf]);
zlabel( 'AFmag','FontSize',15);
title('AFmag');

%Gráfico 3d da diretividade
figure('visible', showImages);
hold on;
surf(PHI,THETA,D);
shading interp;
colormap( 'default');
xlabel( '\phi [deg]','fontsize',15);
set(gca,'XTicklabel',{'-90','-60','-30','0','30','60','90'},'fontsize',15,'fontweight','bold','box','on');
ylabel('\theta [deg]','fontsize',15);
set(gca,'YTicklabel',{'180','150','120','90','60','30','0'},'fontsize',15,'fontweight','bold','box','on');
axis([-pi/2,pi/2,0,pi,-Inf,Inf]);
zlabel( 'Diretividade','FontSize',15);
title('Diretividade em fun??o de \theta e \phi','FontSize',20);
%Dois cortes para a visualização dos ângulos de diretividade máxima.
Domax=max(max(DdB));
[x,y] = find(DdB==Domax,1);
Do_theta = DdB(x,:);
Do_phi=DdB(:,y);

figure('visible', showImages);
hold on;
subplot(2,1,1),line(rad2deg(phiScanAngles),Do_theta, 'LineWidth',2.5);
txt = ['D for \theta = ', num2str(rad2deg(thetaScanAngles(x)),3), ' [deg]'];
legend(txt);
text(-30,-10, ['Diretividade m?xima ', num2str(Domax,3), ' [db]']);
##t2=text(1,1,['D_0 =', num2str(Domax),'(dB)']);
##set(t2,'units','normalized','position',[ll.05],'HorizontalAlign','right','FontSize',15,'FontWeight','Bold');
minDx = rad2deg(min(phiScanAngles));
maxDx = rad2deg(max(phiScanAngles));
Dx = linspace(minDx,maxDx,Nx);
axis([minDx,maxDx,-Inf,Inf]);
set(gca,'XTick',Dx,'XTickLabel',strsplit(num2str(Dx,3)),'fontsize',15,'fontweight','bold');
grid on;
xlabel('\phi [deg]','fontsize',15);
ylabel('Diretividade (dB)','FontSize',15);
title('Diretividade em \phi', 'FontSize',20);

subplot(2,1,2),line(rad2deg(thetaScanAngles),Do_phi, 'LineWidth',2.5);
txt = ['D for \phi = ', num2str(rad2deg(phiScanAngles(y)),3), ' [deg]'];
legend(txt);
##t3=text(1,1,['D_0 =', num2str(Domax),'(dB)']);
##set(t3,'units','normalized','position',[l l.05],'HorizontalAlign','right','FontSize',15,'FontWeight','Bold');
minDx = rad2deg(min(thetaScanAngles));
maxDx = rad2deg(max(thetaScanAngles));
Dx = linspace(minDx,maxDx,Nx);
axis([minDx,maxDx,-Inf,Inf]);
set(gca,'XTick',Dx,'XTickLabel',strsplit(num2str(Dx,3)),'fontsize',15,'fontweight','bold');
grid on;
xlabel('\theta [deg]','fontsize',15);
ylabel('Diretividade (dB)','FontSize',15)
title('Diretividade em \theta', 'FontSize',20);