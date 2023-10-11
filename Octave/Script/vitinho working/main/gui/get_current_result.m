function result = get_current_result()
  global program;
  
  if isempty(program.results)
    new_axes.axes = axes(program.gui.handle,
      'outerposition', [.2 0 .8 .9]);
    new_axes.Name = num2str(new_axes.axes);
    program.results(end+1) = new_axes;
    program.current_result = length(program.results);
    
    if !isempty(program.results)
      set(program.gui.select_result_lstbx.handle,
        'string', {program.results.Name});
    end
  end
  result = program.results(program.current_result);
end