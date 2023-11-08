##close all; clear all; clc;

N = 2;

c0 = 299792458;
f = 433e6;
T = 1/f;
lamb = c0/f;
A = 0.4;

t = 0.5*T;
Dt = 0.125*T;

z_contour = linspace(0, N, 1001);
x_contour = A*cos(2*pi*(z_contour - f*t));
y_contour = A*cos(2*pi*(z_contour - f*t));

z_vector = linspace(0, N, 55);
x_vector = A*cos(2*pi*(z_vector - f*t));
y_vector = A*cos(2*pi*(z_vector - f*t));

figure('visible', show_imgs);
hold on;

xlabel('x', 'fontsize', fontsize);
ylabel('y', 'fontsize', fontsize);
zlabel('z', 'fontsize', fontsize);

axis equal;
xticks([]);
yticks([]);
zticks([]);
grid on;
view(45, 45);

hc = line(x_contour, y_contour, z_contour, 'linewidth', 2.0);
hv = quiver3(
  zeros(size(z_vector)), zeros(size(z_vector)), z_vector,
  x_vector, y_vector, zeros(size(z_vector)),
  0, 'k', 'linewidth', 1.5, "filled");
line([0,0],[0,0],[0,2], 'color', 'b', 'linewidth', 1.5);

saveas(gcf, "LinearPolarizationDiagonal", 'png');

return;

t = t + Dt;

z_contour = linspace(0, N, 1001);
x_contour = Ax*cos(2*pi*(z_contour - f*t));
y_contour = Ay*sin(-2*pi*(z_contour - f*t));

z_vector = linspace(0, N, 55);
x_vector = Ax*cos(2*pi*(z_vector - f*t));
y_vector = Ay*sin(-2*pi*(z_vector - f*t));

figure;
hold on;

xlabel('x');
ylabel('y');
zlabel('z');

axis equal;
##axis('visible', 'off');
grid on;
view(45, 45);

hc = line(x_contour, y_contour, z_contour, 'linewidth', 2.0);
hv = quiver3(
  zeros(size(z_vector)), zeros(size(z_vector)), z_vector,
  x_vector, y_vector, zeros(size(z_vector)),
  0, 'k', 'linewidth', 1.5, "filled");
line([0,0],[0,0],[0,2], 'color', 'b', 'linewidth', 1.5);
