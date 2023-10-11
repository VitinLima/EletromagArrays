function quiver3d(axes, title, antenna, results)
  p = inputParser;
  p.FunctionName = "quiver3d";
  p.addRequired("axes");
  p.addRequired("title");
  p.addRequired("antenna");
  p.addRequired("results");
  
  figure('visible', showIm, 'filename', 'polar3d rE');
  hold on;
  
##  ant = toVectorShape(ant);
  quiver3(ant.k_hat(1,:), ant.k_hat(2,:), ant.k_hat(3,:), field(1,:), field(2,:), field(3,:));
  
  axis equal;
  xlabel('x');
  ylabel('y');
  zlabel('z');
end