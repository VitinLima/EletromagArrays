function select_antenna_lstbx(h,e)
  global program;
  
  if isempty(program.antennas) && isempty(program.arrays)
    return;
  end
  program.current_antenna = get(program.gui.select_antenna_lstbx.handle, 'value');
##  antenna = get_current_antenna();
##  set(program.gui.infotext.handle, 'string', ['Antennas:',antenna.Name]);
end