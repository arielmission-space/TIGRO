
import numpy as np
from scipy.signal import medfilt2d as mfilt 

def median_filter(ima, kernel_size=3):
    if hasattr(ima, 'mask'):
        ima_ = ima.filled(fill_value=ima.mean())
        retval = mfilt(ima_, kernel_size) 
        mask = np.isinf(retval)
        retval[mask] = 0.0
        retval = np.ma.masked_array(
            data = retval,
            mask = mask | ima.mask
        )
    else:
        ima_ = ima
        retval = mfilt(ima_, kernel_size) 
                     
    return retval    