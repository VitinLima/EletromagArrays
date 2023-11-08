clear all; close all; clc;

x = [1, 0, 0]';
y = [0, 1, 0]';
z = [0, 0, 1]';

roll = 60;
elevation = -30;
azimuth = -130;

R = [1,0,0;0,1,0;0,0,1];
R = rotz(-azimuth)*R;
R = roty(-elevation)*R;
R = rotx(-roll)*R;
R = transpose(R);

X = R*[1, 0, 0]';
Y = R*[0, 1, 0]';
Z = R*[0, 0, 1]';

figure;
hold on;
lw = 2.0;
quiver3(0,0,0,x(1), x(2), x(3), 'b', 'linewidth', lw);
quiver3(0,0,0,y(1), y(2), y(3), 'b', 'linewidth', lw);
quiver3(0,0,0,z(1), z(2), z(3), 'b', 'linewidth', lw);
quiver3(0,0,0,X(1), X(2), X(3), 'g', 'linewidth', lw);
quiver3(0,0,0,Y(1), Y(2), Y(3), 'g', 'linewidth', lw);
quiver3(0,0,0,Z(1), Z(2), Z(3), 'g', 'linewidth', lw);
s = 1.1;
fs = 20.0;
text(s*x(1), s*x(2), s*x(3), 'x', 'fontsize', fs);
text(s*y(1), s*y(2), s*y(3), 'y', 'fontsize', fs);
text(s*z(1), s*z(2), s*z(3), 'z', 'fontsize', fs);
text(s*X(1), s*X(2), s*X(3), "x'", 'fontsize', fs);
text(s*Y(1), s*Y(2), s*Y(3), "y'", 'fontsize', fs);
text(s*Z(1), s*Z(2), s*Z(3), "z'", 'fontsize', fs);
grid on;
axis equal;
