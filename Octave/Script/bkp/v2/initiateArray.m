%Grid parameters
  x0 = 0; % <= Posição x do primeiro elemento em unidades de comprimento de onda
  y0 = 0; % <= Posição y do primeiro elemento em unidades de comprimento de onda
  Nx = 1; % <= Número de elementos no eixo x
  Ny = 2; % <= Número de elementos no eixo y
  dx = 0; % <= Espaçamento em x em unidades de comprimento de onda
  dy = 3/2; % <= Espaçamento em y em unidades de comprimento de onda
  default_phi_orientation = 0; % <= Rotação em z
  default_theta_orientation = 0; % <= Rotação em y
  theta_samplei = 0;
  theta_samplef = 180;
  phi_samplei = -180;
  phi_samplef = 180;
  Ntheta = 91; %resolução angular em theta
  Nphi = 181; %resolução angular em phi

base_antenna = readAntenna("Yagi4El.csv");
array = gridArrayConstructor(base_antenna,
  default_phi_orientation, default_theta_orientation,
  x0, Nx, dx, y0, Ny, dy,
  theta_samplei, theta_samplef, Ntheta,
  phi_samplei, phi_samplef, Nphi);