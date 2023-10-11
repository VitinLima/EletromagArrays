function new_antenna_btn(h,e)
  global program;
  
  ListString = {'Load file', 'Ideal dipole', 'Empty antenna', 'Array'};
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
      program.antennas(end+1) = readAntenna(FILENAME);
      program.current_antenna = length(program.antennas);
    case 2
      PROMPT = {
        "Length in wave lengths"
        "Phi sampling i:f:d",
        "Theta sampling i:f:d"
        }';
        DEFAULTS = {
          "0.5",
        "-180:180:31",
        "0:90:21"
        }';
      CSTR = inputdlg(PROMPT, "Ideal dipole settings", 1, DEFAULTS);
      if isempty(CSTR)
        return;
      end
      S2 = strsplit(CSTR{2}, ':');
      S3 = strsplit(CSTR{3}, ':');
      phi_samplei=str2double(S2{1});
      phi_samplef=str2double(S2{2});
      Nphi=str2double(S2{3});
      theta_samplei=str2double(S3{1});
      theta_samplef=str2double(S3{2});
      Ntheta=str2double(S3{3});
      program.antennas(end+1) = idealDipoleAntenna(str2double(CSTR{1}),
        phi_samplei, phi_samplef, Nphi,
        theta_samplei, theta_samplef, Ntheta
      );
      program.current_antenna = length(program.antennas);
    case 3
      program.antennas(end+1) = emptyAntenna();
      program.current_antenna = length(program.antennas);
    case 4
      ListString = {'Load file', 'Ideal dipole', 'Empty antenna'};
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
          base_antenna = readAntenna(FILENAME);
        case 2
          PROMPT = {
            "Length in wave lengths"
            }';
          CSTR = inputdlg(PROMPT, "Ideal dipole settings");
          if isempty(CSTR)
            return;
          end
          base_antenna = idealDipoleAntenna(str2double(cell2mat(CSTR)));
        case 3
          base_antenna = emptyAntenna();
        case 4
          ListString = {program.antennas.Name};
          SelectionMode = 'Single';
          [SEL, OK] = listdlg('ListString', ListString, 'SelectionMode', SelectionMode);
          if !OK
            return;
          end
          base_antenna = program.antennas(SEL);
      end
      PROMPT = {
        "N X:Center X:X spacing",
        "N Y:Center Y:Y spacing",
        "Azimuth:Elevation",
        "phi i:phi f:N phi",
        "theta i:theta f:N theta"}';
      ROWSCOLS = [1,9;1,9;1,9;1,9;1,9];
      DEFAULTS = {
        "3:0:0.5",
        "3:0:0.5",
        "0:0:",
        "-180:180:31",
        "0:180:21"
      }';
      CSTR = inputdlg(PROMPT, "Planar array settings", ROWSCOLS, DEFAULTS);
      if isempty(CSTR)
        return;
      end
      s1 = strsplit(cell2mat(CSTR(1)),':');
      s2 = strsplit(cell2mat(CSTR(2)),':');
      s3 = strsplit(cell2mat(CSTR(3)),':');
      s4 = strsplit(cell2mat(CSTR(4)),':');
      s5 = strsplit(cell2mat(CSTR(5)),':');
      arguments = {
        str2double(cell2mat(s3(1))),
        str2double(cell2mat(s3(2))),
        str2double(cell2mat(s1(1))),
        str2double(cell2mat(s1(2))),
        str2double(cell2mat(s1(3))),
        str2double(cell2mat(s2(1))),
        str2double(cell2mat(s2(2))),
        str2double(cell2mat(s2(3))),
        str2double(cell2mat(s5(1))),
        str2double(cell2mat(s5(2))),
        str2double(cell2mat(s5(3))),
        str2double(cell2mat(s4(1))),
        str2double(cell2mat(s4(2))),
        str2double(cell2mat(s4(3)))
      };
      program.arrays(end+1) = gridArrayConstructor(base_antenna, arguments{:});
      program.current_antenna = length(program.antennas) + length(program.arrays);
  end
  update_antenna_lstbx();
end