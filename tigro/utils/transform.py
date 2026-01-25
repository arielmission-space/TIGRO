import numpy as np
import cv2


def transform(map, xc, yc, Dx, Dy, phi, flags=cv2.INTER_AREA, borderValue=np.nan):
    """
    Apply a rigid 2D transformation (rotation + translation) to a masked image.

    The function rotates the input map by an angle ``phi`` around the point
    (xc, yc) and then applies a translation of (Dx, Dy). Masked values are
    propagated and preserved in the output. OpenCV interpolation and border
    handling can be controlled via optional parameters.

    Parameters
    ----------
    map : np.ma.MaskedArray
        Input 2D image or map to be transformed.
    xc, yc : float
        Coordinates of the rotation center (in pixel units).
    Dx, Dy : float
        Translation applied after rotation along the x and y directions.
    phi : float
        Rotation angle in radians (counterclockwise).
    flags : int, optional
        OpenCV interpolation flag passed to ``cv2.warpAffine``
        (default: ``cv2.INTER_AREA``).
    borderValue : float, optional
        Value used for pixels outside the transformed image domain
        (default: ``np.nan``).

    Returns
    -------
    np.ma.MaskedArray
        Transformed image with masked values preserved.
    """
    RM = cv2.getRotationMatrix2D((xc, yc), np.rad2deg(phi), 1.0)
    RM[:, -1] += Dx, Dy
    M_ = cv2.warpAffine(
        map.filled(np.nan), RM, map.shape, flags=flags, borderValue=borderValue
    )
    return np.ma.MaskedArray(M_, np.isnan(M_))
