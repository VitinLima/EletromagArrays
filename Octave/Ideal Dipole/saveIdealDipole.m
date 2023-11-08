function saveIdealDipole(dipole_length, radiatedPower)
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

  L = dipole_length*lambda;
  theta = linspace(0, pi, 90);
  phi = linspace(-pi, pi, 30);
  [THETA, PHI] = meshgrid(theta, phi);

  A = eta;
  B = 2*pi;
  C = cos(k*L/2*cos(THETA)) - cos(k*L/2);
  E = sin(THETA);
  rE = A ./ B .* C ./ E;
  rE(THETA==0) = 0;
  rE = abs(rE);

  W_ar = 1/2/eta*rE.*rE;
  C = cos(k*L/2*cos(theta)) - cos(k*L/2);
  D = C.*C ./ sin(theta) * pi/(length(theta)-1);
  D(theta==0) = 0;
  P_in = eta/4/pi*sum(D)/radiatedPower;
  I_0 = 1/sqrt(P_in);
  rE *= I_0;

  rE *= 1000;

  st = sin(THETA);
  ct = cos(THETA);
  sp = sin(PHI);
  cp = cos(PHI);

##  min_rE = min(min(rE));
  max_rE = max(max(rE));
  R = rE/max_rE;
  XX = R.*st.*cp;
  YY = R.*st.*sp;
  ZZ = R.*ct;

  disp([num2str(dipole_length), " Prad: ",
  num2str(sum(sum(rE.*st))/prod(size(THETA)))])

  figure('visible', 'on');
  hold on;

  h = surf(XX, YY, ZZ, rE, 'linestyle', 'none', 'facecolor', 'interp');
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
  caxis([0 10000]);
  ylabel(cb, '[mV]');
  axis equal;
##  set(gca, 'cameraposition', [1 1 0.4]);
##  set(gca, 'cameratarget', [0 0 0]);
##  set(gca, 'cameraupvector', [0 0 1]);
  view(-45, 30);
  set(gca, 'fontsize', fontsize);

  dipole_length = strjoin(strsplit(num2str(dipole_length), '.'), '-');
##  in = input("Enter 1 to continue\nEnter 2 to cancel\n");
##  if in==1
    saveas(gcf, ['rE ', dipole_length, '.png']);
##  end
end