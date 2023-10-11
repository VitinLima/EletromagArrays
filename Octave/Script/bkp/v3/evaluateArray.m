function array = evaluateArray(array)
  global f;
  global c;
  global lambda;
  global k;
  
  cp = cosd(array.PHI);
  sp = sind(array.PHI);
  ct = cosd(array.THETA);
  st = sind(array.THETA);
  v = repmat(cat(1,st.*cp,st.*sp,ct),1,1,array.N_antennas);
  pd = repmat(cat(1,-sp,cp,zeros(1,array.N_samples)),1,1,array.N_antennas);
  td = repmat(cat(1,ct.*cp,ct.*sp,-st),1,1,array.N_antennas);

  ct = cosd(cat(3,array.antennas.alpha));
  st = -sind(cat(3,array.antennas.alpha));
  cp = cosd(cat(3,array.antennas.beta));
  sp = -sind(cat(3,array.antennas.beta));
  Rt = zeros(3,3,array.N_antennas);
  Rt(1,1,:) = ct; Rt(1,2,:) = 0; Rt(1,3,:) = st;
  Rt(2,1,:) = 0; Rt(2,2,:) = 1; Rt(2,3,:) = 0;
  Rt(3,1,:) = -st; Rt(3,2,:) = 0; Rt(3,3,:) = ct;
  Rp = zeros(3,3,array.N_antennas);
  Rp(1,1,:) = cp; Rp(1,2,:) = -sp; Rp(1,3,:) = 0;
  Rp(2,1,:) = sp; Rp(2,2,:) = cp; Rp(2,3,:) = 0;
  Rp(3,1,:) = 0; Rp(3,2,:) = 0; Rp(3,3,:) = 1;
  function C = pagemtimes(A,B)
    B = permute(B, [2,1,3]);
    C(3,:,:) = sum(A(3,:,:).*B,2);
    C(2,:,:) = sum(A(2,:,:).*B,2);
    C(1,:,:) = sum(A(1,:,:).*B,2);
  end
  R = pagemtimes(Rt, Rp);

  vi = pagemtimes(R,v);
  R_t = permute(R, [2,1,3]);

  pi = atan2d(vi(2,:,:),vi(1,:,:));
  ti = atan2d(abs(vi(1,:,:) + 1j*vi(2,:,:)),vi(3,:,:));
  ct = cosd(ti);
  st = sind(ti);
  cp = cosd(pi);
  sp = sind(pi);
  pdi = pagemtimes(R_t, cat(1,-sp,cp,zeros(1,array.N_samples,array.N_antennas)));
  tdi = pagemtimes(R_t, cat(1,ct.*cp,ct.*sp,-st));
  Epi = zeros(1,array.N_samples,array.N_antennas);
  Eti = zeros(1,array.N_samples,array.N_antennas);

  for i = 1:array.N_antennas
    ant_i = array.antennas(i);
    
    t = ant_i.THETA_samplings;
    p = ant_i.PHI_samplings;
    
    Et = reshape(ant_i.Etheta, ant_i.N_phi, ant_i.N_theta);
    Ep = reshape(ant_i.Ephi, ant_i.N_phi, ant_i.N_theta);
    
    Epi(:,:,i) = interp2(t, p, Ep, ti(:,:,i), pi(:,:,i));
    Eti(:,:,i) = interp2(t, p, Et, ti(:,:,i), pi(:,:,i));
  end

  av = cat(3, array.antennas.position);
  ai = cat(3, array.antennas.magI);
  api = cat(3, array.antennas.phaseI);

  Af = exp(-1j*k*sum(v.*av,1)).*ai.*exp(1j*deg2rad(api));
  Epi .*= Af;
  Eti .*= Af;

  array.Ephi = sum(dot(pd,Epi.*pdi+Eti.*tdi,1),3);
  array.Etheta = sum(Epi.*dot(td,pdi,1) + Eti.*dot(td,tdi,1),3);

  #Normalize electric fields
  a = array.Ephi.*conj(array.Ephi);
  b = array.Etheta.*conj(array.Etheta);
  array.E = sqrt(a + b);
  max_magE = max(array.E);

  array.E /= max_magE;
  array.Ephi /= max_magE;
  array.Etheta /= max_magE;
end