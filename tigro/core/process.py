import numpy as np
from astropy.stats import sigma_clip

from tigro.utils.util import mymfil
from tigro.utils.util import transform


def filter_phmap(phmap):
    # Outlier rejection, gravity flip, median estimate
    print("Filter sequence : ", end="")
    for seq in phmap.keys():
        print("{:3d}".format(seq), end="")
        rawmap = phmap[seq]["rawmap"].copy()
        for num in range(rawmap.shape[0]):
            rawmap[num] -= rawmap[num].mean()
            mm = mymfil(rawmap[num, ...], kernel_size=3)
            mm = rawmap[num, ...] - mm
            mm = sigma_clip(mm, sigma=10, masked=True)
            rawmap[num].mask |= mm.mask
            del mm

        medmap = np.ma.median(rawmap, axis=0)
        diffrms = np.ma.std(rawmap - medmap, axis=(-2, -1))
        phmap[seq]["diffrms"] = diffrms

        if phmap[seq]["phi_offs"] == np.pi:
            phmap[seq]["cleanmap"] = rawmap[:, ::-1, ::-1]
            print("r ", end="")
        else:
            phmap[seq]["cleanmap"] = rawmap
            print("  ", end="")
        del rawmap

    return phmap


def med_phmap(phmap, threshold, filter_type=np.ma.mean):
    # Median map and supermask
    for seq in phmap.keys():
        idx = phmap[seq]["cleanmap"].count(axis=(1, 2)) > threshold
        medmap = filter_type(phmap[seq]["cleanmap"][idx], axis=0)
        supermask = np.logical_or.reduce(phmap[seq]["cleanmap"][idx].mask, axis=0)
        phmap[seq]["medmap"] = medmap
        phmap[seq]["supermask"] = supermask

    return phmap


def register_phmap(phmap, verbose=True):
    ref_seq = list(phmap.keys())[0]
    shape = phmap[ref_seq]["medmap"].shape
    x0, y0 = shape[1] // 2, shape[0] // 2

    for seq in phmap.keys():
        xc, yc, phi = (
            phmap[seq]["ellipse"]["xc"],
            phmap[seq]["ellipse"]["yc"],
            phmap[seq]["ellipse"]["phi"],
        )
        dx, dy = x0 - xc, y0 - yc

        phmap[seq]["RegMap"] = transform(phmap[seq]["medmap"], xc, yc, dx, dy, phi)
        m_out = np.ma.zeros_like(phmap[seq]["cleanmap"])
        for k in range(phmap[seq]["cleanmap"].shape[0]):
            m_out[k] = transform(phmap[seq]["cleanmap"][k], xc, yc, dx, dy, phi)
        phmap[seq]["RegCleanMap"] = m_out

        if verbose:
            print("|| seq:{:3d} | dx:{:6.2f} dy:{:6.2f}  ||".format(seq, dx, dy))
    return phmap


def zerog_phmap(phmap, diff_idx):

    coeff_med = []
    medmap = []
    color = []
    zerogmap = []

    for u, v, col in diff_idx:
        m0 = phmap[u]["residual"]
        m1 = phmap[v]["residual"]
        mm = (m0 + m1) / 2
        medmap.append(mm)
        m0 = phmap[u]["RegMap-PTTF"]
        m1 = phmap[v]["RegMap-PTTF"]
        mm = (m0 + m1) / 2
        zerogmap.append(mm)
        c0 = phmap[u]["coeff"]
        c1 = phmap[v]["coeff"]
        cm = (c0 + c1) / 2
        coeff_med.append(cm)
        color.append(col)

    medmap = np.ma.MaskedArray(medmap)
    coeff_med = np.ma.MaskedArray(coeff_med)
    cmed = np.ma.median(coeff_med, axis=0)

    med = np.ma.median(medmap, axis=0)
    rms = (medmap - med).std(axis=(-1, -2))

    return medmap, zerogmap, coeff_med, cmed, rms, color


def delta_phmap(
    maps,
    idx1: tuple,
    idx2: tuple,
    gain=None,
    filter_type=np.ma.mean,
):

    map1 = filter_type(maps[idx1[0] : idx1[1]], axis=0)
    map2 = filter_type(maps[idx2[0] : idx2[1]], axis=0)

    if gain is None:
        gain = np.ma.sum(map2 * map1) / np.ma.sum(map2 * map2)

    dmap = gain * map2 - map1

    return dmap
