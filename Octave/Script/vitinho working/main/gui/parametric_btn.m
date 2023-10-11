function parametric_btn(h, e)
  global program;
  
  if ishandle(program.gui.right_panel.handle)
    delete(program.gui.right_panel.handle);
  end
  
end