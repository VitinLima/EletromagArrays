close all
for FID = fopen("all")
  fclose(FID);
end
clear;
clc;

##saveIdealDipole(0.5, 0.82032);
##saveIdealDipole(1.0, 0.14117);
##saveIdealDipole(1.25, 0.18348);
##saveIdealDipole(1.5, 0.18348);

saveIdealDipoleDirectivity(0.5);