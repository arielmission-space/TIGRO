import numpy as np
from tigro.logging import logger


def fit_polynomial(sequence, ima, zkm):
    """
    Fit a set of basis functions to a 2D masked image by linear least squares.

    The input basis functions are fitted simultaneously to the valid pixels
    of `ima`. A common mask is constructed by combining the image mask with
    the masks of all basis functions, so that only pixels valid in both the
    image and every basis function are used in the fit.

    The fitted model is

        ima ~= sum_k coeff[k] * zkm[k]

    where the coefficients are obtained from an ordinary linear least-squares
    solution. The function also estimates the residual variance and the
    covariance matrix of the fitted coefficients.

    Parameters
    ----------
    sequence : int
        Sequence identifier used only for logging.
    ima : numpy.ma.MaskedArray
        Two-dimensional masked image to be fitted, with shape `(ny, nx)`.
    zkm : numpy.ma.MaskedArray
        Set of basis functions with shape `(n_basis, ny, nx)`. The spatial
        dimensions must match those of `ima`.

    Returns
    -------
    model : numpy.ma.MaskedArray
        Individual fitted model components, with shape
        `(n_basis, ny, nx)`. The total fitted model is obtained with

        `model.sum(axis=0)`.

    coeff : numpy.ndarray
        Best-fit coefficients, with shape `(n_basis,)`.

    cov : numpy.ndarray
        Estimated covariance matrix of the fitted coefficients, with shape
        `(n_basis, n_basis)`. It is computed as

        `var * pinv(X.T @ X)`

        where `var` is the residual variance and `X` is the design matrix.

    Raises
    ------
    TypeError
        If either `ima` or `zkm` is not a NumPy masked array.

    Notes
    -----
    The residual variance is estimated as

        RSS / (N - n_basis)

    where `N` is the number of valid fitted pixels and `RSS` is the residual
    sum of squares.

    Pixels masked in `ima` or in any element of `zkm` are excluded from the
    fit and masked in the returned model components.
    """
    
    logger.info(f"Fitting sequence {sequence}")

    if not np.ma.isMaskedArray(zkm) or not np.ma.isMaskedArray(ima):
        raise TypeError("fit_polynomial expects masked arrays")

    zkm = np.ma.asarray(zkm).copy()
    ima = np.ma.asarray(ima).copy()

    # Common mask: reject pixels masked either in the image
    # or in any polynomial basis function
    mask = np.any(np.ma.getmaskarray(zkm), axis=0)
    mask |= np.ma.getmaskarray(ima)

    zkm.mask = np.broadcast_to(mask, zkm.shape)
    ima.mask = mask

    valid = ~mask

    # Design matrix
    X = zkm.data[:, valid].T
    y = ima.data[valid]

    N = y.size

    # Least-squares fit
    coeff, *_ = np.linalg.lstsq(X, y, rcond=None)

    # Model components
    model = coeff[:, None, None] * zkm

    # Residual variance
    residual = y - X @ coeff
    rss = np.sum(residual**2)

    dof = N - coeff.size
    var = rss / dof

    # Coefficient covariance
    cov = var * np.linalg.pinv(X.T @ X)

    return model, coeff, cov
