function neat_vertical_uipanel(h)
  C = get(h, 'children');
  N = length(C);
  
  dy = 1/N;
  
  for i = 1:N
    set(C(i), 'units', 'normalized', 'position', [0 (N-i)*dy 1 dy]);
  end
end