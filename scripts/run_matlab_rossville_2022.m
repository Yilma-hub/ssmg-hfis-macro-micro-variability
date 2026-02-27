% scripts/run_matlab_rossville_2022.m
% Paper: COMPAG-D-26-00416
% Builds a simple Gaussian-MF FIS from an Excel input file (Rossville 2022 example)

clc; clear;

% --- Paths (portable; no D:\ or C:\ hardcoding) ---
repoRoot = fileparts(fileparts(mfilename('fullpath')));
dataFile = fullfile(repoRoot, 'data', 'Rossville_2022_values_based_Getis_analysis_macro_micro_4_Multivariate.xlsx');
outDir   = fullfile(repoRoot, 'results');
if ~exist(outDir, 'dir'); mkdir(outDir); end

% --- Read Excel (assumes variables are in first 6 columns) ---
% If your Excel has headers, readtable is easier than xlsread
T = readtable(dataFile);

Veris_ECa_Shallow_data = T{:,1};
Veris_ECa_Deep_data    = T{:,2};
Veris_CEC_data         = T{:,3};
ndvi_0719_data         = T{:,4};
savi_0810_data         = T{:,5};
yield_data             = T{:,6};

% --- Create FIS ---
fis = newfis('SSMG_FIS');

% Helper inline function for Gaussian MF params
gauss_params = @(x) [std(x), mean(x)];

% ---- Input 1: ECa Shallow
r = [min(Veris_ECa_Shallow_data), max(Veris_ECa_Shallow_data)];
m = mean(Veris_ECa_Shallow_data); s = std(Veris_ECa_Shallow_data);
fis = addvar(fis,'input','Veris_ECa_Shallow', r);
fis = addmf(fis,'input',1,'low','gaussmf',[s, m - s]);
fis = addmf(fis,'input',1,'medium','gaussmf',[s, m]);
fis = addmf(fis,'input',1,'high','gaussmf',[s, m + s]);

% ---- Input 2: ECa Deep
r = [min(Veris_ECa_Deep_data), max(Veris_ECa_Deep_data)];
m = mean(Veris_ECa_Deep_data); s = std(Veris_ECa_Deep_data);
fis = addvar(fis,'input','Veris_ECa_Deep', r);
fis = addmf(fis,'input',2,'low','gaussmf',[s, m - s]);
fis = addmf(fis,'input',2,'medium','gaussmf',[s, m]);
fis = addmf(fis,'input',2,'high','gaussmf',[s, m + s]);

% ---- Input 3: CEC
r = [min(Veris_CEC_data), max(Veris_CEC_data)];
m = mean(Veris_CEC_data); s = std(Veris_CEC_data);
fis = addvar(fis,'input','Veris_CEC', r);
fis = addmf(fis,'input',3,'low','gaussmf',[s, m - s]);
fis = addmf(fis,'input',3,'medium','gaussmf',[s, m]);
fis = addmf(fis,'input',3,'high','gaussmf',[s, m + s]);

% ---- Input 4: NDVI 07/19
r = [min(ndvi_0719_data), max(ndvi_0719_data)];
m = mean(ndvi_0719_data); s = std(ndvi_0719_data);
fis = addvar(fis,'input','NDVI_0719', r);
fis = addmf(fis,'input',4,'low','gaussmf',[s, m - s]);
fis = addmf(fis,'input',4,'medium','gaussmf',[s, m]);
fis = addmf(fis,'input',4,'high','gaussmf',[s, m + s]);

% ---- Input 5: SAVI 08/10
r = [min(savi_0810_data), max(savi_0810_data)];
m = mean(savi_0810_data); s = std(savi_0810_data);
fis = addvar(fis,'input','SAVI_0810', r);
fis = addmf(fis,'input',5,'low','gaussmf',[s, m - s]);
fis = addmf(fis,'input',5,'medium','gaussmf',[s, m]);
fis = addmf(fis,'input',5,'high','gaussmf',[s, m + s]);

% ---- Output: yield (range from observed yield)
yield_range = [min(yield_data), max(yield_data)];
fis = addvar(fis,'output','yield', yield_range);

% NOTE:
% You still need to define output MFs + rules for a working evalfis model.
% This script saves the FIS structure so you can add rules later.

save(fullfile(outDir, 'rossville_2022_fis.mat'), 'fis');
disp("Saved FIS to results/rossville_2022_fis.mat");
