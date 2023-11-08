clear all; close all; clc;

N_theta = 5;
N_phi = 9;

fontsize = 20.0;

elevation = -40;
azimuth = 15;
##roll = 45;
##elevation = 0;
##azimuth = 0;
roll = 0;

theta = linspace(40, 140, N_theta);
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

figure;
hold on;

plot3(r(1,:), r(2,:), r(3,:), 'marker', '*', 'linestyle', 'none', 'color', 'b');
quiver3(r(1,:),r(2,:),r(3,:),t(1,:), t(2,:), t(3,:), 'linewidth', 2.0, 'color', 'g');
quiver3(r(1,:),r(2,:),r(3,:),p(1,:), p(2,:), p(3,:), 'linewidth', 2.0, 'color', 'r');

grid on;
axis equal;
set(gca, 'fontsize', fontsize);
xlabel('x');
ylabel('y');
zlabel('z');
xticklabels([]);
yticklabels([]);
zticklabels([]);
view(45,30);

Re = roty(elevation);
Ra = rotz(azimuth);
Rr = rotx(roll);

R = Ra*Re*Rr;

x = [1; 0; 0];
xl = R*x;
y = [0; 1; 0];
yl = R*y;
z = [0; 0; 1];
zl = R*z;

figure;
hold on;

quiver3(0,0,0,xl(1), xl(2), xl(3), 'linewidth', 2.0, 'color', 'b');
quiver3(0,0,0,yl(1), yl(2), yl(3), 'linewidth', 2.0, 'color', 'g');
quiver3(0,0,0,zl(1), zl(2), zl(3), 'linewidth', 2.0, 'color', 'r');

grid on;
axis equal;
set(gca, 'fontsize', fontsize);
xlabel('x');
ylabel('y');
zlabel('z');
xticklabels([]);
yticklabels([]);
zticklabels([]);
view(45,30);

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

figure;
hold on;

plot3(rlg(1,:), rlg(2,:), rlg(3,:), 'marker', '*', 'linestyle', 'none', 'color', 'b');
quiver3(rlg(1,:),rlg(2,:),rlg(3,:),tlg(1,:), tlg(2,:), tlg(3,:), 'linewidth', 2.0, 'color', 'g');
quiver3(rlg(1,:),rlg(2,:),rlg(3,:),plg(1,:), plg(2,:), plg(3,:), 'linewidth', 2.0, 'color', 'r');

grid on;
axis equal;
set(gca, 'fontsize', fontsize);
xlabel('x');
ylabel('y');
zlabel('z');
xticklabels([]);
yticklabels([]);
zticklabels([]);
view(45,30);
