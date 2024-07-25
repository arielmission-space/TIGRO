from shiny import ui

from tigro.ui.shared import output_text_verbatim
from tigro.ui.shared import ICONS
from tigro.ui.shared import card_header_class_


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
            value=pp._sequence_ids,
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

    cgvt_sidebar_analysis_elems = [
        ui.input_text(
            "phmap_filter_type",
            "Filter type",
            value=pp._phmap_filter_type,
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

    cgvt_sidebar_plots_elems = [
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
            value=pp._plot_allpolys_colors,
        ),
        ui.input_text(
            "plot_polys_seq_ref",
            "Polynomials vs sequence: reference sequence",
            value=pp.plot_polys_seq_ref,
        ),
        ui.input_text(
            "plot_polys_order",
            "Polynomials vs sequence: order",
            value=pp._plot_polys_order,
        ),
        ui.input_text(
            "plot_polys_colors",
            "Polynomials vs sequence: colors",
            value=pp._plot_polys_colors,
        ),
    ]

    zerog_sidebar_analysis_elems = [
        ui.input_text(
            "zerog_idx0",
            "Zero-G index 0",
            value=pp._zerog_idx0,
        ),
        ui.input_text(
            "zerog_idx1",
            "Zero-G index 1",
            value=pp._zerog_idx1,
        ),
        ui.input_text(
            "zerog_colors",
            "Zero-G colors",
            value=pp._zerog_colors,
        ),
        ui.input_text(
            "dphmap_filter_type",
            "Filter type",
            value=pp._dphmap_filter_type,
        ),
        ui.input_text(
            "dphmap_gain",
            "Gain",
            value=pp.dphmap_gain,
        ),
        ui.input_text(
            "dphmap_idx0",
            "Differential phase map index 0",
            value=pp._dphmap_idx0,
        ),
        ui.input_text(
            "dphmap_idx1",
            "Differential phase map index 1",
            value=pp._dphmap_idx1,
        ),
    ]

    zerog_sidebar_plots_elems = [
        ui.input_text(
            "plot_zerog_ylim",
            "Zero-G: Y limits",
            value=pp._plot_zerog_ylim,
        ),
        ui.input_text(
            "plot_dphmap_hlines",
            "Differential phase map: horizontal lines",
            value=pp._plot_dphmap_hlines,
        ),
        ui.input_text(
            "plot_dphmap_vlines",
            "Differential phase map: vertical lines",
            value=pp._plot_dphmap_vlines,
        ),
        ui.input_text(
            "plot_dphmap_hist_xlim",
            "Differential phase map histogram: X limits",
            value=pp._plot_dphmap_hist_xlim,
        ),
        ui.input_text(
            "plot_dphmap_hist_ylim",
            "Differential phase map histogram: Y limits",
            value=pp._plot_dphmap_hist_ylim,
        ),
    ]

    cgvt_main_analysis_elems = [
        ui.card_header(
            "CGVt analysis",
                ui.popover(
                    ICONS["ellipsis"],
                    *[
                        ui.input_select(
                            id="cgvt_analysis_ellipsis",
                            label="Actions",
                            choices=[
                                "Load",
                                "Save",
                            ],
                            selected="Load",
                        ),
                    ],
                    title="",
                    placement="top",
                ),
            class_=card_header_class_,
        ),
        ui.card(
            ui.input_action_button("run_step1_cgvt", "Step 1", icon=ICONS["run"]),
            output_text_verbatim("run_step1_cgvt_output"),
            ui.input_action_button("run_step2_cgvt", "Step 2", icon=ICONS["run"]),
            output_text_verbatim("run_step2_cgvt_output"),
            ui.input_action_button("run_step3_cgvt", "Step 3", icon=ICONS["run"]),
            output_text_verbatim("run_step3_cgvt_output"),
        ),
        ui.card_footer(
            ui.layout_columns(
                ui.input_action_button("run_all_cgvt", "Run all", icon=ICONS["run"]),
                ui.input_action_button("download_phmap", "Download phmap", icon=ICONS["save"]),
            ),
        ),
    ]

    cgvt_main_plots_elems = [
        ui.card_header(
            "CGVt plots",
                ui.popover(
                    ICONS["ellipsis"],
                    *[
                        ui.input_select(
                            id="cgvt_plots_ellipsis",
                            label="Actions",
                            choices=[
                                "Load",
                                "Save",
                            ],
                            selected="Load",
                        ),
                    ],
                    title="",
                    placement="top",
                ),
            class_=card_header_class_,
        ),
        ui.card(
            ui.card(
                ui.output_plot("plot_1_cgvt"),
                ui.card_footer(
                    ui.layout_columns(
                        ui.input_action_button("do_plot_1_cgvt", "Plot 1", icon=ICONS["run"]),
                        ui.input_action_button("download_plot_1_cgvt", "Download plot 1", icon=ICONS["save"]),
                    ),
                ),
                full_screen=True,
            ),
            ui.card(
                ui.output_plot("plot_2_cgvt"),
                ui.card_footer(
                    ui.layout_columns(
                        ui.input_action_button("do_plot_2_cgvt", "Plot 2", icon=ICONS["run"]),
                        ui.input_action_button("download_plot_2_cgvt", "Download plot 2", icon=ICONS["save"]),
                    ),
                ),
                full_screen=True,
            ),
            ui.card(
                ui.output_plot("plot_3_cgvt"),
                ui.card_footer(
                    ui.layout_columns(
                        ui.input_action_button("do_plot_3_cgvt", "Plot 3", icon=ICONS["run"]),
                        ui.input_action_button("download_plot_3_cgvt", "Download plot 3", icon=ICONS["save"]),
                    ),
                ),
                full_screen=True,
            ),
        ),
        ui.card_footer(
            ui.layout_columns(
                ui.input_action_button("plot_all_cgvt", "Plot all", icon=ICONS["run"]),
                ui.input_action_button("download_all_plots_cgvt", "Download all plots", icon=ICONS["save"]),
            ),
        ),
    ]

    zerog_main_analysis_elems = [
        ui.card_header(
            "ZeroG analysis",
                ui.popover(
                    ICONS["ellipsis"],
                    *[
                        ui.input_select(
                            id="zerog_analysis_ellipsis",
                            label="Actions",
                            choices=[
                                "Load",
                                "Save",
                            ],
                            selected="Load",
                        ),
                    ],
                    title="",
                    placement="top",
                ),
            class_=card_header_class_,
        ),
        ui.card(
            ui.input_action_button("run_step1_zerog", "Step 1", icon=ICONS["run"]),
            output_text_verbatim("run_step1_zerog_output"),
            ui.input_action_button("run_step2_zerog", "Step 2", icon=ICONS["run"]),
            output_text_verbatim("run_step2_zerog_output"),
            ui.input_action_button("run_step3_zerog", "Step 3", icon=ICONS["run"]),
            output_text_verbatim("run_step3_zerog_output"),
        ),
        ui.card_footer(
            ui.layout_columns(
                ui.input_action_button("run_all_zerog", "Run all", icon=ICONS["run"]),
                ui.input_action_button("download_zerogmap", "Download ZeroG map", icon=ICONS["save"]),
            ),
        ),
    ]

    zerog_main_plots_elems = [
        ui.card_header(
            "ZeroG plots",
                ui.popover(
                    ICONS["ellipsis"],
                    *[
                        ui.input_select(
                            id="zerog_plots_ellipsis",
                            label="Actions",
                            choices=[
                                "Load",
                                "Save",
                            ],
                            selected="Load",
                        ),
                    ],
                    title="",
                    placement="top",
                ),
            class_=card_header_class_,
        ),
        ui.card(
            ui.card(
                ui.output_plot("plot_1_zerog"),
                ui.card_footer(
                    ui.layout_columns(
                        ui.input_action_button("do_plot_1_zerog", "Plot 1", icon=ICONS["run"]),
                        ui.input_action_button("download_plot_1_zerog", "Download plot 1", icon=ICONS["save"]),
                    ),
                ),
                full_screen=True,
            ),
            ui.card(
                ui.output_plot("plot_2_zerog"),
                ui.card_footer(
                    ui.layout_columns(
                        ui.input_action_button("do_plot_2_zerog", "Plot 2", icon=ICONS["run"]),
                        ui.input_action_button("download_plot_2_zerog", "Download plot 2", icon=ICONS["save"]),
                    ),
                ),
                full_screen=True,
            ),
            ui.card(
                ui.output_plot("plot_3_zerog"),
                ui.card_footer(
                    ui.layout_columns(
                        ui.input_action_button("do_plot_3_zerog", "Plot 3", icon=ICONS["run"]),
                        ui.input_action_button("download_plot_3_zerog", "Download plot 3", icon=ICONS["save"]),
                    ),
                ),
                full_screen=True,
            ),
        ),
        ui.card_footer(
            ui.layout_columns(
                ui.input_action_button("plot_all_zerog", "Plot all", icon=ICONS["run"]),
                ui.input_action_button("download_all_plots_zerog", "Download all plots", icon=ICONS["save"]),
            ),
        ),
    ]

    return (
        general_elems,
        cgvt_sidebar_analysis_elems,
        cgvt_sidebar_plots_elems,
        cgvt_main_analysis_elems,
        cgvt_main_plots_elems,
        zerog_sidebar_analysis_elems,
        zerog_sidebar_plots_elems,
        zerog_main_analysis_elems,
        zerog_main_plots_elems,
    )
