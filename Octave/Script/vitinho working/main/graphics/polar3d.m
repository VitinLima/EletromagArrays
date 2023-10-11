function polar3d(ax_h, ant, field, in_dB=false)
##  figure('visible', 'off', 'filename', 'polar3d rE');
  hold on;
  
  ant = toMeshShape(ant);
  field = reshape(field, [ant.N_phi, ant.N_theta]);
  cp = cosd(ant.PHI);
  sp = sind(ant.PHI);
  ct = cosd(ant.THETA);
  st = sind(ant.THETA);
  XX = st.*cp;
  YY = st.*sp;
  ZZ = ct;
  R = field;
  if in_dB
    C = 20*log10(field);
  else
    C = field;
  end
  surf(ax_h, R.*XX, ...
    R.*YY, ...
    R.*ZZ, ...
    C, ...
    'linestyle', 'none', ...
    'facecolor', 'interp');
  
##  title('polar3d rE');
  axis equal;
  xlabel('x');
  ylabel('y');
  zlabel('z');
  view(45,30);
##  set(gcf, 'filename', [ant.Name,' polar 3d rE'])
end