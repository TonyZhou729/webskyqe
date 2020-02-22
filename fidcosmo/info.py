'''
Some instructions on the structure of the fiducial cosmology files.

1. Unlensed Scalars + Lensed Potential
---Used for 'cl_unl' in the parameter file.
---One file should contain unlensed scalar (TT EE BB TE, in this order) and 
lensing potential data (PP TP EP, again in this order).
---The ells should go up to 7000, though in the computation it probably doesn't need that much. 
For safety you should get lmax=7000 in these files if possible.
---This file should be 8 columns (first for ells, 7 for the data).
---Ensure units on the unlensed scalar Cls are MICROKelvin^2.
---Also ensure the unlensed scalar Cls are Cl*L*(L+1)/(2pi)

2. Lensed Scalars
---Used for 'cl_len' and 'cl_weight' in the parameter file.
---Contains lensed scalar (TT EE BB TE).
---Again try to get ells up to 7000.
---4 columns.
---Ensure L*(L+1)/(2pi), units microkelvin^2.

3. Provided Data Files:
---Came from CAMB with the following parameters.

    pars.set_cosmology(H0=68.0, ombh2=0.0227, omch2=0.121, TCMB=2.7255)
    pars.InitPower.set_params(As=2.075e-9, ns=0.965)
    pars.set_for_lmax(7000, lens_potential_accuracy=1)
'''


















