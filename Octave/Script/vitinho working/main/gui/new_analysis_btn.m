function new_analysis_btn(h,e)
  global program;
  
  CSTR = inputdlg({"Analysis name:", "Enter expression:"}, "New Analysis Dialog");
  if isempty(CSTR)
    return;
  end
  new_analysis.Name = cell2mat(CSTR(1));
  new_analysis.Expression = cell2mat(CSTR(2));
  new_analysis.Data = [];
  program.analysis(end+1) = new_analysis;
  program.current_analysis = length(program.analysis);
  update_analysis_lstbx();
end