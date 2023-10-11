close all;
clear all;
clc;

antenna = readAntenna("big_exportfields_closed.csv");
##antenna.P = [0,0,0];
##antenna.yaw = 70;
##antenna.pitch = 30;
##antenna.row = 0;
##antenna.yaw = 0;
##antenna.pitch = 0;
##antenna.row = 0;
##antenna.theta = linspace(0,pi,11);
##antenna.phi = pi/4*ones(size(antenna.theta));
##antenna.rEphi = 1*ones(size(antenna.theta));
##antenna.rEtheta = 1*ones(size(antenna.theta));
##antenna.phi = linspace(-pi,pi,11);

ct = cos(antenna.theta);
st = sin(antenna.theta);
cp = cos(antenna.phi);
sp = sin(antenna.phi);

P_local = [st.*cp; st.*sp; ct];

##R = (rotx(-antenna.row)*roty(-antenna.pitch)*rotz(-antenna.yaw))';
##P_global = R*P_global;

##theta_local = atan2(sqrt(sum(P_local([1, 2],:).*P_local([1, 2],:),1)), P_local(3,:));
##phi_local = atan2(P_local(2,:), P_local(1,:));

##rEphi_local = griddata( ...
##  antenna.theta, antenna.phi, ...
##  antenna.rEphi, ...
##  theta_local, phi_local)';
##rEtheta_local = griddata( ...
##  antenna.theta, antenna.phi, ...
##  antenna.rEtheta, ...
##  theta_local, phi_local)';

rp = zeros(3,3,length(antenna.phi));
rp(1,1,:) = cp; rp(1,2,:) = -sp; rp(1,3,:) = 0;
rp(2,1,:) = sp; rp(2,2,:) = cp; rp(2,3,:) = 0;
rp(3,1,:) = 0; rp(3,2,:) = 0; rp(3,3,:) = 1;
rt = zeros(3,3,length(antenna.theta));
rt(1,1,:) = ct; rt(1,2,:) = 0; rt(1,3,:) = st;
rt(2,1,:) = 0; rt(2,2,:) = 1; rt(2,3,:) = 0;
rt(3,1,:) = -st; rt(3,2,:) = 0; rt(3,3,:) = ct;

for i = 1:3
  for j = 1:3
    r(i,j,:) = rp(i,1,:).*rt(1,j,:)+rp(i,2,:).*rt(2,j,:)+rp(i,3,:).*rt(3,j,:);
  end
end

vector_theta = squeeze([r(1,1,:); r(2,1,:); r(3,1,:)]);
vector_phi = squeeze([r(1,2,:); r(2,2,:); r(3,2,:)]);

E_phi = antenna.rEphi.*vector_phi;
E_theta = antenna.rEtheta.*vector_theta;

E = E_phi + E_theta;
##E_global = R'*E_local;

figure;
hold on;
line(antenna.theta, antenna.phi, sqrt(sum(E.*E,1)), 'linestyle', 'none', 'marker', '.', 'color', 'b');
line([0 0],[-pi pi], 'color', 'r');
line([pi pi],[-pi pi], 'color', 'r');
line([0 pi],[pi pi], 'color', 'r');
line([0 pi],[-pi -pi], 'color', 'r');
xlabel("Theta");
ylabel("Phi");

figure;
hold on;
##line(P_local(1,:), P_local(2,:), P_local(3,:), 'linestyle', 'none', 'marker', '*', 'color', 'r');
quiver3(P_local(1,:), P_local(2,:), P_local(3,:), vector_theta(1,:), vector_theta(2,:), vector_theta(3,:), 'color', 'g');
quiver3(P_local(1,:), P_local(2,:), P_local(3,:), vector_phi(1,:), vector_phi(2,:), vector_phi(3,:), 'color', 'b');
xlabel('x');
ylabel('y');
zlabel('z');

figure;
hold on;
##line(P_local(1,:), P_local(2,:), P_local(3,:), 'linestyle', 'none', 'marker', '*', 'color', 'r');
quiver3(P_local(1,:), P_local(2,:), P_local(3,:), E_theta(1,:), E_theta(2,:), E_theta(3,:), 'color', 'g');
quiver3(P_local(1,:), P_local(2,:), P_local(3,:), E_phi(1,:), E_phi(2,:), E_phi(3,:), 'color', 'b');
xlabel('x');
ylabel('y');
zlabel('z');

figure;
hold on;
##line(P_local(1,:), P_local(2,:), P_local(3,:), 'linestyle', 'none', 'marker', '*', 'color', 'r');
quiver3(P_local(1,:), P_local(2,:), P_local(3,:), E(1,:), E(2,:), E(3,:), 'color', 'g');
xlabel('x');
ylabel('y');
zlabel('z');

TRI = delaunay(antenna.theta, antenna.phi);

figure;
hold on;
trisurf(TRI, antenna.theta, antenna.phi, sqrt(sum(E.*E,1)), 'linestyle', 'none', 'facecolor', 'interp');
xlabel("Theta");
ylabel("Phi");
zlabel("E");

figure;
hold on;
##TRI = delaunay(antenna.theta, antenna.phi);
trisurf(TRI, antenna.theta, antenna.phi, antenna.rEphi, 'linestyle', 'none', 'facecolor', 'interp');
xlabel("Theta");
ylabel("Phi");
zlabel("rEphi");

figure;
hold on;
##TRI = delaunay(antenna.theta, antenna.phi);
trisurf(TRI, antenna.theta, antenna.phi, antenna.rEtheta, 'linestyle', 'none', 'facecolor', 'interp');
xlabel("Theta");
ylabel("Phi");
zlabel("rEtheta");

figure;
hold on;
plot(antenna.phi(antenna.theta==0), antenna.rEphi(antenna.theta==0));
plot(antenna.phi(antenna.theta==0), antenna.rEtheta(antenna.theta==0));