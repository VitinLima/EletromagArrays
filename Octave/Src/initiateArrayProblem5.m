##clear all;
close all;
clc;

%Constantes
global f = 4.33e8; % <= Frequência de operação [Hz]
global c = 299792458; % <= Velocidade da luz [m/s]
global lambda = c/f; % <= Comprimento de onda [m]
global k = 2*pi/lambda; % <= Número de onda [rad/m]

base_antenna = readAntenna('antenna-Yagi-4Elements.csv');

%Problem 5
  x0 = 0;y0 = 0;
  Nx = 1;Ny = 5;
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

array.antennas(2).position = lambda*[0 1.5 0]';
array.antennas(2).beta = 45;
array.antennas(2).alpha = 0;
array.antennas(3).position = lambda*[0 -1.5 0]';
array.antennas(3).beta = -45;
array.antennas(3).alpha = -45;
array.antennas(4).position = lambda*[0.34, -3.14, 1.423]';
array.antennas(4).beta = 135;
array.antennas(4).alpha = -45;
array.antennas(5).position = lambda*[0.83, 1.19, -0.72]';
array.antennas(5).beta = 14;
array.antennas(5).alpha = 72;
array.Name = 'Octave 5';

field_name = 'angEtheta'
plot_type = 'inverted sphere'

tic;
array = evaluateArray(array);
toc;
disp(['Time elapsed for calculating ',array.Name,': ',num2str(toc),' seconds']);
displayResults(array, field_name, plot_type);

antv = readAntenna("5Y-4EL.csv");
antv.Name = 'HFSS 5';
displayResults(antv, field_name, plot_type);
