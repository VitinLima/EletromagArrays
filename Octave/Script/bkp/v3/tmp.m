close all;
clc;

importDataGraphics;

ant = idealDipoleAntenna(0.5, -180, 180, 105, 0, 180, 103);
rant = rotateElectricFields(ant, 45, 0);

##displayResults(ant);
displayResults(rant);

return;
##  figure;
##  hold on;
##
####  quiver3(ant.k_hat(1,:), ant.k_hat(2,:), ant.k_hat(3,:), ant.theta_hat(1,:), ant.theta_hat(2,:), ant.theta_hat(3,:), 'color', 'b');
####  rE_vec = ant.Etheta.*ant.theta_hat + ant.Ephi.*ant.phi_hat;
####  quiver3(ant.k_hat(1,:), ant.k_hat(2,:), ant.k_hat(3,:), rE_vec(1,:), rE_vec(2,:), rE_vec(3,:), 'color', 'g');
##  
##  quiver3(rant.k_hat(1,:), rant.k_hat(2,:), rant.k_hat(3,:), rant.theta_hat(1,:), rant.theta_hat(2,:), rant.theta_hat(3,:), 'color', 'r');
##  quiver3(rant.k_hat(1,:), rant.k_hat(2,:), rant.k_hat(3,:), rant.phi_hat(1,:), rant.phi_hat(2,:), rant.phi_hat(3,:), 'color', 'b');
##  rE_vec = rant.Etheta.*rant.theta_hat + rant.Ephi.*rant.phi_hat;
##  quiver3(rant.k_hat(1,:), rant.k_hat(2,:), rant.k_hat(3,:), rE_vec(1,:), rE_vec(2,:), rE_vec(3,:), 'color', 'y');
##  axis equal;
##  xlabel('x');
##  ylabel('y');
##  zlabel('z');
##return;

alpha = 45;
beta = 0;

ant = toVectorShape(ant);
tool_ant = ant;

R = roty(-alpha)*rotz(-beta);
rE_vec = R*(ant.Etheta.*ant.theta_hat + ant.Ephi.*ant.phi_hat);
tool_ant.k_hat = R*ant.k_hat;

tool_ant.THETA = atan2d(sqrt(dot(tool_ant.k_hat(1:2,:), tool_ant.k_hat(1:2,:), 1)), tool_ant.k_hat(3,:));
tool_ant.PHI = atan2d(tool_ant.k_hat(2,:), tool_ant.k_hat(1,:));

ct = cosd(tool_ant.THETA);
st = sind(tool_ant.THETA);
cp = cosd(tool_ant.PHI);
sp = sind(tool_ant.PHI);
tool_ant.k_hat = zeros(3,tool_ant.N_samples);
tool_ant.phi_hat = zeros(3,tool_ant.N_samples);
tool_ant.theta_hat = zeros(3,tool_ant.N_samples);
tool_ant.k_hat(1,:) = st.*cp;
tool_ant.k_hat(2,:) = st.*sp;
tool_ant.k_hat(3,:) = ct;
tool_ant.phi_hat(1,:) = -sp;
tool_ant.phi_hat(2,:) = cp;
tool_ant.theta_hat(1,:) = ct.*cp;
tool_ant.theta_hat(2,:) = ct.*sp;
tool_ant.theta_hat(3,:) = -st;
##R = R';
tool_ant.theta_hat = R*ant.theta_hat;
tool_ant.phi_hat = R*ant.phi_hat;

ant = toMeshShape(ant);
tool_ant = toMeshShape(tool_ant);

##  rE_vec = ant.Etheta.*ant.theta_hat + ant.Ephi.*ant.phi_hat;
##  
##  rE_vec(:,:,1) = interp2(ant.THETA, ant.PHI, rE_vec(:,:,1), tool_ant.THETA, tool_ant.PHI);
##  rE_vec(:,:,2) = interp2(ant.THETA, ant.PHI, rE_vec(:,:,2), tool_ant.THETA, tool_ant.PHI);
##  rE_vec(:,:,3) = interp2(ant.THETA, ant.PHI, rE_vec(:,:,3), tool_ant.THETA, tool_ant.PHI);
##  
##  tool_ant.Etheta = dot(rE_vec, tool_ant.theta_hat,3);
##  tool_ant.Ephi = dot(rE_vec, tool_ant.phi_hat,3);
##  
##  ant = toVectorShape(ant);
##  tool_ant = toVectorShape(tool_ant);

tool_ant.Etheta = interp2(ant.THETA, ant.PHI, ant.Etheta, tool_ant.THETA, tool_ant.PHI);
tool_ant.Ephi = interp2(ant.THETA, ant.PHI, ant.Ephi, tool_ant.THETA, tool_ant.PHI);

ant = toVectorShape(ant);
tool_ant = toVectorShape(tool_ant);

rE_vec = tool_ant.theta_hat.*tool_ant.Etheta + tool_ant.phi_hat.*tool_ant.Ephi;

ant.Etheta = dot(rE_vec, ant.theta_hat, 1);
ant.Ephi = dot(rE_vec, ant.phi_hat, 1);
  figure;
  hold on;
  
##  quiver3(tool_ant.k_hat(:,:,1), tool_ant.k_hat(:,:,2), tool_ant.k_hat(:,:,3), tool_ant.theta_hat(:,:,1), tool_ant.theta_hat(:,:,2), tool_ant.theta_hat(:,:,3), 'color', 'r');
##  quiver3(tool_ant.k_hat(:,:,1), tool_ant.k_hat(:,:,2), tool_ant.k_hat(:,:,3), rE_vec(:,:,1), rE_vec(:,:,2), rE_vec(:,:,3), 'color', 'y');

  quiver3(ant.k_hat(1,:), ant.k_hat(2,:), ant.k_hat(3,:), ant.theta_hat(1,:), ant.theta_hat(2,:), ant.theta_hat(3,:), 'color', 'b');
  rE_vec = ant.Etheta.*ant.theta_hat + ant.Ephi.*ant.phi_hat;
  quiver3(ant.k_hat(1,:), ant.k_hat(2,:), ant.k_hat(3,:), rE_vec(1,:), rE_vec(2,:), rE_vec(3,:), 'color', 'g');
  
##  quiver3(ant.k_hat(1,:), ant.k_hat(2,:), ant.k_hat(3,:), tool_ant.theta_hat(1,:), tool_ant.theta_hat(2,:), tool_ant.theta_hat(3,:), 'color', 'r');
##  rE_vec = tool_ant.Etheta.*tool_ant.theta_hat + tool_ant.Ephi.*tool_ant.phi_hat;
##  quiver3(tool_ant.k_hat(1,:), tool_ant.k_hat(2,:), tool_ant.k_hat(3,:), rE_vec(1,:), rE_vec(2,:), rE_vec(3,:), 'color', 'y');
  axis equal;
  xlabel('x');
  ylabel('y');
  zlabel('z');
return;

#Re-evaluate rE total
a = ant.Ephi.*conj(ant.Ephi);
b = ant.Etheta.*conj(ant.Etheta);
ant.E = sqrt(a + b);