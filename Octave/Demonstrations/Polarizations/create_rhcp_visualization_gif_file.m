close all; clear all; clc;

N = 2;

c0 = 299792458;
f = 433e6;
T = 1/f;
lamb = c0/f;
Ax = 0.4;
Ay = Ax;

gif_duration = 12;
gif_fps = 15;
gif_frames = 2*gif_fps;
t = linspace(0, 4*T, round(gif_duration*gif_fps) + 1);

z_contour = linspace(0, N, 1001);
x_contour = Ax*cos(2*pi*(z_contour - f*t(1)));
y_contour = Ay*sin(-2*pi*(z_contour - f*t(1)));

z_vector = linspace(0, N, 55);
x_vector = Ax*cos(2*pi*(z_vector - f*t(1)));
y_vector = Ay*sin(-2*pi*(z_vector - f*t(1)));

figure;
hold on;

xlabel('x');
ylabel('y');
zlabel('z');

axis equal;
grid on;
view(135, 45);

hc = line(x_contour, y_contour, z_contour, 'linewidth', 2.0);
hv = quiver3(
  zeros(size(z_vector)), zeros(size(z_vector)), z_vector,
  x_vector, y_vector, zeros(size(z_vector)),
  0, 'k', 'linewidth', 1.5, "filled");
k_vector = quiver3(0,0,0,0,0,1.6*N, 'b', 'linewidth', 1.5);

h_fps = title(["fps: ", num2str(gif_fps)]);

frame = getframe(gcf);
img_data = zeros([size(frame.cdata),gif_frames]);

for i = 2:length(t)
  t_i = t(i);

  x_contour = Ax*cos(2*pi*(z_contour - f*t_i));
  y_contour = Ay*sin(-2*pi*(z_contour - f*t_i));

  x_vector = Ax*cos(2*pi*(z_vector - f*t_i));
  y_vector = Ay*sin(-2*pi*(z_vector - f*t_i));

  set(hc,
    'xdata', x_contour,
    'ydata', y_contour);
  set(hv,
    'udata', x_vector,
    'vdata', y_vector);

  frame = getframe(gcf);
  img_data(:,:,:,i) = frame.cdata;
end

imwrite(img_data, "ani.gif", 'delaytime', 1/gif_fps);
