function [fis, T] = build_fis_from_excel(excel_path)
% build_fis_from_excel
% Reads Excel and builds a simple Sugeno FIS with Gaussian MFs
% NOTE: This is a minimal working example. You can expand rules later.

T = readtable(excel_path);

ECaSh = T{:,1};
ECaDp = T{:,2};
CEC   = T{:,3};
NDVI  = T{:,4};
SAVI  = T{:,5};
Y     = T{:,6};

fis = newfis('SSMG_FIS','sugeno');

% Helper: add Gaussian low/med/high
add_gauss3 = @(fis, idx, name, x) addvar_and_mfs(fis, idx, name, x);

% Inputs
fis = add_gauss3(fis, 1, 'ECa_Shallow', ECaSh);
fis = add_gauss3(fis, 2, 'ECa_Deep',    ECaDp);
fis = add_gauss3(fis, 3, 'CEC',         CEC);
fis = add_gauss3(fis, 4, 'NDVI_0719',    NDVI);
fis = add_gauss3(fis, 5, 'SAVI_0810',    SAVI);

% Output: yield constants (low/med/high)
q = quantile(Y, [0.25 0.50 0.75]);
fis = addvar(fis,'output','yield',[min(Y) max(Y)]);
fis = addmf(fis,'output',1,'low','constant',q(1));
fis = addmf(fis,'output',1,'medium','constant',q(2));
fis = addmf(fis,'output',1,'high','constant',q(3));

% Simple rules (based mainly on NDVI + SAVI; others "don't care" = 0)
% Format: [in1 in2 in3 in4 in5 out weight andOr]
ruleList = [
    0 0 0 1 1 1 1 1;  % NDVI low AND SAVI low -> yield low
    0 0 0 2 0 2 1 1;  % NDVI medium -> yield medium
    0 0 0 3 3 3 1 1;  % NDVI high AND SAVI high -> yield high
];
fis = addrule(fis, ruleList);

end


function fis = addvar_and_mfs(fis, idx, varname, x)
r = [min(x) max(x)];
m = mean(x);
s = std(x);

fis = addvar(fis,'input',varname,r);
fis = addmf(fis,'input',idx,'low','gaussmf',[s, m - s]);
fis = addmf(fis,'input',idx,'medium','gaussmf',[s, m]);
fis = addmf(fis,'input',idx,'high','gaussmf',[s, m + s]);
end
