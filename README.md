# ssmg-hfis-macro-micro-variability
A Novel Approach to Couple Macro and Micro-scale Variability for Delineation of Site-Specific Management Grid
# Coupling Macro and Micro-scale Variability for Delineation of Site-Specific Management Grid (SSMG)

This repository contains MATLAB and Python code supporting the manuscript:

**"Coupling Macro and Micro-scale Variability for Delineation of Site-Specific Management Grid"**  
Computers and Electronics in Agriculture (Manuscript: **COMPAG-D-26-00416**)

## Overview
The code implements components of a Hybrid Fuzzy Inference System (H-FIS) / ANFIS workflow to couple:
- Macro-scale soil variability (e.g., Veris ECa shallow/deep, OM, CEC, topography)
- Micro-scale crop variability from UAV vegetation indices (e.g., NDRE, NDVI)

Outputs include fuzzy productivity maps / classifications used to delineate Site-Specific Management Grids (SSMGs).

## Repository structure
- `scripts/` : entry-point scripts to reproduce key outputs
- `src/matlab/` : MATLAB functions (FIS/ANFIS, preprocessing)
- `src/python/` : Python scripts (fuzzy control system, post-processing)
- `data/` : input data (not included publicly if large/sensitive)

## Requirements
### MATLAB
- MATLAB R20xx (tested with: <your version>)
- Fuzzy Logic Toolbox (required for `newfis`, `addmf`, `evalfis`, ANFIS)

### Python
- Python 3.9+ (recommended)
- Install dependencies:
  ```bash
  pip install -r requirements.txt
