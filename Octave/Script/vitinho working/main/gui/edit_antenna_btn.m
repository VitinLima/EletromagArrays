function edit_antenna_btn(h, e)
  global program;
  
  if isempty(program.antennas) && isempty(program.arrays)
    return;
  end
  if ishandle(program.gui.right_panel.handle)
    delete(program.gui.right_panel.handle);
  end
  
  if program.current_antenna > length(program.antennas)
    idx = program.current_antenna-length(program.antennas);
    program.gui.right_panel.handle = uipanel(program.gui.handle,
      'units', 'normalized',
      'position', [0 0 .2 .9]);
    program.gui.edit_antenna_properties_btn.handle = uicontrol(program.gui.right_panel.handle,
      'units', 'normalized',
      'position', [0 .9 1 .1],
      'string', 'edit properties',
      'callback', @edit_antenna_properties_btn);
    program.gui.resample_antenna_btn.handle = uicontrol(program.gui.right_panel.handle,
      'units', 'normalized',
      'position', [0 .8 1 .1],
      'string', 'resample',
      'callback', @resample_antenna_btn);
    program.gui.new_array_antenna_btn.handle = uicontrol(program.gui.right_panel.handle,
      'units', 'normalized',
      'position', [0 .7 1 .1],
      'string', 'new antenna',
      'callback', @new_array_antenna_btn);
    program.gui.edit_array_antenna_btn.handle = uicontrol(program.gui.right_panel.handle,
      'units', 'normalized',
      'position', [0 .6 1 .1],
      'string', 'edit antenna',
      'callback', @edit_array_antenna_btn);
    program.gui.delete_array_antenna_btn.handle = uicontrol(program.gui.right_panel.handle,
      'units', 'normalized',
      'position', [0 .5 1 .1],
      'string', 'delete antenna',
      'callback', @delete_array_antenna_btn);
    program.gui.select_array_antenna_lstbx.handle = uicontrol(program.gui.right_panel.handle,
      'style', 'listbox',
      'units', 'normalized',
      'position', [0 0 1 .5],
      'string', {''},
      'callback', @select_array_antenna_lstbx);
      
      update_array_antenna_lstbx();
  else
    program.gui.right_panel.handle = uipanel(program.gui.handle,
      'units', 'normalized',
      'position', [0 0 .2 .9]);
    program.gui.edit_antenna_properties_btn.handle = uicontrol(program.gui.right_panel.handle,
      'units', 'normalized',
      'position', [0 .9 1 .1],
      'string', 'edit properties',
      'callback', @edit_antenna_properties_btn);
##    program.gui.resample_antenna_btn.handle = uicontrol(program.gui.right_panel.handle,
##      'units', 'normalized',
##      'position', [0 .8 1 .1],
##      'string', 'resample',
##      'callback', @resample_antenna_btn);
    program.gui.edit_antenna_electric_field_btn.handle = uicontrol(program.gui.right_panel.handle,
      'units', 'normalized',
      'position', [0 .8 1 .1],
      'string', 'edit electric field',
      'callback', @edit_antenna_electric_field_btn);
  end
end