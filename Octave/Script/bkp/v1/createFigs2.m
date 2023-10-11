close all;
clc;

##figure;
##hold on;
##line(antenna.theta, antenna.phi, 'linestyle', 'none', 'marker', '.', 'color', 'b');
##line(theta_local, phi_local, 'linestyle', 'none', 'marker', '*', 'color', 'g');
##line([0 0],[-pi pi], 'color', 'r');
##line([pi pi],[-pi pi], 'color', 'r');
##line([0 pi],[pi pi], 'color', 'r');
##line([0 pi],[-pi -pi], 'color', 'r');
##xlabel("Theta");
##ylabel("Phi");
##
##figure;
##hold on;
##quiver3(P_local(1,:), P_local(2,:), P_local(3,:), vector_theta_local(1,:), vector_theta_local(2,:), vector_theta_local(3,:), 'color', 'g');
##quiver3(P_local(1,:), P_local(2,:), P_local(3,:), vector_phi_local(1,:), vector_phi_local(2,:), vector_phi_local(3,:), 'color', 'b');
##xlabel('x');
##ylabel('y');
##zlabel('z');
##
##figure;
##hold on;
##quiver3(P_local(1,:), P_local(2,:), P_local(3,:), E_theta_local(1,:), E_theta_local(2,:), E_theta_local(3,:), 'color', 'g');
##quiver3(P_local(1,:), P_local(2,:), P_local(3,:), E_phi_local(1,:), E_phi_local(2,:), E_phi_local(3,:), 'color', 'b');
##xlabel('x');
##ylabel('y');
##zlabel('z');

figure;
hold on;
quiver3(P_local(1,:), P_local(2,:), P_local(3,:), E_local(1,:), E_local(2,:), E_local(3,:), 'color', 'g');
xlabel('x');
ylabel('y');
zlabel('z');

figure;
hold on;
quiver3(P_global(1,:), P_global(2,:), P_global(3,:), E_global(1,:), E_global(2,:), E_global(3,:), 'color', 'g');
xlabel('x');
ylabel('y');
zlabel('z');

TRI = delaunay(theta_local, phi_local);
TETR = delaunay(P_global');
getFaces;

figure;
hold on;
trisurf(TRI, theta_local, phi_local, sqrt(sum(E_local.*E_local,1)), 'linestyle', 'none', 'facecolor', 'interp');
line([0 0],[-pi pi], 'color', 'r');
line([pi pi],[-pi pi], 'color', 'r');
line([0 pi],[pi pi], 'color', 'r');
line([0 pi],[-pi -pi], 'color', 'r');
xlabel("Theta");
ylabel("Phi");
zlabel("E");

figure;
hold on;
trisurf(TRIfaces, P_local(1,:), P_local(2,:), P_local(3,:), sqrt(sum(E_local.*E_local,1)), 'linestyle', 'none', 'facecolor', 'interp');
xlabel("x");
ylabel("y");
zlabel("z");

figure;
hold on;
trisurf(TRIfaces, P_global(1,:), P_global(2,:), P_global(3,:), magE, 'linestyle', 'none', 'facecolor', 'interp');
xlabel("x");
ylabel("y");
zlabel("z");

figure;
hold on;
trisurf(TRIfaces, magE.*P_global(1,:), magE.*P_global(2,:), magE.*P_global(3,:), magE, 'linestyle', 'none', 'facecolor', 'interp');
xlabel("x");
ylabel("y");
zlabel("z");

##  figure;
##  hold on;
####  CN = 64;
####  cm = jet(CN);
####  Ex = E_global(1,:)';
####  Ec = sum(Ex(TETR),2)/4;
####  minEc = min(Ec);
####  maxEc = max(Ec);
####  C = round((CN-1)*(Ec-minEc)/(maxEc-minEc)) + 1;
##  TETR = delaunay(x_global, y_global, z_global);
##  tetramesh(TETR, P_global');
##  xlabel('x');
##  ylabel('y');
##  zlabel('z');
##
##  getFaces;
##  figure;
##  hold on;
##  CN = 64;
##  cm = jet(CN);
##  E = sqrt(sum(E_global.*E_global, 1));
####  Ec = sum(Ex(TRI),2)/3;
##  minE = min(E);
##  maxE = max(E);
##  C = round((CN-1)*(E-minE)/(maxE-minE)) + 1;
####  TETR = delaunay(x_global, y_global, z_global);
##  PE = P_global.*E;
##  trisurf(TRI, P_global(1,:), P_global(2,:), P_global(3,:), C, 'facecolor', 'interp');
##  xlabel('x');
##  ylabel('y');
##  zlabel('z');