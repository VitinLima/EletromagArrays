function array = evaluateArray(array)
  global f;
  global c;
  global lambda;
  global k;
  
  # Este código foi feito como uma forma mais didática de entender o primeiro
  ## código, como este utiliza loops for para ilustrar mais facilmente os
  ## processos, é muito mais devagar. (Não testei ainda)
  
  theta_samples = linspace(0,180,91); # Amostragens em theta
  phi_samples = linspace(-180,180,91); # Amostragens em phi
  
  N_theta = length(theta); # Número de amostragens em theta
  N_phi = length(phi); # Número de amostragens em phi
  N_antennas = length(array.antennas); # Número de antenas
  
  array.Ephi = zeros(N_theta, N_phi); # Pré alocando espaço para o campo
  ## elétrico resultante do arranjo na polarização phi
  array.Etheta = zeros(N_theta, N_phi); # Pré alocando espaço para o campo
  ## elétrico resultante do arranjo na polarização theta
  
##  Rt = arrayfun(@roty, theta, 'UniformOutput', false); Ignora
##  Rp = arrayfun(@rotz, phi, 'UniformOutput', false);
  
  for phi_idx = 1:N_phi
    phi = phi_samples(phi_idx); # Para cada amostragem em phi
    R_phi = rotz(phi); # Calculando matriz de rotação em phi (em Z)
    
    hat_phi = R_phi*[0, 1, 0]'; # A direção phi chapéu depende apenas de phi,
    ## pois a rotação em theta é uma rotação em Y, e a base de phi é um vetor Y,
    ## então a rotação em theta não muda
    
    for theta_idx = 1:N_theta
      theta = theta_samples(theta_idx); # Para cada amostragem em theta
      R_theta = roty(theta); # Calculando a matriz de rotação em theta (em Y)
      
      R = R_phi*R_theta; # Matriz de rotação em phi e theta
      hat_r = R*[0, 0, 1]'; # Vetor r chapéu, rotacionando primeiro em theta e
      ## depois em phi
      hat_theta = R*[1, 0, 0]'; # Vetor theta chapéu
      
      for antenna_idx = 1:N_antennas
        antenna = array.antennas(antenna_idx); # Para cada antena do arranjo
        alpha = antenna.alpha; # Elevação da antena (Mesma rotação em theta,
        ## muda o nome para não confundir)
        beta = antenna.beta; # Azimuth da antena (Mesma rotação em phi, muda o
        ## nome para não confundir)
        R_alpha = roty(alpha); # Matriz de rotação em alpha (Y)
        R_beta = rotz(beta); # Matriz de rotação em beta (Z)
        R_antenna = R_beta*R_alpha; # Matriz de rotação de mudança de base do
        ## sistema global do arranjo para o sistema local da antena
        
        global_hat_phi = R_antenna*hat_phi; # Vetor phi chapéu global expresso no
        ## sistema de coordenadas local
        global_hat_theta = R_antenna*hat_theta; # Vetor theta global chapéu expresso no
        ## sistema de coordenadas local
        
        # Coordenadas do vetor r chapéu no sistema de coordenadas local
        local_x = local_hat_r(1);
        local_y = local_hat_r(2);
        local_z = local_hat_r(3);
        
        # Calculando os novos ângulos phi e theta no sistema de coordenadas
        ## local a partir das coordenadas x, y e z do vetor r chapéu
        local_phi = atan2d(local_y, local_x);
        local_theta = atan2d(sqrt(local_x*local_x+local_y*local_y), local_z);
        local_R = rotz(local_phi)*roty(local_theta); # Matriz de rotação dos
        ## novos ângulos
        local_hat_phi = local_R*[0 1 0]'; # Vetor phi chapéu da antena local, a
        ## antena guarda o valor do campo elétrico sobre este vetor
        local_hat_theta = local_R*[0 0 1]'; # Vetor theta chapéu da antena local, a
        ## antena guarda o valor do campo elétrico sobre este vetor
        
        # Amostragens do campo elétrico da antena
        local_phi_samples = antenna.phi_samples;
        local_theta_samples = antenna.theta_samples;
        local_Ephi_samples = antenna.Ephi;
        local_Etheta_samples = antenna.Etheta;
        
        # Interpolando o campo elétrico da antena nas coordenadas da amostragem
        ## do sistema global do arranjo
        local_Ephi = interp2(local_phi_samples, local_theta_samples, local_Ephi_samples, local_phi, local_theta);
        local_Etheta = interp2(local_phi_samples, local_theta_samples, local_Etheta_samples, local_phi, local_theta);
        
        # É como uma mudança de base, temos um
        ## vetor expresso nas coordenadas phi e theta do sistema local e
        ## queremos o mesmo vetor no sistema de coordenadas global
        Ephi = local_Ephi*dot(global_hat_phi, local_hat_phi) + local_Etheta*dot(global_hat_phi, local_hat_theta);
        Etheta = local_Ephi*dot(global_hat_theta, local_hat_phi) + local_Etheta*dot(global_hat_theta, local_hat_theta);
        
        position = antenna.position;
        
        Af = exp(-1j*k*dot(position, hat_r)).*antenna.magI.*exp(1j*deg2rad(antenna.phaseI));
        
        array.Ephi(theta_idx, phi_idx) += Ephi*Af;
        array.Etheta(theta_idx, phi_idx) += Etheta*Af;
      end
    end
  end

  #Normalize electric fields
  a = array.Ephi.*conj(array.Ephi);
  b = array.Etheta.*conj(array.Etheta);
  array.E = sqrt(a + b);
  max_magE = max(array.E);

  array.E /= max_magE;
  array.Ephi /= max_magE;
  array.Etheta /= max_magE;
end