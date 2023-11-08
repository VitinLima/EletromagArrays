close all;

function putgrid()
  l = 1.0;
  lw = 0.05;
  c = 0.85;
  lc = [c, c, c];
  G = 2.0;
  for i = -1:0.25:1
    line(G*[-l l],i*G*[-l -l],G*[-l -l], 'color', lc, 'linewidth', lw);
    line(i*G*[-l -l],G*[l l],G*[-l l], 'color', lc, 'linewidth', lw);
    line(G*[-l l],G*[l l],i*G*[-l -l], 'color', lc, 'linewidth', lw);
    line(i*G*[-l -l],G*[-l l],G*[-l -l], 'color', lc, 'linewidth', lw);
    line(G*[-l -l],G*[-l l],i*G*[-l -l], 'color', lc, 'linewidth', lw);
    line(G*[-l -l],i*G*[-l -l],G*[-l l], 'color', lc, 'linewidth', lw);
  end
end

function newfig()
  show_imgs = true;
  fontsize = 20;

  figure('visible', show_imgs);
  hold on;
  xticklabels([]);
  yticklabels([]);
  zticklabels([]);
  axis equal;
  axis off;
  grid on;
  view(55,30);

##  xlabel('x', 'fontsize', fontsize);
##  ylabel('y', 'fontsize', fontsize);
##  zlabel('z', 'fontsize', fontsize);
##  l = 1.0;
##  xlim([-l, l]);
##  ylim([-l, l]);
##  zlim([-l, l]);

  putgrid();

  G = 2.0;
  x = G*[1, 0, 0]';
  y = G*[0, 1, 0]';
  z = G*[0.0001, 0, 1]';

  quiver3(0,0,0,x(1),x(2),x(3), 'blue', 'linewidth', 2.0);
  quiver3(0,0,0,y(1),y(2),y(3), 'blue', 'linewidth', 2.0);
  quiver3(0,0,0,z(1),z(2),z(3), 'blue', 'linewidth', 2.0);
  text(x(1),x(2)+0.2,x(3),'x', 'fontsize', fontsize);
  text(y(1),y(2),y(3),'y', 'fontsize', fontsize);
  text(z(1),z(2),z(3),'z', 'fontsize', fontsize);
end

G = 2.0;

x = G*[1, 0, 0]';
y = G*[0, 1, 0]';
z = G*[0.0001, 0, 1]';

elevation = -30;
azimuth = -130;
roll = 60;
re = roty(elevation);
ra = rotz(azimuth);
rr = rotx(roll);
R = ra*re*rr;

t = linspace(0,1,100);
A = 0.2;
B = 1.4;

show_roll;
show_elevation;
show_azimuth;
