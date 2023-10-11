function edit_array_antenna_properties_btn(h, e)
  global program;
  
  array = get_current_antenna();
  if isempty(array.antennas)
    return;
  end
  antenna = get_current_array_antenna();
  
  PROMPT = {
    "Antenna name",
    "Azimuth",
    "Elevation",
    "Position x:y:z"
  }';
  DEFAULTS = {
    antenna.Name,
    num2str(antenna.beta),
    num2str(antenna.alpha),
    [num2str(antenna.position(1)),':',num2str(antenna.position(2)),':',num2str(antenna.position(3))]
  }';
  CSTR = inputdlg(PROMPT, '', 1, DEFAULTS);
  if isempty(CSTR)
    return;
  end
  antenna.Name = CSTR{1};
  antenna.beta = str2double(CSTR{2});
  antenna.alpha = str2double(CSTR{3});
  xyz = strsplit(CSTR{4},':');
  x = str2double(xyz{1});
  y = str2double(xyz{2});
  z = str2double(xyz{3});
  antenna.position = [x,y,z];
  set_current_array_antenna(antenna);
end