function neat_horizontal_uipanel(h)
  C = get(h, 'children');
  N = length(C);
  
  dx = 1/N;
  
  for i = 1:N
    set(C(i), 'units', 'normalized', 'position', [(N-i)*dx 0 dx 1]);
  end
end