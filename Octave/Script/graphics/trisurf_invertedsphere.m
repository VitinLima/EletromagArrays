function trisurf_invertedsphere(PHI, THETA, Z, C, name, varargin)
  TRI = delaunay(PHI, THETA);
  
  hfig = figure('visible', 'off');
  set(hfig, 'filename', name);
  colormap('jet');
  hold on;
  trisurf( ...
    TRI, ...
    THETA.*cosd(PHI), ...
    THETA.*sind(PHI), ...
    Z, ...
    C, ...
    'linestyle', 'none', ...
    'facecolor', 'interp', ...
    varargin{:});
  
  grid_handles = [
    polar(linspace(0,2*pi,361), 45*ones(1,361)),
    polar(linspace(0,2*pi,361), 90*ones(1,361)),
    polar(linspace(0,2*pi,361), 135*ones(1,361)),
    polar([0 0], [0 180]),
    polar([0 pi/4], [0 180]),
    polar([0 pi/2], [0 180]),
    polar([0 3*pi/4], [0 180]),
    polar([0 pi], [0 180]),
    polar([0 5*pi/4], [0 180]),
    polar([0 3*pi/2], [0 180]),
    polar([0 7*pi/4], [0 180])
  ];
  set(grid_handles, 'color', [.5 .5 .5], 'linewidth', 1);
  thick_handles = [
    text(0, 45, "45º"),
    text(0, 90, "90º"),
    text(0, 135, "135º"),
    text(180, 0, "0º"),
    text(180*cosd(45), 180*sind(45), "45º", 'verticalalignment', 'bottom'),
    text(180*cosd(90), 180*sind(90), "90º", 'verticalalignment', 'bottom'),
    text(180*cosd(135), 180*sind(135), "135º", 'horizontalalignment', 'right', 'verticalalignment', 'bottom'),
    text(180*cosd(180), 180*sind(180), "180º", 'horizontalalignment', 'right'),
    text(180*cosd(225), 180*sind(225), "225º", 'horizontalalignment', 'right', 'verticalalignment', 'top'),
    text(180*cosd(270), 180*sind(270), "270º", 'verticalalignment', 'top'),
    text(180*cosd(315), 180*sind(315), "315º", 'verticalalignment', 'top')
  ];
  grid off;
  axis off;
  colorbar;
end