function createGraphics(array, antv)
  global f;
  global c;
  global lambda;
  global k;
  
  cd graphics
  
  C = array.E;

  trisurf_invertedsphere( ...
    array.PHI, ...
    array.THETA, ...
    zeros(1,length(array.PHI)), ...
    C, ...
    'array_magE');
  title("Electric field magnitude");

  cd ..
end