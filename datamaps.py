import healpy as hp
import numpy as np

from plancklens import utils

### Input the path to temperature map here. Ensure units are *Micro*Kelvin.
tlm_path = '/mount/citadel1/zz1994/codes/plqe/maps/lensed_alm.fits'

class websky_lensed:
    '''
    Websky lensed temperature map (in harmonics).
    Map does not contain gaussian noise. Noise can be specified in param file.

    No e, b maps are provided, so this class returns zero for both. No calculation
    is dones with e, b maps. 
    '''
    
    def __init__(self):
        self.tlm = hp.read_alm(tlm_path)
        self.alm_size = self.tlm.size

    def hashdict(self):
        ### For Plancklens caching and retrieval.
        return {'sim_lib': 'Websky lensed scalar cmb inputs, freq 0'}

   
    def get_sim_tlm(self, idx):
        '''
        Returns temperature map. 
        'idx' normally specifies simulation, but no simulated data is returned here.
        It is just kept to mimic the plancklens structure.
        '''
        tlm = self.tlm
        return tlm

   
    def get_sim_elm(idx):
        return np.zeros(self.alm_size)

  
    def get_sim_blm(idx):
        return np.zeros(self.alm_size)


    
