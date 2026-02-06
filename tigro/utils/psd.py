import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import get_window


def make_window2d(shape, window="hann"):
    """
    Create a separable (2D window can be written as the product of two 1D
    windows) 2D tapering window with unit RMS power.

    The window is built as the outer product of two 1D windows (y and x),
    produced by :func:`scipy.signal.get_window`. The resulting 2D window is
    normalized so that its mean-square value is 1 (i.e., unit RMS), which
    preserves the overall power scaling when applied multiplicatively.

    Parameters
    ----------
    shape : tuple of int
        Window shape as (ny, nx), matching the 2D data array shape.
    window : str or tuple, optional
        Window specification passed to :func:`scipy.signal.get_window`
        (default: "hann"). Examples: "hann", "hamming", ("kaiser", beta).

    Returns
    -------
    w : ndarray of shape `shape`
        2D window array normalized to unit RMS (sqrt(mean(w**2)) == 1).

    Notes
    -----
    - Uses `fftbins=False` so the generated 1D windows are symmetric.
    - Normalizing to unit RMS is convenient for PSD estimation because it
      reduces window-dependent power bias (while still changing spectral leakage).
    """

    ny, nx = shape
    wx = get_window(window, nx, fftbins=False)
    wy = get_window(window, ny, fftbins=False)

    w = wy[:, None] * wx[None, :]

    # Preserve power scaling
    w = w / np.sqrt(np.mean(w**2))

    return w


def make_ellipse_window2d(shape, ellipse):
    """
    Create an elliptical Hann-taper window as a masked array, normalized to unit RMS.

    This constructs an ellipse in pixel coordinates, optionally rotated by `phi`,
    and defines an "elliptical radius" r such that r=1 is the ellipse boundary.
    A Hann taper is applied as a function of r for points inside the ellipse:
        w(r) = 0.5 * (1 + cos(pi * r))   for r <= 1
    Points outside the ellipse are masked. The unmasked region is normalized to
    unit RMS (sqrt(mean(w**2)) == 1 over the unmasked samples).

    Parameters
    ----------
    shape : tuple of int
        Window shape as (ny, nx), matching the 2D data array shape.
    ellipse : dict
        Ellipse definition with the following keys:
        - "a"   : float, semi-axis length in x'-direction (pixels)
        - "b"   : float, semi-axis length in y'-direction (pixels)
        - "xc"  : float, x-center in pixel coordinates
        - "yc"  : float, y-center in pixel coordinates
        - "phi" : float, rotation angle (radians), positive for
        counterclockwise rotation

    Returns
    -------
    w : numpy.ma.MaskedArray of shape `shape`
        Masked 2D window. Samples outside the ellipse are masked. The window is
        normalized to unit RMS over unmasked samples.

    Notes
    -----
    - The coordinate origin is at the image index origin (row/column indices).
      The ellipse is centered by subtracting (xc, yc) from the coordinate grids.
    - The mask is `True` outside the ellipse, enabling straightforward use with
      masked data (e.g., data * w).
    """

    a = ellipse["a"]
    b = ellipse["b"]
    xc = ellipse["xc"]
    yc = ellipse["yc"]
    phi = ellipse["phi"]

    # pixel coordinate grids
    y, x = np.indices(shape, dtype=float)
    x -= xc
    y -= yc

    # rotate into ellipse frame (x', y')
    ca, sa = np.cos(phi), np.sin(phi)
    xp = ca * x + sa * y
    yp = -sa * x + ca * y

    # elliptical radius
    r = np.sqrt((xp / a) ** 2 + (yp / b) ** 2)

    # Hann taper in elliptical radius
    w = np.zeros_like(r)
    inside = r <= 1.0
    w[inside] = 0.5 * (1.0 + np.cos(np.pi * r[inside]))  # 1 at r=0, 0 at r=1

    w = np.ma.MaskedArray(w, ~inside)
    w = w / np.ma.sqrt(np.ma.mean(w**2))

    return w


