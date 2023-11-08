clear all; close all; clc;

%Constantes
global f = 4.33e8; % <= Frequência de operação [Hz]
global c = 299792458; % <= Velocidade da luz [m/s]
global lambda = c/f; % <= Comprimento de onda [m]
global k = 2*pi/lambda; % <= Número de onda [rad/m]

##base_antenna = readAntenna('1Y-4EL.csv'); # Not good,
##  creates several "ghost" passive elements
base_antenna = readAntenna('antenna-Yagi-4Elements.csv');

%Problem 1
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
array_1 = gridArrayConstructor(base_antenna,
  default_phi_orientation, default_theta_orientation,
  x0, Nx, dx, y0, Ny, dy,
  theta_samplei, theta_samplef, Ntheta,
  phi_samplei, phi_samplef, Nphi);
array_1.Name = 'Octave 1';

##Problem 2
  x0 = 0;y0 = 0;
  Nx = 1;Ny = 2;
  dx = 0;dy = 0;
  default_phi_orientation = 0;
  default_theta_orientation = 0;
  theta_samplei = 0;
  theta_samplef = 180;
  phi_samplei = -180;
  phi_samplef = 180;
  Ntheta = 91;
  Nphi = 181;
array_2 = gridArrayConstructor(base_antenna,
  default_phi_orientation, default_theta_orientation,
  x0, Nx, dx, y0, Ny, dy,
  theta_samplei, theta_samplef, Ntheta,
  phi_samplei, phi_samplef, Nphi);
array_2.antennas(1).magI = 1;
array_2.antennas(2).position = lambda*[0 1.5 0]';
array_2.antennas(2).beta = 45;
array_2.antennas(2).alpha = 0;
array_2.antennas(2).magI = 1;
array_2.Name = 'Octave 2';

%Problem 3
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
array_3 = gridArrayConstructor(base_antenna,
  default_phi_orientation, default_theta_orientation,
  x0, Nx, dx, y0, Ny, dy,
  theta_samplei, theta_samplef, Ntheta,
  phi_samplei, phi_samplef, Nphi);
array_3.antennas(2).position = lambda*[0 1.5 0]';
array_3.antennas(2).beta = 45;
array_3.antennas(2).alpha = 0;
array_3.antennas(3).position = lambda*[0 -1.5 0]';
array_3.antennas(3).beta = -45;
array_3.antennas(3).alpha = -45;
array_3.Name = 'Octave 3';

%Problem 4
  x0 = 0;y0 = 0;
  Nx = 1;Ny = 4;
  dx = 0;dy = 0;
  default_phi_orientation = 0;
  default_theta_orientation = 0;
  theta_samplei = 0;
  theta_samplef = 180;
  phi_samplei = -180;
  phi_samplef = 180;
  Ntheta = 91;
  Nphi = 181;
array_4 = gridArrayConstructor(base_antenna,
  default_phi_orientation, default_theta_orientation,
  x0, Nx, dx, y0, Ny, dy,
  theta_samplei, theta_samplef, Ntheta,
  phi_samplei, phi_samplef, Nphi);
array_4.antennas(2).position = lambda*[0 1.5 0]';
array_4.antennas(2).beta = 45;
array_4.antennas(2).alpha = 0;
array_4.antennas(3).position = lambda*[0 -1.5 0]';
array_4.antennas(3).beta = -45;
array_4.antennas(3).alpha = -45;
array_4.antennas(4).position = lambda*[0.34, -3.14, 1.423]';
array_4.antennas(4).beta = 135;
array_4.antennas(4).alpha = -45;
array_4.Name = 'Octave 4';

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
array_5 = gridArrayConstructor(base_antenna,
  default_phi_orientation, default_theta_orientation,
  x0, Nx, dx, y0, Ny, dy,
  theta_samplei, theta_samplef, Ntheta,
  phi_samplei, phi_samplef, Nphi);
array_5.antennas(2).position = lambda*[0 1.5 0]';
array_5.antennas(2).beta = 45;
array_5.antennas(2).alpha = 0;
array_5.antennas(3).position = lambda*[0 -1.5 0]';
array_5.antennas(3).beta = -45;
array_5.antennas(3).alpha = -45;
array_5.antennas(4).position = lambda*[0.34, -3.14, 1.423]';
array_5.antennas(4).beta = 135;
array_5.antennas(4).alpha = -45;
array_5.antennas(5).position = lambda*[0.83, 1.19, -0.72]';
array_5.antennas(5).beta = 14;
array_5.antennas(5).alpha = 72;
array_5.Name = 'Octave 5';

