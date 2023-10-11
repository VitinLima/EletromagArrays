function displayResults(antenna)
  ##close all;

  showImages = 'on';
  printImages = false;
  overwriteImages = true;

  importDataGraphics;

##  quiver3d(antenna, antenna.Ephi.*antenna.phi_hat + antenna.Etheta.*antenna.theta_hat, false);
##  quiver3d(antenna, antenna.phi_hat, false);
##  polar3d(antenna, 'E', false);
  invertedSphere_rE(antenna, 'E', false);
##  radiationDiagram(antenna, 0, 0, false);
##  polar_Directivity(antenna, false);

  HFIGS = findall('type', 'figure');
  if strcmp(showImages, 'on')
    set(HFIGS, 'visible', 'on');
  end
  if printImages
    cd images
    if strcmp(showImages, 'on')
##      input("Press enter to continue.");
    end
    for i = 1:length(HFIGS)
      hfig = HFIGS(i);
      filename = get(hfig, 'filename');
      if or(!isfile([filename, '.png']), overwriteImages)
        print(hfig, filename, '-dpng');
      end
##      if or(!isfile([filename, '.fig']), overwriteImages)
##        savefig(hfig, filename);
##      end
    end
    cd ..
  end
end
