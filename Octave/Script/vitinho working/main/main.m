clear all;
close all;
clc;

initConstants;
global program;

program.pwd = fileparts(mfilename('fullpath'));
addpath(program.pwd);
addpath(fullfile(program.pwd, 'gui'));
addpath(fullfile(program.pwd, 'graphics'));

program.antennas = [];
program.arrays = [];
program.analysis = {};
program.results = [];

unwind_protect
  gui;
unwind_protect_cleanup
  
end
return;

tic;
base_antenna = readAntenna('Dipolo.csv');
disp(['Time elapsed for reading base antenna: ',num2str(toc),' seconds']);

tic;

ant = idealDipoleAntenna(0.5, -180, 180, 91, 0, 180, 91);
tg_ant = rotateAntenna(ant, 45, 0);
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

arr = rotateAntenna(arr, 0, 70);

tic;
displayResults(tg_ant);
displayResults(ant);
disp(['Time elapsed for displaying results: ',num2str(toc),' seconds']);

tic;
arr = optimization(arr, tg_ant);
disp(['Time elapsed for achieving target antenna: ',num2str(toc),' seconds']);

##if program.logger != stdout
##  fclose(program.logger);
##end
##
##if program.save_path != -1
##  save(program.save_path, 'program');
##end