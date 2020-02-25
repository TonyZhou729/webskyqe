import os

### Set to where the plancklens module is located at.
os.environ['PLENS'] = '/mount/citadel1/zz1994/GitHub/plancklens'

import healpy as hp
import numpy as np
import matplotlib.pyplot as plt
from plancklens import utils
import param as parfile

qe_key = 'ptt' # Temperature lensing gradient
# To be honest I still don't know how these keys work but if they work they work.

ell = np.arange(2049)

# Loads the lensing estimate calculated in the parameter file.
qlm = parfile.qlms_dd.get_sim_qlm(qe_key, -1)

# Lensing repsonse according to the fiducial cosmology:
qresp = parfile.qresp_dd.get_response(qe_key, 'p')

# Estimator normalization is the inverse response:
qnorm = utils.cli(qresp)

# Semi-analytical realization-dependent Gaussian noise bias (of the unnormalized estimator):
nhl = parfile.nhl_dd.get_sim_nhl(-1, qe_key, qe_key)

### Plotting the result ###
w = lambda ell : ell ** 2 * (ell + 1.) ** 2  / 4

# Self-correlated $C_L^{\kappa \kappa}$ from lensing estimate.
qecl_kk = (hp.alm2cl(qlm)[ell]-nhl[ell]) * qnorm[ell] ** 2 / parfile.qlms_dd.fsky12 * w(ell)

plt.figure()
plt.title('Lensing Gradient (TT)')
label=r'$C_L^{\hat \kappa \hat \kappa} - \hat N_L^{(0)}}$' if qe_key[0] == 'p' else r'$C_L^{\hat \omega \hat \omega}$'

plt.loglog(ell, qecl_kk, label=label)
plt.loglog(ell, nhl[ell] * qnorm[ell] ** 2 * w(ell), label=r'$\hat N_L^{(0)}$ (semi-analytical)')

plt.xlabel('$L$', fontsize=12)
plt.ylabel('$C_L^{\kappa \kappa}$', fontsize=12)
plt.legend(fontsize=12, loc='lower left')
plt.show()
