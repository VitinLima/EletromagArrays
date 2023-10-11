##clear all;
close all;
clc;

%Constantes
global f = 4.33e8; % <= Frequência de operação [Hz]
global c = 299792458; % <= Velocidade da luz [m/s]
global lambda = c/f; % <= Comprimento de onda [m]
global k = 2*pi/lambda; % <= Número de onda [rad/m]

base_antenna = readAntenna('Yagi4El.csv');

%Problem 2
  x0 = 0;y0 = 0;
  Nx = 1;Ny = 2;
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

array.antennas(2).beta = 45;

antv = readAntenna("2-Yagi-4El-validation.csv");
array = evaluateArray(array);

array.Name = 'Octave 2';
antv.Name = 'HFSS 2';
displayResults(antv);
displayResults(array);