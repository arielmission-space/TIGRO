from .tophat_filter import tophat_filter
from .median_filter import median_filter
from astropy.stats import sigma_clip


def hp_filter(ima, kernel_size=11, filt = tophat_filter,
              flag_outliers=False, sigma=5):
    hp = ima - filt(ima, kernel_size=kernel_size)
    if flag_outliers:
        hp = sigma_clip(hp, sigma=sigma)

    return hp