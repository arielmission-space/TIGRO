import numpy as np
from tigro.utils import LsqEllipseNew

def fit_ellipse(sequence, mask, boundary_th = 0.65):
    """
    Fit an ellipse to the boundary of a masked 2D region.

    The function identifies the boundary of a binary mask by computing the
    gradient magnitude of the inverted mask. Boundary pixels above a given
    threshold are selected and used to fit an ellipse using a least-squares
    method. An iterative rejection scheme removes points lying inside the
    fitted ellipse to improve robustness against outliers.

    Parameters
    ----------
    sequence : int
        Sequence index (used for logging or bookkeeping purposes).
    mask : ndarray (2D, boolean)
        Input mask defining the region of interest. Masked pixels are assumed
        to be `True`.
    boundary_th : float, optional
        Threshold applied to the gradient magnitude to select boundary pixels.
        Default is 0.65.

    Returns
    -------
    dict
        Dictionary containing the fitted ellipse parameters:
        - 'a' : semi-major axis length
        - 'b' : semi-minor axis length
        - 'b/a' : axis ratio
        - 'xc' : x-coordinate of ellipse center
        - 'yc' : y-coordinate of ellipse center
        - 'phi' : rotation angle (radians), following Wolfram ellipse notation
        - 'rf_inverted' : bool flag indicating whether axes were swapped to
          restore the reference-frame convention
    """
    
    if mask.dtype != np.bool_:
        raise ValueError('mask not bool array.')
    
    data_mask = 1.0 - mask.astype(float)
    Grad = np.gradient(data_mask)
    boundary = np.sqrt(Grad[0]**2 + Grad[1]**2)
    idx = np.where(boundary.flatten()>boundary_th)[0]
    XX = idx % boundary.shape[1]
    YY = idx // boundary.shape[1]
    
    # Remove outliers inside the edge
    max_iter = 1000
    for _iter_ in range(max_iter):
        _ellipse = LsqEllipseNew().fit(np.c_[XX, YY])
        cond = _ellipse.inside(XX, YY)

        if not np.any(cond): break

        XX = XX[~cond]
        YY = YY[~cond]
    else:
        raise RuntimeError("Ellipse filtering did not converge")
    
    (xc, yc), a, b, phi = _ellipse.as_parameters()
  
    if np.abs(phi - 0.5*np.pi) < np.deg2rad(5.0):
        rf_inverted = True
        a, b = b, a
        phi -= 0.5*np.pi
    else:
        rf_inverted = False

    
    return {'a': a, 'b':b, 'b/a': b/a, 'xc': xc, 'yc': yc, 'phi': phi, 'rf_inverted': rf_inverted}