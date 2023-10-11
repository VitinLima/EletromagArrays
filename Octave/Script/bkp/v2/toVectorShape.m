function ant = toVectorShape(ant)
  if ant.mesh_grid==false
    return;
  end
  
  ant.THETA = ant.THETA(:);
  ant.PHI = ant.PHI(:);
  ant.k_hat = reshape(permute(ant.k_hat, [3,2,1]), [3, ant.N_samples]);
  ant.theta_hat = reshape(permute(ant.theta_hat, [3,2,1]), [3, ant.N_samples]);
  ant.phi_hat = reshape(permute(ant.phi_hat, [3,2,1]), [3, ant.N_samples]);
  ant.Etheta = ant.Etheta(:);
  ant.Ephi = ant.Ephi(:);
  ant.E = ant.E(:);
  
  ant.mesh_grid = false;
end