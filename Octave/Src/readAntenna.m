function antenna = readAntenna(filename)
  antenna = struct(
    'header', [],
    'Name', ['Antenna imported from file ',filename],
    'PHI_samplings', [],
    'THETA_samplings', [],
    'PHI', [],
    'THETA', [],
    'k_hat', [],
    'phi_hat', [],
    'theta_hat', [],
    'Ephi', [],
    'Etheta', [],
    'E', [],
    'magI', 1,
    'phaseI', 0,
    'position', [0 0 0],
    'alpha', 0,
    'beta', 0,
    'referenceSystem', 'local',
    'data_shape', 'vector',
    'N_samples', [],
    'N_phi', [],
    'N_theta', []);

  if !isempty(filename)
    ##antennas_dir = 'C:\Users\160047412\OneDrive - unb.br\LoraAEB\Antennas';
##    antennas_dir = '/media/vitinho/DADOS/TCC/Antennas';
    antennas_dir = '/mnt/325947A912590BDE/TCC/Antennas';
    FID = fopen([antennas_dir, filesep, filename]);
    antenna.header = fgetl(FID);
    C = textscan(FID, "%q,%f,%f,%f %f,%f %f");
  ##  antenna.variations = C(1);
    antenna.PHI = rad2deg(cell2mat(C(2)))';
    antenna.THETA = rad2deg(cell2mat(C(3)))';
    antenna.PHI_samplings = antenna.PHI(antenna.THETA==antenna.THETA(1));
    antenna.THETA_samplings = antenna.THETA(antenna.PHI==antenna.PHI(1));

    antenna.N_theta = length(antenna.THETA_samplings);
    antenna.N_phi = length(antenna.PHI_samplings);
    antenna.N_samples = antenna.N_theta*antenna.N_phi;

    antenna.k_hat = zeros(3,antenna.N_samples);
    antenna.phi_hat = zeros(3,antenna.N_samples);
    antenna.theta_hat = zeros(3,antenna.N_samples);

    cp = cosd(antenna.PHI);
    sp = sind(antenna.PHI);
    ct = cosd(antenna.THETA);
    st = sind(antenna.THETA);

    antenna.k_hat(1,:) = st.*cp;
    antenna.k_hat(2,:) = st.*sp;
    antenna.k_hat(3,:) = ct;
    antenna.phi_hat(1,:) = -sp;
    antenna.phi_hat(2,:) = cp;
    antenna.theta_hat(1,:) = ct.*cp;
    antenna.theta_hat(2,:) = ct.*sp;
    antenna.theta_hat(3,:) = -st;

##    antenna.Ephi = transpose(cell2mat(C(4)) .* exp(1j*cell2mat(C(5))));
##    antenna.Etheta = transpose(cell2mat(C(6)) .* exp(1j*cell2mat(C(7))));
    antenna.Ephi = transpose(cell2mat(C(4)) .* exp(-1j*cell2mat(C(5))));
    antenna.Etheta = transpose(cell2mat(C(6)) .* exp(-1j*cell2mat(C(7))));

    #Normalize electric fields
    a = antenna.Ephi.*conj(antenna.Ephi);
    b = antenna.Etheta.*conj(antenna.Etheta);
    antenna.E = sqrt(a + b);
    max_magE = max(max(antenna.E));

    antenna.E /= max_magE;
    antenna.Ephi /= max_magE;
    antenna.Etheta /= max_magE;

    fclose(FID);
  end
end
