from astropy.stats import sigma_clip
from tigro.logging import logger
from tigro.utils import median_filter

def flag_outliers(sequence, rawmap, kernel_size=3, sigma=100):
    """
    Flag outlier pixels in a sequence of 2D maps using median filtering
    and sigma clipping.

    For each frame in the input `rawmap`, the function:
      1. Removes the mean value.
      2. Estimates a smooth background using a 2D median filter.
      3. Computes residuals with respect to the background.
      4. Applies sigma clipping to identify outliers.
      5. Updates the mask of the output array to flag the detected outliers.

    Parameters
    ----------
    sequence : int
        Identifier of the sequence being processed (used for logging only).

    rawmap : numpy.ma.MaskedArray
        Input masked array of shape (N, Y, X), where N is the number of
        frames. Existing masks are preserved and extended with newly
        detected outliers.

    kernel_size : int, optional
        Size of the square kernel used for the median filter.
        Default is 3.

    sigma : float, optional
        Sigma threshold for the sigma-clipping step.
        Default is 100.

    Returns
    -------
    numpy.ma.MaskedArray
        A copy of `rawmap` with its mask updated to include pixels
        identified as outliers.

    Notes
    -----
    - The median filtering is performed frame by frame.
    - Sigma clipping is applied to the residuals after background removal.
    - This function does not modify the input `rawmap` in place.

    """

    logger.info("Filtering sequence {:3d}".format(sequence))
    retval = rawmap.copy()
    for num in range(rawmap.shape[0]):
        mm = rawmap[num] - rawmap[num].mean()
        mm = median_filter(mm, kernel_size=kernel_size)
        mm = rawmap[num, ...] - mm
        mm = sigma_clip(mm, sigma=sigma, masked=True)
        retval[num].mask |= mm.mask

    return retval    