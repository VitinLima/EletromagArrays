function array = gridArrayConstructor(baseAntenna,
    default_beta, default_alpha,
    x0, Nx, dx, y0, Ny, dy,
    theta_samplei, theta_samplef, Ntheta,
    phi_samplei, phi_samplef, Nphi)
  disp(['Constructing array with ',num2str(Nx*Ny), ' antennas']);

  global f;
  global c;
  global lambda;
  global k;

  baseAntenna.beta = default_beta;
  baseAntenna.alpha = default_alpha;
  baseAntenna.magI = 1;
  baseAntenna.phaseI = 0;

  antennas = repmat(baseAntenna, 1, Nx*Ny);

  for i = 1:Nx
    for j = 1:Ny
      antennas((i-1)*Ny + j).position = [ ...
        (x0+(i-1)*dx)*lambda,(y0+(j-1)*dy)*lambda,0]';
    end
  end

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
  theta_hat(3,:) = -st;

  array = struct(
    'Name', 'Planar Antenna Array',
    'antennas', antennas,
    'THETA_samplings', THETA_samplings,
    'PHI_samplings', PHI_samplings,
    'THETA', THETA,
    'PHI', PHI,
    'k_hat', k_hat,
    'phi_hat', phi_hat,
    'theta_hat', theta_hat,
    'Ephi', zeros(1,Nsamples),
    'Etheta', zeros(1,Nsamples),
    'E', zeros(1,Nsamples),
    'E_db', zeros(1,Nsamples),
    'data_shape', 'vector',
    'N_antennas', Nx*Ny,
    'N_samples', Nsamples,
    'N_phi', Nphi,
    'N_theta', Ntheta);
end
