# Websky Q.E.

Lensing Reconstruction Script that builds on the 'plancklens' computation module by Julien Carron. This module is needed to use
the computations made by the above scripts.
For plancklens, see: https://github.com/carronj/plancklens

### Description

Provides lensing reconstruction through Quadratic Estimation of lensed CMB map.
Currently works for temperature map (At least for the provided scripts above), but in theory it should work for 
polarization data.

The plancklens module that this script uses is built for lensing reconstruction on the CMB simulations of Planck2018 lensing maps on the NERSC server.
This script is a way to generalize the module for the lensing estimate of an arbitrary data map.
Plancklens also adds Gaussian noise based on specified pixel size and temperature overdensity intensity. 

### Usage

Ensure your python environment can access plancklens. If not, follow the link at top for download instructions.

In the 'param.py' file, specify path to the plancklens module, as well as fiducial cosmology Cls. For info on requirements of the
fiducial files, see fidcosmo/info.py. Also some CAMB fiducial cosmology is included if you want a quicktest.

In the 'datamaps.py' file, specify the path to your lensed temperature map on which the lensing estimation will be performed.
This map should not contain noise and should not be smoothed (the parameter file provides smoothing). 

All computations are done in param.py. 'demo.py' contains some lines on how you may access these results, as well as some
plotting code that should be simple if you know matplotlib. 

### Demo

Maybe I will work on an ipynb demo later. For now I need some dinner. 
