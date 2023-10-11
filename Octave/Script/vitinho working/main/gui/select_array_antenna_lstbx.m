function select_array_antenna_lstbx(h, e)
  global program;
  
  array = get_current_antenna();
  if isempty(array.antennas)
    set(program.gui.infotext.handle, 'string', array.Name);
    return;
  end
  program.current_array_antenna = get(program.gui.select_array_antenna_lstbx.handle, 'value');
  antenna = get_current_array_antenna();
  set(program.gui.infotext.handle, 'string', [array.Name, '->', antenna.Name]);
end