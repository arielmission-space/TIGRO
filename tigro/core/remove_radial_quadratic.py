import numpy as np


def remove_radial_quadratic(
    im,
    mask=None,
    return_model=False,
    return_coeff=False,
):
    """
    Fit and subtract the model

        M(x, y) = b0
                + b1 * (x - xc)
                + b2 * (y - yc)
                + b3 * ((x - xc)**2 + (y - yc)**2)

    where (xc, yc) is the geometrical centre of the image.

    The radial quadratic term is therefore zero at the image centre.

    Parameters
    ----------
    im : array_like or numpy.ma.MaskedArray
        Two-dimensional input image.

    mask : array_like of bool, optional
        Additional mask with the same shape as `im`.
        Pixels for which `mask` is True are excluded from the fit.
        mask is not applied to the returned corrected array.

    return_model : bool, default=False
        If True, also return the fitted model.

    return_coeff : bool, default=False
        If True, also return the coefficients [b0, b1, b2, b3].

    Returns
    -------
    corrected : ndarray or numpy.ma.MaskedArray
        Input image after subtraction of the fitted model.

    model : ndarray, optional
        Fitted model, returned if `return_model=True`.

    coeff : ndarray, optional
        Coefficients [b0, b1, b2, b3], returned if
        `return_coeff=True`.
    """
    im_ma = np.ma.asarray(im, dtype=float)

    if im_ma.ndim != 2:
        raise ValueError("`im` must be a two-dimensional array.")

    ny, nx = im_ma.shape

    y, x = np.indices((ny, nx), dtype=float)

    # Geometrical centre of the array
    xc = nx / 2.0
    yc = ny / 2.0

    xx = (x - xc)/xc
    yy = (y - yc)/yc
    rr2 = xx**2 + yy**2
    
    invalid = np.ma.getmaskarray(im_ma).copy()
    invalid |= ~np.isfinite(im_ma.data)

    if mask is not None:
        mask = np.asarray(mask, dtype=bool)

        if mask.shape != im_ma.shape:
            raise ValueError("`mask` must have the same shape as `im`.")

        invalid |= mask

    valid = ~invalid
    
    if np.count_nonzero(valid) < 4:
        raise ValueError("At least four valid pixels are required.")

    # Design matrix for:
    # M = b0 + b1*xx + b2*yy + b3*rr2
    A = np.column_stack((
        np.ones(np.count_nonzero(valid)),
        xx[valid],
        yy[valid],
        rr2[valid],
    ))

    values = im_ma.data[valid]

    coeff, _, rank, _ = np.linalg.lstsq(A, values, rcond=None)

    if rank < 4:
        raise ValueError("The least-squares problem is rank deficient.")

    b0, b1, b2, b3 = coeff

    model = b0 + b1*xx + b2*yy + b3*rr2
    corrected_data = im_ma - model
    
    # if np.ma.isMaskedArray(im) or mask is not None:
    #     corrected = np.ma.array(corrected_data, mask=invalid)
    # else:
    #     corrected = corrected_data
    #     corrected[invalid] = np.nan

    # output = [corrected]
    
    output = [corrected_data]

    if return_model:
        output.append(model)

    if return_coeff:
        output.append(coeff)

    return output[0] if len(output) == 1 else tuple(output)