def compute_numerical_error(data, bins, psd, verbose=True):
    """
    Estimate numerical error of a radially binned PSD via a Parseval consistency check.

    The error metric compares the variance of the spatial-domain data to the
    integral of the estimated power spectral density (PSD). With ideal discrete
    normalization and no numerical artifacts, Parseval's theorem implies that
    the PSD integral matches the variance (for zero-mean data). This function
    reports the relative discrepancy:

        err = 1 - (sum(psd * df) / var(data))

    where df is the bin spacing.

    Parameters
    ----------
    data : array_like or numpy.ma.MaskedArray
        Input data used to compute the PSD. If masked, the variance is computed
        on the masked array according to NumPy's masked-array semantics.
    bins : ndarray
        PSD bin edges (length = nbins). Assumes uniform spacing; `df` is taken
        as `bins[1] - bins[0]`.
    psd : ndarray
        PSD values per bin (length = len(bins) - 1), typically returned by
        `compute_psd`.
    verbose : bool, optional
        If True, prints the computed numerical error (default: True).

    Returns
    -------
    err : float
        Relative discrepancy between PSD integral and data variance. Values near
        0 indicate good consistency.

    Notes
    -----
    - For best interpretability, the input data should have its DC component removed
      (zero mean), consistent with typical PSD practice.
    - This is a diagnostic metric; nonzero values can arise from masking, windowing,
      normalization choices, and finite-precision effects.
    """

    df = bins[1] - bins[0]
    err = 1 - np.sum(psd * df) / data.var()

    if verbose:
        print(f"Numerical error: {err}")
    return err


