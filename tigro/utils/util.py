import numpy as np
from matplotlib import pyplot as plt
from photutils.aperture import EllipticalAperture
import cv2
from ellipse import LsqEllipse


def mymfil(ima, kernel_size=3):
    from scipy.signal import medfilt2d as mfilt

    if hasattr(ima, "mask"):
        ima_ = ima.filled(fill_value=ima.mean())
        retval = mfilt(ima_, kernel_size)
        mask = np.isinf(retval)
        retval[mask] = 0.0
        retval = np.ma.masked_array(data=retval, mask=mask | ima.mask)
    else:
        ima_ = ima
        retval = mfilt(ima_, kernel_size)

    return retval


class myLsqEllipse(LsqEllipse):
    def as_parameters(self):
        """Returns the definition of the fitted ellipse as localized parameters

        Returns
        _______
        center : tuple
            (x0, y0)
        width : float
            Total length (diameter) of horizontal axis.
        height : float
            Total length (diameter) of vertical axis.
        phi : float
            The counterclockwise angle [radians] of rotation from the x-axis to the semimajor axis
        """

        # Eigenvectors are the coefficients of an ellipse in general form
        # the division by 2 is required to account for a slight difference in
        # the equations between (*) and (**)
        # a*x^2 +   b*x*y + c*y^2 +   d*x +   e*y + f = 0  (*)  Eqn 1
        # a*x^2 + 2*b*x*y + c*y^2 + 2*d*x + 2*f*y + g = 0  (**) Eqn 15
        # We'll use (**) to follow their documentation
        a = self.coefficients[0]
        b = self.coefficients[1] / 2.0
        c = self.coefficients[2]
        d = self.coefficients[3] / 2.0
        f = self.coefficients[4] / 2.0
        g = self.coefficients[5]

        # Finding center of ellipse [eqn.19 and 20] from (**)
        x0 = (c * d - b * f) / (b**2 - a * c)
        y0 = (a * f - b * d) / (b**2 - a * c)
        center = (x0, y0)

        # Find the semi-axes lengths [eqn. 21 and 22] from (**)
        numerator = 2 * (
            a * f**2 + c * d**2 + g * b**2 - 2 * b * d * f - a * c * g
        )
        denominator1 = (b**2 - a * c) * (
            np.sqrt((a - c) ** 2 + 4 * b**2) - (c + a)
        )  # noqa: E201
        denominator2 = (b**2 - a * c) * (
            -np.sqrt((a - c) ** 2 + 4 * b**2) - (c + a)
        )
        width = np.sqrt(numerator / denominator1)
        height = np.sqrt(numerator / denominator2)

        # Angle of counterclockwise rotation of major-axis of ellipse to x-axis
        # [eqn. 23] from (**)
        # w/ trig identity eqn 9 form (***)
        if b == 0 and a < c:
            phi = 0.0
        elif b == 0 and a > c:
            phi = np.pi / 2
        elif b != 0 and a < c:
            phi = 0.5 * np.arctan(2 * b / (a - c))
        elif b != 0 and a > c:
            phi = 0.5 * (np.pi + np.arctan(2 * b / (a - c)))
        elif a == c:
            phi = 0.0
        else:
            raise RuntimeError("Unreachable")

        return center, width, height, phi

    def inside(self, x, y, threshold=0.9):
        # Check if coordinate (x, y) are withing the ellipse
        #   that has been fit previously returing the following

        (xc, yc), a, b, phi = self.as_parameters()

        c, s = np.cos(phi), np.sin(phi)
        R = np.array([[c, -s], [s, c]])
        v = np.vstack((x - xc, y - yc))
        v = R.T @ v
        condition = (v[0] / a) ** 2 + (v[1] / b) ** 2 < threshold

        return condition


def transform(M, xc, yc, Dx, Dy, phi):
    RM = cv2.getRotationMatrix2D((xc, yc), np.rad2deg(phi), 1.0)
    RM[:, -1] += Dx, Dy
    M_ = cv2.warpAffine(
        M.filled(np.nan), RM, M.shape, flags=cv2.INTER_AREA, borderValue=np.nan
    )
    return np.ma.MaskedArray(M_, np.isnan(M_))


# def filled(ima, kernel_size=3):
#     mima = mylib.median_filter(ima, kernel_size=kernel_size)
#     mm = ima.filled(0)
#     mm[ima.mask] = mima[ima.mask]
#     return mm


def get_threshold(phmap, threshold="lo", plot=True):
    # Get threshold for outlier rejection
    ncounts = np.hstack(
        [phmap[seq]["cleanmap"].count(axis=(1, 2)) for seq in phmap.keys()]
    )

    lo, threshold, med, hi = np.percentile(ncounts, [0.0, 0.1, 50, 99.9])
    if threshold == "lo":
        threshold = lo

    if plot:
        plt.figure()
        plt.plot(ncounts)
        plt.ylim(lo, hi)
        xlim = plt.xlim()
        plt.hlines([threshold, med], *xlim)
        plt.title("Check threshold by eye!!!")
        plt.show()

    return threshold


def get_uref(phmap, semi_major, semi_minor, sequence_ref):
    uref = {}
    shape = phmap[sequence_ref]["RegMap"].shape

    x0, y0 = shape[1] // 2, shape[0] // 2
    aperture = EllipticalAperture((x0, y0), semi_major, semi_minor, theta=0.0)
    mask = ~aperture.to_mask("center").to_image(shape).astype(bool)

    x = (np.arange(shape[1]) - x0) / semi_major
    y = (np.arange(shape[0]) - y0) / semi_major

    uref["pupil_mask"] = mask
    uref["xc"] = x0
    uref["yc"] = y0
    uref["a"] = semi_major
    uref["b"] = semi_minor
    uref["yx"] = [y, x]
    uref["extent"] = x.min(), x.max(), y.min(), y.max()

    return uref


def get_diff_idx(idx0, idx1, colors):
    assert len(idx0) == len(idx1), "Length mismatch"
    diff_idx = []
    for i0, i1, color in zip(idx0, idx1, colors):
        for j0, j1 in zip(i0, i1):
            diff_idx.append([int(j0), int(j1), color])
    return diff_idx
