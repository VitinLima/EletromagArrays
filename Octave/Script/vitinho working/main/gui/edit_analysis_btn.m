function edit_analysis_btn(h,e)
  global program;
  
  if isempty(program.analysis)
    return;
  end
  current_analysis = get_current_analysis();
  DEFAULTS = {
    current_analysis.Name,
    current_analysis.Expression
  }';
  CSTR = inputdlg({"Analysis name:", "Enter expression:"}, "Edit Analysis Dialog", 1, DEFAULTS);
  if isempty(CSTR)
    return;
  end
  current_analysis.Name = cell2mat(CSTR(1));
  current_analysis.Expression = cell2mat(CSTR(2));
  program.analysis(program.current_analysis) = current_analysis;
  update_analysis_lstbx();
end