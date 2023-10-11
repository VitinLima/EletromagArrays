%Problem 3
  x0 = -3/2;y0 = 0;
  Nx = 1;Ny = 3;
  dx = 0;dy = 3/2;
  default_phi_orientation = 0;
  default_theta_orientation = 0;
  theta_samplei = 0;
  theta_samplef = 180;
  phi_samplei = -180;
  phi_samplef = 180;
  Ntheta = 91;
  Nphi = 181;

array = gridArrayConstructor(base_antenna,
  default_phi_orientation, default_theta_orientation,
  x0, Nx, dx, y0, Ny, dy,
  theta_samplei, theta_samplef, Ntheta,
  phi_samplei, phi_samplef, Nphi);

array.antennas(3).phi_orientation = 45;
array.antennas(1).phi_orientation = -45;
array.antennas(1).theta_orientation = -45;

antv = readAntenna("3-Yagi-4El-validation.csv");