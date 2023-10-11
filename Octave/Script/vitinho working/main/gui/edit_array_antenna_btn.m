function edit_array_antenna_btn(h, e)
  global program;
  
  if isempty(program.antennas) && isempty(program.arrays)
    return;
  end
  if ishandle(program.gui.right_panel.handle)
    delete(program.gui.right_panel.handle);
  end
  
  program.gui.right_panel.handle = uipanel(program.gui.handle,
    'units', 'normalized',
    'position', [0 0 .2 .9]);
  program.gui.edit_antenna_btn.edit_array_antenna_properties_btn.handle = uicontrol(program.gui.right_panel.handle,
    'units', 'normalized',
    'position', [0 .9 1 .1],
    'string', 'edit properties',
    'callback', @edit_array_antenna_properties_btn);
  program.gui.edit_antenna_btn.edit_array_antenna_electric_field_btn.handle = uicontrol(program.gui.right_panel.handle,
    'units', 'normalized',
    'position', [0 .8 1 .1],
    'string', 'edit electric field',
    'callback', @edit_array_antenna_electric_field_btn);
end