function delete_array_antenna_btn(h, e)
  global program;
  
  array = get_current_antenna();
  if isempty(array.antennas)
    return;
  end
  array.antennas(program.current_array_antenna) = [];
  set_current_antenna(array);
  update_array_antenna_lstbx();
end