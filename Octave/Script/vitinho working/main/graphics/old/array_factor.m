##HFIGS(end+1) = figure('visible', showImages);
##FILENAMES(end+1) = 'Af_plane_xy';
##hold on;
##N = 151;
####ids = antennaArray.theta==90;
##PHI = linspace(-180,180,N);
##THETA = 90*ones(1,N);
##RHO = griddata( ...
##  antennaArray.theta, antennaArray.phi, ...
##  abs(antennaArray.Af), ...
##  THETA, PHI)';
####PHI = antennaArray.phi(ids);
####THETA = antennaArray.theta(ids);
####RHO = abs(antennaArray.Af(ids));
##polar(deg2rad(PHI), RHO);
##D = RHO(2:end)-RHO(1:end-1);
##DD = shift(D,-1)-D;
##idsD = find(sign(D) != sign(shift(D,1)));
##if !isempty(idsD)
##  idsC = idsD==shift(idsD+1,1);
##  idsD(idsC) = [];
##  idsDD = idsD(DD(idsD)<0);
##  [XDD, YDD] = pol2cart(deg2rad(PHI(idsDD)),RHO(idsDD));
##  line(XDD, YDD, 'linestyle', 'none', 'marker', '*', 'color', 'g');
##  for i = 1:length(idsDD)
##    n = 20*log10(RHO(idsDD(i)));
##    n(n*n<1e-2) = 0;
##    text(XDD(i), YDD(i), num2str(n,3));
##  end
##end
##axis equal;
##axis off;
##grid on;
##title("Arrange factor at the xy plane");
##xlabel("x");
##ylabel("y");
##
##HFIGS(end+1) = figure('visible', showImages);
##FILENAMES(end+1) = 'Af_plane_xz';
##hold on;
##N = 151;
##THETA = linspace(-180,180,N);
##PHI = zeros(1,N);
##ids = THETA < 0;
##PHI(ids) = 180;
##THETA(ids) *= -1;
##RHO = griddata( ...
##  antennaArray.theta, antennaArray.phi, ...
##  abs(antennaArray.Af), ...
##  THETA, PHI)';
##THETA(ids) *= -1;
##PHI(ids) = 0;
##polar(deg2rad(THETA), RHO);
##D = RHO(2:end)-RHO(1:end-1);
##DD = shift(D,-1)-D;
##idsD = find(sign(D) != sign(shift(D,1)));
##if !isempty(idsD)
##  idsC = idsD==shift(idsD+1,1);
##  idsD(idsC) = [];
##  idsDD = idsD(DD(idsD)<0);
##  [XDD, YDD] = pol2cart(deg2rad(THETA(idsDD)),RHO(idsDD));
##  line(XDD, YDD, 'linestyle', 'none', 'marker', '*', 'color', 'g');
##  for i = 1:length(idsDD)
##    n = 20*log10(RHO(idsDD(i)));
##    n(n*n<1e-2) = 0;
##    text(XDD(i), YDD(i), num2str(n,3));
##  end
##end
##axis equal;
##axis off;
##grid on;
##title("Array factor at the xz plane");
##xlabel("x");
##ylabel("z");

HFIGS(end+1) = figure('visible', showImages);
FILENAMES(end+1) = 'Af_invertedSphere';
colormap('jet');
hold on;
trisurf(TRI, antennaArray.theta.*cosd(antennaArray.phi), antennaArray.theta.*sind(antennaArray.phi), zeros(1,length(antennaArray.theta)), antennaArray.Af, 'linestyle', 'none', 'facecolor', 'interp');
colorbar;
title("Array factor magnitude");
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