close all
for FID = fopen("all")
  fclose(FID)
end
##clear
clc

%DIRNAME = uigetdir("D:\\WS\\AnsysEM\\DipoloTeste\\Results\\", "Select a directory with .csv 3d polar plot exported from HFSS");
DIRNAME = [pwd, filesep, "Resultados", filesep, "Dipoles"];
save3DPolarPlot([DIRNAME,filesep,"rE Plot 0-5.csv"]);
save3DPolarPlot([DIRNAME,filesep,"rE Plot 1-0.csv"]);
save3DPolarPlot([DIRNAME,filesep,"rE Plot 1-25.csv"]);
save3DPolarPlot([DIRNAME,filesep,"rE Plot 1-5.csv"]);
##saveGraphs("LogPeriodica");

##DIRNAME = [pwd, filesep, "Resultados", filesep, "Yagis"];
##saveGraphs([DIRNAME,filesep,"Dipolo"], 1,2,3);
##saveGraphs([DIRNAME,filesep,"2EL"],1,2,3);
##saveGraphs([DIRNAME,filesep,"3EL"],1,2,3);
##saveGraphs([DIRNAME,filesep,"4EL"],1,2,3);

##[n,v] = readFile(["Resultados",filesep,"Dipole 0-5.csv"]);
##save3DDirectivity(n,v,"Dipole 0-5");
