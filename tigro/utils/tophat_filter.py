from scipy.signal import convolve2d
import numpy as np


def tophat_filter(ima, kernel_size=3):
    """
    Apply a square top-hat mean filter to a masked 2D array.

    The local mean is computed using only unmasked pixels within each
    ``kernel_size x kernel_size`` neighborhood. Masked pixels do not
    contribute to either the sum or the normalization.

    Parameters
    ----------
    ima : numpy.ma.MaskedArray
        Two-dimensional masked input array. Masked elements are ignored
        when computing the local mean.

    kernel_size : int, optional
        Size of the square top-hat kernel, in pixels. Default is 3.

    Returns
    -------
    out : numpy.ma.MaskedArray
        Filtered array with the same shape as ``ima``. A pixel is masked
        in the output only if its kernel footprint contains no valid input
        pixels.

    Notes
    -----
    The filter computes

        out[i, j] = sum(valid data in kernel) / number of valid pixels

    rather than dividing by ``kernel_size**2``. This ensures that masked
    pixels and pixels outside the image boundaries do not bias the local
    mean.

    Consequently, originally masked pixels may have valid values in the
    output if their neighborhood contains at least one valid pixel.

    Examples
    --------
    >>> filtered = masked_tophat(ima, kernel_size=11)
    """
    kernel = np.ones((kernel_size, kernel_size), dtype=float)

    valid = (~np.ma.getmaskarray(ima)).astype(float)
    data = np.ma.filled(ima, 0.0)

    num = convolve2d(
        data, kernel, mode='same',
        boundary='fill', fillvalue=0
    )

    den = convolve2d(
        valid, kernel, mode='same',
        boundary='fill', fillvalue=0
    )

    with np.errstate(divide='ignore', invalid='ignore'):
        out = num / den

    return np.ma.array(out, mask=(den == 0))