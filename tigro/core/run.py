from tigro.classes.parser import Parser

from tigro.io.load import load_phmap
from tigro.core.process import filter_phmap
from tigro.utils.util import get_threshold
from tigro.core.process import med_phmap
from tigro.core.fit import fit_ellipse
from tigro.core.process import register_phmap
from tigro.utils.util import get_uref
from tigro.plots.plot import plot_sag
from tigro.core.fit import fit_zernike
from tigro.io.save import to_pickle
from tigro.plots.plot import plot_allpolys
from tigro.plots.plot import plot_polys
from tigro.io.load import from_pickle
from tigro.utils.util import get_diff_idx
from tigro.core.process import zerog_phmap
from tigro.plots.plot import plot_zerog
from tigro.core.process import delta_phmap
from tigro.plots.plot import plot_map

from tigro import logger


def run_cgvt(pp):
    if not pp.run_cgvt:
        return

    logger.info("Running CGVT")

    logger.info("Loading phase maps")
    phmap = load_phmap(pp.datapath, pp.sequence_ids)

    logger.info("Filtering phase maps")
    phmap = filter_phmap(phmap)

    logger.info("Getting threshold for outlier rejection")
    threshold = get_threshold(phmap, pp.phmap_threshold)

    logger.info("Computing median map and supermask")
    phmap = med_phmap(
        phmap,
        threshold,
        filter_type=pp.phmap_filter_type,
    )

    logger.info("Fitting ellipse to phase maps")
    phmap = fit_ellipse(phmap)

    logger.info("Registering phase maps")
    phmap = register_phmap(phmap)

    logger.info("Getting reference map")
    uref = get_uref(
        phmap,
        pp.phmap_semi_major,
        pp.phmap_semi_minor,
        pp.phmap_seq_ref,
    )

    if pp.plot_regmap:
        logger.info("Plotting sag of registered phase map")
        plot_sag(
            phmap,
            uref,
            imkey=pp.plot_regmap_imkey,
            imsubkey="RegMap",
            outpath=pp.outpath,
        )

    logger.info("Fitting Zernike orthonormal polynomials")
    phmap = fit_zernike(
        phmap,
        uref,
        NZernike=pp.n_zernike,
    )

    if pp.plot_regmap_no_pttf:
        logger.info(
            "Plotting sag of registered phase map, minus the Piston, Tip, Tilts and Defocus"
        )
        plot_sag(
            phmap,
            uref,
            imkey=pp.plot_regmap_no_pttf_imkey,
            imsubkey="RegMap-PTTF",
            outpath=pp.outpath,
        )

    if pp.store_phmap:
        logger.info("Saving results to pickle file")
        to_pickle(phmap, pp.fname_phmap)

    if pp.plot_allpolys:
        logger.info("Plotting all polynomials")
        plot_allpolys(
            phmap,
            sequence_ids=pp.sequence_ids,
            sequence_ref=pp.plot_allpolys_seq_ref,
            NZernike=pp.n_zernike,
            colors=pp.plot_allpolys_colors,
            outpath=pp.outpath,
        )

    if pp.plot_polys:
        logger.info("Plotting subset of polynomials vs. sequence")
        plot_polys(
            phmap,
            sequence_ids=pp.sequence_ids,
            sequence_ref=pp.plot_polys_seq_ref,
            poly_order=pp.plot_polys_order,
            colors=pp.plot_polys_colors,
            outpath=pp.outpath,
        )

    logger.info("CGVT completed")

    return phmap


def run_zerog(pp, phmap=None):
    if not pp.run_zerog:
        return

    logger.info("Running ZeroG")

    if not phmap:
        try:
            logger.info("Loading phase maps")
            phmap = from_pickle(pp.fname_phmap)
        except FileNotFoundError:
            logger.error("File not found")
            return

    logger.info("Getting diff indices")
    diff_idx = get_diff_idx(pp.idx_gplus, pp.idx_gminus, pp.zerog_colors)

    logger.info("ZeroG-ing phase maps")
    medmap, zerogmap, coeff_med, cmed, rms, color = zerog_phmap(phmap, diff_idx)

    if pp.plot_zerog:
        logger.info("Plotting ZeroG results")
        plot_zerog(
            coeff_med=coeff_med,
            cmed=cmed,
            rms=rms,
            NZernike=pp.n_zernike,
            color=color,
            ylim=pp.plot_zerog_ylim,
            outpath=pp.outpath,
        )

    logger.info("Computing delta phase map")
    dphmap = delta_phmap(
        zerogmap,
        idx0=pp.dphmap0_idx,
        idx1=pp.dphmap1_idx,
        gain=pp.dphmap_gain,
        filter_type=pp.dphmap_filter_type,
    )

    if pp.plot_dphmap:
        logger.info("Plotting delta phase map")

        plot_map(
            dphmap,
            hlines=pp.plot_dphmap_hlines,
            vlines=pp.plot_dphmap_vlines,
            hist_xlim=pp.plot_dphmap_hist_xlim,
            hist_ylim=pp.plot_dphmap_hist_ylim,
            outpath=pp.outpath,
        )

    logger.info("ZeroG completed")


def run(config, outpath):
    logger.info("Parsing configuration file")
    pp = Parser(config, outpath)

    logger.setLevel(pp.loglevel)

    phmap = run_cgvt(pp)

    run_zerog(pp, phmap)
