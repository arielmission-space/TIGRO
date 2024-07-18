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


def run(config_file):
    logger.info("Parsing configuration file")
    pp = Parser(config_file)

    logger.setLevel(pp.loglevel)

    if pp.run_cgvt:
        logger.info("Running CGVT")

        logger.info("Loading phase maps")
        phmap = load_phmap(pp.datapath, pp.sequence_ids)

        logger.info("Filtering phase maps")
        phmap = filter_phmap(phmap)

        logger.info("Getting threshold for outlier rejection")
        threshold = get_threshold(phmap)

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
            )

        if pp.save_pickle:
            logger.info("Saving results to pickle file")
            to_pickle(phmap, pp.outpath)

        if pp.plot_allpolys:
            logger.info("Plotting all polynomials")
            plot_allpolys(
                phmap,
                sequence_ids=pp.sequence_ids,
                sequence_ref=pp.plot_allpolys_seq_ref,
                NZernike=pp.n_zernike,
                colors=pp.plot_allpolys_colors,
            )

        if pp.plot_polys:
            logger.info("Plotting subset of polynomials vs. sequence")
            plot_polys(
                phmap,
                sequence_ids=pp.sequence_ids,
                sequence_ref=pp.plot_polys_seq_ref,
                poly_order=pp.plot_polys_order,
                colors=pp.plot_polys_colors,
            )
        
        logger.info("CGVT completed")

    if pp.run_zerog:
        logger.info("Running ZeroG")

        if not phmap:
            try:
                logger.info("Loading phase maps")
                phmap = from_pickle(pp.outpath)
            except FileNotFoundError:
                logger.error("File not found")
                return

        logger.info("Getting diff indices")
        diff_idx = get_diff_idx(
            pp.zerog_start_indices_pairs, pp.zerog_num_pairs, pp.zerog_colors
        )

        logger.info("ZeroG-ing phase maps")
        medmap, zerogmap, coeff_med, cmed, rms, color = zerog_phmap(phmap, diff_idx)

        if pp.plot_zerog:
            logger.info("Plotting ZeroG results")
            plot_zerog(
                coeff_med,
                cmed,
                rms,
                color,
                pp.plot_zerog_ylim,
            )

        logger.info("Computing delta phase map")
        dphmap = delta_phmap(
            zerogmap,
            idx0=pp.dphmap_idx[0],
            idx1=pp.dphmap_idx[1],
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
            )

        logger.info("ZeroG completed")