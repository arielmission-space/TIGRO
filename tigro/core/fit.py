import numpy as np
from paos.classes.zernike import PolyOrthoNorm

from tigro.utils.util import myLsqEllipse

from tigro import logger


def fit_ellipse(phmap):
    # Edge ellipse fit
    for seq in phmap.keys():
        # data_mask= 1-phmap[seq]['medmap'].mask.astype(float)
        data_mask = 1 - phmap[seq]["supermask"].astype(float)

        Grad = np.gradient(data_mask)
        boundary = np.sqrt(Grad[0] ** 2 + Grad[1] ** 2)
        idx = np.where(boundary.flatten() > 0.65)[0]
        XX = idx % boundary.shape[1]
        YY = idx // boundary.shape[1]
        _ellipse = myLsqEllipse().fit(np.c_[XX, YY])
        (xc, yc), a, b, phi = _ellipse.as_parameters()
        # Remove outliers inside the edge
        cond = _ellipse.inside(XX, YY)
        if np.any(cond):
            XX = XX[~cond]
            YY = YY[~cond]
            _ellipse = myLsqEllipse().fit(np.c_[XX, YY])

        (xc, yc), a, b, phi = _ellipse.as_parameters()

        if np.abs(phi - 0.5 * np.pi) < np.deg2rad(5.0):
            logger.debug("** Sequence: {:3d} is outlier".format(seq))
            a, b = b, a
            phi -= 0.5 * np.pi

        phmap[seq]["ellipse"] = {
            "a": a,
            "b": b,
            "b/a": b / a,
            "xc": xc,
            "yc": yc,
            "phi": phi,
        }

        logger.debug(f"{seq} ({xc:.1f} {yc:.1f}) {a:.1f} {b:.1f} {np.rad2deg(phi):.1f}")

    return phmap


def calculate_zernike(phmap, uref, NZernike=15):
    logger.debug("Calculating {:d} Polys... ".format(NZernike))
    pupil_mask = uref["pupil_mask"]
    y_, x_ = uref["yx"]
    xx, yy = np.meshgrid(x_, y_)

    phi = np.arctan2(yy, xx)
    rho = np.ma.masked_array(
        data=np.sqrt(yy**2 + xx**2), mask=pupil_mask, fill_value=0.0
    )

    poly = PolyOrthoNorm(NZernike, rho, phi, normalize=True, ordering="noll")
    zkm = poly()
    A = poly.cov()
    logger.debug("... done!")
    return zkm, A


def fit_zernike(phmap, uref, NZernike=15, zkm=None, A=None):
    if zkm is None or A is None:
        zkm, A = calculate_zernike(phmap, uref, NZernike)

    logger.debug("Fitting sequence n: ...")
    for seq in phmap.keys():
        logger.debug("{:3d}".format(seq))
        B = np.ma.mean(zkm * phmap[seq]["RegMap"], axis=(-2, -1))
        # Note: below one could have set coeff=B because A is diagonal.
        # However, A is not quite diagonal because of holes in the maps.
        # But this is not implemented below, and should be fixed!!!!
        # Flags need to be accounted for in the estimate of A.
        coeff = np.linalg.lstsq(A, B, rcond=-1)[0]
        phmap[seq]["coeff"] = coeff
        model = coeff.reshape(-1, 1, 1) * zkm
        phmap[seq]["PTTF"] = np.ma.sum(model[0:4, ...], axis=0)
        phmap[seq]["RegMap-PTTF"] = phmap[seq]["RegMap"] - phmap[seq]["PTTF"]
        phmap[seq]["model"] = np.ma.sum(model, axis=0)
        phmap[seq]["residual"] = phmap[seq]["RegMap"] - phmap[seq]["model"]

    return phmap
