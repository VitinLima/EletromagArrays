function antenna = evaluateExpression(antenna)
  global f;
  global c;
  global lambda;
  global k;
  
  if isempty(program.analysis)
    return;
  end
  
  for i = 1:length(program.analysis)
    a = program.analysis(i);
    expression = strsplit(a.Expression);
    a.Data = eval(expression);
    program.analysis(i) = a;
  end
end