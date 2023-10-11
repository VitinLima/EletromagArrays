function update_antenna_lstbx()
  global program;
  
  names = {};
  if !isempty(program.antennas)
    names = [names,{program.antennas.Name}];
  end
  if !isempty(program.arrays)
    names = [names,{program.arrays.Name}];
  end
  if !isempty(names)
    set(program.gui.select_antenna_lstbx.handle, 'string', names);
  else
    set(program.gui.select_antenna_lstbx.handle, 'string', '');
  end
  set(program.gui.select_antenna_lstbx.handle, 'value', 1);
  select_antenna_lstbx();
end