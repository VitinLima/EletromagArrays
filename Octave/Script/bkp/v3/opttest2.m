#Loop dado pelo número de antenas
#Gerar o fator de antenas para um dado número de antenas
# Função de custo euclediana
#gostaríamos de uma potencia de 16dB, então o critério de parada pode ser o erro do arranjo para antena ser próximo de 16dB.


clear all;
##base_antenna = readAntenna("Yagi4El.csv");
close all;
clc;

%Constantes
global f = 4.33e8; % <= Frequência de operação [Hz]
global c = 299792458; % <= Velocidade da luz [m/s]
global lambda = c/f; % <= Comprimento de onda [m]
global k = 2*pi/lambda; % <= Número de onda [rad/m]

disp('Construindo arranjo');
  x0 = 0;y0 = 0;
  Nx = 1;Ny = 4;
  dx = 0;dy = 0.5;
  default_beta = 0;
  default_alpha = 0;
  theta_samplei = 0;
  theta_samplef = 180;
  phi_samplei = -180;
  phi_samplef = 180;
  Ntheta = 41;
  Nphi = 51;

antenna = idealDipoleAntenna(0.5, -180, 180, 91, 0, 180, 91);
global array;
array = gridArrayConstructor(antenna,
  default_beta, default_alpha,
  x0, Nx, dx, y0, Ny, dy,
  theta_samplei, theta_samplef, Ntheta,
  phi_samplei, phi_samplef, Nphi);
for i = 1:array.N_antennas
  array.antennas(i).position += lambda*(rand(1,3)-0.5)*0.3;
##  array.antennas(i).alpha = 10*(rand-0.5);
##  array.antennas(i).beta = 10*(rand-0.5);
end

disp('Construindo campo elétrico alvo');
global tg_antenna;
tg_antenna = gridArrayConstructor(antenna,
  default_beta, default_alpha,
  x0, Nx, dx, y0, Ny, dy,
  theta_samplei, theta_samplef, Ntheta,
  phi_samplei, phi_samplef, Nphi);
##tg_antenna.antennas(1).alpha = 45;
##tg_antenna.antennas(1).beta = 62;
##tg_antenna.antennas(2).alpha = 73;
##tg_antenna.antennas(2).beta = 14;
##tg_antenna.antennas(3).alpha = 34;
##tg_antenna.antennas(3).beta = 92;
tg_antenna = evaluateArray(tg_antenna);
##tg_antenna = rotateElectricFields(tg_antenna, 15, 73);

disp('Construindo chute');
X0 = zeros(1,5*array.N_antennas);
for i = 1:array.N_antennas
  n = i - 1;
  X0(5*n+1) = array.antennas(i).position(1);
  X0(5*n+2) = array.antennas(i).position(2);
  X0(5*n+3) = array.antennas(i).position(3);
  X0(5*n+4) = array.antennas(i).beta;
  X0(5*n+5) = array.antennas(i).alpha;
endfor

function C = costfunction(X)
  global f;
  global c;
  global lambda;
  global k;
  
  global array;
  global tg_antenna;
  
  for i = 1:array.N_antennas
    n = i-1;
    array.antennas(i).position = [X(5*n+1),X(5*n+2),X(5*n+3)]';
    array.antennas(i).beta = X(5*n+4); %beta
    array.antennas(i).alpha = X(5*n+5); %alpha
  endfor
  
  array = evaluateArray(array);
  dEphi = abs(array.Ephi) - abs(tg_antenna.Ephi);
  dEtheta = abs(array.Etheta) - abs(tg_antenna.Etheta);
##  C = sum(dEphi.*conj(dEphi) + dEtheta.*conj(dEtheta), 2);
  C = sum(sum(dEphi.*dEphi + dEtheta.*dEtheta));
##  input('continuar');
  disp(['Evaluated cost function C = ',num2str(C)]);%,' with X = ', num2str(X)]);
end

disp('Comecando')
[X, FVAL, INFO, OUTPUT, FJAC] = fsolve(@costfunction, X0);

disp(INFO);
disp(OUTPUT);

disp(['Optimization finalized with cost function C = ',num2str(FVAL)]);%,', Position X = ', num2str(X(1:3)), ', beta = ', num2str(X(4)), ' and alpha = ', num2str(X(5))]);

for i = 1:array.N_antennas
  n = i-1;
  array.antennas(i).position = [X0(5*n+1),X0(5*n+2),X0(5*n+3)]';
  array.antennas(i).beta = X0(5*n+4); %beta
  array.antennas(i).alpha = X0(5*n+5); %alpha
endfor
array = evaluateArray(array);
displayResults(array);

for i = 1:array.N_antennas
  n = i-1;
  array.antennas(i).position = [X(5*n+1),X(5*n+2),X(5*n+3)]';
  array.antennas(i).beta = X(5*n+4); %beta
  array.antennas(i).alpha = X(5*n+5); %alpha
endfor
array = evaluateArray(array);
displayResults(array);

displayResults(tg_antenna);