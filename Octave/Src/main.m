##clear all;
close all;
clc;

%Constantes
global f = 4.33e8; % <= Frequência de operação [Hz]
global c = 299792458; % <= Velocidade da luz [m/s]
global lambda = c/f; % <= Comprimento de onda [m]
global k = 2*pi/lambda; % <= Número de onda [rad/m]

tic;
base_antenna = readAntenna('antenna-Dipole.csv');
disp(['Time elapsed for reading base antenna: ',num2str(toc),' seconds']);

tic;

ant = idealDipoleAntenna(0.5, -180, 180, 91, 0, 180, 91);
tg_ant = rotateElectricFields(ant, 45, 0);
arr = gridArrayConstructor(ant,
  0, 0,
  0, 1, 0,
  0, 1, 0,
  0, 180, 91,
  -180, 180, 91);
disp(['Time elapsed for initiating array: ',num2str(toc),' seconds']);

tic;
arr = evaluateArray(arr);
disp(['Time elapsed for evaluating array: ',num2str(toc),' seconds']);

arr = rotateElectricFields(arr, 0, 70);

tic;
displayResults(tg_ant);
displayResults(ant);
disp(['Time elapsed for displaying results: ',num2str(toc),' seconds']);

tic;
arr = optimization(arr, tg_ant);
disp(['Time elapsed for achieving target antenna: ',num2str(toc),' seconds']);