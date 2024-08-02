import itertools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
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
    fig = plt.figure(figsize=figsize)

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
    outpath=None,
):
    fig, ax0 = plt.subplots(1, 1, figsize=figsize)

    ipol = np.arange(5, NZernike + 1)
    for k, seq in enumerate(sequence_ids):
        ax0.plot(
            ipol + k / 20 / 2,
            phmap[seq]["coeff"][4:] - phmap[sequence_ref]["coeff"][4:],
            "." + colors[k],
            markersize=10,
        )

    k = np.arange(5, 16, 1)
    ylim = ax0.get_ylim()
    ax0.vlines(k, *ylim)
    # set xticklabels
    ax0.set_xticks(k)
    ax0.set_ylim(*ylim)
    ax0.grid(which="both", linestyle="--", alpha=0.5)
    ax0.set_ylabel("Amplitude [nm]")
    ax0.set_xlabel("Poly order")

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
            phmap[seq]["coeff"][k] - phmap[sequence_ref]["coeff"][k],
            "." + colors[poly_order.index(k)],
            markersize=10,
        )

    # plot the labels for the poly_order
    for k in poly_order:
        ax0.plot([], [], "." + colors[poly_order.index(k)], label="Poly {:d}".format(k))

    xlim = ax0.get_xlim()
    ylim = ax0.get_ylim()

    ax0.vlines(
        np.arange(xlim[0], xlim[1]), *ylim, color="0.5", lw=1, ls="-.", alpha=0.5
    )
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
    color,
    ylim=(-50, 50),
    outpath=None,
):
    fig = plt.figure(123, figsize=figsize)
    gs = GridSpec(4, 4, figure=fig)
    ax = fig.add_subplot(gs[0:4, 0:3])
    fig.subplots_adjust(wspace=0.5)

    nseq, npoly = coeff_med.shape
    for k, cseries in enumerate(coeff_med):
        ax.plot(
            np.arange(cseries.size) + 1 + k / (nseq + 5), cseries - cmed, "x" + color[k]
        )

    ax.set_xlim(4.9, npoly + 0.9)
    ax.set_ylim(*ylim)
    ax.grid(which="both", linestyle="--", alpha=0.5)
    ax.set_ylabel("Amplitude [nm]")
    ax.set_xlabel("Poly order")
    ax.vlines(np.arange(5, 16), *ylim, alpha=1, color="0.8")
    ax.hlines([-5, 5], 0, 16)

    ax = fig.add_subplot(gs[0:4, 3:])
    ax.plot(rms, "x")
    ax.set_ylabel("RMS [nm]")
    ax.set_xlabel("Sequence")

    if outpath is not None:
        plt.savefig(
            f"{outpath}/zerog.png",
            dpi=300,
            bbox_inches="tight",
        )

    return fig


def plot_map(
    M,
    hlines=[240, 512],
    vlines=[512],
    hist_xlim=(-200, 200),
    hist_ylim=(-200, 200),
    outpath=None,
):
    fig = plt.figure(figsize=figsize)
    gs = fig.add_gridspec(
        6,
        6,  # width_ratios=(4, 1, 1), height_ratios=(1, 4),
        left=0.1,
        right=0.9,
        bottom=0.1,
        top=0.9,
        wspace=0.05,
        hspace=0.05,
    )

    ax0 = fig.add_subplot(gs[2:, 0:3])
    ax1 = fig.add_subplot(gs[1, 0:3], sharex=ax0)
    ax2 = fig.add_subplot(gs[2:, 3], sharey=ax0)

    ax1.set_xticklabels("")
    ax2.set_yticklabels("")

    im0 = ax0.imshow(M, origin="lower", vmin=-50, vmax=50, cmap="Reds")
    plt.colorbar(im0, ax=ax2)

    ax0.hlines(hlines, 0, M.shape[1], "b")
    for hline in hlines:
        ax1.plot(np.arange(M.shape[1]), M[hline, :], "b")

    ax0.vlines(vlines, 0, M.shape[0], "r")
    for vline in vlines:
        ax2.plot(M[:, vline], np.arange(M.shape[0]), "r")

    ax0.set_ylim(0, M.shape[0])
    ax0.set_xlim(0, M.shape[1])
    ax1.set_ylim(*hist_ylim)
    ax2.set_xlim(*hist_xlim)
    # print((M10).std(), M20.std(), M.std(), gain)

    if outpath is not None:
        plt.savefig(
            f"{outpath}/dphmap.png",
            dpi=300,
            bbox_inches="tight",
        )

    return fig
