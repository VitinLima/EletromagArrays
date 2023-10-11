close all
for FID = fopen("all")
  fclose(FID)
end
##clear
clc

%DIRNAME = uigetdir("D:\\WS\\AnsysEM\\DipoloTeste\\Results\\", "Select a directory with .csv 3d polar plot exported from HFSS");
##save3DPolarPlot([DIRNAME,filesep,"rE Plot 0-5.csv"]);
##save3DPolarPlot([DIRNAME,filesep,"rE Plot 1-0.csv"]);
##save3DPolarPlot([DIRNAME,filesep,"rE Plot 1-25.csv"]);
##save3DPolarPlot([DIRNAME,filesep,"rE Plot 1-5.csv"]);
##saveGraphs("LogPeriodica");

##saveGraphs("Dipolo", 1,2,3);
##saveGraphs("2EL",1,2,3);
##saveGraphs("3EL",1,2,3);
##saveGraphs("4EL",1,2,3);

[n,v] = readFile(["Resultados",filesep,"Dipole 0-5.csv"]);
save3DDirectivity(n,v,"Dipole 0-5");