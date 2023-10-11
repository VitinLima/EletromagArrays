function radiationDiagram(antenna, beta, alpha, showIm=true)
  global program;
  
  N = 301;
  angles = linspace(-pi,pi,N);
  points = zeros(3, N);
  points(1,:) = cos(angles);
  points(2,:) = sin(angles);
  
  points = rotz(beta)*roty(alpha)*points;
  interp_phi = atan2d(points(2,:), points(1,:));
  interp_theta = atan2d(sqrt(dot(points(1:2,:),points(1:2,:),1)),points(3,:));
  
  antenna = toMeshShape(antenna);
  Ephi = interp2(antenna.THETA_samplings,antenna.PHI_samplings, antenna.Ephi, interp_theta, interp_phi);
  Etheta = interp2(antenna.THETA_samplings,antenna.PHI_samplings, antenna.Etheta, interp_theta, interp_phi);
  
  figure('visible', showIm, 'filename', 'radiation diagram rE');
  hold on;
  
  line(rad2deg(angles), Ephi);
  
  grid on;
  xlabel("Angle");
  ylabel("rE");
  hold off;
end