function antenna = resample(antenna, ...
    theta_samplei, theta_samplef, Ntheta, ...
    phi_samplei, phi_samplef, Nphi)
  Nsamples = Nphi*Ntheta;

  PHI_samplings = linspace(phi_samplei,phi_samplef,Nphi);
  THETA_samplings = linspace(theta_samplei,theta_samplef,Ntheta);
  [THETA, PHI] = meshgrid(THETA_samplings, PHI_samplings);
  THETA = THETA(:)';
  PHI = PHI(:)';

  cp = cosd(PHI);
  sp = sind(PHI);
  ct = cosd(THETA);
  st = sind(THETA);

  k_hat = zeros(3,Nsamples);
  phi_hat = zeros(3,Nsamples);
  theta_hat = zeros(3,Nsamples);

  k_hat(1,:) = st.*cp;
  k_hat(2,:) = st.*sp;
  k_hat(3,:) = ct;
  phi_hat(1,:) = -sp;
  phi_hat(2,:) = cp;
  theta_hat(1,:) = ct.*cp;
  theta_hat(2,:) = ct.*sp;
  theta_hat(3,:) = st;

  antenna.THETA_samplings = THETA_samplings;
  antenna.PHI_samplings = PHI_samplings;
  antenna.THETA = THETA;
  antenna.PHI = PHI;
  antenna.k_hat = k_hat;
  antenna.phi_hat = phi_hat;
  antenna.theta_hat = theta_hat;

  antenna.data_shape = 'vector';

  antenna.N_samples = Nsamples;
  antenna.N_phi = Nphi;
  antenna.N_theta = Ntheta;
end
