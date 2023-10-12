c = 299792458;
f = 433e6;
eta = 120*pi;
w = 2*pi*f;
lambda = c/f;
k = w/c;

dipole_length = 0.5;
L = dipole_length*lambda;

z = linspace(-L/2,L/2,200);

I = cos(k*z);

##I = zeros(1,length(z));
##for i = 1:length(I)
##  if z >= 0
##    I(i) = sin(k.*(L/2 - z(i)));
##  else
##    I(i) = sin(k.*(L/2 + z(i)));
##  end
##end

plot(z, I);