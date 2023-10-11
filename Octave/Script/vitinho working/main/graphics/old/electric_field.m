##HFIGS(end+1) = figure('visible', showImages);
##FILENAMES(end+1) = 'Ephi';
##colormap('jet');
##hold on;
##trisurf(TRI, P_global(1,:), P_global(2,:), P_global(3,:), magrEphi, 'linestyle', 'none', 'facecolor', 'interp');
##colorbar;
##title("E_{phi} field magnitude");
##xlabel("x");
##ylabel("y");
##zlabel("z");
##
##HFIGS(end+1) = figure('visible', showImages);
##FILENAMES(end+1) = 'Etheta';
##colormap('jet');
##hold on;
##trisurf(TRI, P_global(1,:), P_global(2,:), P_global(3,:), magrEtheta, 'linestyle', 'none', 'facecolor', 'interp');
##colorbar;
##title("E_{theta} field magnitude");
##xlabel("x");
##ylabel("y");
##zlabel("z");
##
##HFIGS(end+1) = figure('visible', showImages);
##FILENAMES(end+1) = 'E';
##colormap('jet');
##hold on;
##trisurf(TRI,
##  P_global(1,:),
##  P_global(2,:),
##  P_global(3,:),
##  magrE,
##  'linestyle', 'none',
##  'facecolor', 'interp');
##colorbar;
##title("Electric field magnitude");
##xlabel("x");
##ylabel("y");
##zlabel("z");
##
##HFIGS(end+1) = figure('visible', showImages);
##FILENAMES(end+1) = 'Efield_phi_theta';
##colormap('jet');
##hold on;
##quiver3(P_global(1,:), P_global(2,:), P_global(3,:), vector_Etheta(1,:), vector_Etheta(2,:), vector_Etheta(3,:), 'color', 'g');
##quiver3(P_global(1,:), P_global(2,:), P_global(3,:), vector_Ephi(1,:), vector_Ephi(2,:), vector_Ephi(3,:), 'color', 'b');
##colorbar;
##title("E_{phi} and E_{theta} fields");
##xlabel('x');
##ylabel('y');
##zlabel('z');
##
##HFIGS(end+1) = figure('visible', showImages);
##FILENAMES(end+1) = 'EField';
##colormap('jet');
##hold on;
##quiver3(P_global(1,:), P_global(2,:), P_global(3,:), vector_E(1,:), vector_E(2,:), vector_E(3,:), 'color', 'b');
##colorbar;
##title("Electric field");
##xlabel('x');
##ylabel('y');
##zlabel('z');
##
##HFIGS(end+1) = figure('visible', showImages);
##FILENAMES(end+1) = 'magEphi';
##colormap('jet');
##hold on;
##trisurf(TRI,
##  magrEphi.*P_global(1,:),
##  magrEphi.*P_global(2,:),
##  magrEphi.*P_global(3,:),
##  magrEphi,
##  'linestyle', 'none',
##  'facecolor', 'interp');
##colorbar;
##title("E_{phi} field magnitude");
##xlabel("x");
##ylabel("y");
##zlabel("z");
##
##HFIGS(end+1) = figure('visible', showImages);
##FILENAMES(end+1) = 'magEtheta';
##colormap('jet');
##hold on;
##trisurf(TRI,
##  magrEtheta.*P_global(1,:),
##  magrEtheta.*P_global(2,:),
##  magrEtheta.*P_global(3,:),
##  magrEtheta,
##  'linestyle', 'none',
##  'facecolor', 'interp');
##colorbar;
##title("E_{theta} field magnitude");
##xlabel("x");
##ylabel("y");
##zlabel("z");
##
##HFIGS(end+1) = figure('visible', showImages);
##FILENAMES(end+1) = 'magE';
##colormap('jet');
##hold on;
##trisurf(TRI,
##  magrE.*P_global(1,:),
##  magrE.*P_global(2,:),
##  magrE.*P_global(3,:),
##  magrE,
##  'linestyle', 'none',
##  'facecolor', 'interp');
##colorbar;
##title("Electric field magnitude");
##xlabel("x");
##ylabel("y");
##zlabel("z");

HFIGS(end+1) = figure('visible', showImages);
FILENAMES(end+1) = 'magE_invertedSphere';
colormap('jet');
hold on;
trisurf(TRI, antennaArray.theta.*cosd(antennaArray.phi), antennaArray.theta.*sind(antennaArray.phi), zeros(1,length(antennaArray.theta)), magrE, 'linestyle', 'none', 'facecolor', 'interp');
colorbar;
title("Electric field magnitude");
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