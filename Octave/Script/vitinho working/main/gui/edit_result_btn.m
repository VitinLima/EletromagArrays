function edit_result_btn(h, e)
  global program;
  
  if isempty(program.results)
    return;
  end
  
  update_result_lstbx();
end