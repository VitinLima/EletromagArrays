function [Names,Values] = readFile(filename)
  FID = fopen(filename);
  if FID==-1
    Names = [];
    Values = [];
    disp("File not found");
    return
  end
  s = fgetl(FID);
  if s(1)=='"'
    s(1) = [];
    s(end) = [];
    s = strsplit(s,'\",\"');
  else
    s = strsplit(s,',');
  end
  Names = s;
##  template = strjoin(repmat({"%f"},1,length(Names)), ',');
  Values = csvread(FID);
  fclose(FID);
##  [VAL, COUNT, ERRMSG] = fscanf(FID, template);
##  Values = [];
##  while (s=fgetl(FID))!=-1
##    if isempty(s)
##      continue;
##    end
##    s = strsplit(s,",");
##    Values(end+1,:) = s = str2double(s);
##  end
end