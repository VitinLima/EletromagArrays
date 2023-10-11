function delete_result_btn(h, e)
  global program;
  if isempty(program.results)
    return;
  end
  
  delete(program.results(program.current_result).axes);
  program.results(program.current_result) = [];
  program.current_result = length(program.results);
  update_result_lstbx();
end