def compute_psd(data, nbins, delta_d=1.0, remove_dc_offs=True, verbose=True):
    """
    Compute a radially averaged (isotropic) 2D power spectral density (PSD).

    This function estimates the 2D periodogram of the input image using the
    squared magnitude of the 2D FFT, then performs radial binning in frequency
    space to obtain a 1D PSD as a function of the radial spatial frequency.

    Non-finite values are handled by converting the input to a masked array
    (if it is not already one) and filling masked entries with zero prior to
    the FFT. Optionally, the mean (DC offset) is removed before computing the FFT

    Parameters
    ----------
    data : array_like or numpy.ma.MaskedArray
        Input 2D array (image). If `data` is not a masked array, non-finite values
        (NaN/Inf) are masked internally. If `data` is a masked array, its mask is
        respected; masked samples are filled with zeros for the FFT.
    nbins : int or None
        Number of radial frequency bins (i.e., number of bin edges). The returned
        PSD has length `nbins - 1`. If None, a default is chosen as
        `min(ny//2, nx//2)`.
    delta_d : float, optional
        Sample spacing in the spatial domain (default: 1.0). This sets the units
        of the frequency axis via `np.fft.fftfreq`, so frequencies are in cycles
        per unit of `delta_d`.
    remove_dc_offs : bool, optional
        If True (default), subtracts the mean of `data` before FFT computation.
        This removes the DC component, which otherwise can dominate the lowest
        frequency bin.
    verbose : bool, optional
        If True (default), prints a numerical consistency error estimate based on
        a Parseval-type check (see Notes).

    Returns
    -------
    psd : ndarray, shape (len(bins) - 1,)
        Radially binned PSD estimate. Values correspond to the sum of the 2D
        periodogram within each radial bin, divided by the bin width and by the
        number of unmasked samples (`data.count()`).
    bins : ndarray, shape (nbins,)
        Radial frequency bin edges spanning from `freq.min()` to `freq.max()`,
        where `freq = sqrt(fx^2 + fy^2)` and `fx, fy` are the FFT frequency grids.
    dataf : ndarray, shape data.shape
        Shifted 2D periodogram-like array used for binning:
        `fftshift(|fft2(data_filled)|^2)` with an additional normalization by
        `(ny * nx)`.
    ff : ndarray, shape (len(bins) - 1,)
        Radial frequency bin centers (midpoints of consecutive `bins` edges).
    error : float
        Numerical error metric returned by :func:`compute_numerical_error`, defined as
        `1 - (sum(psd * df) / var(data))` with `df = bins[1] - bins[0]`.

    Notes
    -----
    - **Masked / non-finite data**: If `data` is not masked, NaN/Inf values are masked.
    The FFT is performed on `data.filled(0)`, so masked samples contribute zero.
    - **Radial binning**: Uses `scipy.stats.binned_statistic(..., statistic="sum")`
    on the flattened radial frequency map and the flattened 2D periodogram.
    - **Normalization**: The 2D periodogram is scaled by `1/(ny*nx)`. The binned sum
    is then divided by the bin widths (`np.diff(bins)`) and by the number of
    unmasked samples (`data.count()`), yielding a density-like quantity in radial
    frequency.
    - **Consistency check**: The reported `error` is a diagnostic for how closely the
    integral of the 1D PSD matches the spatial-domain variance under the chosen
    normalization and masking strategy. Windowing or masking can change this value.
    """

    from scipy.stats import binned_statistic

    if not hasattr(data, "mask"):
        data = np.ma.MaskedArray(data.copy(), ~np.isfinite(data))

    if remove_dc_offs:
        data -= data.mean()

    dataf = np.abs(np.fft.fft2(data.filled(0)))
    dataf = np.fft.fftshift(dataf**2)
    dataf /= data.shape[0] * data.shape[1]
    fx = np.fft.fftshift(np.fft.fftfreq(data.shape[1], d=delta_d))
    fy = np.fft.fftshift(np.fft.fftfreq(data.shape[0], d=delta_d))

    fxx, fyy = np.meshgrid(fx, fy)
    freq = np.sqrt(fxx**2 + fyy**2)

    if nbins is None:
        nbins = min(data.shape[1] // 2, data.shape[0] // 2)
    bins = np.linspace(freq.min(), freq.max(), nbins)

    psd, _, _ = binned_statistic(freq.ravel(), dataf.ravel(), "sum", bins=bins)
    psd /= np.diff(bins)
    psd /= data.count()

    ff = 0.5 * (bins[1:] + bins[:-1])

    error = compute_numerical_error(data, bins, psd, verbose=verbose)

    return psd, bins, dataf, ff, error


def compute_psd_windowed(
    data,
    nbins,
    delta_d=1.0,
    remove_dc_offs=True,
    verbose=True,
    ellipse=None,
    plot=False,
):
    """
    Compute a radially averaged PSD from 2D data after applying a 2D window.

    This function prepares `data` as a masked array (masking non-finite values),
    optionally removes its mean (DC offset), applies either:
    - a separable 2D window from :func:`make_window2d`, or
    - an elliptical Hann-taper mask from :func:`make_ellipse_window2d`,
    and then delegates PSD estimation to :func:`compute_psd`.

    Parameters
    ----------
    data : array_like or numpy.ma.MaskedArray
        Input 2D data. Non-finite values are masked if `data` is not already a
        masked array.
    nbins : int or None
        Number of radial frequency bins. If None, :func:`compute_psd` selects a
        default based on the data dimensions.
    delta_d : float, optional
        Sample spacing in the spatial domain (default: 1.0). Passed through to
        :func:`compute_psd` for frequency axis construction.
    remove_dc_offs : bool, optional
        If True, subtracts the data mean before windowing/FFT (default: True).
    verbose : bool, optional
        If True, prints numerical error diagnostics (default: True).
    ellipse : dict or None, optional
        If provided, defines an elliptical Hann window/mask via
        :func:`make_ellipse_window2d`. If None, a separable 2D window is used.
        See :func:`make_ellipse_window2d` for required keys.
    plot : bool, optional
        If True, displays the original data and the windowed data side-by-side
        using Matplotlib (default: False).

    Returns
    -------
    psd : ndarray
        Radially binned PSD values (one per bin interval).
    bins : ndarray
        Bin edges used for radial averaging.
    dataf : ndarray
        Shifted squared-magnitude FFT (2D periodogram-like estimate) used for binning.
    ff : ndarray
        Bin-center frequencies (midpoints of `bins`).
    error : float
        Numerical error estimate from :func:`compute_numerical_error`.
    """

    if not hasattr(data, "mask"):
        data = np.ma.MaskedArray(data.copy(), ~np.isfinite(data))

    if remove_dc_offs:
        data -= data.mean()

    if ellipse:
        w2d = make_ellipse_window2d(shape=data.shape, ellipse=ellipse)
    else:
        w2d = make_window2d(data.shape)

    data_win = data * w2d

    if plot:
        fig, axs = plt.subplots(1, 2)
        axs[0].imshow(data)
        axs[1].imshow(data_win)
        plt.show()

    return compute_psd(
        data_win,
        nbins=nbins,
        delta_d=delta_d,
        remove_dc_offs=True,
        verbose=verbose,
    )
