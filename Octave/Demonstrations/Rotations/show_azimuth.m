newfig;

x3 = ra*x2;
y3 = ra*y2;
z3 = ra*z2;

quiver3(0,0,0,x3(1),x3(2),x3(3), 'g', 'linewidth', 2.0);
quiver3(0,0,0,y3(1),y3(2),y3(3), 'g', 'linewidth', 2.0);
quiver3(0,0,0,z3(1),z3(2),z3(3), 'g', 'linewidth', 2.0);
text(x3(1),x3(2),x3(3), "x\'", 'fontsize', fontsize);
text(y3(1),y3(2),y3(3), "y\'", 'fontsize', fontsize);
text(z3(1),z3(2),z3(3), "z\'", 'fontsize', fontsize);

angles = pi/180*315*t;
aa = G*[-A*cos(angles); -A*sin(angles); 0.5*ones(size(t))];
arrow = G*0.01*sqrt(2)/2*[-1; -1; 0];
line(aa(1,:), aa(2,:), aa(3,:), 'color', 'black', 'linewidth', 1.0);
quiver3(aa(1,end), aa(2,end), aa(3,end), arrow(1), arrow(2), arrow(3),
'color', 'black', 'linewidth', 1.0, 'maxheadsize', 10);

beta = G*[-0.3,0,0.5]';
text(beta(1),beta(2),beta(3), '\beta', 'fontsize', fontsize);

saveas(gcf, "RefSysAzimuthOctave", 'png');
