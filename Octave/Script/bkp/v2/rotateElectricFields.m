function ant = rotateElectricFields(ant, alpha, beta)
  ant = toVectorShape(ant);
  
  R = roty(-alpha)*rotz(-beta);
  rE_vec = R*(ant.Etheta.*ant.theta_hat + ant.Ephi.*ant.phi_hat);
  k_hat = R*ant.k_hat;
  theta_hat = R*ant.theta_hat;
  phi_hat = R*ant.phi_hat;
  
  theta_local = atan2d(sqrt(dot(k_hat(1:2,:), k_hat(1:2,:), 1)), k_hat(3,:));
  phi_local = atan2d(k_hat(2,:), k_hat(1,:));
  
  ant = toMeshShape(ant);
  
  Etheta = interp2(ant.THETA, ant.PHI, ant.Etheta, theta_local, phi_local);
  Ephi = interp2(ant.THETA, ant.PHI, ant.Ephi, theta_local, phi_local);
  
  ant = toVectorShape(ant);
  
  ant.Etheta = Etheta;
  ant.Ephi = Ephi;
  
##  c = dot(theta_hat, ant.theta_hat, 1);
##  s = dot(phi_hat, ant.theta_hat, 1);
##  
##  ant.Etheta = Etheta.*c + Ephi.*s;
##  ant.Ephi = Ephi.*c - Etheta.*s;
  
  #Normalize electric fields
  a = ant.Ephi.*conj(ant.Ephi);
  b = ant.Etheta.*conj(ant.Etheta);
  ant.E = sqrt(a + b);
end