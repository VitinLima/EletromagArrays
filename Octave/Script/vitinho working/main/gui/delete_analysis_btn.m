function delete_analysis_btn(h,e)
  global program;
  
  if isempty(program.analysis)
    return;
  end
  
  program.analysis(program.current_analysis) = [];
  update_analysis_lstbx();
end