%Problem 3
  x0 = 0;y0 = 0;
  Nx = 1;Ny = 6;
  dx = 0;dy = 0;
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

array.antennas(2).position = lambda*[1 1 0]';
array.antennas(2).phi_orientation = 45;
array.antennas(2).theta_orientation = 45;
array.antennas(3).position = lambda*[0 -1.5 0]';
array.antennas(3).phi_orientation = 90;
array.antennas(3).theta_orientation = 0;
array.antennas(4).position = lambda*[-1.5 1 0]';
array.antennas(4).phi_orientation = 25;
array.antennas(4).theta_orientation = -70;
array.antennas(5).position = lambda*[1 -2.3 1.7]';
array.antennas(5).phi_orientation = -35;
array.antennas(5).theta_orientation = -20;

antv = readAntenna("2-Yagi-4El-validation.csv");