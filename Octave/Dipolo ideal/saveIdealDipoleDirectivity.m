function saveIdealDipoleDirectivity()
  c = 299792458;
  f = 433e6;
  eta = 120*pi;
  w = 2*pi*f;
  lambda = c/f;
  k = w/c;

  fontsize = 20.0;

  %P_in = 1;
  %C_in = 2.435;
  %I_0 = sqrt(P_in/C_in/eta*8*pi);

  dipole_length = 0.5;
  L = dipole_length*lambda;
  theta = linspace(1e-3, pi-1e-3, 90);
  phi = linspace(-pi, pi, 90);
  [THETA, PHI] = meshgrid(theta, phi);

  A = eta/2/pi;
  C = cos(k*L/2*cos(THETA)) - cos(k*L/2);
  E = sin(THETA);
  rE = A .* C ./ E;
  rE(THETA==0) = 0;
  rE = abs(rE);

##  W_ar = 1/2/eta*rE.*rE;
##  C = cos(k*L/2*cos(theta)) - cos(k*L/2);
##  D = C.*C ./ sin(theta) * pi/(length(theta)-1);
##  D(theta==0) = 0;
##  P_in = eta/4/pi*sum(D)/radiatedPower;
##  I_0 = 1/sqrt(P_in);
##  rE *= 1000*I_0;

##  min_rE = min(min(rE));
##  max_rE = max(max(rE));
  C = cos(k*L/2*cos(theta)) - cos(k*L/2);

  U = rE.*rE/2/eta;
##  P_rad = sum(sum(U.*sin(THETA)))*pi/length(theta)*2*pi/length(phi);
  P_rad = eta/4/pi*sum(C.*C./sin(theta))*pi/length(theta)
  U_iso = P_rad/4/pi;
  D = U/U_iso;
  D_dB = 10*log10(D);

  XX = D.*sin(THETA).*cos(PHI);
  YY = D.*sin(THETA).*sin(PHI);
  ZZ = D.*cos(THETA);

  figure('visible', 'on');
  hold on;

  h = surf(XX, YY, ZZ, D_dB, 'linestyle', 'none', 'facecolor', 'interp');
  rotate(h, [0 1 0], 90);
  rotate(h, [0 0 1], 90);

  xlabel('x');
  ylabel('y');
  zlabel('z');
  xticks([]);
  yticks([]);
  zticks([]);
  grid on;
  colormap jet;
  cb = colorbar;
  ylabel(cb, '[dB]');
  axis equal;
  view(-45,30);
  set(gca, 'fontsize', fontsize);
  title(['Diretividade máxima = ', num2str(max(max(D_dB)),2), ' dB']);

  dipole_length = strjoin(strsplit(num2str(dipole_length), '.'), '-');
##  in = input("Enter 1 to continue\nEnter 2 to cancel\n");
##  if in==1
    saveas(gcf, ['rE ', dipole_length, '.png']);
##  end
end
