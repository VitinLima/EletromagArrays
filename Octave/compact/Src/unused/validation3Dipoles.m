##clear all;
close all;
clc;

%Constantes
global f = 4.33e8; % <= Frequência de operação [Hz]
global c = 299792458; % <= Velocidade da luz [m/s]
global lambda = c/f; % <= Comprimento de onda [m]
global k = 2*pi/lambda; % <= Número de onda [rad/m]

base_antenna = readAntenna('Dipole.csv');

%Problem 3 Dipoles
  x0 = 0;y0 = 0;
  Nx = 1;Ny = 3;
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

array.antennas(1).position = lambda*[0 0 0]';
array.antennas(2).position = lambda*[-0.25 0.25 0]';
array.antennas(3).position = lambda*[-0.25 -0.25 0]';
array.Name = 'Octave 3 Dipoles';

field_name = 'E'
plot_type = 'inverted sphere'

tic;
array = evaluateArray(array);
toc;
disp(['Time elapsed for calculating ',array.Name,': ',num2str(toc),' seconds']);
displayResults(array, field_name, plot_type);

antv = readAntenna("Dipoles3.csv");
antv.Name = 'HFSS 3 Dipoles';
displayResults(antv, field_name, plot_type);
