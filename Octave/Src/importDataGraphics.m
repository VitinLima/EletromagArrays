1;
##disp('Importing data graphical functions');

function quiver3d(ant, field, showIm)
  figure('visible', showIm, 'filename', 'polar3d rE');
  hold on;

##  ant = toVectorShape(ant);
  quiver3(ant.k_hat(1,:), ant.k_hat(2,:), ant.k_hat(3,:), field(1,:), field(2,:), field(3,:));

  axis equal;
  xlabel('x');
  ylabel('y');
  zlabel('z');
end

function polar3d(ant, field_name, showIm)
  figure('visible', showIm, 'filename', ['polar3d rE', field_name]);
  hold on;

  ant = toMeshShape(ant);
  field = getfield(ant, field_name);
  cp = cosd(ant.PHI);
  sp = sind(ant.PHI);
  ct = cosd(ant.THETA);
  st = sind(ant.THETA);
  XX = st.*cp;
  YY = st.*sp;
  ZZ = ct;
  surf(abs(field).*XX, ...
    abs(field).*YY, ...
    abs(field).*ZZ, ...
    abs(field), ...
    'linestyle', 'none', ...
    'facecolor', 'interp');

##  title('polar3d field');
  axis equal;
  xlabel('x');
  ylabel('y');
  zlabel('z');
  view(45,30);
  set(gcf, 'filename', [ant.Name,' polar 3d ', field_name])
end

function invertedSphere_rE(varargin)
  p = inputParser();
  p.FunctionName = "invertedSphere_rE";
  p.addRequired("mesh_theta");
  p.addRequired("mesh_phi");
  p.addRequired("mesh_field");
  p.addParameter("showIm", false);
  p.addParameter("cmap", "jet");
  p.addParameter("title", "");
  p.addParameter("color_range", "auto");

  p.parse(varargin{:});
  args_in = p.Results;

  figure('visible', args_in.showIm, 'filename', ['inverted sphere rE', args_in.title]);
  hold on;

  surf(args_in.mesh_theta.*cosd(args_in.mesh_phi), ...
    args_in.mesh_theta.*sind(args_in.mesh_phi), ...
    zeros(size(args_in.mesh_field)), ...
    args_in.mesh_field, ...
    'linestyle', 'none', ...
    'facecolor', 'interp');

  R_ticks = [45, 90, 135, 180];
  Theta_ticks = [0, 45, 90, 135, 180, 225, 270, 315];
  grid_handles = [];
  thick_handles = [];
  for i = 1:length(R_ticks)
    R = R_ticks(i);
    grid_handles(end+1) = polar(linspace(0,2*pi,361), R*ones(1,361));
    thick_handles(end+1) = text(R*cosd(67.5), R*sind(67.5), [num2str(R_ticks(i)),"º"], ...
      'horizontalalignment', 'center', ...
      'verticalalignment', 'bottom');
  end
  for i = 1:length(Theta_ticks)
    grid_handles(end+1) = polar(deg2rad(Theta_ticks(i))*[1 1], [R_ticks(1) R_ticks(end)]);
    if -22.5 < Theta_ticks(i) && Theta_ticks(i) < 22.5
      v_alignment = 'middle';
      h_alignment = 'left';
    elseif 22.5 <= Theta_ticks(i) && Theta_ticks(i) < 67.5
      v_alignment = 'bottom';
      h_alignment = 'left';
    elseif 67.5 <= Theta_ticks(i) && Theta_ticks(i) < 112.5
      v_alignment = 'bottom';
      h_alignment = 'center';
    elseif 112.5 <= Theta_ticks(i) && Theta_ticks(i) < 157.5
      v_alignment = 'bottom';
      h_alignment = 'right';
    elseif 157.5 <= Theta_ticks(i) && Theta_ticks(i) < 202.5
      v_alignment = 'middle';
      h_alignment = 'right';
    elseif 202.5 <= Theta_ticks(i) && Theta_ticks(i) < 247.5
      v_alignment = 'top';
      h_alignment = 'right';
    elseif 247.5 <= Theta_ticks(i) && Theta_ticks(i) < 292.5
      v_alignment = 'top';
      h_alignment = 'center';
    elseif 292.5 <= Theta_ticks(i) && Theta_ticks(i) < 337.5
      v_alignment = 'top';
      h_alignment = 'left';
    else
      v_alignment = 'middle';
      h_alignment = 'left';
    end
    R = R_ticks(end);
    thick_handles(end+1) = text(R*cosd(Theta_ticks(i)), R*sind(Theta_ticks(i)), [num2str(Theta_ticks(i)),"º"], 'verticalalignment', v_alignment, 'horizontalalignment', h_alignment);
  end
  set(grid_handles, 'color', [1 1 1], 'linewidth', 1);

  colormap(args_in.cmap);
  colorbar;
  caxis(args_in.color_range);
