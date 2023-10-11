function new_result_btn(h, e)
  global program;
  
  if !isempty(program.results)
    set(cell2mat({program.results.axes}), 'visible', 'off');
  end
  new_axes.axes = axes(program.gui.handle,
    'outerposition', [.2 0 .8 .9]);
  new_axes.Name = num2str(new_axes.axes);
  program.results(end+1) = new_axes;
  program.current_result = length(program.results);
  update_result_lstbx();
end