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
  p.addParameter("printImages", false);
  p.addParameter("savedir", pwd);
  p.addParameter("overwriteImages", true);
  p.addParameter("close_after", false);

  p.parse(varargin{:});
  args_in = p.Results;

  args_in.antenna = toMeshShape(args_in.antenna);

  ##images_dir = 'C:\Users\160047412\OneDrive - unb.br\LoraAEB\Octave\Validation\Images';
##  images_dir = '/media/vitinho/DADOS/TCC/Octave/Validation/Images';
  images_dir = args_in.savedir;

  importDataGraphics;

  if strcmp(args_in.field_name, 'E') || strcmp(args_in.field_name, 'magE')
    field = args_in.antenna.E;
    color_map = "jet";
  elseif strcmp(args_in.field_name, 'Etheta') || strcmp(args_in.field_name, 'magEtheta')
    field = abs(args_in.antenna.Etheta);
    color_map = "jet";
  elseif strcmp(args_in.field_name, 'angEtheta')
    field = angle(args_in.antenna.Etheta);
    color_map = "hsv";
  elseif strcmp(args_in.field_name, 'angEtheta normalized')
    field = angle(args_in.antenna.Etheta*exp(-1j*mean(mean(angle(args_in.antenna.Etheta)))));
    color_map = "hsv";
  elseif strcmp(args_in.field_name, 'Ephi') || strcmp(args_in.field_name, 'magEphi')
    field = abs(args_in.antenna.Ephi);
    color_map = "jet";
  elseif strcmp(args_in.field_name, 'angEphi')
    field = angle(args_in.antenna.Ephi);
    color_map = "hsv";
  elseif strcmp(args_in.field_name, 'angEphi normalized')
    field = angle(args_in.antenna.Ephi*exp(-1j*mean(mean(angle(args_in.antenna.Ephi)))));
    color_map = "hsv";
  else
    error(["Unknow field ", args_in.field_name])
  endif

  if strcmp(args_in.plot_type, 'inverted sphere')
    invertedSphere_rE(args_in.antenna.THETA, args_in.antenna.PHI, field,
    "title", [args_in.antenna.Name, ' ', args_in.field_name],
    "showIm", args_in.showIm,
    "cmap", color_map
    );
  elseif strcmp(args_in.plot_type, 'radiation diagram')
    radiationDiagram(args_in.antenna, 0, 0, false);
  elseif strcmp(args_in.plot_type, 'polar directivity')
    polar_Directivity(args_in.antenna, false);
  elseif
    quiver3d(args_in.antenna, args_in.antenna.Ephi.*args_in.antenna.phi_hat + args_in.antenna.Etheta.*args_in.antenna.theta_hat, false);
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