antv_1 = readAntenna("1Y-4EL.csv");
antv_1.Name = 'HFSS 1';
antv_2 = readAntenna("2Y-4EL.csv");
antv_2.Name = 'HFSS 2';
antv_3 = readAntenna("3Y-4EL.csv");
antv_3.Name = 'HFSS 3';
antv_4 = readAntenna("4Y-4EL.csv");
antv_4.Name = 'HFSS 4';
antv_5 = readAntenna("5Y-4EL.csv");
antv_5.Name = 'HFSS 5';

tic;
array_1 = evaluateArray(array_1);
array_1_time = toc;
tic;
array_2 = evaluateArray(array_2);
array_2_time = toc;
tic;
array_3 = evaluateArray(array_3);
array_3_time = toc;
tic;
array_4 = evaluateArray(array_4);
array_4_time = toc;
tic;
array_5 = evaluateArray(array_5);
array_5_time = toc;

plot_type = 'inverted sphere'
s = {
  'magE db',
  'magE normalized',
  'magEtheta db',
  'magEtheta normalized',
  'angEtheta',
  'magEphi db',
  'magEphi normalized',
  'angEphi'
  };
for i = 1:length(s)
  field_name = cell2mat(s(i))
  displayResults(array_1, field_name, plot_type, ...
    'showImages','off', 'printImages', true, 'savedir', ...
    [pwd,filesep,'Images',filesep,'Array_1',filesep], ...
    'close_after', true);
  displayResults(antv_1, field_name, plot_type, ...
    'showImages','off', 'printImages', true, 'savedir', ...
    [pwd,filesep,'Images',filesep,'Array_1',filesep], ...
    'close_after', true);
  displayResults(array_2, field_name, plot_type, ...
    'showImages','off', 'printImages', true, 'savedir', ...
    [pwd,filesep,'Images',filesep,'Array_2',filesep], ...
    'close_after', true);
  displayResults(antv_2, field_name, plot_type, ...
    'showImages','off', 'printImages', true, 'savedir', ...
    [pwd,filesep,'Images',filesep,'Array_2',filesep], ...
    'close_after', true);
  displayResults(array_3, field_name, plot_type, ...
    'showImages','off', 'printImages', true, 'savedir', ...
    [pwd,filesep,'Images',filesep,'Array_3',filesep], ...
    'close_after', true);
  displayResults(antv_3, field_name, plot_type, ...
    'showImages','off', 'printImages', true, 'savedir', ...
    [pwd,filesep,'Images',filesep,'Array_3',filesep], ...
    'close_after', true);
  displayResults(array_4, field_name, plot_type, ...
    'showImages','off', 'printImages', true, 'savedir', ...
    [pwd,filesep,'Images',filesep,'Array_4',filesep], ...
    'close_after', true);
  displayResults(antv_4, field_name, plot_type, ...
    'showImages','off', 'printImages', true, 'savedir', ...
    [pwd,filesep,'Images',filesep,'Array_4',filesep], ...
    'close_after', true);
  displayResults(array_5, field_name, plot_type, ...
    'showImages','off', 'printImages', true, 'savedir', ...
    [pwd,filesep,'Images',filesep,'Array_5',filesep], ...
    'close_after', true);
  displayResults(antv_5, field_name, plot_type, ...
    'showImages','off', 'printImages', true, 'savedir', ...
    [pwd,filesep,'Images',filesep,'Array_5',filesep], ...
    'close_after', true);
end

disp(['Time elapsed for calculating ',array_1.Name,': ',...
    num2str(array_1_time),' seconds']);
disp(['Time elapsed for calculating ',array_2.Name,': ',...
    num2str(array_2_time),' seconds']);
disp(['Time elapsed for calculating ',array_3.Name,': ',...
    num2str(array_3_time),' seconds']);
disp(['Time elapsed for calculating ',array_4.Name,': ',...
    num2str(array_4_time),' seconds']);
disp(['Time elapsed for calculating ',array_5.Name,': ',...
    num2str(array_5_time),' seconds']);
