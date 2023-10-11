function select_analysis_lstbx(h,e)
  global program;
  
  if isempty(program.analysis)
    return;
  end
  
  program.current_analysis = get(program.gui.select_analysis_lstbx.handle, 'value');
##  analysis = get_current_analysis();
##  set(program.gui.infotext.handle, 'string', ['Analysis:',analysis.Name]);
end