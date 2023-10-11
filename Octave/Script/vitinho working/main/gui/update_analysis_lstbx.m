function update_analysis_lstbx()
  global program;
  
  if !isempty(program.analysis)
    set(program.gui.select_analysis_lstbx.handle, 'string', {program.analysis.Name});
  else
    set(program.gui.select_analysis_lstbx.handle, 'string', '');
  end
  set(program.gui.select_analysis_lstbx.handle, 'value', 1);
  select_analysis_lstbx();
end