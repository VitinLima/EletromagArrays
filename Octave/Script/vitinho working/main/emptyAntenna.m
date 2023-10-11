function antenna = emptyAntenna(phi_samplei=-180, phi_samplef=180, Nphi=31,
    theta_samplei=0, theta_samplef=90, Ntheta=21)
  
  Nsamples = Nphi*Ntheta;
  PHI_samplings = linspace(phi_samplei,phi_samplef,Nphi);
  THETA_samplings = linspace(theta_samplei,theta_samplef,Ntheta);
  [THETA, PHI] = meshgrid(THETA_samplings, PHI_samplings);
  THETA = THETA(:)';
  PHI = PHI(:)';
  
  k_hat = zeros(3,Nsamples);
  phi_hat = zeros(3,Nsamples);
  theta_hat = zeros(3,Nsamples);
  
  cp = cosd(PHI);
  sp = sind(PHI);
  ct = cosd(THETA);
  st = sind(THETA);
  
  k_hat(1,:) = st.*cp;
  k_hat(2,:) = st.*sp;
  k_hat(3,:) = ct;
  phi_hat(1,:) = -sp;
  phi_hat(2,:) = cp;
  theta_hat(1,:) = ct.*cp;
  theta_hat(2,:) = ct.*sp;
  theta_hat(3,:) = -st;
  
  antenna = struct(
    'header', [],
    'Name', 'Empty antenna',
    'PHI_samplings', PHI_samplings,
    'THETA_samplings', THETA_samplings,
    'PHI', PHI,
    'THETA', THETA,
    'k_hat', k_hat,
    'phi_hat', phi_hat,
    'theta_hat', theta_hat,
    'Ephi', zeros(1, Nsamples),
    'Etheta', zeros(1, Nsamples),
    'E', zeros(1, Nsamples),
    'magI', 1,
    'phaseI', 0,
    'position', [0 0 0],
    'alpha', 0,
    'beta', 0,
    'referenceSystem', 'local',
    'data_shape', 'vector',
    'N_samples', Nsamples,
    'N_phi', Nphi,
    'N_theta', Ntheta,
    'evaluate_argument', '',
    'eval', false,
    'evaluate', []);
end