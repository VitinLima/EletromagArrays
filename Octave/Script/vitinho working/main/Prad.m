function Prad = Prad(antenna)
  global eta;
  
  antenna = toVectorShape(antenna);
  Prad = sum(antenna.E.*antenna.E/2/eta.*sin(antenna.THETA))/length(antenna.THETA);
end