from faicons import icon_svg

from shiny import ui

from tigro.ui.shared import output_text_verbatim
from tigro.ui.shared import ICONS
from tigro.ui.shared import card_header_class_


def app_elems(pp):
    system_sidebar_elems = [
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
            ],
            selected=pp.loglevel,
        ),
    ]

    system_quicklook_elems = [
        ui.card_header(
            "Quicklook",
            class_=card_header_class_,
        ),
        ui.card(
            ui.card_header(
                "RawMap",
                ui.popover(
                    ICONS["ellipsis"],
                    *[
                        ui.input_select(
                            "select_1_system",
                            "Map",
                            choices=list(pp.sequence_ids.astype(str)),
                        ),
                    ],
                    title="",
                    placement="top",
                ),
                class_=card_header_class_,
            ),
            ui.output_plot("plot_1_system", width="700px", height="550px", fill=True),
            ui.card_footer(
                ui.layout_columns(
                    ui.input_action_button(
                        "run_step1_system", "Load", icon=ICONS["run"]
                    ),
                    ui.input_action_button(
                        "do_plot_1_system", "Plot", icon=ICONS["run"]
                    ),
                    ui.input_action_button(
                        "download_plot_1_system", "Save", icon=ICONS["save"]
                    ),
                ),
            ),
            full_screen=True,
        ),
    ]

    cgvt_analysis_elems = [
        ui.card_header(
            "CGVt analysis",
            ui.popover(
                ICONS["ellipsis"],
                *[
                    ui.input_text(
                        "phmap_threshold",
                        "Phase map threshold",
                        value=pp.phmap_threshold,
                    ),
                    ui.input_text(
                        "phmap_filter_type",
                        "Phmap filter type",
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
                    ui.input_select(
                        "phmap_seq_ref",
                        "Reference sequence",
                        choices=list(pp.sequence_ids.astype(str)),
                        selected=pp.phmap_seq_ref,
                    ),
                    ui.input_text(
                        "n_zernike",
                        "Number of Zernike polynomials",
                        value=pp.n_zernike,
                    ),
                ],
                title="",
                placement="top",
            ),
            class_=card_header_class_,
        ),
        ui.card(
            ui.card(
                ui.card_header(
                    "1. Load",
                    ui.popover(
                        icon_svg("circle-info").add_class("ms-2"),
                        ui.markdown("blabla"),
                        placement="right",
                    ),
                ),
                ui.input_action_button("run_step1_cgvt", "Run", icon=ICONS["run"]),
                # output_text_verbatim("run_step1_cgvt_output"),
            ),
            ui.card(
                ui.card_header(
                    "2. Filter",
                    ui.popover(
                        icon_svg("circle-info").add_class("ms-2"),
                        ui.markdown("blabla"),
                        placement="right",
                    ),
                ),
                ui.input_action_button("run_step2_cgvt", "Run", icon=ICONS["run"]),
                # output_text_verbatim("run_step2_cgvt_output"),
            ),
            ui.card(
                ui.card_header(
                    "3. Threshold",
                    ui.popover(
                        icon_svg("circle-info").add_class("ms-2"),
                        ui.markdown("blabla"),
                        placement="right",
                    ),
                ),
                ui.input_action_button("run_step3_cgvt", "Run", icon=ICONS["run"]),
                # output_text_verbatim("run_step3_cgvt_output"),
            ),
            ui.card(
                ui.card_header(
                    "4. Average",
                    ui.popover(
                        icon_svg("circle-info").add_class("ms-2"),
                        ui.markdown("blabla"),
                        placement="right",
                    ),
                ),
                ui.input_action_button("run_step4_cgvt", "Run", icon=ICONS["run"]),
                # output_text_verbatim("run_step4_cgvt_output"),
            ),
            ui.card(
                ui.card_header(
                    "5. Fit ellipse",
                    ui.popover(
                        icon_svg("circle-info").add_class("ms-2"),
                        ui.markdown("blabla"),
                        placement="right",
                    ),
                ),
                ui.input_action_button("run_step5_cgvt", "Run", icon=ICONS["run"]),
                # output_text_verbatim("run_step5_cgvt_output"),
            ),
            ui.card(
                ui.card_header(
                    "6. Register",
                    ui.popover(
                        icon_svg("circle-info").add_class("ms-2"),
                        ui.markdown("blabla"),
                        placement="right",
                    ),
                ),
                ui.input_action_button("run_step6_cgvt", "Run", icon=ICONS["run"]),
                # output_text_verbatim("run_step6_cgvt_output"),
            ),
            ui.card(
                ui.card_header(
                    "7. Reference",
                    ui.popover(
                        icon_svg("circle-info").add_class("ms-2"),
                        ui.markdown("blabla"),
                        placement="right",
                    ),
                ),
                ui.input_action_button("run_step7_cgvt", "Run", icon=ICONS["run"]),
                # output_text_verbatim("run_step7_cgvt_output"),
            ),
            ui.card(
                ui.card_header(
                    "8. Zernike",
                    ui.popover(
                        icon_svg("circle-info").add_class("ms-2"),
                        ui.markdown("blabla"),
                        placement="right",
                    ),
                ),
                ui.input_action_button("run_step8_cgvt", "Run", icon=ICONS["run"]),
                # output_text_verbatim("run_step8_cgvt_output"),
            ),
        ),
        ui.card_footer(
            ui.layout_columns(
                ui.input_action_button("run_all_cgvt", "Run all", icon=ICONS["run"]),
                ui.input_action_button("download_phmap", "Save", icon=ICONS["save"]),
            ),
        ),
    ]

    cgvt_plots_elems = [
        ui.card_header(
            "CGVt plots",
            class_=card_header_class_,
        ),
        ui.card(
            ui.card(
                ui.card_header(
                    "Threshold",
                    ui.popover(
                        icon_svg("circle-info").add_class("ms-2"),
                        ui.markdown("blabla"),
                        placement="right",
                    ),
                    class_=card_header_class_,
                ),
                ui.output_plot("plot_0_cgvt", width="700px", height="550px", fill=True),
                ui.card_footer(
                    ui.layout_columns(
                        ui.input_action_button(
                            "do_plot_0_cgvt", "Plot", icon=ICONS["run"]
                        ),
                        ui.input_action_button(
                            "download_plot_0_cgvt", "Save", icon=ICONS["save"]
                        ),
                    ),
                ),
                full_screen=True,
            ),
            ui.card(
                ui.card_header(
                    "RegMap",
                    ui.popover(
                        icon_svg("circle-info").add_class("ms-2"),
                        ui.markdown("blabla"),
                        placement="right",
                    ),
                    ui.popover(
                        ICONS["ellipsis"],
                        *[
                            ui.input_select(
                                "plot_regmap_imkey",
                                "Map",
                                choices=list(pp.sequence_ids.astype(str)),
                                selected=pp.plot_regmap_imkey,
                            ),
                        ],
                        title="",
                        placement="top",
                    ),
                    class_=card_header_class_,
                ),
                ui.output_plot("plot_1_cgvt", width="700px", height="550px", fill=True),
                ui.card_footer(
                    ui.layout_columns(
                        ui.input_action_button(
                            "do_plot_1_cgvt", "Plot", icon=ICONS["run"]
                        ),
                        ui.input_action_button(
                            "download_plot_1_cgvt", "Save", icon=ICONS["save"]
                        ),
                    ),
                ),
                full_screen=True,
            ),
            ui.card(
                ui.card_header(
                    "RegMap-PTTF",
                    ui.popover(
                        icon_svg("circle-info").add_class("ms-2"),
                        ui.markdown("blabla"),
                        placement="right",
                    ),
                    ui.popover(
                        ICONS["ellipsis"],
                        *[
                            ui.input_select(
                                "plot_regmap_no_pttf_imkey",
                                "Map",
                                choices=list(pp.sequence_ids.astype(str)),
                                selected=pp.plot_regmap_no_pttf_imkey,
                            ),
                        ],
                        title="",
                        placement="top",
                    ),
                    class_=card_header_class_,
                ),
                ui.output_plot("plot_2_cgvt", width="700px", height="550px", fill=True),
                ui.card_footer(
                    ui.layout_columns(
                        ui.input_action_button(
                            "do_plot_2_cgvt", "Plot", icon=ICONS["run"]
                        ),
                        ui.input_action_button(
                            "download_plot_2_cgvt", "Save", icon=ICONS["save"]
                        ),
                    ),
                ),
                full_screen=True,
            ),
            ui.card(
                ui.card_header(
                    "Allpolys",
                    ui.popover(
                        icon_svg("circle-info").add_class("ms-2"),
                        ui.markdown("blabla"),
                        placement="right",
                    ),
                    ui.popover(
                        ICONS["ellipsis"],
                        *[
                            ui.input_select(
                                "plot_allpolys_seq_ref",
                                "Reference map",
                                choices=list(pp.sequence_ids.astype(str)),
                                selected=pp.plot_allpolys_seq_ref,
                            ),
                            ui.input_text(
                                "plot_allpolys_colors",
                                "Colors",
                                value=pp._plot_allpolys_colors,
                            ),
                        ],
                        title="",
                        placement="top",
                    ),
                    class_=card_header_class_,
                ),
                ui.output_plot("plot_3_cgvt", width="700px", height="550px", fill=True),
                ui.card_footer(
                    ui.layout_columns(
                        ui.input_action_button(
                            "do_plot_3_cgvt", "Plot", icon=ICONS["run"]
                        ),
                        ui.input_action_button(
                            "download_plot_3_cgvt", "Save", icon=ICONS["save"]
                        ),
                    ),
                ),
                full_screen=True,
            ),
            ui.card(
                ui.card_header(
                    "Polys",
                    ui.popover(
                        icon_svg("circle-info").add_class("ms-2"),
                        ui.markdown("blabla"),
                        placement="right",
                    ),
                    ui.popover(
                        ICONS["ellipsis"],
                        *[
                            ui.input_select(
                                "plot_polys_seq_ref",
                                "Reference map",
                                choices=list(pp.sequence_ids.astype(str)),
                                selected=pp.plot_polys_seq_ref,
                            ),
                            ui.input_text(
                                "plot_polys_order",
                                "Colors",
                                value=pp._plot_polys_order,
                            ),
                            ui.input_text(
                                "plot_polys_colors",
                                "Colors",
                                value=pp._plot_polys_colors,
                            ),
                        ],
                        title="",
                        placement="top",
                    ),
                    class_=card_header_class_,
                ),
                ui.output_plot("plot_4_cgvt", width="700px", height="550px", fill=True),
                ui.card_footer(
                    ui.layout_columns(
                        ui.input_action_button(
                            "do_plot_4_cgvt", "Plot", icon=ICONS["run"]
                        ),
                        ui.input_action_button(
                            "download_plot_4_cgvt", "Save", icon=ICONS["save"]
                        ),
                    ),
                ),
                full_screen=True,
            ),
        ),
        ui.card_footer(
            ui.layout_columns(
                ui.input_action_button("plot_all_cgvt", "Plot all", icon=ICONS["run"]),
                ui.input_action_button(
                    "download_all_plots_cgvt", "Save all", icon=ICONS["save"]
                ),
            ),
        ),
    ]

    zerog_analysis_elems = [
        ui.card_header(
            "ZeroG analysis",
            ui.popover(
                ICONS["ellipsis"],
                *[
                    ui.input_text(
                        "zerog_idx0",
                        "ZeroG index 0",
                        value=pp._zerog_idx0,
                    ),
                    ui.input_text(
                        "zerog_idx1",
                        "ZeroG index 1",
                        value=pp._zerog_idx1,
                    ),
                    ui.input_text(
                        "zerog_colors",
                        "ZeroG colors",
                        value=pp._zerog_colors,
                    ),
                    ui.input_text(
                        "dphmap_filter_type",
                        "Dphmap filter type",
                        value=pp._dphmap_filter_type,
                    ),
                    ui.input_text(
                        "dphmap_gain",
                        "Dphmap Gain",
                        value=pp.dphmap_gain,
                    ),
                    ui.input_text(
                        "dphmap_idx0",
                        "Dphmap index 0",
                        value=pp._dphmap_idx0,
                    ),
                    ui.input_text(
                        "dphmap_idx1",
                        "Dphmap index 1",
                        value=pp._dphmap_idx1,
                    ),
                ],
                title="",
                placement="top",
            ),
            class_=card_header_class_,
        ),
        ui.card(
            ui.card(
                ui.card_header(
                    "1. Load",
                    ui.popover(
                        icon_svg("circle-info").add_class("ms-2"),
                        ui.markdown("blabla"),
                        placement="right",
                    ),
                ),
                ui.input_action_button("run_step1_zerog", "Run", icon=ICONS["run"]),
                # output_text_verbatim("run_step1_zerog_output"),
            ),
            ui.card(
                ui.card_header(
                    "2. Get indices",
                    ui.popover(
                        icon_svg("circle-info").add_class("ms-2"),
                        ui.markdown("blabla"),
                        placement="right",
                    ),
                ),
                ui.input_action_button("run_step2_zerog", "Run", icon=ICONS["run"]),
                # output_text_verbatim("run_step2_zerog_output"),
            ),
            ui.card(
                ui.card_header(
                    "3. ZeroG",
                    ui.popover(
                        icon_svg("circle-info").add_class("ms-2"),
                        ui.markdown("blabla"),
                        placement="right",
                    ),
                ),
                ui.input_action_button("run_step3_zerog", "Run", icon=ICONS["run"]),
                # output_text_verbatim("run_step3_zerog_output"),
            ),
            ui.card(
                ui.card_header(
                    "4. Dphmap",
                    ui.popover(
                        icon_svg("circle-info").add_class("ms-2"),
                        ui.markdown("blabla"),
                        placement="right",
                    ),
                ),
                ui.input_action_button("run_step4_zerog", "Run", icon=ICONS["run"]),
                # output_text_verbatim("run_step4_zerog_output"),
            ),
        ),
        ui.card_footer(
            ui.layout_columns(
                ui.input_action_button("run_all_zerog", "Run all", icon=ICONS["run"]),
                ui.input_action_button("download_zerogmap", "Save", icon=ICONS["save"]),
            ),
        ),
    ]

    zerog_plots_elems = [
        ui.card_header(
            "ZeroG plots",
            class_=card_header_class_,
        ),
        ui.card(
            ui.card(
                ui.card_header(
                    "ZeroG",
                    ui.popover(
                        icon_svg("circle-info").add_class("ms-2"),
                        ui.markdown("blabla"),
                        placement="right",
                    ),
                    ui.popover(
                        ICONS["ellipsis"],
                        *[
                            ui.input_text(
                                "plot_zerog_ylim",
                                "Y limits",
                                value=pp._plot_zerog_ylim,
                            ),
                        ],
                        title="",
                        placement="top",
                    ),
                    class_=card_header_class_,
                ),
                ui.output_plot(
                    "plot_1_zerog", width="700px", height="550px", fill=True
                ),
                ui.card_footer(
                    ui.layout_columns(
                        ui.input_action_button(
                            "do_plot_1_zerog", "Plot", icon=ICONS["run"]
                        ),
                        ui.input_action_button(
                            "download_plot_1_zerog", "Save", icon=ICONS["save"]
                        ),
                    ),
                ),
                full_screen=True,
            ),
            ui.card(
                ui.card_header(
                    "Dphmap",
                    ui.popover(
                        icon_svg("circle-info").add_class("ms-2"),
                        ui.markdown("blabla"),
                        placement="right",
                    ),
                    ui.popover(
                        ICONS["ellipsis"],
                        *[
                            ui.input_text(
                                "plot_dphmap_hlines",
                                "Horizontal lines",
                                value=pp._plot_dphmap_hlines,
                            ),
                            ui.input_text(
                                "plot_dphmap_vlines",
                                "Vertical lines",
                                value=pp._plot_dphmap_vlines,
                            ),
                            ui.input_text(
                                "plot_dphmap_hist_xlim",
                                "Histogram: X limits",
                                value=pp._plot_dphmap_hist_xlim,
                            ),
                            ui.input_text(
                                "plot_dphmap_hist_ylim",
                                "Histogram: Y limits",
                                value=pp._plot_dphmap_hist_ylim,
                            ),
                        ],
                        title="",
                        placement="top",
                    ),
                    class_=card_header_class_,
                ),
                ui.output_plot(
                    "plot_2_zerog", width="700px", height="550px", fill=True
                ),
                ui.card_footer(
                    ui.layout_columns(
                        ui.input_action_button(
                            "do_plot_2_zerog", "Plot", icon=ICONS["run"]
                        ),
                        ui.input_action_button(
                            "download_plot_2_zerog", "Save", icon=ICONS["save"]
                        ),
                    ),
                ),
                full_screen=True,
            ),
        ),
        ui.card_footer(
            ui.layout_columns(
                ui.input_action_button("plot_all_zerog", "Plot all", icon=ICONS["run"]),
                ui.input_action_button(
                    "download_all_plots_zerog", "Save all", icon=ICONS["save"]
                ),
            ),
        ),
    ]

    return (
        system_sidebar_elems,
        system_quicklook_elems,
        cgvt_analysis_elems,
        cgvt_plots_elems,
        zerog_analysis_elems,
        zerog_plots_elems,
    )
