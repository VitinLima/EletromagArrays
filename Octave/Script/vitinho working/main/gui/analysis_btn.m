function analysis_btn(h,e)
  global program;
  
  if ishandle(program.gui.right_panel.handle)
    delete(program.gui.right_panel.handle);
  end
  
  program.gui.right_panel.handle = uipanel(program.gui.handle,
    'units', 'normalized',
    'position', [0 0 .2 .9]);
  program.gui.eval_all_analysis_lstbx_btn.handle = uicontrol(program.gui.right_panel.handle,
    'units', 'normalized',
    'position', [0 .9 1 .1],
    'string', 'eval all analysis',
    'callback', @new_analysis_btn);
  program.gui.new_analysis_btn.handle = uicontrol(program.gui.right_panel.handle,
    'units', 'normalized',
    'position', [0 .9 1 .1],
    'string', 'new analysis',
    'callback', @new_analysis_btn);
  program.gui.edit_analysis_btn.handle = uicontrol(program.gui.right_panel.handle,
    'units', 'normalized',
    'position', [0 .8 1 .1],
    'string', 'edit analysis',
    'callback', @edit_analysis_btn);
  program.gui.delete_analysis_btn.handle = uicontrol(program.gui.right_panel.handle,
    'units', 'normalized',
    'position', [0 .7 1 .1],
    'string', 'delete analysis',
    'callback', @delete_analysis_btn);
##  program.gui.eval_analysis_lstbx_btn.handle = uicontrol(program.gui.right_panel.handle,
##    'units', 'normalized',
##    'position', [0 .6 1 .1],
##    'string', 'evaluate all',
##    'callback', @eval_analysis_btn);
  program.gui.select_analysis_lstbx.handle = uicontrol(program.gui.right_panel.handle,
    'style', 'listbox',
    'units', 'normalized',
    'position', [0 0 1 .7],
    'string', '',
    'callback', @select_analysis_lstbx);
end