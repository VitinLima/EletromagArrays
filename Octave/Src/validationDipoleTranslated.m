##clear all;
close all;
clc;

%Constantes
global f = 4.33e8; % <= Frequência de operação [Hz]
global c = 299792458; % <= Velocidade da luz [m/s]
global lambda = c/f; % <= Comprimento de onda [m]
global k = 2*pi/lambda; % <= Número de onda [rad/m]

base_antenna = readAntenna('Dipole.csv');
##base_antenna = readAntenna('1Y-4EL.csv');

%Problem Translated Dipole
  x0 = 0;y0 = 0;
  Nx = 1;Ny = 1;
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

array.antennas(1).position = lambda*[1 0 0]';
array.Name = 'Octave Dipole';

field_name = 'E'
plot_type = 'inverted sphere'

tic;
array = evaluateArray(array);
toc;
disp(['Time elapsed for calculating ',array.Name,': ',num2str(toc),' seconds']);
displayResults(array, field_name, plot_type);

antv = readAntenna("DipoleTranslated.csv");
antv.Name = 'HFSS Dipole';
displayResults(antv, field_name, plot_type);
