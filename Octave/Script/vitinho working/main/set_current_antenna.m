function set_current_antenna(antenna)
  global program;
  
  idx = program.current_antenna;
  if idx > length(program.antennas)
    idx -= length(program.antennas);
    program.arrays(idx) = antenna;
  else
    program.antennas(idx) = antenna;
  end
end