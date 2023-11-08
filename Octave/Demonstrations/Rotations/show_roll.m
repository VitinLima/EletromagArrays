newfig;

x1 = rr*x;
y1 = rr*y;
z1 = rr*z;

quiver3(0,0,0,x1(1),x1(2),x1(3), 'g', 'linewidth', 2.0);
quiver3(0,0,0,y1(1),y1(2),y1(3), 'g', 'linewidth', 2.0);
quiver3(0,0,0,z1(1),z1(2),z1(3), 'g', 'linewidth', 2.0);
text(x1(1),x1(2),x1(3), "x\'", 'fontsize', fontsize);
text(y1(1),y1(2),y1(3), "y\'", 'fontsize', fontsize);
text(z1(1),z1(2),z1(3), "z\'", 'fontsize', fontsize);

angles = pi/180*315*t;
ar = G*[0.5*ones(size(t)); -A*cos(angles); -A*sin(angles)];
arrow = G*0.01*sqrt(2)/2*[0, -1, -1];
line(ar(1,:), ar(2,:), ar(3,:), 'color', 'black', 'linewidth', 1.0);
quiver3(ar(1,end), ar(2,end), ar(3,end), arrow(1), arrow(2), arrow(3),
'color', 'black', 'linewidth', 1.0, 'maxheadsize', 10);

gamma = G*[0.5,-0.5,0]';
text(gamma(1),gamma(2),gamma(3), '\gamma', 'fontsize', fontsize);

saveas(gcf, "RefSysRollOctave", 'png');
