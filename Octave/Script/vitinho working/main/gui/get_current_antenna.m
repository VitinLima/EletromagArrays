function antenna = get_current_antenna()
  global program;
  
  idx = program.current_antenna;
  if idx > length(program.antennas)
    idx -= length(program.antennas);
    if !isempty(program.arrays)
      antenna = program.arrays(idx);
    else
      antenna = [];
    end
  else
    if !isempty(program.antennas)
      antenna = program.antennas(idx);
    else
      antenna = [];
    end
  end
end