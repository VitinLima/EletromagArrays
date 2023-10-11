function new_array_antenna_btn(h, e)
  global program;
  
  ListString = {'Load file', 'Ideal dipole', 'Create empty antenna'};
  if !isempty(program.antennas)
    ListString = [ListString, {'From current antennas'}];
  end
  SelectionMode = 'Single';
  [SEL, OK] = listdlg('ListString', ListString, 'SelectionMode', SelectionMode);
  if !OK
    return;
  end
  switch SEL
    case 1
      [FNAME, FPATH, FLTIDX] = uigetfile('.csv', '');
      if FNAME==0
        return;
      end
      FILENAME = fullfile(FPATH, FNAME);
      antenna = readAntenna(FILENAME);
    case 2
      PROMPT = {
        "Length in wave lengths"
        }';
      CSTR = inputdlg(PROMPT, "Ideal dipole settings");
      if isempty(CSTR)
        return;
      end
      antenna = idealDipoleAntenna(str2double(cell2mat(CSTR)));
    case 3
      antenna = emptyAntenna();
    case 4
      ListString = {program.antennas.Name};
      SelectionMode = 'Single';
      [SEL, OK] = listdlg('ListString', ListString, 'SelectionMode', SelectionMode);
      if !OK
        return;
      end
      antenna = program.antennas(SEL);
  end
  
  PROMPT = {
    'Name',
    'Position x:y:z'
  }';
  DEFAULTS = {
    antenna.Name,
    [num2str(antenna.position(1)),':',num2str(antenna.position(2)),':',num2str(antenna.position(3))]
  }';
  CSTR = inputdlg(PROMPT, '', 1, DEFAULTS);
  xyz = strsplit(CSTR{2},':');
  x = str2double(xyz{1});
  y = str2double(xyz{2});
  z = str2double(xyz{3});
  antenna.Name = CSTR{1};
  antenna.position = [x,y,z];
  
  array = get_current_antenna();
  array.antennas(end+1) = antenna;
  set_current_antenna(array);
  update_array_antenna_lstbx();
end