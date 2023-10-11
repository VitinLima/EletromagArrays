clear;
close all;
clc;

  % resoluÃ§Ã£o angular
  a=181;
  thetaScanAngles = linspace(0,pi,a);
  phiScanAngles = linspace(-pi,pi,a);
  thetaSteerAngle = 90;
  phiSteerAngle = 0;
  elementWeights = [1,1,1];
  theta=0:0.01:2*pi;
  [THETA,PHI]= meshgrid(thetaScanAngles,phiScanAngles);

  % matriz caracterÃ­stica das antenas em cada uma de suas coordenadas
  Xpos = [1,2,3];
  Ypos = [0,0,0];
  Zpos = [0,0,0];

  % NÃºmero de onda
  f = 4.33e8;
  c = 299792458; % <= CorreÃ§Ã£o na velocidade da luz
  k = 2*pi*f/c;
  dtheta=pi/a;
  dphi=pi/a;

  % NÃºmero de elementos do arranjo
  P = length(Xpos);


%---------Considerando coordenadas esfÃ©ricas temos que:---------

  % O tamanho dos vetores que contem os Ã¢ngulo de escaneamento
  M = length(thetaScanAngles);
  N = length(phiScanAngles);

  % Calculando as coordenadas
  u = sin(thetaScanAngles)'*cos(phiScanAngles);
  v = sin(thetaScanAngles)'*sin(phiScanAngles);
  w = repmat(cos(thetaScanAngles)', 1, N);

  % Applicando a rotaÃ§Ã£o
  us = u - sin(thetaSteerAngle)*cos(phiSteerAngle);
  vs = v - sin(thetaSteerAngle)*sin(phiSteerAngle);
  ws = w - cos(thetaSteerAngle);

  % Calculando o fator de arranjo
  uu = bsxfun(@times, us, reshape(Xpos, 1, 1, P));
  vv = bsxfun(@times, vs, reshape(Ypos, 1, 1, P));
  ww = bsxfun(@times, ws, reshape(Zpos, 1, 1, P));
  g = repmat(reshape(elementWeights, 1, 1, P), M, N);
  AF = sum(g.*exp(1j*k*(uu + vv + ww)),3);

  % Diretividade
  figure;
  hold on;
  AFmag = abs(AF);
  Utheta = AFmag.^2;
  Prad=sum(sum(Utheta.*sin(THETA)*dtheta*dphi));
  D = 4*pi*Utheta/Prad;
  DdB = 20.*log10(D);

  % plotar em Ã¢ngulo
  subplot(2,1,1),polar(thetaScanAngles,AFmag(:,phiScanAngles==0));
  title('Eixo polar E do arranjo de antena normalizado');
  AFdb = 20*log10(AFmag);
  AFplot=(AFdb + abs(AFdb))/2;
  subplot(2,1,2),polar(thetaScanAngles,AFplot(:,phiScanAngles==0));
  title('Eixo polar E do arranjo de antena normalizado em db');
  FNBW=(180/pi)*2*(pi/2-acos(D));
  HPBW=(180/pi)*2*(pi/2-acos(1.391*D/pi));
  FSLBW=(180/pi)*2*(pi/2-acos(1.5*D));

  % visualizando
  figure;
  colormap('jet');
  hold on;

  % surf(PHI,THETA,AFmag);
  surf(180*cos(PHI).*sin(THETA),180*sin(PHI).*sin(THETA),zeros(size(AFmag)), AFmag);
  shading interp;
  ##colormap('padrÃ£o');
##  colormap( 'default');
##  xlabel( '\phi [deg]','fontsize',15);

  
  grid_handles = [
    polar(linspace(0,2*pi,361), 45*ones(1,361)),
    polar(linspace(0,2*pi,361), 90*ones(1,361)),
    polar(linspace(0,2*pi,361), 135*ones(1,361)),
    polar([0 0], [0 180]),
    polar([0 pi/4], [0 180]),
    polar([0 pi/2], [0 180]),
    polar([0 3*pi/4], [0 180]),
    polar([0 pi], [0 180]),
    polar([0 5*pi/4], [0 180]),
    polar([0 3*pi/2], [0 180]),
    polar([0 7*pi/4], [0 180])
  ];
  set(grid_handles, 'color', [1 1 1], 'linewidth', 1);
  thick_handles = [
    text(0, 45, "45º"),
    text(0, 90, "90º"),
    text(0, 135, "135º"),
    text(180, 0, "0º"),
    text(180*cosd(45), 180*sind(45), "45º", 'verticalalignment', 'bottom'),
    text(180*cosd(90), 180*sind(90), "90º", 'verticalalignment', 'bottom'),
    text(180*cosd(135), 180*sind(135), "135º", 'horizontalalignment', 'right', 'verticalalignment', 'bottom'),
    text(180*cosd(180), 180*sind(180), "180º", 'horizontalalignment', 'right'),
    text(180*cosd(225), 180*sind(225), "225º", 'horizontalalignment', 'right', 'verticalalignment', 'top'),
    text(180*cosd(270), 180*sind(270), "270º", 'verticalalignment', 'top'),
    text(180*cosd(315), 180*sind(315), "315º", 'verticalalignment', 'top')
  ];
  grid off;
  axis off;
  colorbar;
  %set(gca,'XTicklabel',{'-90','-60','-30','0','30','60','90'},'fontsize',15,'fontweight','bold','box','on');
  %ylabel('\theta [deg]','fontsize',15);
  %set(gca,'YTicklabel',{'180','150','120','90','60','30','0'},'fontsize',15,'fontweight','bold','box','on');
  %axis([-pi/2,pi/2,0,pi,-Inf,Inf]);
  zlabel( 'AFmag','FontSize',15);
  title('AFmag');
  
  % GrÃ¡fico 3d da diretividade
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
  title('Diretividade em funÃ§Ã£o de \theta e \phi','FontSize',20);

  % Dois cortes para a visualizaÃ§Ã£o dos Ã¢ngulos de diretividade mÃ¡xima.
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
  text(.0,.8, ['Diretividade mÃ¡xima ', num2str(Domax,3), ' [deg]']);
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


  % semicÃ©u em phi e em theta projeÃ§Ã£o do mapa do cÃ©u.
  % u = sintheta cos phiv
  % v = sin theta sin phi

