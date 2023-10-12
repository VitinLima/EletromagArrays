function save3DPolarPlot(filename)
  [n,v] = readFile(filename);
  if !isempty(n) && !isempty(v)
    phi = v(v(:,2)==v(1,2),1);
    theta = v(v(:,1)==v(1,1),2);
    
    [THETA, PHI] = meshgrid(theta, phi);
    mesh_shape = [length(phi) length(theta)];
    C = reshape(v(:,3), mesh_shape);
    R = reshape((v(:,3)-min(v(:,3)))/(max(v(:,3))-min(v(:,3))), mesh_shape);
    
    figure('visible', 'off');
    hold on;
    
    cp = cosd(PHI);
    sp = sind(PHI);
    ct = cosd(THETA);
    st = sind(THETA);
    XX = R.*st.*cp;
    YY = R.*st.*sp;
    ZZ = R.*ct;
    h = surf(XX, YY, ZZ, C, 'linestyle', 'none', 'facecolor', 'interp');
##    rotate(h, [0 1 0], 45);
##    rotate(h, [0 0 1], 45);
    
    colormap("jet");
    cb = colorbar;
    xlabel("x");
    ylabel("y");
    %zlabel("z");
    grid on;
    axis equal;
##    set(gcf, 'visible', 'on');
    set(gca, 'cameraposition', [1 1 0.4]);
    set(gca, 'cameratarget', [0 0 0]);
    set(gca, 'cameraupvector', [0 0 1]);
    ylabel(cb, '[mV]');
    hold off;
    
    in = 1;%input("Enter 1 to continue\nEnter 2 to cancel\n");
    if in==1
      print([filename,".png"]);
    end
  else
    disp("No variables to plot");
  end
end