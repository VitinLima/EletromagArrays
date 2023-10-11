function antennas_btn(h,e)
  global program;
  
  if ishandle(program.gui.right_panel.handle)
    delete(program.gui.right_panel.handle);
  end
  
  program.gui.right_panel.handle = uipanel(program.gui.handle,
    'units', 'normalized',
    'position', [0 0 .2 .9]);
  program.gui.new_antenna_btn.handle = uicontrol(program.gui.right_panel.handle,
    'units', 'normalized',
    'position', [0 .9 1 .1],
    'string', 'new antenna',
    'callback', @new_antenna_btn);
  program.gui.edit_antenna_btn.handle = uicontrol(program.gui.right_panel.handle,
    'units', 'normalized',
    'position', [0 .8 1 .1],
    'string', 'edit antenna',
    'callback', @edit_antenna_btn);
  program.gui.delete_antenna_btn.handle = uicontrol(program.gui.right_panel.handle,
    'units', 'normalized',
    'position', [0 .7 1 .1],
    'string', 'delete antenna',
    'callback', @delete_antenna_btn);
  program.gui.select_antenna_lstbx.handle = uicontrol(program.gui.right_panel.handle,
    'style', 'listbox',
    'units', 'normalized',
    'position', [0 0 1 .7],
    'string', {''},
    'callback', @select_antenna_lstbx);
  
  update_antenna_lstbx();
end