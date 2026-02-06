import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import get_window


def make_window2d(shape, window="hann"):

    ny, nx = shape
    wx = get_window(window, nx, fftbins=False)
    wy = get_window(window, ny, fftbins=False)

    w = wy[:, None] * wx[None, :]

    # Preserve power scaling
    w = w / np.sqrt(np.mean(w**2))

    return w


def make_ellipse_window2d(shape, ellipse):

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

    df = bins[1] - bins[0]
    err = 1 - np.sum(psd * df) / data.var()  # Parceval theorem

    if verbose:
        print(f"Numerical error: {err}")
    return err


def compute_psd(data, nbins, delta_d=1.0, remove_dc_offs=True, verbose=True):
    """
    Calculate PSD from a 2D data image

    data: array
      input array. Can be a masked array.
    nbins: int
        number of PSD bins. The PSD estiamte has one fewer point than bins
    delta: scalar
        Sample spacing (inverse of the sampling rate). Defaults to 1.
    remove_dc_offs: bool
        if True, then data.mean() is removed before calculating the FT
    verbose: bool
        if True, prints numerical error
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
    delta_d=1,
    verbose=True,
    ellipse=None,
    plot=False,
):
    if not hasattr(data, "mask"):
        data = np.ma.MaskedArray(data.copy(), ~np.isfinite(data))

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
