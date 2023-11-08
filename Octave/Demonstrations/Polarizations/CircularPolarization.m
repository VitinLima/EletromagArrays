clear all;
close all;
clc;

f = 1;
w = 2*pi*f;
t = linspace(0, 1, 51);

hat_rhcp = [1; -1j]/sqrt(2);
hat_lhcp = [1; 1j]/sqrt(2);

F_theta = 1;
F_phi = 1j;
t_exp = exp(1j*w*t);
vec_F = [F_theta; F_phi];

F_rhcp = sum(vec_F.*conj(hat_rhcp), 1);
F_lhcp = sum(vec_F.*conj(hat_lhcp), 1);

vec_F2 = F_rhcp*hat_rhcp + F_lhcp*hat_lhcp;

F_theta2 = F_rhcp*hat_rhcp(1) + F_lhcp*hat_lhcp(1);
F_phi2 = F_rhcp*hat_rhcp(2) + F_lhcp*hat_lhcp(2);

function error = error(f1, f2)
  error = abs(f1-f2);
end

disp(["RHCP: ", num2str(F_rhcp)]);
disp(["LHCP: ", num2str(F_lhcp)]);

disp(["Error theta: ", num2str(error(F_theta, F_theta2))]);
disp(["Error phi: ", num2str(error(F_phi, F_phi2))]);

##figure;
##hold on;
##
##plot(t, real(F_theta.*t_exp), 'displayname', "\\theta");
##plot(t, real(F_phi.*t_exp), 'displayname', "\\phi");
##
##legend;

figure;
hold on;

h1 = quiver(0,0,real(F_theta(1)), real(F_phi(1)));
h2 = line(real(F_theta(1)), real(F_phi(1)), 'marker', '*');

axis equal;
grid on;
xlim([-1,1]);
ylim([-1,1]);
line(cos(2*pi*t), sin(2*pi*t), 'color', 'k');

flag = true;
while flag
  flag = false;
  for i = 1:length(t)
    vec_F = F_rhcp*hat_rhcp + F_lhcp*hat_lhcp;
    u = vec_F(1).*t_exp(i);
    v = vec_F(2).*t_exp(i);
    set(h1, 'udata', real(u), 'vdata', real(v));
    set(h2, 'xdata', real(u), 'ydata', real(v));
    pause(0.01);
  endfor
end
