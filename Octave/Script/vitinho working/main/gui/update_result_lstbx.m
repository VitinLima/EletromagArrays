function update_result_lstbx()
  global program;
  
  if !isempty(program.results)
    set(program.gui.select_result_lstbx.handle, 'string', {program.results.Name});
  else
    set(program.gui.select_result_lstbx.handle, 'string', '');
  end
  set(program.gui.select_result_lstbx.handle, 'value', 1);
  select_result_lstbx();
end