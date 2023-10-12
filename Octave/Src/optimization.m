function [array, X, C] = optimization(array, tg_antenna, optpar)
  disp('Extracting initial guess from current antenna array.');
  X0 = zeros(1,optpar.N*array.N_antennas);
  for i = 1:array.N_antennas
    n = i - 1;
    idx = 1;
    if optpar.x
      X0(optpar.N*n+idx) = array.antennas(i).position(1);
      idx++;
    end
    if optpar.y
      X0(optpar.N*n+idx) = array.antennas(i).position(2);
      idx++;
    end
    if optpar.z
      X0(optpar.N*n+idx) = array.antennas(i).position(3);
      idx++;
    end
    if optpar.beta
      X0(optpar.N*n+idx) = array.antennas(i).beta;
      idx++;
    end
    if optpar.alpha
      X0(optpar.N*n+idx) = array.antennas(i).alpha;
    end
  endfor

  function C = costfunction(X, array, tg_antenna, optpar)
    global f;
    global c;
    global lambda;
    global k;
    
    for i = 1:array.N_antennas
      n = i-1;
      idx = 1;
      if optpar.x
        array.antennas(i).position(1) = X(optpar.N*n+idx);
        idx++;
      end
      if optpar.y
        array.antennas(i).position(2) = X(optpar.N*n+idx);
        idx++;
      end
      if optpar.z
        array.antennas(i).position(3) = X(optpar.N*n+idx);
        idx++;
      end
      if optpar.beta
        array.antennas(i).beta = X(optpar.N*n+idx);
        idx++;
      end
      if optpar.alpha
        array.antennas(i).alpha = X(optpar.N*n+idx);
      end
    endfor
    
    array = evaluateArray(array);
    dEphi = abs(array.Ephi) - abs(tg_antenna.Ephi);
    dEtheta = abs(array.Etheta) - abs(tg_antenna.Etheta);
  ##  C = sum(dEphi.*conj(dEphi) + dEtheta.*conj(dEtheta), 2);
    C = sum(sum(dEphi.*dEphi + dEtheta.*dEtheta));
    disp(['Evaluated cost function C = ',num2str(C)]);%,' with X = ', num2str(X)]);
  end

  disp('Optimization started.')
  [X, FVAL, INFO, OUTPUT, FJAC] = fsolve(@(X) costfunction(X, array, tg_antenna, optpar), X0);

  disp(['Optimization finalized with cost function C = ',num2str(FVAL)]);%,', Position X = ', num2str(X(1:3)), ', beta = ', num2str(X(4)), ' and alpha = ', num2str(X(5))]);
  
  for i = 1:array.N_antennas
    n = i-1;
    idx = 1;
    if optpar.x
      array.antennas(i).position(1) = X(optpar.N*n+idx);
      idx++;
    end
    if optpar.y
      array.antennas(i).position(2) = X(optpar.N*n+idx);
      idx++;
    end
    if optpar.z
      array.antennas(i).position(3) = X(optpar.N*n+idx);
      idx++;
    end
    if optpar.beta
      array.antennas(i).beta = X(optpar.N*n+idx);
      idx++;
    end
    if optpar.alpha
      array.antennas(i).alpha = X(optpar.N*n+idx);
    end
  endfor
  array = evaluateArray(array);

  disp(INFO);
  disp(OUTPUT);
end