function edit_antenna_properties_btn(h, e)
  global program;
  
  antenna = get_current_antenna();
  PROMPT = {
    "Antenna name",
    "Azimuth",
    "Elevation"
  }';
  DEFAULTS = {
    antenna.Name,
    num2str(antenna.beta),
    num2str(antenna.alpha)
  }';
  CSTR = inputdlg(PROMPT, '', 1, DEFAULTS);
  if isempty(CSTR)
    return;
  end
  antenna.Name = CSTR{1};
  antenna.beta = str2double(CSTR{2});
  antenna.alpha = str2double(CSTR{3});
  set_current_antenna(antenna);
end