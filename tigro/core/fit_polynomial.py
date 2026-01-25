import numpy as np
from tigro.logging import logger


def fit_polynomial(sequence, ima, zkm):
    """
    Fit a polynomial model to a 2D image using a masked polynomial basis.

    This function performs a least-squares fit of a set of polynomial basis
    functions (`zkm`) to an input image (`ima`). The fit is carried out only
    on valid (unmasked) pixels, and masking from the input image is propagated
    to the polynomial basis before fitting.

    The polynomial coefficients are obtained by solving the normal equations
    constructed from the inner products of the basis functions. The resulting
    model is returned as a linear combination of the input basis.

    Parameters
    ----------
    sequence : int
        Sequence identifier, used only for logging purposes.
    ima : numpy.ma.MaskedArray
        Input 2D image to be fitted. Must be a masked array.
    zkm : numpy.ma.MaskedArray
        Polynomial basis array of shape (N, Ny, Nx), where N is the number
        of basis functions. Must be a masked array.

    Returns
    -------
    model : numpy.ma.MaskedArray
        Reconstructed model image(s), obtained as the linear combination
        of the polynomial basis with the fitted coefficients.
    coeff : numpy.ndarray
        Array of fitted polynomial coefficients of length N.

    Raises
    ------
    TypeError
        If `ima` is not a masked array.
    """
    logger.info("Fitting sequence {:d}".format(sequence))
    zkm = zkm.copy()
    if hasattr(ima, "mask"):
        zkm.mask |= ima.mask
    else:
        raise TypeError("plyfit expects polynomials as masked arrays")

    A = np.einsum("ijk,ljk", zkm.filled(0), zkm.filled(0))
    A /= zkm[0].count()

    A[np.abs(A) < 1e-10] = 0.0

    B = np.ma.mean(zkm * ima, axis=(-2, -1))
    coeff = np.linalg.lstsq(A, B, rcond=-1)[0]

    model = coeff.reshape(-1, 1, 1) * zkm
    return model, coeff
