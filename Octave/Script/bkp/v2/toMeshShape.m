function ant = toMeshShape(ant)
  if ant.mesh_grid==true
    return;
  end
  
  mesh_shape = [ant.N_phi, ant.N_theta];
  
  ant.THETA = reshape(ant.THETA, mesh_shape);
  ant.PHI = reshape(ant.PHI, mesh_shape);
  ant.k_hat = permute(reshape(ant.k_hat, [3, mesh_shape]), [3,2,1]);
  ant.theta_hat = permute(reshape(ant.theta_hat, [3, mesh_shape]), [3,2,1]);
  ant.phi_hat = permute(reshape(ant.phi_hat, [3, mesh_shape]), [3,2,1]);
  ant.Etheta = reshape(ant.Etheta, mesh_shape);
  ant.Ephi = reshape(ant.Ephi, mesh_shape);
  ant.E = reshape(ant.E, mesh_shape);
  
  ant.mesh_grid = true;
end