##function array = interpolateElectricField(array)
global f;
global c;
global lambda;
global k;

for antenna = array.antennas
  R = roty(-antenna.theta_orientation)*rotz(-antenna.phi_orientation);
  samples_local = R*array.samples;
  
  theta_samples_local = atan2d(sqrt(dot(samples_local([1, 2],:), samples_local([1, 2],:),1)), samples_local(3,:));
  phi_samples_local = atan2d(samples_local(2,:), samples_local(1,:));
  
  Ephi_local = griddata( ...
    antenna.theta_samples, antenna.phi_samples, ...
    antenna.Ephi, ...
    theta_samples_local, phi_samples_local)';
  Etheta_local = griddata( ...
    antenna.theta_samples, antenna.phi_samples, ...
    antenna.Etheta, ...
    theta_samples_local, phi_samples_local)';

  ct = cosd(theta_samples_local);
  st = sind(theta_samples_local);
  cp = cosd(phi_samples_local);
  sp = sind(phi_samples_local);
  
  rp = zeros(3,3,length(phi_samples_local));
  rp(1,1,:) = cp; rp(1,2,:) = -sp; rp(1,3,:) = 0;
  rp(2,1,:) = sp; rp(2,2,:) = cp; rp(2,3,:) = 0;
  rp(3,1,:) = 0; rp(3,2,:) = 0; rp(3,3,:) = 1;
  rt = zeros(3,3,length(theta_samples_local));
  rt(1,1,:) = ct; rt(1,2,:) = 0; rt(1,3,:) = st;
  rt(2,1,:) = 0; rt(2,2,:) = 1; rt(2,3,:) = 0;
  rt(3,1,:) = -st; rt(3,2,:) = 0; rt(3,3,:) = ct;
  
  for i = 1:3
    for j = 1:3
      r(i,j,:) = rp(i,1,:).*rt(1,j,:)+rp(i,2,:).*rt(2,j,:)+rp(i,3,:).*rt(3,j,:);
    end
  end
  
  vector_theta_local = squeeze([r(1,1,:); r(2,1,:); r(3,1,:)]);
  vector_phi_local = squeeze([r(1,2,:); r(2,2,:); r(3,2,:)]);
  
  vector_Ephi_local = Ephi_local.*vector_phi_local;
  vector_Etheta_local = Etheta_local.*vector_theta_local;
  
  vectorE_local = ...
    vector_Ephi_local + ...
    vector_Etheta_local;
  vectorE_global = R'*vectorE_local;
  
  Af = exp(1j*k*sum(array.samples.*antenna.position,1))*antenna.magI*exp(1j*deg2rad(antenna.phaseI));
  vectorE_global .*= Af;
  
  array.vectorE += vectorE_global;
end

array.Ephi = dot(array.vectorE,array.phi_direction,1);
array.Etheta = dot(array.vectorE,array.theta_direction,1);

#Normalize electric fields
a = array.Ephi.*conj(array.Ephi);
b = array.Etheta.*conj(array.Etheta);
array.E = sqrt(a + b);
max_magE = max(array.E);
array.vectorE /= max_magE;
array.E /= max_magE;
array.E_db = 20*log10(array.E);

array.Ephi /= max_magE;
array.Etheta /= max_magE;