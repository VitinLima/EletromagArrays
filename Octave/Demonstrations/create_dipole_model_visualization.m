close all; clear all; clc;

figure;
hold on;

grid off;
axis equal;
xlabel('x');
ylabel('y');
zlabel('z');
view(45,45);

t = linspace(0, 1, 51);

##quiver3(0,0,0,1,0,0,'k');
##quiver3(0,0,0,0,1,0,'k');
##quiver3(0,0,0,0,0,1,'k');

line([0,0],[0,0],[0.1,0.4], 'color', 'b', 'linewidth', 3.0);
line([0,0],[0,0],[-0.1,-0.4], 'color', 'b', 'linewidth', 3.0);

quiver3(-0.1, 0, 0.2, 0.0001, 0, 0.2, 'color', 'k', 'linewidth', 1.0);
quiver3(-0.1, 0, 0.2, 0.0001, 0, -0.2, 'color', 'k', 'linewidth', 1.0);
line([-0.05, -0.15],[0,0],[0.4,0.4], 'color', 'k', 'linewidth', 1.0);
line([-0.05, -0.15],[0,0],[0,0], 'color', 'k', 'linewidth', 1.0);

text(-0.15, 0, 0.2, 'h');
