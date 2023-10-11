function analysis = get_current_analysis()
  global program;
  
  if !isempty(program.analysis)
    analysis = program.analysis(program.current_analysis);
  else
    analysis = [];
  end
end