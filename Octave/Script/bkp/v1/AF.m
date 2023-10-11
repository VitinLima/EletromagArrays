f = 433e6;
c = 299792458;
lambda = c/f;
k = 2*pi/lambda;

N = 30;
phi = linspace(-180, 180, 503);
y = linspace(-N*lambda/4,N*lambda/4,N);
x = zeros(1,N);

DefGeo = zeros(1,N);
Af = zeros(1,N);

for i = 1:N
  DefGeo(i) = 
end