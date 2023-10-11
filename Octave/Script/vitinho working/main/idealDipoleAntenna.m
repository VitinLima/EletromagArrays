function antenna = idealDipoleAntenna(L,
    phi_samplei=-180, phi_samplef=180, Nphi=31,
    theta_samplei=0, theta_samplef=90, Ntheta=21)
  global lambda;
  global k;
  
  antenna = emptyAntenna( ...
    phi_samplei, phi_samplef, Nphi, ...
    theta_samplei, theta_samplef, Ntheta);
  
  antenna.Ephi = zeros(1,antenna.N_samples);
  antenna.Etheta = zeros(1,antenna.N_samples);
  
  A = k*L*lambda/2;
  st = sind(antenna.THETA);
  ct = cosd(antenna.THETA);
  
  ids = st != 0;
  antenna.Ephi(ids) = (cos(A*ct(ids)) - cos(A))./st(ids);
  
  #Normalize electric fields
  a = antenna.Ephi.*conj(antenna.Ephi);
  b = antenna.Etheta.*conj(antenna.Etheta);
  antenna.E = sqrt(a + b);
  max_magE = max(max(antenna.E));
  
  antenna.E /= max_magE;
  antenna.Ephi /= max_magE;
  antenna.Etheta /= max_magE;
  
  antenna.Name = ["Ideal dipole with length=",num2str(L)];
end