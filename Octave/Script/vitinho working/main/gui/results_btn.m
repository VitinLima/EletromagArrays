function results_btn(h, e)
  global program;
  
  if ishandle(program.gui.right_panel.handle)
    delete(program.gui.right_panel.handle);
  end
  
  program.gui.right_panel.handle = uipanel(program.gui.handle,
    'units', 'normalized',
    'position', [0 0 .2 .9]);
  program.gui.new_result_btn.handle = uicontrol(program.gui.right_panel.handle,
    'units', 'normalized',
    'position', [0 .9 1 .1],
    'string', 'new result',
    'callback', @new_result_btn);
  program.gui.close_result_btn.handle = uicontrol(program.gui.right_panel.handle,
    'units', 'normalized',
    'position', [0 .8 1 .1],
    'string', 'delete result',
    'callback', @delete_result_btn);
  program.gui.plot_result_btn.handle = uicontrol(program.gui.right_panel.handle,
    'units', 'normalized',
    'position', [0 .7 1 .1],
    'string', 'plot result',
    'callback', @plot_result_btn);
  program.gui.select_result_lstbx.handle = uicontrol(program.gui.right_panel.handle,
    'style', 'listbox',
    'units', 'normalized',
    'position', [0 0 1 .7],
    'string', '',
    'callback', @select_result_lstbx);
  
  update_result_lstbx();
end