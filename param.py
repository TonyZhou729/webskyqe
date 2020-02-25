import os
import healpy as hp
import numpy as np

### Plancklens utilities
import plancklens
from plancklens.filt import filt_simple, filt_util
from plancklens import utils
from plancklens import qest, qecl, qresp
from plancklens import nhl
from plancklens.sims import phas, maps, utils as map_utils

### Data Library. Should be in the same directory as current file.
import datamaps

### Enter the absolute path to the plancklens module.
os.environ['PLENS'] = '/mount/citadel1/zz1994/GitHub/plancklens'
assert 'PLENS' in os.environ.keys(), 'Set env. variable PLENS to a writeable folder'

'''
Directory in which datasets (maps, simulated noise, etc.) are cached. 
If you change your input map, or ANY parameter for a new calculation, plancklens 
will read a missmatch in hashing, in which case modify the path below so that
plancklens may cache new data and compute.
'''
TEMP = os.path.join(os.environ['PLENS'], 'temp', 'websky%d' % 1)

### Enter the absolute path to the fiducial cosmology data. 
### Structure of sample data is provided (or just use them.)
### Ensure that temperature Cls are Cl*L(L+1)/(2pi), and have units microK^2
### If you use the provided fiducial cosmology, enter path to 'fidcosmo' which should be in the same directory.
cls_path = '/mount/citadel1/zz1994/codes/webskyqe/fidcosmo'

#--- definition of simulation and inverse-variance filtered simulation libraries:
lmax_ivf = 2048
lmin_ivf = 100
lmax_qlm = 4096 # We will calculate lensing estimates until multipole lmax_qlm.
nside = 2048 # Healpix resolution of the data and sims.
fwhm = 7.1 # Pixel size of the survey, in arc-miniutes.
int_survey = 6. # (delta T)/T intensity of the survey, in microkelvin.
nlev_t = fwhm * int_survey # Set by the above two parameters and determines
# Gaussian noise standard deviation. Also used for noise processing.

nlev_p = 55. # Setting in case polarization data is provided. In this script no calculation
# with polarization is done, so this is just a place holder.

transf = hp.gauss_beam(fwhm / 60. / 180. * np.pi, lmax=lmax_ivf) * hp.pixwin(nside)[:lmax_ivf + 1]
# CMB transfer function. Here a Gaussian beam and healpix pixel window function. Used in smoothing.

cl_unl = utils.camb_clfile(os.path.join(cls_path, 'CAMB_lenspotentialCls.dat'))
cl_len = utils.camb_clfile(os.path.join(cls_path, 'CAMB_lensedCls.dat'))
# Fiducial unlensed and lensed power spectra used for the analysis.

cl_weight = cl_len
cl_weight['bb'] *= 0
# CMB spectra entering the QE weights (the spectra multplying the inverse-variance filtered maps in the QE legs)

libdir_pixphas = os.path.join(TEMP, 'pix_phas_nside%s'%nside)
pix_phas = phas.pix_lib_phas(libdir_pixphas, 3, (hp.nside2npix(nside),))
# Noise simulation T, Q, U random phases instance.

lib = maps.cmb_maps_nlev(datamaps.websky_lensed(), transf, nlev_t, nlev_p, nside, pix_lib_phas=pix_phas)
# Datamap library that also applies gaussian noise to input temperature map.


# --- We turn to the inverse-variance filtering library. In this file we use trivial isotropic filtering,
#     (independent T and Pol. filtering)
ftl = utils.cli(cl_len['tt'][:lmax_ivf + 1] + (nlev_t / 60. / 180. * np.pi / transf) ** 2)
fel = utils.cli(cl_len['ee'][:lmax_ivf + 1] + (nlev_p / 60. / 180. * np.pi / transf) ** 2)
fbl = utils.cli(cl_len['bb'][:lmax_ivf + 1] + (nlev_p / 60. / 180. * np.pi / transf) ** 2)
ftl[:lmin_ivf] *= 0.
fel[:lmin_ivf] *= 0.
fbl[:lmin_ivf] *= 0.
#: Inverse CMB co-variance in T, E and B (neglecting TE coupling).

ivfs = filt_simple.library_fullsky_sepTP(os.path.join(TEMP, 'ivfs'), lib, nside, transf, cl_len, ftl, fel, fbl, cache=True)
#: Inverse-variance filtering instance. Here a trivial isotropic inverse variance weighting.

# QE Library that builds lensing estimation with data map on both legs. 
qlms_dd = qest.library_sepTP(os.path.join(TEMP, 'qlms_dd'), ivfs, ivfs,   cl_len['te'], nside, lmax_qlm=lmax_qlm)

# Semi-analytical Gaussian lensing bias library. It is callable as a noise power spectrum output.
nhl_dd = nhl.nhl_lib_simple(os.path.join(TEMP, 'nhl_dd'), ivfs, cl_weight, lmax_qlm)

# QE response calculation library. Provides normalization to both lensing estimate and noise.
qresp_dd = qresp.resp_lib_simple(os.path.join(TEMP, 'qresp'), lmax_ivf, cl_weight, cl_len,
                                         {'t': ivfs.get_ftl(), 'e':ivfs.get_fel(), 'b':ivfs.get_fbl()}, lmax_qlm)
