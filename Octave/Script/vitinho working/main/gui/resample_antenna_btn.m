function resample_antenna_btn(h, e)
  global program;
  
  array = get_current_antenna();
  PROMPT = {
    "Phi sampling i:f:d",
    "Theta sampling i:f:d"
  }';
  DEFAULTS = {
    "-180:180:31",
    "0:90:21"
  }';
  CSTR = inputdlg(PROMPT, '', 1, DEFAULTS);
  if isempty(CSTR)
    return;
  end
  S1 = strsplit(CSTR{1}, ':');
  S2 = strsplit(CSTR{2}, ':');
  phi_samplei=str2double(S1{1});
  phi_samplef=str2double(S1{2});
  Nphi=str2double(S1{3});
  theta_samplei=str2double(S2{1});
  theta_samplef=str2double(S2{2});
  Ntheta=str2double(S2{3});
  
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
  
  array.PHI_samplings = PHI_samplings;
  array.THETA_samplings = THETA_samplings;
  array.PHI = PHI;
  array.THETA = THETA;
  array.k_hat = k_hat;
  array.phi_hat = phi_hat;
  array.theta_hat = theta_hat;
  array.Ephi = zeros(1, Nsamples);
  array.Etheta = zeros(1, Nsamples);
  array.E = zeros(1, Nsamples);
  array.N_samples = Nsamples;
  array.N_phi = Nphi;
  array.N_theta = Ntheta;
  array.eval = false;
  set_current_antenna(array);
end