##figure('visible', showImages);
##FILENAMES(end+1) = 'data_samples';
##hold on;
##line(antenna.theta, antenna.phi, 'linestyle', 'none', 'marker', '.', 'color', 'b');
##line(angle_theta_local, angle_phi_local, 'linestyle', 'none', 'marker', '*', 'color', 'g');
##line([0 0],[-pi pi], 'color', 'r');
##line([pi pi],[-pi pi], 'color', 'r');
##line([0 pi],[pi pi], 'color', 'r');
##line([0 pi],[-pi -pi], 'color', 'r');
##title("Data and sampled points in local coordinates");
##xlabel("Theta");
##ylabel("Phi");
##
figure('visible', showImages);
FILENAMES(end+1) = 'mesh2d';
hold on;
trimesh(TRI, angle_theta_local, angle_phi_local, 'color', 'g');
line([0 0],[-pi pi], 'color', 'r');
line([pi pi],[-pi pi], 'color', 'r');
line([0 pi],[pi pi], 'color', 'r');
line([0 pi],[-pi -pi], 'color', 'r');
title("Meshing of sampled sphere");
xlabel("Theta");
ylabel("Phi");
##
##figure('visible', showImages);
##FILENAMES(end+1) = 'mesh3d';
##hold on;
##trimesh(TRI, P_global(1,:), P_global(2,:), P_global(3,:));
##title("Meshing of sampled sphere");
##xlabel("x");
##ylabel("y");
##zlabel("z");

HFIGS(end+1) = figure('visible', showImages);
FILENAMES(end+1) = 'mesh_invertedSphere';
hold on;
trimesh(TRI, antennaArray.theta.*cosd(antennaArray.phi), antennaArray.theta.*sind(antennaArray.phi), 'color', 'k');
title("Meshing of sampled inverted sphere");
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