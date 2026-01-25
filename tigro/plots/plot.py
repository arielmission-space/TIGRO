import itertools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.colorbar import Colorbar
from matplotlib.patches import Ellipse


figsize = (8, 8 / 1.618)


def plot_threshold(ncounts, lo, threshold, med, hi, outpath=None):
    fig = plt.figure(figsize=figsize)
    plt.plot(ncounts)
    plt.ylim(lo, hi)
    xlim = plt.xlim()
    plt.hlines([threshold, med], *xlim)
    plt.title("Check threshold by eye!!!")
    plt.grid(which="both", linestyle="--", alpha=0.5)

    if outpath is not None:
        plt.savefig(
            f"{outpath}/threshold.png",
            dpi=300,
            bbox_inches="tight",
        )

    return fig


def plot_sag_quicklook(
    phmap,
    imkey,
    imsubkey="rawmap",
    outpath=None,
):
    nkeys = len(phmap[imkey][imsubkey])
    ncols = 6
    nrows = int(np.ceil(nkeys / ncols))
    fig = plt.figure(figsize=(3 * ncols, 3 * nrows))

    vmin, vmax = [], []
    for i in range(nkeys):
        vmin = np.min(phmap[imkey][imsubkey][i])
        vmax = np.max(phmap[imkey][imsubkey][i])
    vmin = np.median(vmin) - 3 * np.std(vmin)
    vmax = np.median(vmax) + 3 * np.std(vmax)

    for i in range(nkeys):
        ax = fig.add_subplot(nrows, ncols, i + 1)
        if i < nkeys:
            im = ax.imshow(
                phmap[imkey][imsubkey][i],
                origin="lower",
                interpolation="none",
                zorder=0,
                alpha=1,
                cmap="Reds",
                vmin=vmin,
                vmax=vmax,
            )
            ax.set_title(f"Map {i+1}", fontsize=10)
            ax.set_xticks([])
            ax.set_yticks([])
        else:
            ax.axis("off")

    figname = phmap[imkey]["name"][0].split("_")
    figname = "_".join([figname[0]] + figname[2:])
    fig.suptitle(f"{figname}", fontsize=14)

    if outpath is not None:
        plt.savefig(
            f"{outpath}/{imkey}_{imsubkey}.png",
            dpi=300,
            bbox_inches="tight",
        )

    return fig


def plot_sag(
    phmap,
    uref,
    imkey,
    imsubkey="RegMap",
    outpath=None,
    vmin=None,
    vmax=None,
):
    fig = plt.figure(111, figsize=figsize)
    ax = fig.add_subplot(111)
    img = ax.imshow(
        phmap[imkey][imsubkey],
        origin="lower",
        interpolation="none",
        extent=uref["extent"],
        zorder=0,
        alpha=1,
        cmap="Reds",
        vmin=vmin,
        vmax=vmax,
    )

    bar = plt.colorbar(img)

    ellipse = Ellipse(
        xy=[0, 0],
        width=2,
        height=2 * uref["b"] / uref["a"],
        angle=0,
        edgecolor="c",
        lw=1,
        fc="none",
        label="pupil",
        ls="--",
        zorder=3,
    )
    ax.add_patch(ellipse)

    ax.arrow(-1, -0.75, 0.0, 0.1, head_width=0.05, label="+g", fc="r", color="r")
    ax.arrow(-0.90, -0.60, 0.0, -0.1, head_width=0.05, label="-g", fc="b", color="b")

    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)

    bar.set_label("Sag [nm]")
    figname = phmap[imkey]["name"][0].split("_")
    figname = "_".join([figname[0]] + figname[2:])
    ax.set_title(f"{figname}", fontsize=14)
    ax.legend(loc=1, fontsize=10)
    ax.grid(which="both", linestyle="--", alpha=0.5)

    if outpath is not None:
        plt.savefig(
            f"{outpath}/{imkey}_{imsubkey}.png",
            dpi=300,
            bbox_inches="tight",
        )

    return fig


def plot_allpolys(
    phmap,
    sequence_ids,
    sequence_ref,
    NZernike,
    colors,
    separator=40,
    ylim=None,
    outpath=None,
):
    fig = plt.figure(figsize=figsize)
    gs = GridSpec(4, 4)
    gs.update(left=0.08, right=0.90, bottom=0.12, top=0.95, wspace=0.1, hspace=0.04)

    ax0 = plt.subplot(gs[0:4, 0:3])
    ax1 = plt.subplot(gs[0:4, 3:])

    ipol = np.arange(5, NZernike + 1)
    for k, seq in enumerate(sequence_ids):
        ax0.plot(
            ipol + k / separator / 2,
            phmap[seq]["coeff"][4:] - phmap[sequence_ref]["coeff"][4:],
            "." + colors[k],
            markersize=5,
        )
        ax1.plot(
            seq,
            phmap[seq]["residual"].std(),
            "." + colors[k],
            markersize=5,
        )

    k = np.arange(5, NZernike + 1, 1)
    if ylim is None:
        ylim = ax0.get_ylim()
    ax0.vlines(k, *ylim, lw=0.5)
    ax0.set_xticks(k)
    ax0.set_ylim(*ylim)
    ax0.grid(which="both", linestyle="--", alpha=0.5)
    ax0.set_ylabel("Amplitude [nm]")
    ax0.set_xlabel("Poly order")

    ax1.set_ylabel("Residual RMS [nm]")
    ax1.set_xlabel("Sequence number")
    ax1.grid(which="both", linestyle="--", alpha=0.5)
    ax1.set_xticks(np.arange(sequence_ids[0], sequence_ids[-1], 4).astype(int))
    ax1.tick_params(axis="x", rotation=45)
    ax1.yaxis.tick_right()
    ax1.yaxis.set_label_position("right")

    if outpath is not None:
        plt.savefig(
            f"{outpath}/allpolys.png",
            dpi=300,
            bbox_inches="tight",
        )

    return fig


