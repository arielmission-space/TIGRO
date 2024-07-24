from shiny import ui


def app_elems(pp):
    general_elems = [
        ui.input_text(
            "project",
            "Project name",
            value=pp.project,
        ),
        ui.input_text(
            "comment",
            "Comment",
            value=pp.comment,
        ),
        ui.input_text(
            "version",
            "Version",
            value=pp.version,
        ),
        ui.input_text(
            "datapath",
            "Data path",
            value=pp.datapath,
        ),
        ui.input_text(
            "sequence_ids",
            "Sequence IDs",
            value=pp.sequence_ids_config,
        ),
        ui.input_text(
            "n_zernike",
            "Number of Zernike polynomials",
            value=pp.n_zernike,
        ),
        ui.input_checkbox(
            "store_phmap",
            "Store phase map",
            value=pp.store_phmap,
        ),
        ui.input_text(
            "fname_phmap",
            "Phase map file name",
            value=pp.fname_phmap,
        ),
        ui.input_select(
            "loglevel",
            "Log level",
            choices=[
                "DEBUG",
                "INFO",
                "WARNING",
                "ERROR",
                "CRITICAL",
            ],
            selected=pp.loglevel,
        ),
    ]

    cgvt_analysis_elems = [
        ui.input_text(
            "phmap_filter_type",
            "Filter type",
            value=pp.phmap_filter_type_config,
        ),
        ui.input_text(
            "phmap_semi_major",
            "Semi-major axis",
            value=pp.phmap_semi_major,
        ),
        ui.input_text(
            "phmap_semi_minor",
            "Semi-minor axis",
            value=pp.phmap_semi_minor,
        ),
        ui.input_text(
            "phmap_seq_ref",
            "Reference sequence",
            value=pp.phmap_seq_ref,
        ),
    ]

    cgvt_plots_elems = [
        ui.input_text(
            "plot_regmap_imkey",
            "Registered map image key",
            value=pp.plot_regmap_imkey,
        ),
        ui.input_text(
            "plot_regmap_no_pttf_imkey",
            "Registered map without PTTF image key",
            value=pp.plot_regmap_no_pttf_imkey,
        ),
        ui.input_text(
            "plot_allpolys_seq_ref",
            "All polynomials: reference sequence",
            value=pp.plot_allpolys_seq_ref,
        ),
        ui.input_text(
            "plot_allpolys_colors",
            "All polynomials: colors",
            value=pp.plot_allpolys_colors_config,
        ),
        ui.input_text(
            "plot_polys_seq_ref",
            "Polynomials vs sequence: reference sequence",
            value=pp.plot_polys_seq_ref,
        ),
        ui.input_text(
            "plot_polys_order",
            "Polynomials vs sequence: order",
            value=pp.plot_polys_order_config,
        ),
        ui.input_text(
            "plot_polys_colors",
            "Polynomials vs sequence: colors",
            value=pp.plot_polys_colors_config,
        ),
    ]

    zerog_analysis_elems = [
        ui.input_text(
            "zerog_idx0",
            "Zero-G index 0",
            value=pp.zerog_idx0_config,
        ),
        ui.input_text(
            "zerog_idx1",
            "Zero-G index 1",
            value=pp.zerog_idx1_config,
        ),
        ui.input_text(
            "zerog_colors",
            "Zero-G colors",
            value=pp.zerog_colors_config,
        ),
        ui.input_text(
            "dphmap_filter_type",
            "Filter type",
            value=pp.dphmap_filter_type_config,
        ),
        ui.input_text(
            "dphmap_gain",
            "Gain",
            value=pp.dphmap_gain,
        ),
        ui.input_text(
            "dphmap_idx0",
            "Differential phase map index 0",
            value=pp.dphmap_idx0_config,
        ),
        ui.input_text(
            "dphmap_idx1",
            "Differential phase map index 1",
            value=pp.dphmap_idx1_config,
        ),
    ]

    zerog_plots_elems = [
        ui.input_text(
            "plot_zerog_ylim",
            "Zero-G: Y limits",
            value=pp.plot_zerog_ylim_config,
        ),
        ui.input_text(
            "plot_dphmap_hlines",
            "Differential phase map: horizontal lines",
            value=pp.plot_dphmap_hlines_config,
        ),
        ui.input_text(
            "plot_dphmap_vlines",
            "Differential phase map: vertical lines",
            value=pp.plot_dphmap_vlines_config,
        ),
        ui.input_text(
            "plot_dphmap_hist_xlim",
            "Differential phase map histogram: X limits",
            value=pp.plot_dphmap_hist_xlim_config,
        ),
        ui.input_text(
            "plot_dphmap_hist_ylim",
            "Differential phase map histogram: Y limits",
            value=pp.plot_dphmap_hist_ylim_config,
        ),
    ]

    return (
        general_elems,
        cgvt_analysis_elems,
        cgvt_plots_elems,
        zerog_analysis_elems,
        zerog_plots_elems,
    )
