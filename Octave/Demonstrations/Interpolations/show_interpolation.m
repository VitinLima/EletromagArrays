clear all; close all; clc;

N_theta = 9;
N_phi = 11;

fontsize = 20.0;

elevation = -40;
azimuth = 15;
##roll = 45;
##elevation = 0;
##azimuth = 0;
roll = 0;

theta = linspace(0, 180, N_theta);
phi = linspace(-180, 180, N_phi);

[THETA, PHI] = meshgrid(theta, phi);
N = N_theta*N_phi;
mesh_shape = [N_phi, N_theta];
vector_shape = [1, N];

THETA = THETA(:)';
PHI = PHI(:)';

ct = cosd(THETA);
st = sind(THETA);
cp = cosd(PHI);
sp = sind(PHI);

r = [st.*cp; st.*sp; ct];
t = [ct.*cp; ct.*sp; -st];
p = [-sp; cp; zeros(1, N)];

Re = roty(elevation);
Ra = rotz(azimuth);
Rr = rotx(roll);

R = Ra*Re*Rr;

R_LG = Ra'*Re'*Rr';
R_GL = R_LG';

rll = r;
tll = t;
pll = p;
rgg = r;
tgg = t;
pgg = p;

rlg = R_LG*rll;
tlg = R_LG*tll;
plg = R_LG*pll;

rgl = R_GL*rgg;
tgl = R_GL*tgg;
pgl = R_GL*pgg;

THETAll = THETA;
PHIll = PHI;
THETAgg = THETA;
PHIgg = PHI;

THETAlg = atan2d(sqrt(sum(rlg([1,2],:).^2,1)), rlg(3,:));
PHIlg = atan2d(plg(1,:), plg(2,:));

THETAgl = atan2d(sqrt(sum(rgl([1,2],:).^2,1)), rgl(3,:));
PHIgl = atan2d(pgl(1,:), pgl(2,:));

figure('visible', 'off');
hold on;

scatter(PHIgg, THETAgg, "b", 'marker', '*');
scatter(PHIlg, THETAlg, "r", 'marker', '*');
PHIgg = reshape(PHIgg, mesh_shape);
THETAgg = reshape(THETAgg, mesh_shape);
mesh(PHIgg, THETAgg, zeros(mesh_shape), 'facecolor', 'none', 'edgecolor', 'b');
PHIgg = reshape(PHIgg, vector_shape);
THETAgg = reshape(THETAgg, vector_shape);

grid on;
xlim([-190, 190]);
ylim([-10, 190]);
set(gca, 'fontsize', fontsize);
xlabel("\\phi [^{\\circ}]");
ylabel("\\theta [^{\\circ}]");
saveas(gcf, "badInterpolation", 'png');

figure('visible', 'off');
hold on;

scatter(PHIll, THETAll, "r", 'marker', '*');
scatter(PHIgl, THETAgl, "b", 'marker', '*');
PHIll = reshape(PHIll, mesh_shape);
THETAll = reshape(THETAll, mesh_shape);
mesh(PHIll, THETAll, zeros(mesh_shape), 'facecolor', 'none', 'edgecolor', 'r');
PHIll = reshape(PHIll, vector_shape);
THETAll = reshape(THETAll, vector_shape);

grid on;
xlim([-190, 190]);
ylim([-10, 190]);
set(gca, 'fontsize', fontsize);
xlabel("\\phi [^{\\circ}]");
ylabel("\\theta [^{\\circ}]");
saveas(gcf, "goodInterpolation", 'png');
