clear all;
close all;
clc;

%Constantes
global f = 4.33e8; % <= Frequência de operação [Hz]
global c = 299792458; % <= Velocidade da luz [m/s]
global lambda = c/f; % <= Comprimento de onda [m]
global k = 2*pi/lambda; % <= Número de onda [rad/m]

tic;
##base_antenna = readAntenna('Dipolo.csv');
base_ant = idealDipoleAntenna(0.5, -180, 180, 91, 0, 180, 91);
disp(['Time elapsed for reading base antenna: ',num2str(toc),' seconds']);

disp('Constructing initial array');
tic;
  x0 = 0;y0 = 0;
  Nx = 1;Ny = 3;
  dx = 1;dy = 1;
  default_beta = 0;
  default_alpha = 45;
  theta_samplei = 0;
  theta_samplef = 90;
  Ntheta = 91;
  phi_samplei = -90;
  phi_samplef = 90;
  Nphi = 91;

disp('Constructing target antenna');
tic;
  tg_ant = gridArrayConstructor(base_ant,
    default_beta, default_alpha,
    x0, Nx, dx, y0, Ny, dy,
    theta_samplei, theta_samplef, Ntheta,
    phi_samplei, phi_samplef, Nphi);
  tg_ant.Name = 'Target antenna array';
    
  tg_ant.antennas(1).alpha = 45;
  tg_ant.antennas(1).beta = 62;
  tg_ant.antennas(2).alpha = 73;
  tg_ant.antennas(2).beta = 14;
  tg_ant.antennas(3).alpha = 34;
  tg_ant.antennas(3).beta = 92;

  tg_ant = evaluateArray(tg_ant);
disp(['Time elapsed for initiating target antenna: ',num2str(toc),' seconds']);
displayResults(tg_ant);

  arr = gridArrayConstructor(base_ant,
    default_beta, default_alpha,
    x0, Nx, dx, y0, Ny, dy,
    theta_samplei, theta_samplef, Ntheta,
    phi_samplei, phi_samplef, Nphi);
  arr.Name = 'Optimized antenna array';
  
  arr.antennas(1).alpha += 60*(rand-0.5);
  arr.antennas(1).beta += 60*(rand-0.5);
  arr.antennas(2).alpha += 60*(rand-0.5);
  arr.antennas(2).beta += 60*(rand-0.5);
  arr.antennas(3).alpha += 60*(rand-0.5);
  arr.antennas(3).beta += 60*(rand-0.5);
disp(['Time elapsed for initiating array: ',num2str(toc),' seconds']);

arr = evaluateArray(arr);
displayResults(arr);

optpar = struct( ...
  'x', false,
  'y', false,
  'z', false,
  'alpha', true,
  'beta', true);
optpar.N = optpar.x+optpar.y+optpar.z+optpar.beta+optpar.alpha;

tic;
  [arr, x] = optimization(arr, tg_ant, optpar);
disp(['Time elapsed for optimization: ',num2str(toc),' seconds']);

displayResults(tg_ant);
displayResults(arr);