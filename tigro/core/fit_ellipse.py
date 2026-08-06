import numpy as np
from scipy.ndimage import median_filter
from tigro.utils import LsqEllipseNew


def fit_ellipse(
    sequence,
    mask,
    boundary_th=0.65,
    inside_th=0.96,
    full=False,
    max_iter=100,
    kernel_size=101,
    n_sigma=3.0,
    theta_th=5.0,
):
    """
    Fit an ellipse to the boundary of a masked two-dimensional region.

    The boundary is identified from the gradient magnitude of the
    inverted Boolean mask. An ellipse is then fitted iteratively while
    rejecting:

    1. points identified by ``LsqEllipseNew.inside`` as lying
       sufficiently far inside the fitted ellipse;
    2. local radial outliers relative to a circular median-filtered
       residual.

    For each iteration, the measured radial distance of every boundary
    point is compared with the ellipse radius at the same polar angle.
    The radial residuals are ordered by angle and a median filter with
    periodic boundary conditions is applied. Points whose detrended
    residual exceeds ``n_sigma`` times its standard deviation are
    rejected.

    Parameters
    ----------
    sequence : int
        Sequence identifier used in exception messages.

    mask : ndarray of bool, shape (ny, nx)
        Boolean mask defining the region of interest. Masked pixels are
        assumed to be ``True``.

    boundary_th : float, optional
        Minimum gradient magnitude used to select boundary pixels.
        Default is 0.65.

    inside_th : float, optional
        Threshold on the squared normalized elliptical radius used by
        ``LsqEllipseNew.inside``. Points satisfying

        ``rho**2 < inside_th``

        are rejected. For example, ``inside_th=0.96`` corresponds to a
        normalized radial threshold of ``sqrt(0.96)``, approximately
        0.98. Default is 0.96.

    full : bool, optional
        If ``False``, return only the fitted ellipse parameters. If
        ``True``, also return diagnostic quantities for the retained
        boundary points. Default is ``False``.

    max_iter : int, optional
        Maximum number of fit-and-rejection iterations. Default is 100.

    kernel_size : int, optional
        Size of the one-dimensional median-filtering kernel applied to
        the angularly ordered radial residuals. It must be a positive
        odd integer. Periodic boundary conditions are used. Default is
        101.

    n_sigma : float, optional
        Rejection threshold for local radial outliers, expressed in
        units of the standard deviation of the detrended residual.
        Points satisfying

        ``abs(detrended_residual) > n_sigma * sigma``

        are rejected. Default is 3.0.

    theta_th : float, optional
        Maximum permitted angular separation, in degrees, between
        consecutive retained points after sorting by angle. The check
        is non-periodic and does not include the separation between the
        last and first sorted samples. Default is 5.0 degrees.

    Returns
    -------
    ret_par : dict
        Dictionary containing the fitted ellipse parameters:

        ``a``
            First ellipse semi-axis after application of the adopted
            reference-frame convention.

        ``b``
            Second ellipse semi-axis after application of the adopted
            reference-frame convention.

        ``b/a``
            Ratio between the returned semi-axes.

        ``xc``, ``yc``
            Coordinates of the fitted ellipse centre.

        ``phi``
            Ellipse rotation angle in radians after application of the
            adopted reference-frame convention.

        ``rf_inverted``
            Boolean indicating whether the semi-axes were exchanged
            because the fitted angle was close to pi/2.

    theta : ndarray, optional
        Polar angle of each retained boundary point relative to the
        final ellipse principal-axis orientation. Returned only when
        ``full=True``.

    r_data : ndarray, optional
        Distance of each retained boundary point from the fitted ellipse
        centre. Returned only when ``full=True``.

    r_model : ndarray, optional
        Radius of the fitted ellipse evaluated at each value of
        ``theta``. Returned only when ``full=True``.

    x_normalized, y_normalized : ndarray, optional
        Centre-subtracted image-frame coordinates divided respectively
        by the returned semi-axes ``a`` and ``b``. These coordinates are
        not rotated into the ellipse principal-axis frame. Returned only
        when ``full=True``.

    Raises
    ------
    TypeError
        If ``mask`` is not a NumPy array.

    ValueError
        If ``mask`` is not a two-dimensional Boolean array, if an input
        parameter is invalid, if fewer than five initial boundary points
        are found, or if the maximum angular separation exceeds
        ``theta_th``.

    RuntimeError
        If fewer than five points remain during filtering or if the
        iterative rejection does not converge within ``max_iter``
        iterations.
    """

    # ---------------------------------------------------------------
    # Validate inputs
    # ---------------------------------------------------------------

    if not isinstance(mask, np.ndarray):
        raise TypeError("mask must be a NumPy array.")

    if mask.ndim != 2:
        raise ValueError("mask must be a two-dimensional array.")

    if mask.dtype != np.bool_:
        raise ValueError("mask must be a Boolean array.")

    if boundary_th < 0.0:
        raise ValueError("boundary_th must be non-negative.")

    if not 0.0 < inside_th < 1.0:
        raise ValueError("inside_th must be between 0 and 1.")

    if not isinstance(max_iter, (int, np.integer)) or max_iter < 1:
        raise ValueError("max_iter must be a positive integer.")

    if (
        not isinstance(kernel_size, (int, np.integer))
        or kernel_size < 1
        or kernel_size % 2 == 0
    ):
        raise ValueError("kernel_size must be a positive odd integer.")

    if n_sigma <= 0.0:
        raise ValueError("n_sigma must be positive.")

    if theta_th <= 0.0:
        raise ValueError("theta_th must be positive.")

    # ---------------------------------------------------------------
    # Extract boundary points
    # ---------------------------------------------------------------

    data_mask = 1.0 - mask.astype(float)

    grad_y, grad_x = np.gradient(data_mask)
    boundary = np.hypot(grad_x, grad_y)

    YY, XX = np.where(boundary > boundary_th)

    XX = XX.astype(float)
    YY = YY.astype(float)

    if XX.size < 5:
        raise ValueError(
            f"Sequence {sequence}: only {XX.size} boundary points found."
        )

    # ---------------------------------------------------------------
    # Iterative fit and rejection
    # ---------------------------------------------------------------

    for iteration in range(max_iter):

        if XX.size < 5:
            raise RuntimeError(
                f"Sequence {sequence}: too few boundary points remain."
            )

        ellipse = LsqEllipseNew().fit(
            np.column_stack((XX, YY))
        )

        # Points sufficiently far inside the fitted ellipse
        cond_inside = ellipse.inside(
            XX,
            YY,
            threshold=inside_th,
        )

        (xc, yc), a, b, phi = ellipse.as_parameters()

        dx = XX - xc
        dy = YY - yc

        psi = np.arctan2(dy, dx)

        # Angle relative to the ellipse principal-axis orientation
        theta = psi - phi

        # Sort by angle before applying the median filter
        idx_sort = np.argsort(theta)
        theta_sort = theta[idx_sort]

        r_data = np.hypot(
            dx[idx_sort],
            dy[idx_sort],
        )

        r_model = (a * b) / np.sqrt(
            (b * np.cos(theta_sort)) ** 2
            + (a * np.sin(theta_sort)) ** 2
        )

        residual = r_data - r_model

        # Circular median filtering: the first and last elements of the
        # sorted sequence correspond to adjacent physical directions.
        local_residual = median_filter(
            residual,
            size=kernel_size,
            mode="wrap",
        )

        detrended_residual = residual - local_residual

        # Standard-deviation estimate and zero-centred rejection
        sigma = np.std(detrended_residual)

        if np.isfinite(sigma) and sigma > 0.0:
            cond_outlier_sort = (
                np.abs(detrended_residual)
                > n_sigma * sigma
            )
        else:
            cond_outlier_sort = np.zeros(
                detrended_residual.size,
                dtype=bool,
            )

        # Restore the original point ordering
        cond_outlier = np.zeros(
            XX.size,
            dtype=bool,
        )
        cond_outlier[idx_sort] = cond_outlier_sort

        cond = cond_inside | cond_outlier

        if not np.any(cond):
            break

        XX = XX[~cond]
        YY = YY[~cond]

    else:
        raise RuntimeError(
            f"Sequence {sequence}: ellipse filtering did not converge "
            f"within {max_iter} iterations."
        )

    # ---------------------------------------------------------------
    # Final fit on the retained points
    # ---------------------------------------------------------------

    if XX.size < 5:
        raise RuntimeError(
            f"Sequence {sequence}: too few points remain for the final fit."
        )

    ellipse = LsqEllipseNew().fit(
        np.column_stack((XX, YY))
    )

    (xc, yc), a, b, phi = ellipse.as_parameters()

    dx = XX - xc
    dy = YY - yc

    psi = np.arctan2(dy, dx)
    theta = psi - phi

    idx_sort = np.argsort(theta)
    theta_sort = theta[idx_sort]

    # Non-periodic angular-gap check
    dtheta = np.rad2deg(
        np.max(
            np.abs(
                np.diff(theta_sort)
            )
        )
    )

    if dtheta > theta_th:
        raise ValueError(
            f"Sequence {sequence}: ellipse fit opened an angular gap "
            f"of {dtheta:.1f} deg.\n"
            "Reduce inside_th or relax the rejection parameters."
        )

    # ---------------------------------------------------------------
    # Restore the adopted reference-frame convention
    # ---------------------------------------------------------------

    if np.abs(phi - 0.5 * np.pi) < np.deg2rad(5.0):
        rf_inverted = True

        a, b = b, a
        phi -= 0.5 * np.pi

    else:
        rf_inverted = False

    ret_par = {
        "a": a,
        "b": b,
        "b/a": b / a,
        "xc": xc,
        "yc": yc,
        "phi": phi,
        "rf_inverted": rf_inverted,
    }

    # ---------------------------------------------------------------
    # Optional full output
    # ---------------------------------------------------------------

    if full:
        dx = XX - xc
        dy = YY - yc

        psi = np.arctan2(dy, dx)
        theta = psi - phi
        idx = np.argsort(theta)
        theta = theta[idx]
        dx = dx[idx]
        dy = dy[idx]

        r_model = (a * b) / np.sqrt(
            (b * np.cos(theta)) ** 2
            + (a * np.sin(theta)) ** 2
        )

        r_data = np.hypot(dx, dy)

        return (
            ret_par,
            theta,
            r_data,
            r_model,
            dx / a,
            dy / b,
        )

    return ret_par


