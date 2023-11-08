function saveGraphs(tgt, phi_id, theta_id, D_dB_id)
  [n,v] = readFile(["Resultados",filesep,tgt,".csv"]);

  save3DDirectivity(n,v,tgt);
  fontsize = 20.0;

  phi = v(:,phi_id);
  theta = v(:,theta_id);
  D_dB = v(:,D_dB_id);

  if !isempty(n) && !isempty(v)
    figure('visible', 'off');
    hold on;
    grid on;
    idx = phi==0;
    line(theta(idx), D_dB(idx), 'linewidth', 2, 'color', 'red');
    xlabel("\\theta [º]", 'fontsize', fontsize);
    ylabel("Diretividade [dB]", 'fontsize', fontsize);
    set(gca, 'fontsize', fontsize);
    hold off;
    print(["Resultados",filesep,tgt,"-DirectivityTheta.png"]);
  end

  if !isempty(n) && !isempty(v)
    figure('visible', 'off');
    hold on;
    grid on;
    idx = theta==90;
    line(phi(idx), D_dB(idx), 'linewidth', 2, 'color', 'red');
    xlabel("\\phi [º]", 'fontsize', fontsize);
    ylabel("Diretividade [dB]", 'fontsize', fontsize);
    set(gca, 'fontsize', fontsize);
    hold off;
    print(["Resultados",filesep,tgt,"-DirectivityPhi.png"]);
  end

  [n,v] = readFile(["Resultados",filesep,"SweepPlot",tgt,".csv"]);
  if !isempty(n) && !isempty(v)
    figure('visible', 'off');
    hold on;
    grid on;
    line(v(:,1), v(:,2), 'linewidth', 2, 'color', 'red');
    xlabel(n(1), 'fontsize', fontsize);
    ylabel("S_{11} [dB]", 'fontsize', fontsize);
    set(gca, 'fontsize', fontsize);
    hold off;
    print(["Resultados",filesep,tgt,"-SweepPlot.png"]);
  end
end
