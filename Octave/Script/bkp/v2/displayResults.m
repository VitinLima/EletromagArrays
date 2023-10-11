##close all;

showImages = 'on';
printImages = false;
overwriteImages = true;

createGraphics(array);
title(['opt calculated array (',add_info,')']);
createGraphics(antv);
title(['opt simulated antenna (',add_info,')']);

HFIGS = findall('type', 'figure');
if strcmp(showImages, 'on')
  set(HFIGS, 'visible', 'on');
end
if printImages
  cd images
  if strcmp(showImages, 'on')
    input("Press enter to continue.");
  end
  for i = 1:length(HFIGS)
    hfig = HFIGS(i);
    filename = get(hfig, 'filename');
    if or(!isfile([filename, '.png']), overwriteImages)
      print(hfig, filename, '-dpng');
    end
    if or(!isfile([filename, '.fig']), overwriteImages)
      savefig(hfig, filename);
    end
  end
  cd ..
end