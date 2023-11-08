function displayResults(varargin)
  p = inputParser();
  p.FunctionName = "displayResults";
  p.addRequired("antenna");
  p.addRequired("field_name");
  p.addRequired("plot_type");
  p.addParameter("showIm", false);
  p.addParameter("cmap", "jet");
  p.addParameter("title", "");
  p.addParameter("showImages", 'on');
  p.addParameter("printImages", true);
  p.addParameter("savedir", pwd);
  p.addParameter("overwriteImages", true);
  p.addParameter("close_after", false);

  p.parse(varargin{:});
  args_in = p.Results;

  args_in.antenna = toMeshShape(args_in.antenna);

  images_dir = args_in.savedir;

  importDataGraphics;

  color_range = "auto";
  cmap_label = "";
  if strcmp(args_in.field_name, 'E') || strcmp(args_in.field_name, ...
      'magE')
    field = args_in.antenna.E;
    color_map = "jet";
    cmap_label = "[mV]";
  elseif strcmp(args_in.field_name, 'E db') || strcmp(args_in.field_name, 'magE db')
    field = args_in.antenna.E/max(max(args_in.antenna.E));
    field = 20*log10(field);
    color_range = [-30 0];
    color_map = "jet";
    cmap_label = "[dB]";
  elseif strcmp(args_in.field_name, 'E normalized') || strcmp(args_in.field_name, 'magE normalized')
    field = args_in.antenna.E/max(max(args_in.antenna.E));
    color_range = [0 1];
    color_map = "jet";
  elseif strcmp(args_in.field_name, 'Etheta') || ...
    strcmp(args_in.field_name, 'magEtheta')
    field = abs(args_in.antenna.Etheta);
    color_map = "jet";
    cmap_label = "[mV]";
  elseif strcmp(args_in.field_name, 'Etheta db') || strcmp(args_in.field_name, 'magEtheta db')
    field = abs(args_in.antenna.Etheta);
    field /= max(max(field));
    field = 20*log10(field);
    color_range = [-30 0];
    color_map = "jet";
    cmap_label = "[dB]";
  elseif strcmp(args_in.field_name, 'Etheta normalized') || strcmp(args_in.field_name, 'magEtheta normalized')
    field = abs(args_in.antenna.Etheta);
    field /= max(max(field));
    color_range = [0 1];
    color_map = "jet";
  elseif strcmp(args_in.field_name, 'angEtheta')
    field = angle(args_in.antenna.Etheta);
    color_map = "hsv";
    cmap_label = "[rad]";
  elseif strcmp(args_in.field_name, 'angEtheta normalized')
    field = angle(args_in.antenna.Etheta*exp(-1j*mean(mean(angle(...
    args_in.antenna.Etheta)))));
    color_map = "hsv";
    cmap_label = "[rad]";
  elseif strcmp(args_in.field_name, 'Ephi') || ...
    strcmp(args_in.field_name, 'magEphi')
    field = abs(args_in.antenna.Ephi);
    color_map = "jet";
    cmap_label = "[mV]";
  elseif strcmp(args_in.field_name, 'Ephi db') || strcmp(args_in.field_name, 'magEphi db')
    field = abs(args_in.antenna.Ephi);
    field /= max(max(field));
    field = 20*log10(field);
    color_range = [-30 0];
    color_map = "jet";
    cmap_label = "[dB]";
  elseif strcmp(args_in.field_name, 'Ephi normalized') || strcmp(args_in.field_name, 'magEphi normalized')
    field = abs(args_in.antenna.Ephi);
    field /= max(max(field));
    color_range = [0 1];
    color_map = "jet";
  elseif strcmp(args_in.field_name, 'angEphi')
    field = angle(args_in.antenna.Ephi);
    color_map = "hsv";
    cmap_label = "[rad]";
  elseif strcmp(args_in.field_name, 'angEphi normalized')
    field = angle(args_in.antenna.Ephi*exp(-1j*mean(mean(angle(...
    args_in.antenna.Ephi)))));
    color_map = "hsv";
    cmap_label = "[rad]";
  else
    error(["Unknow field ", args_in.field_name])
  endif

  if strcmp(args_in.plot_type, 'inverted sphere')
    invertedSphere_rE(args_in.antenna.THETA, ...
    args_in.antenna.PHI, field,
    "title", [args_in.antenna.Name, ' ', args_in.field_name],
    "showIm", args_in.showIm,
    "cmap", color_map,
    "color_range", color_range,
    "cmap_label", cmap_label
    );
  elseif strcmp(args_in.plot_type, 'radiation diagram')
    radiationDiagram(args_in.antenna, 0, 0, false);
  elseif strcmp(args_in.plot_type, 'polar directivity')
    polar_Directivity(args_in.antenna, false);
  elseif
    quiver3d(args_in.antenna, args_in.antenna.Ephi.*...
    args_in.antenna.phi_hat + args_in.antenna.Etheta.*...
    args_in.antenna.theta_hat, false);
  elseif
    polar3d(args_in.antenna, 'E', false);
  endif

  HFIGS = findall('type', 'figure');
  if strcmp(args_in.showImages, 'on')
    set(HFIGS, 'visible', 'on');
  end
  if args_in.printImages
    if strcmp(args_in.showImages, 'on')
##      input("Press enter to continue.");
    end
    if !exist(images_dir)
      mkdir(images_dir);
    endif
    for i = 1:length(HFIGS)
      hfig = HFIGS(i);
##      images_dir
      filename = [images_dir, filesep, get(hfig, 'filename'), '.png'];
      if or(!isfile([filename, '.png']), args_in.overwriteImages)
        print(hfig, filename, '-dpng');
      end
##      if or(!isfile([filename, '.fig']), overwriteImages)
##        savefig(hfig, filename);
##      end
    end
  end

  if args_in.close_after
    close all;
  endif
end
