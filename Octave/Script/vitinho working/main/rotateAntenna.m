function ant = rotateElectricFields(ant, alpha, beta)
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
  tool_ant.phi_hat = zeros(3,tool_ant.N_samples);
  tool_ant.theta_hat = zeros(3,tool_ant.N_samples);
  tool_ant.phi_hat(1,:) = -sp;
  tool_ant.phi_hat(2,:) = cp;
  tool_ant.theta_hat(1,:) = ct.*cp;
  tool_ant.theta_hat(2,:) = ct.*sp;
  tool_ant.theta_hat(3,:) = -st;
  R = R';
  tool_ant.theta_hat = R*tool_ant.theta_hat;
  tool_ant.phi_hat = R*tool_ant.phi_hat;
  
  ant = toMeshShape(ant);
  tool_ant = toMeshShape(tool_ant);
  
  tool_ant.Etheta = interp2(ant.THETA, ant.PHI, ant.Etheta, tool_ant.THETA, tool_ant.PHI);
  tool_ant.Ephi = interp2(ant.THETA, ant.PHI, ant.Ephi, tool_ant.THETA, tool_ant.PHI);
  
  ant = toVectorShape(ant);
  tool_ant = toVectorShape(tool_ant);
  
  rE_vec = tool_ant.theta_hat.*tool_ant.Etheta + tool_ant.phi_hat.*tool_ant.Ephi;
  
  ant.Etheta = dot(rE_vec, ant.theta_hat, 1);
  ant.Ephi = dot(rE_vec, ant.phi_hat, 1);
  
  a = ant.Ephi.*conj(ant.Ephi);
  b = ant.Etheta.*conj(ant.Etheta);
  ant.E = sqrt(a + b);
end