def plot_polys(
    phmap,
    sequence_ids,
    sequence_ref,
    poly_order=[5, 8],
    colors="rb",
    outpath=None,
):
    fig, ax0 = plt.subplots(1, 1, figsize=figsize)

    for seq, k in itertools.product(sequence_ids, poly_order):
        ax0.plot(
            seq,
            phmap[seq]["coeff"][k - 1] - phmap[sequence_ref]["coeff"][k - 1],
            "." + colors[poly_order.index(k)],
            markersize=10,
        )

    # plot the labels for the poly_order
    for k in poly_order:
        ax0.plot([], [], "." + colors[poly_order.index(k)], label="Poly {:d}".format(k))

    xlim = ax0.get_xlim()
    ylim = ax0.get_ylim()

    ax0.set_xlim(xlim)
    ax0.set_ylim(ylim)
    ax0.grid(which="both", linestyle="--", alpha=0.5)

    ax0.set_xlabel("Sequence")
    ax0.set_ylabel("Amplitude [nm]")

    ax0.legend()

    if outpath is not None:
        plt.savefig(
            f"{outpath}/polys.png",
            dpi=300,
            bbox_inches="tight",
        )

    return fig


def plot_zerog(
    coeff_med,
    cmed,
    rms,
    NZernike,
    color,
    ylim=(-50, 50),
    outpath=None,
):
    fig = plt.figure(figsize=figsize)
    gs = GridSpec(4, 4)
    gs.update(left=0.08, right=0.90, bottom=0.12, top=0.95, wspace=0.1, hspace=0.04)

    ax0 = plt.subplot(gs[0:4, 0:3])
    ax1 = plt.subplot(gs[0:4, 3:])

    nseq, npoly = coeff_med.shape
    for k, cseries in enumerate(coeff_med):
        ax0.plot(
            np.arange(cseries.size) + 1 + k / (nseq + 5), cseries - cmed, "x" + color[k]
        )

    ax0.set_xlim(4.9, npoly + 0.9)
    ax0.set_ylim(*ylim)
    ax0.grid(which="both", linestyle="--", alpha=0.5)
    ax0.set_ylabel("Amplitude [nm]")
    ax0.set_xlabel("Poly order")
    ax0.vlines(np.arange(5, NZernike + 1), *ylim, alpha=1, color="0.8")
    ax0.hlines([-5, 5], 0, NZernike + 1)

    ax1.plot(rms, "x")
    ax1.set_ylabel("RMS [nm]")
    ax1.set_xlabel("Sequence")
    ax1.grid(which="both", linestyle="--", alpha=0.5)
    ax1.set_xticks(np.arange(0, cseries.size + 1, 4).astype(int))
    ax1.yaxis.tick_right()
    ax1.yaxis.set_label_position("right")

    if outpath is not None:
        plt.savefig(
            f"{outpath}/zerog.png",
            dpi=300,
            bbox_inches="tight",
        )

    return fig


def plot_map(
    M,
    Mlim=[-50, 50],
    hlines=[240, 512],
    vlines=[512],
    hist_xlim=(-200, 200),
    hist_ylim=(-200, 200),
    title=None,
    outpath=None,
):
    fig = plt.figure(figsize=(8, 8))
    gs = GridSpec(3, 3, height_ratios=[0.05, 0.95, 0.2], width_ratios=[0.2, 0.95, 0.05])
    gs.update(left=0.03, right=0.85, bottom=0.03, top=0.85, wspace=0.04, hspace=0.04)

    ax0 = plt.subplot(gs[1, 1])
    ax1 = plt.subplot(gs[2, 1], sharex=ax0)
    ax2 = plt.subplot(gs[1, 0], sharey=ax0)

    ax1.set_xticklabels([])
    ax2.set_yticklabels([])
    ax2.xaxis.tick_top()

    im0 = ax0.imshow(M, origin="lower", cmap="Reds", vmin=Mlim[0], vmax=Mlim[1])

    cbax = plt.subplot(gs[1, 2])
    cb = Colorbar(
        ax=cbax,
        mappable=im0,
        orientation="vertical",
        ticklocation="right",
    )
    cb.set_label("Sag [nm]")

    ax0.hlines(hlines, 0, M.shape[1], "b")
    for hline in hlines:
        ax1.plot(np.arange(M.shape[1]), M[hline, :], "b")

    ax0.vlines(vlines, 0, M.shape[0], "r")
    for vline in vlines:
        ax2.plot(M[:, vline], np.arange(M.shape[0]), "r")

    ax0.set_ylim(0, M.shape[0])
    ax0.set_xlim(0, M.shape[1])
    ax0.grid(which="both", linestyle="--", alpha=0.5)

    ax1.set_ylim(*hist_ylim)
    ax1.grid(which="both", linestyle="--", alpha=0.5)

    ax2.set_xlim(*hist_xlim)
    ax2.grid(which="both", linestyle="--", alpha=0.5)

    # print((M10).std(), M20.std(), M.std(), gain)

    if title is not None:
        fig.suptitle(title, fontsize=20, y=0.93)

    if outpath is not None:
        plt.savefig(
            f"{outpath}/dphmap.png",
            dpi=300,
            bbox_inches="tight",
        )

    return fig
