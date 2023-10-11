function delete_antenna_btn(h,e)
  global program;
  
  if isempty(program.antennas) && isempty(program.arrays)
    return;
  end
  
  idx = program.current_antenna;
  if idx > length(program.antennas)
    idx -= length(program.antennas);
    program.arrays(idx) = [];
  else
    program.antennas(idx) = [];
  end
  program.current_antenna = length(program.antennas) + length(program.arrays);
  update_antenna_lstbx();
end