def fit_ellipse_deprecated(sequence, mask, boundary_th=0.65):
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
        raise ValueError("mask not bool array.")

    data_mask = 1.0 - mask.astype(float)
    Grad = np.gradient(data_mask)
    boundary = np.sqrt(Grad[0] ** 2 + Grad[1] ** 2)
    idx = np.where(boundary.flatten() > boundary_th)[0]
    XX = idx % boundary.shape[1]
    YY = idx // boundary.shape[1]

    # Remove outliers inside the edge
    max_iter = 1000
    for _iter_ in range(max_iter):
        _ellipse = LsqEllipseNew().fit(np.c_[XX, YY])
        cond = _ellipse.inside(XX, YY)

        if not np.any(cond):
            break

        XX = XX[~cond]
        YY = YY[~cond]
    else:
        raise RuntimeError("Ellipse filtering did not converge")

    (xc, yc), a, b, phi = _ellipse.as_parameters()

    if np.abs(phi - 0.5 * np.pi) < np.deg2rad(5.0):
        rf_inverted = True
        a, b = b, a
        phi -= 0.5 * np.pi
    else:
        rf_inverted = False

    return {
        "a": a,
        "b": b,
        "b/a": b / a,
        "xc": xc,
        "yc": yc,
        "phi": phi,
        "rf_inverted": rf_inverted,
    }
