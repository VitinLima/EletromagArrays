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
  Nx = 1;Ny = 1;
  dx = 0;dy = 0;
  default_phi_orientation = 45;
  default_theta_orientation = 0;
  theta_samplei = 0;
  theta_samplef = 180;
  phi_samplei = -180;
  phi_samplef = 180;
  Ntheta = 21;
  Nphi = 21;

base_antenna = readAntenna("Dipolo.csv");
global array;
array = gridArrayConstructor(base_antenna,
  default_phi_orientation, default_theta_orientation,
  x0, Nx, dx, y0, Ny, dy,
  theta_samplei, theta_samplef, Ntheta,
  phi_samplei, phi_samplef, Nphi);

theta = array.THETA;
phi = array.PHI;

disp('Construindo campo elétrico alvo');
global Ephi;
global Etheta;
phi_hat = zeros(3,array.N_samples);
theta_hat = zeros(3,array.N_samples);

ct = cosd(theta);
st = sind(theta);
cp = cosd(phi);
sp = sind(phi);

phi_hat(1,:) = -sp;
phi_hat(2,:) = cp;
theta_hat(1,:) = ct.*cp;
theta_hat(2,:) = ct.*sp;
theta_hat(3,:) = st;

[rEtheta, rEphi] = rotateElectricFields(Etheta, Ephi, theta, phi, )

#Normalize electric fields
a = Ephi.*conj(Ephi);
b = Etheta.*conj(Etheta);
E = sqrt(a + b);
max_magE = max(E);
E /= max_magE;
E_db = 20*log10(E);
Ephi /= max_magE;
Etheta /= max_magE;

disp('Construindo chute');
X0 = zeros(1,5*array.N_antennas);
for i = 1:array.N_antennas
  n = i - 1;
  X0(5*n+1) = array.antennas(i).position(1);
  X0(5*n+2) = array.antennas(i).position(2);
  X0(5*n+3) = array.antennas(i).position(3);
  X0(5*n+4) = array.antennas(i).phi_orientation;
  X0(5*n+5) = array.antennas(i).theta_orientation;
endfor

function C = costfunction(X)
  global f;
  global c;
  global lambda;
  global k;
  
  global array;
  global Ephi;
  global Etheta;
  
  N = length(X)/5;
  
  for i = 1:N
    n = i-1;
    array.antennas(i).position = [X(5*n+1),X(5*n+2),X(5*n+3)]';
    array.antennas(i).phi_orientation = X(5*n+4);
    array.antennas(i).theta_orientation = X(5*n+5);
  endfor
  
  interpolateElectricField_interp;
  dEphi = abs(array.Ephi) - abs(Ephi);
  dEtheta = abs(array.Etheta) - abs(Etheta);
##  C = sum(dEphi.*conj(dEphi) + dEtheta.*conj(dEtheta), 2);
  C = sum(sum(dEphi.*dEphi + dEtheta.*dEtheta));
##  input('continuar');
  disp(['Evaluated cost function C = ',num2str(C),' with X = ', num2str(X)]);
##  C = C*ones(size(X));
end

disp('Comecando')
[X, FVAL, INFO, OUTPUT, FJAC] = fsolve(@costfunction, X0);

disp(INFO);
disp(OUTPUT);