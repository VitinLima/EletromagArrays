newfig;

x2 = re*x1;
y2 = re*y1;
z2 = re*z1;

quiver3(0,0,0,x2(1),x2(2),x2(3), 'g', 'linewidth', 2.0);
quiver3(0,0,0,y2(1),y2(2),y2(3), 'g', 'linewidth', 2.0);
quiver3(0,0,0,z2(1),z2(2),z2(3), 'g', 'linewidth', 2.0);
text(x2(1),x2(2),x2(3), "x\'", 'fontsize', fontsize);
text(y2(1),y2(2),y2(3), "y\'", 'fontsize', fontsize);
text(z2(1),z2(2),z2(3), "z\'", 'fontsize', fontsize);

angles = pi/180*315*t;
ae = G*[-A*cos(angles); 0.5*ones(size(t)); -A*sin(angles)];
arrow = G*0.01*sqrt(2)/2*[-1; 0; -1];
line(ae(1,:), ae(2,:), ae(3,:), 'color', 'black', 'linewidth', 1.0);
quiver3(ae(1,end), ae(2,end), ar(3,end), arrow(1), arrow(2), arrow(3),
'color', 'black', 'linewidth', 1.0, 'maxheadsize', 10);

alpha = G*[0,0.5,0.3]';
text(alpha(1),alpha(2),alpha(3), '\alpha', 'fontsize', fontsize);

##view(19,40);

saveas(gcf, "RefSysElevationOctave", 'png');
