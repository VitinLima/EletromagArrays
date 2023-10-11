function plot_result_btn(h, e)
  global eta;
  global program;
  
  if isempty(program.antennas) && isempty(program.arrays)
    return;
  end
  
  ListString = {};
  if !isempty(program.antennas)
    ListString = [ListString,{program.antennas.Name}];
  end
  if !isempty(program.arrays)
    ListString = [ListString,{program.arrays.Name}];
  end
  SelectionMode = 'Single';
  [SEL, OK] = listdlg('ListString', ListString, 'SelectionMode', SelectionMode);
  if !OK
    return;
  end
  if SEL > length(program.antennas)
    SEL -= length(program.antennas);
    antenna = program.arrays(SEL);
    antenna = evaluateArray(antenna);
  else
    antenna = program.antennas(SEL);
  end
  
  ListString = {'rE', 'rE_phi', 'rE_theta', 'Dir', 'Dir_phi', 'Dir_theta'};
  if !isempty(program.analysis)
    ListString = [{program.analysis.Name},ListString];
  end
  SelectionMode = 'Single';
  [SEL, OK] = listdlg('ListString', ListString, 'SelectionMode', SelectionMode);
  if !OK
    return;
  end
  
  antenna = toVectorShape(antenna);
  switch find(strcmp(ListString(SEL), {'rE', 'rE_phi', 'rE_theta', 'Dir', 'Dir_phi', 'Dir_theta'}))
    case 1
      analysis.Name = 'Electric field magnitude';
      analysis.Expression = 'rE';
      analysis.Data = antenna.E;
    case 2
      analysis.Name = 'Electric field magnitude in phi polarization';
      analysis.Expression = 'rE_phi';
      analysis.Data = abs(antenna.Ephi);
    case 3
      analysis.Name = 'Electric field magnitude in theta polarization';
      analysis.Expression = 'rE_theta';
      analysis.Data = abs(antenna.Etheta);
    case 4
      analysis.Name = 'Directivity';
      analysis.Expression = 'Dir';
      analysis.Data = antenna.E.*antenna.E/2/eta/Prad(antenna)*4*pi;
    case 5
      analysis.Name = 'Directivity in phi polarization';
      analysis.Expression = 'Dir_phi';
      analysis.Data = antenna.Ephi.*conj(antenna.Ephi)/2/eta/Prad(antenna)*4*pi;
    case 6
      analysis.Name = 'Directivity in theta polarization';
      analysis.Expression = 'Dir_theta';
      analysis.Data = antenna.Etheta.*conj(antenna.Etheta)/2/eta/Prad(antenna)*4*pi;
    otherwise
      analysis = program.analysis(SEL);
      evaluate_analysis(analysis);
  end
  
  ListString = {'Rectangular', 'Polar', 'Inverted sphere', 'Polar 3D', 'Sphere 3D'};
  SelectionMode = 'Single';
  [SEL, OK] = listdlg('ListString', ListString, 'SelectionMode', SelectionMode);
  if !OK
    return;
  end
  
  switch SEL
    case 1
      
    case 2
      
    case 3
      invertedSphere(get_current_result.axes, antenna, analysis.Data);
    case 4
      polar3d(get_current_result.axes, antenna, analysis.Data);
    case 5
      
  end
end