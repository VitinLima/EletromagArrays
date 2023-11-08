clear all; close all; clc;

fontsize = 20;
show_imgs = 'off';

create_lhcp_visualization;
create_rhcp_visualization;
create_ecp_visualization;
create_hlp_visualization;
create_vlp_visualization;
create_dlp_visualization;
show_rotations;

return;

[img, map, alpha] = imread("Johnson 1-2 (blank).png");
imshow(img);
axis on;
text(162, 108, "Posição da\nantena",
  'fontsize', fontsize,
  'verticalalignment', 'middle',
  'horizontalalignment', 'right',
  'interpreter', 'latex');
text(360, 297, "\\phi",
  'fontsize', fontsize,
  'verticalalignment', 'top',
  'horizontalalignment', 'right');
text(400, 180, "\\theta",
  'fontsize', fontsize,
  'verticalalignment', 'bottom',
  'horizontalalignment', 'center',
  'interpreter', 'latex');
text(450, 190, "\\tau",
  'fontsize', fontsize,
  'verticalalignment', 'top',
  'horizontalalignment', 'right',
  'interpreter', 'latex');
text(440, 215, "\\vec{u}_\\theta",
  'fontsize', fontsize,
  'verticalalignment', 'top',
  'horizontalalignment', 'right',
  'interpreter', 'latex');
text(500, 145, "\\vec{u}_\\phi",
  'fontsize', fontsize,
  'verticalalignment', 'top',
  'horizontalalignment', 'right',
  'interpreter', 'latex');
