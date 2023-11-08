close all;

show_imgs = true;
fontsize = 20;

figure('visible', show_imgs);
view(15,30);
hold on;
xticks([]);
yticks([]);
zticks([]);
axis equal;
axis off;

xlabel('x', 'fontsize', fontsize);
ylabel('y', 'fontsize', fontsize);
zlabel('z', 'fontsize', fontsize);

x = [1, 0, 0]';
y = [0, 1, 0]';
z = [0.0001, 0, 1]';

x1 = x;
y1 = y;
z1 = z;

elevation = -30;
azimuth = -130;
roll = 60;
re = roty(elevation);
ra = rotz(azimuth);
rr = rotx(roll);
R = ra*re*rr;

x1 = R*x;
y1 = R*y;
z1 = R*z;

quiver3(0,0,0,x(1),x(2),x(3), 'b', 'linewidth', 2.0);
quiver3(0,0,0,y(1),y(2),y(3), 'b', 'linewidth', 2.0);
quiver3(0,0,0,z(1),z(2),z(3), 'b', 'linewidth', 2.0);
quiver3(0,0,0,x1(1),x1(2),x1(3), 'g', 'linewidth', 2.0);
quiver3(0,0,0,y1(1),y1(2),y1(3), 'g', 'linewidth', 2.0);
quiver3(0,0,0,z1(1),z1(2),z1(3), 'g', 'linewidth', 2.0);
B = 1.1;
x = B*x;
y = B*y;
z = B*z;
x1 = B*x1;
y1 = B*y1;
z1 = B*z1;
text(x(1),x(2),x(3), 'x', 'fontsize', fontsize);
text(y(1),y(2),y(3), 'y', 'fontsize', fontsize);
text(z(1),z(2),z(3), 'z', 'fontsize', fontsize);
text(1.1*x1(1),x1(2),x1(3), "x\'", 'fontsize', fontsize);
text(y1(1),y1(2),y1(3), "y\'", 'fontsize', fontsize);
text(z1(1),z1(2),z1(3), "z\'", 'fontsize', fontsize);

t = linspace(0,1,100);
A = 0.5;

angles = pi/180*azimuth*t;
aa = [cos(angles); sin(angles); zeros(size(t))];
line(A*aa(1,:), A*aa(2,:), A*aa(3,:), 'color', 'black', 'linewidth', 1.0);
line([0, x1(1)], [0, x1(2)], [0, 0],
'linestyle', '--', 'color', 'black', 'linewidth', 1.0);
line([x1(1), x1(1)], [x1(2), x1(2)], [0, x1(3)],
'linestyle', '--', 'color', 'black', 'linewidth', 1.0);

angles = pi/180*elevation*t;
ae = A*ra*[cos(angles); zeros(size(t)); sin(-angles)];
line(ae(1,:), ae(2,:), ae(3,:), 'color', 'black', 'linewidth', 1.0);

angles = pi/180*roll*t;
ar = A*ra*re*[zeros(size(t)); cos(angles); sin(angles)];
line(ar(1,:), ar(2,:), ar(3,:), 'color', 'black', 'linewidth', 1.0);

B = 1.3;
beta = A*B*[cosd(azimuth/2),sind(azimuth/2),0]';
text(beta(1),beta(2),beta(3), '\beta', 'fontsize', fontsize);
alpha = A*B*ra*[cosd(elevation/2),0,-sind(elevation/2)]';
text(alpha(1),alpha(2),alpha(3), '\alpha', 'fontsize', fontsize);
gamma = A*B*ra*re*[0,cosd(roll/2),sind(roll/2)]';
text(gamma(1),gamma(2),gamma(3), '\gamma', 'fontsize', fontsize);

##saveas(gcf, "orientationOctave", 'png');
