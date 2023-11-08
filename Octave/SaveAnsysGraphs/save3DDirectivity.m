function save3DDirectivity(n, v, tgt)
  Phi = v(:,1);
  Theta = v(:,2);
  Ddb = v(:,3);

  delta_Phi = sum(Theta==Theta(1));
  delta_Theta = sum(Phi==Phi(1));

  Phi = reshape(Phi, delta_Phi, delta_Theta);
  Theta = reshape(Theta, delta_Phi, delta_Theta);
  Ddb = reshape(Ddb, delta_Phi, delta_Theta);

  D = 10.^(Ddb./10);

  X = D.*sind(Theta).*cosd(Phi);
  Y = D.*sind(Theta).*sind(Phi);
  Z = D.*cosd(Theta);

  figure('visible', 'off');
  hold on;
  colormap(jet(64));
  ##scatter3(X, Y, Z, [], v(:,3)-min(v(:,3)), 'filled');
  surf(X, Y, Z, Ddb, 'linestyle', 'none', 'facecolor', 'interp');
  xlabel('x');
  ylabel('y');
  zlabel('z');
  xticks([]);
  yticks([]);
  zticks([]);
  cb = colorbar;
  ylabel(cb, '[dB]');

  grid on;
  title(['Diretividade máxima = ', num2str(max(max(Ddb)),2), ' dB']);
  axis equal;
  view(-45,25);

  hold off;
  print(["Resultados",filesep,tgt,"-3DDirectivity.png"]);
end
