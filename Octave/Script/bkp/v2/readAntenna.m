function antenna = readAntenna(filename)
  antenna = emptyAntenna();
  
  if !isempty(filename)
    cd antennas
    FID = fopen(filename);
    antenna.header = fgetl(FID);
    C = textscan(FID, "%q,%f,%f,%f %f,%f %f");
  ##  antenna.variations = C(1);
    antenna.PHI = rad2deg(cell2mat(C(2)))';
    antenna.THETA = rad2deg(cell2mat(C(3)))';
    antenna.PHI_samplings = antenna.PHI(antenna.THETA==antenna.THETA(1));
    antenna.THETA_samplings = antenna.THETA(antenna.PHI==antenna.PHI(1));
    antenna.Ephi = (cell2mat(C(4)) .* exp(1j*cell2mat(C(5))))';
    antenna.Etheta = (cell2mat(C(6)) .* exp(1j*cell2mat(C(7))))';
    
    #Normalize electric fields
    a = antenna.Ephi.*conj(antenna.Ephi);
    b = antenna.Etheta.*conj(antenna.Etheta);
    antenna.E = sqrt(a + b);
    max_magE = max(max(antenna.E));
    antenna.E /= max_magE;
    antenna.E_db = 20*log10(antenna.E);
    
    antenna.Ephi /= max_magE;
    antenna.Etheta /= max_magE;
    
    antenna.N_theta_samples = length(antenna.THETA_samplings);
    antenna.N_phi_samples = length(antenna.PHI_samplings);
    antenna.N_samples = antenna.N_theta_samples*antenna.N_phi_samples;
    
    fclose(FID);
    cd ..
  end
end