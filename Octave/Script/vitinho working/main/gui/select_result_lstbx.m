function select_result_lstbx(h,e)
  global program;
  
  if isempty(program.results)
    return;
  end
  
  set(cell2mat({program.results.axes}), 'outerposition', [0 0 0 0]);
  set(program.results(get(program.gui.select_result_lstbx.handle, 'value')).axes, 'outerposition', [.2 0 .8 .85]);
  program.current_result = get(program.gui.select_result_lstbx.handle, 'value');
end