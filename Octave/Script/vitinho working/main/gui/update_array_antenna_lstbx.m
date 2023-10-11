function update_array_antenna_lstbx()
  global program;
  
  array = get_current_antenna();
  if !isempty(array.antennas)
    set(program.gui.select_array_antenna_lstbx.handle, 'string', {array.antennas.Name});
  else
    set(program.gui.select_array_antenna_lstbx.handle, 'string', '');
  end
  set(program.gui.select_array_antenna_lstbx.handle, 'value', 1);
  select_array_antenna_lstbx();
end