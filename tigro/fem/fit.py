from scipy.spatial.transform import Rotation as Rot
from scipy.optimize import curve_fit
import numpy as np



def func_fit(xyz, *par, full_output=False):
    npar = len(par)

    if npar == 7:
        # For OAP use this
        c, dx, dy, dz, ox, oy, k = par 
        oz = 0.0
    elif npar == 6:
        c, dx, dy, dz, ox, oy = par 
        k = oz = 0.0
    elif npar == 5:
        c, dx, dy, dz, k = par 
        ox = oy = oz = 0.0
    elif npar == 4:
        # For Spherical mirror use this
        c, dx, dy, dz = par 
        k = ox = oy = oz = 0.0
    else:
        raise ValueError
    
    R     = xyz
    R0    = np.array( [dx, dy, dz] )

    M = Rot.from_euler('XYZ', [ox, oy, oz])
    
    R1 = M.apply( R - R0, inverse=True )
    #R1 = M.as_matrix()@(R.T-R0).T; R1 = R1.T
    
    x1, y1, z1 = R1[:, 0], R1[:, 1], R1[:, 2]
    
    #z1m = 0.5*c * (x1**2 + y1**2)
    
    rho2 = x1**2 + y1**2
    z1m = c * rho2 / (1+np.sqrt(1-(1+k)*c**2 * rho2))

    if full_output:
        R1m = np.vstack( [x1, y1, z1m]).T
        #Rm = M.apply(R1m, inverse=False)+R0
        return R1, R1m
        
    
    return z1-z1m

def fem_fit(xyz, p0):

    par, cov = curve_fit(func_fit, xyz, 0, p0=p0 )
    npar = len(par)
    if npar == 7:
        # For OAP use this
        c, dx, dy, dz, ox, oy, k = par 
        oz = 0.0
    elif npar == 6:
        c, dx, dy, dz, ox, oy = par 
        k = oz = 0.0
    elif npar == 5:
        c, dx, dy, dz, k = par 
        ox = oy = oz = 0.0
    elif npar == 4:
        # For Spherical mirror use this
        c, dx, dy, dz = par 
        k = ox = oy = oz = 0.0
    else:
        raise ValueError
    return 1/c, dx, dy, dz, ox, oy, k
