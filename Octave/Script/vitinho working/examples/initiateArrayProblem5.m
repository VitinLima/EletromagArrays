##clear all;
close all;
clc;

%Constantes
global f = 4.33e8; % <= Frequência de operação [Hz]
global c = 299792458; % <= Velocidade da luz [m/s]
global lambda = c/f; % <= Comprimento de onda [m]
global k = 2*pi/lambda; % <= Número de onda [rad/m]

base_antenna = readAntenna('Yagi4El.csv');

%Problem 3
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

array.antennas(2).position = lambda*[1 1 0]';
array.antennas(2).beta = 45;
array.antennas(2).alpha = 45;
array.antennas(3).position = lambda*[0 -1.5 0]';
array.antennas(3).beta = 90;
array.antennas(3).alpha = 0;
array.antennas(4).position = lambda*[-1.5 1 0]';
array.antennas(4).beta = 25;
array.antennas(4).alpha = -70;
array.antennas(5).position = lambda*[1 -2.3 1.7]';
array.antennas(5).beta = -35;
array.antennas(5).alpha = -20;

antv = readAntenna("5-Yagi-4El-validation.csv");
array = evaluateArray(array);

array.Name = 'Octave 5';
antv.Name = 'HFSS 5';
displayResults(antv);
displayResults(array);