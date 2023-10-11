function set_current_array_antenna(antenna)
  global program;
  
  array = get_current_antenna();
  array.antennas(program.current_array_antenna) = antenna;
  set_current_antenna(array);
end