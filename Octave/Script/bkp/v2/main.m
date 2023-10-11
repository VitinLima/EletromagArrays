##clear all;
##base_antenna = readAntenna("Yagi4El.csv");
close all;
clc;

%Constantes
global f = 4.33e8; % <= Frequência de operação [Hz]
global c = 299792458; % <= Velocidade da luz [m/s]
global lambda = c/f; % <= Comprimento de onda [m]
global k = 2*pi/lambda; % <= Número de onda [rad/m]

tic;
base_antenna = readAntenna('Yagi4El.csv');
disp(['Time elapsed for reading base antenna: ',num2str(toc),' seconds']);

tic;
initiateArrayProblem5;
disp(['Time elapsed for initiating array: ',num2str(toc),' seconds']);

tic;
interpolateElectricField_interp;
disp(['Time elapsed for interpolating electic fields with interp2: ',num2str(toc),' seconds']);
tic;
add_info = 'interp2';
displayResults;
disp(['Time elapsed for displaying results: ',num2str(toc),' seconds']);

tic;
interpolateElectricField_griddata;
disp(['Time elapsed for interpolating electic fields with griddata: ',num2str(toc),' seconds']);
tic;
add_info = 'griddata';
displayResults;
disp(['Time elapsed for displaying results: ',num2str(toc),' seconds']);