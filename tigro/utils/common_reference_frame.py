import numpy as np
from photutils.aperture import EllipticalAperture

def common_reference_frame(meta, shape, crop_factor=0.0):
    """
    Construct a common reference frame based on the average ellipse parameters
    extracted from multiple datasets.

    The function computes a reference elliptical aperture centered in the image,
    using the mean semi-major and semi-minor axes derived from the input metadata.
    It then builds normalized Cartesian and polar coordinate grids within this
    aperture and returns them together with the corresponding pupil mask.

    Parameters
    ----------
    meta : dict
        Dictionary containing per-sequence metadata. Each entry must include
        ellipse parameters under ``meta[key]['ellipse']`` with fields ``'a'`` and
        ``'b'`` representing the semi-major and semi-minor axes.
    shape : tuple of int
        Shape of the reference image as ``(ny, nx)``.
    crop_factor : float, optional
        Fractional reduction applied to the ellipse semi-axes to define a
        smaller effective aperture. A value of 0.0 keeps the full aperture,
        while larger values progressively crop it (default: 0.0).

    Returns
    -------
    dict
        Dictionary containing the reference geometry and coordinate mappings:

        - ``pupil_mask`` : 2D bool array  
          Mask defining the valid elliptical aperture region.
        - ``xc``, ``yc`` : int  
          Pixel coordinates of the aperture center.
        - ``a``, ``b`` : float  
          Mean semi-major and semi-minor axes of the ellipse.
        - ``yx`` : list of ndarray  
          Normalized coordinate vectors ``[y, x]``.
        - ``polar_rho`` : np.ma.MaskedArray  
          Radial coordinate normalized to the semi-major axis.
        - ``polar_phi`` : np.ma.MaskedArray  
          Angular coordinate (radians).
        - ``extent`` : list of float  
          Plotting extent ``[xmin, xmax, ymin, ymax]`` in normalized units.
    """
    xc = shape[1]//2; yc = shape[0]//2
    semi_major = np.mean([meta[key]['ellipse']['a'] for key in meta.keys()])
    semi_minor = np.mean([meta[key]['ellipse']['b'] for key in meta.keys()])
    aperture = EllipticalAperture( (xc, yc), 
                               (1.0 - crop_factor) * semi_major, 
                               (1.0 - crop_factor) * semi_minor, 
                               theta=0.0)
    mask = ~aperture.to_mask('center').to_image(shape).astype(bool)
    x = (np.arange(shape[1])-xc)/semi_major
    y = (np.arange(shape[0])-yc)/semi_major

    xx, yy = np.meshgrid(x, y)
    rho = np.ma.MaskedArray(data = np.sqrt(xx**2 + yy**2), 
                            mask = mask, 
                            fill_value = 0.0)
    phi = np.ma.MaskedArray(data = np.arctan2(yy, xx), 
                            mask = mask, 
                            fill_value = 0.0)
    
    retval = {
        'pupil_mask':mask,
        'xc':xc,
        'yc':yc,
        'a':semi_major,
        'b':semi_minor,
        'yx':[y, x],
        'polar_rho':rho,
        'polar_phi':phi,
        'extent' : [x.min(), x.max(), y.min(), y.max()]
    }

    return retval