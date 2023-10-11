function antenna = get_current_array_antenna()
  global program;
  
  array = get_current_antenna();
  antenna = array.antennas(program.current_array_antenna);
end