close all;
clear all;
clc;

##T_0 = 1;
##f_0 = 1/T_0;
##w_0 = 2*pi*f_0;
##F = fft(s);

x = [0 0 1 1 0 0];
N = length(x);
n = 2*pi/N*([1:N] - 1);
epy = 1e-4;

%FT
X = zeros(size(x));
for k = 1:N
  X += x(k)*exp(-1j*n*(k-1));
end
X(X<epy) = 0;
X'

%Inverse DFT
x = zeros(size(X));
for k = 1:N
  x += X(k)*exp(1j*n*(k-1));
end
x(x<epy) = 0;
x /= N;
x'

##t = linspace(0,1,11);
##h = F(1)*ones(size(t));
##for i = 2:length(F)
##  h += F(i)*exp(2j*pi/T_0*(i-1)*t);
##end
##h'