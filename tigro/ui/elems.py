from shiny import ui

from tigro.ui.shared import ICONS
from tigro.ui.shared import card_header_class_
from tigro.ui.shared import hline
from tigro.ui.shared import vline


def step_card(id, label, text="blabla", width="80%"):
    return ui.tags.div(
        ui.input_action_button(
            id,
            label,
            icon=ICONS["run"],
            class_="ms-2",
            width=width,
        ),
        ui.popover(
            ICONS["info"].add_class("ms-2"),
            ui.markdown(text),
            title="Info",
            placement="right",
        ),
    )


def plot_card(
    id,
    interactive=False,
    width="100%",
    height="550px",
):
    if interactive:
        out = ui.output_ui(
            id,
            width=width,
            height=height,
            fill=True,
        )
    else:
        out = ui.output_plot(
            id,
            width=width,
            height=height,
            fill=True,
        )

    return [
        ui.layout_columns(
            out,
            vline,
            [
                ui.input_action_button(f"do_{id}", "Plot", icon=ICONS["run"]),
                ui.input_action_button(f"download_{id}", "Save", icon=ICONS["save"]),
            ],
            col_widths=(9, 1, 2),
        ),
    ]


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
            "outpath",
            "Output path",
            value=pp.outpath,
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
            ui.markdown(
                """
                    ##### Quicklook
                """
            ),
            step_card("run_step1_system", "1. Load", width=None),
            class_=card_header_class_,
        ),
        ui.card(
            ui.card_header(
                "RawMap",
                ui.popover(
                    ICONS["info"].add_class("ms-2"),
                    ui.markdown("blabla"),
                    title="Info",
                    placement="right",
                ),
                ui.popover(
                    ICONS["gear"],
                    *[
                        ui.input_select(
                            "select_1_system",
                            "Map",
                            choices=list(pp.sequence_ids.astype(str)),
                        ),
                    ],
                    title="Options",
                    placement="top",
                ),
                class_=card_header_class_,
            ),
            plot_card("plot_1_system"),
            full_screen=True,
        ),
    ]

    cgvt_analysis_elems = [
        ui.card_header(
            ui.tags.div(
                ui.input_action_button("run_all_cgvt", "Run all", icon=ICONS["run"]),
                ui.input_action_button("download_phmap", "Save", icon=ICONS["save"]),
            ),
            ui.popover(
                ICONS["gear"],
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
                title="Options",
                placement="top",
            ),
            class_=card_header_class_,
        ),
        hline,
        ui.card(
            step_card("run_step1_cgvt", "1. Load"),
            step_card("run_step2_cgvt", "2. Filter"),
            step_card("run_step3_cgvt", "3. Threshold"),
            step_card("run_step4_cgvt", "4. Average"),
            step_card("run_step5_cgvt", "5. Fit ellipse"),
            step_card("run_step6_cgvt", "6. Register"),
            step_card("run_step7_cgvt", "7. Reference"),
            step_card("run_step8_cgvt", "8. Zernike"),
        ),
    ]

    cgvt_plots_elems = [
        ui.card_header(
            ui.markdown(
                """
                    ##### CGVt Plots
                """
            ),
            ui.tags.div(
                ui.input_action_button("plot_all_cgvt", "Plot all", icon=ICONS["run"]),
                ui.input_action_button(
                    "download_all_plots_cgvt", "Save all", icon=ICONS["save"]
                ),
            ),
            class_=card_header_class_,
        ),
        ui.tags.div(style="height: 5px;"),
        ui.navset_card_pill(
            ui.nav_panel(
                "Threshold",
                ui.card(
                    ui.card_header(
                        "Threshold",
                        ui.popover(
                            ICONS["info"].add_class("ms-2"),
                            ui.markdown("blabla"),
                            title="Info",
                            placement="right",
                        ),
                        ui.popover(
                            ICONS["gear"],
                            *[
                                ui.p(""),
                            ],
                            title="Options",
                            placement="top",
                        ),
                        class_=card_header_class_,
                    ),
                    plot_card("plot_1_cgvt", interactive=True),
                    full_screen=True,
                ),
            ),
            ui.nav_panel(
                "RegMap",
                ui.card(
                    ui.card_header(
                        "RegMap",
                        ui.popover(
                            ICONS["info"].add_class("ms-2"),
                            ui.markdown("blabla"),
                            title="Info",
                            placement="right",
                        ),
                        ui.popover(
                            ICONS["gear"],
                            *[
                                ui.input_select(
                                    "plot_regmap_imkey",
                                    "Map",
                                    choices=list(pp.sequence_ids.astype(str)),
                                    selected=pp.plot_regmap_imkey,
                                ),
                            ],
                            title="Options",
                            placement="top",
                        ),
                        class_=card_header_class_,
                    ),
                    plot_card("plot_2_cgvt", interactive=True),
                    full_screen=True,
                ),
            ),
            ui.nav_panel(
                "RegMap-PTTF",
                ui.card(
                    ui.card_header(
                        "RegMap-PTTF",
                        ui.popover(
                            ICONS["info"].add_class("ms-2"),
                            ui.markdown("blabla"),
                            title="Info",
                            placement="right",
                        ),
                        ui.popover(
                            ICONS["gear"],
                            *[
                                ui.input_select(
                                    "plot_regmap_no_pttf_imkey",
                                    "Map",
                                    choices=list(pp.sequence_ids.astype(str)),
                                    selected=pp.plot_regmap_no_pttf_imkey,
                                ),
                            ],
                            title="Options",
                            placement="top",
                        ),
                        class_=card_header_class_,
                    ),
                    plot_card("plot_3_cgvt", interactive=True),
                    full_screen=True,
                ),
            ),
            ui.nav_panel(
                "Allpolys",
                ui.card(
                    ui.card_header(
                        "Allpolys",
                        ui.popover(
                            ICONS["info"].add_class("ms-2"),
                            ui.markdown("blabla"),
                            title="Info",
                            placement="right",
                        ),
                        ui.popover(
                            ICONS["gear"],
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
                            title="Options",
                            placement="top",
                        ),
                        class_=card_header_class_,
                    ),
                    plot_card("plot_4_cgvt", interactive=True),
                    full_screen=True,
                ),
            ),
            ui.nav_panel(
                "Polys",
                ui.card(
                    ui.card_header(
                        "Polys",
                        ui.popover(
                            ICONS["info"].add_class("ms-2"),
                            ui.markdown("blabla"),
                            title="Info",
                            placement="right",
                        ),
                        ui.popover(
                            ICONS["gear"],
                            *[
                                ui.input_select(
                                    "plot_polys_seq_ref",
                                    "Reference map",
                                    choices=list(pp.sequence_ids.astype(str)),
                                    selected=pp.plot_polys_seq_ref,
                                ),
                                ui.input_text(
                                    "plot_polys_order",
                                    "Orders",
                                    value=pp._plot_polys_order,
                                ),
                                ui.input_text(
                                    "plot_polys_colors",
                                    "Colors",
                                    value=pp._plot_polys_colors,
                                ),
                            ],
                            title="Options",
                            placement="top",
                        ),
                        class_=card_header_class_,
                    ),
                    plot_card("plot_5_cgvt", interactive=True),
                    full_screen=True,
                ),
            ),
        ),
    ]

    zerog_analysis_elems = [
        ui.card_header(
            ui.tags.div(
                ui.input_action_button("run_all_zerog", "Run all", icon=ICONS["run"]),
            ),
            ui.popover(
                ICONS["gear"],
                *[
                    ui.input_text(
                        "idx_gplus",
                        "+g sequences",
                        value=pp._idx_gplus,
                    ),
                    ui.input_text(
                        "idx_gminus",
                        "-g sequences",
                        value=pp._idx_gminus,
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
                        "dphmap0_idx",
                        "Dphmap 0 index",
                        value=pp._dphmap0_idx,
                    ),
                    ui.input_text(
                        "dphmap1_idx",
                        "Dphmap 1 index",
                        value=pp._dphmap1_idx,
                    ),
                ],
                title="Options",
                placement="top",
            ),
            class_=card_header_class_,
        ),
        hline,
        ui.card(
            step_card("run_step1_zerog", "1. Load"),
            step_card("run_step2_zerog", "2. Get indices"),
            step_card("run_step3_zerog", "3. ZeroG"),
            step_card("run_step4_zerog", "4. Dphmap"),
        ),
    ]

    zerog_plots_elems = [
        ui.card_header(
            ui.markdown(
                """
                    ##### ZeroG Plots
                """
            ),
            ui.tags.div(
                ui.input_action_button("plot_all_zerog", "Plot all", icon=ICONS["run"]),
                ui.input_action_button(
                    "download_all_plots_zerog", "Save all", icon=ICONS["save"]
                ),
            ),
            class_=card_header_class_,
        ),
        ui.tags.div(style="height: 5px;"),
        ui.navset_card_pill(
            ui.nav_panel(
                "ZeroG",
                ui.card(
                    ui.card_header(
                        "ZeroG",
                        ui.popover(
                            ICONS["info"].add_class("ms-2"),
                            ui.markdown("blabla"),
                            title="Info",
                            placement="right",
                        ),
                        ui.popover(
                            ICONS["gear"],
                            *[
                                ui.input_text(
                                    "plot_zerog_ylim",
                                    "Y limits",
                                    value=pp._plot_zerog_ylim,
                                ),
                            ],
                            title="Options",
                            placement="top",
                        ),
                        class_=card_header_class_,
                    ),
                    plot_card("plot_1_zerog", interactive=True),
                    full_screen=True,
                ),
            ),
            ui.nav_panel(
                "Dphmap",
                ui.card(
                    ui.card_header(
                        "Dphmap",
                        ui.popover(
                            ICONS["info"].add_class("ms-2"),
                            ui.markdown("blabla"),
                            title="Info",
                            placement="right",
                        ),
                        ui.popover(
                            ICONS["gear"],
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
                            title="Options",
                            placement="top",
                        ),
                        class_=card_header_class_,
                    ),
                    plot_card("plot_2_zerog"),
                    full_screen=True,
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