##  title("inverted sphere rE");
  set(gcf, 'filename', [args_in.title,' inverted sphere rE'])
  grid off;
  axis off;
end

function polar_Directivity(ant, showIm)
  figure('visible', showIm, 'filename', 'polar directivity');
  hold on;

  ant = toVectorShape(ant);

  r_grid = 1.3;
  r1 = 1;
  r2 = 1/sqrt(2);
  r3 = 1/sqrt(10);
  grid_handles = [ ...
    polar(linspace(0,2*pi,361), ones(1,361)*r1), ...
    polar(linspace(0,2*pi,361), ones(1,361)*r2), ...
    polar(linspace(0,2*pi,361), ones(1,361)*r3), ...
    polar([0 0], [0 r_grid]), ...
    polar([0 pi/4], [0 r_grid]), ...
    polar([0 pi/2], [0 r_grid]), ...
    polar([0 3*pi/4], [0 r_grid]), ...
    polar([0 pi], [0 r_grid]), ...
    polar([0 5*pi/4], [0 r_grid]), ...
    polar([0 3*pi/2], [0 r_grid]), ...
    polar([0 7*pi/4], [0 r_grid])
  ];
  set(grid_handles, 'color', [.9 .9 .9], 'linewidth', 0.1);
  thick_handles = [
    text(r3*cosd(67.5), r3*sind(67.5), num2str(20*log(r3)), ...
      'horizontalalignment', 'center', ...
      'verticalalignment', 'bottom'), ...
    text(r2*cosd(67.5), r2*sind(67.5), num2str(20*log(r2)), ...
      'horizontalalignment', 'center', ...
      'verticalalignment', 'bottom'), ...
    text(r1*cosd(67.5), r1*sind(67.5), num2str(20*log(r1)), ...
      'horizontalalignment', 'center', ...
      'verticalalignment', 'bottom'), ...
    text(r_grid, 0, "0º"), ...
    text(r_grid*cosd(45), r_grid*sind(45), "45º", ...
      'verticalalignment', 'bottom'), ...
    text(r_grid*cosd(90), r_grid*sind(90), "90º", ...
      'verticalalignment', 'bottom'), ...
    text(r_grid*cosd(135), r_grid*sind(135), "135º", ...
      'horizontalalignment', 'right', ...
      'verticalalignment', 'bottom'), ...
    text(r_grid*cosd(180), r_grid*sind(180), "180º", ...
      'horizontalalignment', 'right'), ...
    text(r_grid*cosd(225), r_grid*sind(225), "225º", ...
      'horizontalalignment', 'right', ...
      'verticalalignment', 'top'), ...
    text(r_grid*cosd(270), r_grid*sind(270), "270º", ...
      'verticalalignment', 'top'), ...
    text(r_grid*cosd(315), r_grid*sind(315), "315º", ...
      'verticalalignment', 'top')
  ];

  ids = ant.THETA==90;

  THETA = ant.PHI(ids);
  RHO = abs(ant.E(ids));
  h = polar(deg2rad(THETA), RHO);
  set(h, 'color', 'b');
  D = RHO(2:end)-RHO(1:end-1);
  DD = shift(D,-1)-D;
  idsD = find(sign(D) != sign(shift(D,1)));
  if !isempty(idsD)
    idsC = idsD==shift(idsD+1,1);
    idsD(idsC) = [];
    idsDD = idsD(DD(idsD)<0);
    [XDD, YDD] = pol2cart(deg2rad(THETA(idsDD)),RHO(idsDD));
    line(XDD, YDD, 'linestyle', 'none', 'marker', '*', 'color', 'g');
    [XDD, YDD] = pol2cart(deg2rad(THETA(idsDD)),RHO(idsDD)+0.05);
    for i = 1:length(idsDD)
      n = 20*log10(RHO(idsDD(i)));
      n(n*n<1e-2) = 0;
      text(XDD(i), YDD(i), num2str(n,3), ...
        'horizontalalignment', 'center', ...
        'verticalalignment', 'middle');
    end
  end

  title('polar directivity');
  axis equal;
  axis off;
  grid on;
  xlabel('x');
  ylabel('y');
end
