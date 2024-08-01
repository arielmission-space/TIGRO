import os
import time

import matplotlib.pyplot as plt

from htmltools import Tag
from starlette.requests import Request as StarletteRequest
from shiny import App
from shiny import ui
from shiny import reactive
from shiny import render
from shiny import req
from shiny.types import FileInfo

from tigro import __author__
from tigro import __version__
from tigro import __license__

from tigro.classes.parser import Parser
from tigro.io.load import load_phmap
from tigro.core.process import filter_phmap
from tigro.utils.util import get_threshold
from tigro.core.process import med_phmap
from tigro.core.fit import fit_ellipse
from tigro.core.process import register_phmap
from tigro.utils.util import get_uref
from tigro.core.fit import calculate_zernike
from tigro.core.fit import fit_zernike
from tigro.io.save import to_pickle

from tigro.plots.plot import plot_sag_quicklook
from tigro.plots.plot import plot_threshold
from tigro.plots.plot import plot_sag
from tigro.plots.plot import plot_allpolys
from tigro.plots.plot import plot_polys

from tigro.ui.items import menu_items
from tigro.ui.items import system_sidebar
from tigro.ui.elems import app_elems
from tigro.ui.shared import refresh_ui
from tigro.ui.shared import nested_div
from tigro.ui.shared import modal_download
from tigro.ui.shared import ICONS
from tigro.ui.io import update_ini

plt.style.use("default")


def app_ui(request: StarletteRequest) -> Tag:
    return ui.page_navbar(
        ui.nav_spacer(),
        *menu_items,
        ui.nav_spacer(),
        ui.nav_panel(
            "System",
            ui.layout_sidebar(
                ui.sidebar(
                    ui.accordion(*system_sidebar, open=False),
                    width=350,
                ),
                ui.card(
                    nested_div("system_quicklook"),
                    full_screen=True,
                ),
            ),
        ),
        ui.nav_panel(
            "CGVt",
            ui.layout_columns(
                ui.card(nested_div("cgvt_analysis"), full_screen=True),
                ui.card(nested_div("cgvt_plots"), full_screen=True),
                col_widths=(3, 9),
            ),
        ),
        ui.nav_panel(
            "ZeroG",
            ui.layout_columns(
                ui.card(nested_div("zerog_analysis"), full_screen=True),
                ui.card(nested_div("zerog_plots"), full_screen=True),
                col_widths=(3, 9),
            ),
        ),
        # fillable="TIGRO UI",
        id="navbar",
        title=ui.tags.div(
            ui.popover(
                [
                    "TIGRO UI",
                    ICONS["info"].add_class("ms-2"),
                ],
                ui.markdown("blabla"),
                placement="right",
            ),
            ui.input_action_button("refresh", "", icon=ICONS["refresh"], class_="ms-2"),
        ),
        window_title="TIGRO UI",
        # selected="System",
    )


def server(input, output, session):
    config = reactive.value("config")
    pp = reactive.value({})
    phmap = reactive.value({})
    figure_quicklook = reactive.value(None)
    threshold = reactive.value(None)
    uref = reactive.value(None)
    figure_threshold = reactive.value(None)
    figure_regmap = reactive.value(None)
    figure_regmap_no_pttf = reactive.value(None)
    figure_allpolys = reactive.value(None)
    figure_polys = reactive.value(None)

    def full_refresh():
        req(pp.get())
        (
            system_sidebar_elems,
            system_quicklook_elems,
            cgvt_analysis_elems,
            cgvt_plots_elems,
            zerog_analysis_elems,
            zerog_plots_elems,
        ) = app_elems(pp.get())

        refresh_ui("system_sidebar", system_sidebar_elems)
        refresh_ui("system_quicklook", system_quicklook_elems)
        refresh_ui("cgvt_analysis", cgvt_analysis_elems)
        refresh_ui("cgvt_plots", cgvt_plots_elems)
        refresh_ui("zerog_analysis", zerog_analysis_elems)
        refresh_ui("zerog_plots", zerog_plots_elems)

    @reactive.effect
    @reactive.event(input.refresh)
    def _():
        req(pp.get())

        path = os.path.join(pp.get().outpath, "tmp.ini")

        update_ini(input, path)

        pp.set(Parser(config=path))

        full_refresh()

    @reactive.effect
    @reactive.event(input.run_all_cgvt, input.run_step1_cgvt, input.run_step1_system)
    def _load_phmap_():
        req(pp.get())

        sequence_ids = pp.get().sequence_ids
        retval = {}
        with ui.Progress(min=0, max=len(sequence_ids)) as p:
            p.set(message="Loading sequences", detail="")
            time.sleep(1.0)

            # phmap = load_phmap(pp.get().datapath, sequence_ids)
            for i, sequence_id in enumerate(sequence_ids):
                p.set(i, message=f"Loading sequence {sequence_id}", detail="")
                retval.update(load_phmap(pp.get().datapath, [sequence_id]))

            phmap.set(retval)

            p.set(len(sequence_ids), message="Done!", detail="")
            time.sleep(1.0)

    def save_generic_plot(figure, outfile):

        fig = figure.get()

        if outfile is None:
            outfile = fig.get_title()

        path = os.path.join(pp.get().outpath, f"{outfile}")

        with ui.Progress(min=0, max=15) as p:
            p.set(message="Saving in progress", detail="")
            time.sleep(1.0)

            fig.savefig(path, dpi=300, bbox_inches="tight")

            p.set(15, message="Done!", detail="")
            time.sleep(1.0)

    def generic_plot(figure, plot_func, *args):
        with ui.Progress(min=0, max=15) as p:
            p.set(message="Plotting in progress", detail="")
            time.sleep(1.0)

            fig = plot_func(*args)

            p.set(15, message="Done!", detail="")
            time.sleep(1.0)

        figure.set(fig)

    @render.plot(alt="Quicklook plot")
    @reactive.event(input.do_plot_1_system)
    def plot_1_system():
        req(pp.get())
        req(phmap.get())
        generic_plot(
            figure_quicklook,
            plot_sag_quicklook,
            phmap.get(),
            int(input.select_1_system()),
            "rawmap",
        )

    @reactive.effect
    @reactive.event(input.download_plot_1_system)
    def download_quicklook():
        req(pp.get())
        req(phmap.get())
        req(figure_quicklook.get())
        modal_download("quicklook", "png")

    @reactive.effect
    @reactive.event(input.download_quicklook_png)
    def download_quicklook_png():
        outfile: list[FileInfo] | None = input.save_quicklook_png()
        save_generic_plot(figure_quicklook, outfile)

    @reactive.effect
    @reactive.event(input.run_all_cgvt, input.run_step2_cgvt)
    def _filter_phmap_():
        req(pp.get())
        req(phmap.get())

        sequence_ids = pp.get().sequence_ids

        with ui.Progress(min=0, max=len(sequence_ids)) as p:
            p.set(message="Filtering in progress", detail="")
            time.sleep(1.0)

            retval = {}
            for i, sequence_id in enumerate(sequence_ids):
                p.set(i, message=f"Filtering sequence {sequence_id}", detail="")
                _phmap = {sequence_id: phmap.get()[sequence_id]}
                retval.update(filter_phmap(_phmap))

            phmap.set(retval)

            p.set(len(sequence_ids), message="Done!", detail="")
            time.sleep(1.0)

    @reactive.effect
    @reactive.event(input.run_all_cgvt, input.run_step3_cgvt)
    def _get_threshold_():
        req(pp.get())
        req(phmap.get())

        sequence_ids = pp.get().sequence_ids
        for seq in sequence_ids:
            if "cleanmap" not in phmap.get()[seq].keys():
                return

        with ui.Progress(min=0, max=15) as p:
            p.set(message="Thresholding in progress", detail="")
            time.sleep(1.0)

            threshold.set(
                get_threshold(
                    phmap.get(),
                    level=pp.get().phmap_threshold,
                    plot=False,
                    full_return=True,
                )
            )

            p.set(15, message="Done!", detail="")
            time.sleep(1.0)

    @render.plot(alt="Threshold plot")
    @reactive.event(input.plot_all_cgvt, input.do_plot_1_cgvt)
    def plot_1_cgvt():
        req(pp.get())
        req(phmap.get())
        req(threshold.get())
        generic_plot(figure_threshold, plot_threshold, *threshold.get())

    @reactive.effect
    @reactive.event(input.download_all_plots_cgvt, input.download_plot_1_cgvt)
    def download_threshold():
        req(pp.get())
        req(phmap.get())
        req(figure_threshold.get())
        modal_download("threshold", "png")

    @reactive.effect
    @reactive.event(input.download_threshold_png)
    def download_threshold_png():
        outfile: list[FileInfo] | None = input.save_threshold_png()
        save_generic_plot(figure_threshold, outfile)

    @reactive.effect
    @reactive.event(input.run_all_cgvt, input.run_step4_cgvt)
    def _med_phmap_():
        req(pp.get())
        req(phmap.get())
        req(threshold.get())

        sequence_ids = pp.get().sequence_ids

        with ui.Progress(min=0, max=len(sequence_ids)) as p:
            p.set(message="Averaging in progress", detail="")
            time.sleep(1.0)

            retval = {}
            for i, sequence_id in enumerate(sequence_ids):
                p.set(i, message=f"Averaging sequence {sequence_id}", detail="")
                _phmap = {sequence_id: phmap.get()[sequence_id]}
                retval.update(
                    med_phmap(
                        _phmap,
                        threshold.get()[2],
                        filter_type=pp.get().phmap_filter_type,
                    )
                )

            phmap.set(retval)

            p.set(len(sequence_ids), message="Done!", detail="")
            time.sleep(1.0)

    @reactive.effect
    @reactive.event(input.run_all_cgvt, input.run_step5_cgvt)
    def _fit_ellipse_():
        req(pp.get())
        req(phmap.get())

        sequence_ids = pp.get().sequence_ids
        for seq in sequence_ids:
            if "medmap" not in phmap.get()[seq].keys():
                return

        with ui.Progress(min=0, max=len(sequence_ids)) as p:
            p.set(message="Ellipse fit in progress", detail="")
            time.sleep(1.0)

            retval = {}
            for i, sequence_id in enumerate(sequence_ids):
                p.set(i, message=f"Fitting ellipse {sequence_id}", detail="")
                _phmap = {sequence_id: phmap.get()[sequence_id]}
                retval.update(fit_ellipse(_phmap))

            phmap.set(retval)

            p.set(len(sequence_ids), message="Done!", detail="")
            time.sleep(1.0)

    @reactive.effect
    @reactive.event(input.run_all_cgvt, input.run_step6_cgvt)
    def _register_phmap_():
        req(pp.get())
        req(phmap.get())

        sequence_ids = pp.get().sequence_ids
        for seq in sequence_ids:
            if "ellipse" not in phmap.get()[seq].keys():
                return

        with ui.Progress(min=0, max=len(sequence_ids)) as p:
            p.set(message="Registration in progress", detail="")
            time.sleep(1.0)

            retval = {}
            for i, sequence_id in enumerate(sequence_ids):
                p.set(i, message=f"Registering {sequence_id}", detail="")
                _phmap = {sequence_id: phmap.get()[sequence_id]}
                retval.update(register_phmap(_phmap))

            phmap.set(retval)

            p.set(len(sequence_ids), message="Done!", detail="")
            time.sleep(1.0)

    @reactive.effect
    @reactive.event(input.run_all_cgvt, input.run_step7_cgvt)
    def _get_uref_():
        req(pp.get())
        req(phmap.get())

        sequence_ids = pp.get().sequence_ids
        for seq in sequence_ids:
            if "RegMap" not in phmap.get()[seq].keys():
                return

        with ui.Progress(min=0, max=15) as p:
            p.set(message="Getting reference in progress", detail="")
            time.sleep(1.0)

            uref.set(
                get_uref(
                    phmap.get(),
                    pp.get().phmap_semi_major,
                    pp.get().phmap_semi_minor,
                    pp.get().phmap_seq_ref,
                )
            )

            p.set(15, message="Done!", detail="")
            time.sleep(1.0)

    @render.plot(alt="RegMap plot")
    @reactive.event(input.plot_all_cgvt, input.do_plot_2_cgvt)
    def plot_2_cgvt():
        req(pp.get())
        req(phmap.get())

        sequence_ids = pp.get().sequence_ids
        for seq in sequence_ids:
            if "RegMap" not in phmap.get()[seq].keys():
                return

        generic_plot(
            figure_regmap,
            plot_sag,
            phmap.get(),
            uref.get(),
            int(input.plot_regmap_imkey()),
            "RegMap",
        )

    @reactive.effect
    @reactive.event(input.download_all_plots_cgvt, input.download_plot_2_cgvt)
    def download_regmap():
        req(pp.get())
        req(phmap.get())
        req(figure_regmap.get())
        modal_download("regmap", "png")

    @reactive.effect
    @reactive.event(input.download_regmap_png)
    def download_regmap_png():
        outfile: list[FileInfo] | None = input.save_regmap_png()
        save_generic_plot(figure_regmap, outfile)

    @reactive.effect
    @reactive.event(input.run_all_cgvt, input.run_step8_cgvt)
    def _fit_zernike_():
        req(pp.get())
        req(phmap.get())
        req(uref.get())

        zkm, A = calculate_zernike(phmap.get(), uref.get(), NZernike=pp.get().n_zernike)
        sequence_ids = pp.get().sequence_ids

        with ui.Progress(min=0, max=len(sequence_ids)) as p:
            p.set(message="Zernike fitting in progress", detail="")
            time.sleep(1.0)

            retval = {}
            for i, sequence_id in enumerate(sequence_ids):
                p.set(i, message=f"Fitting Zernike {sequence_id}", detail="")
                _phmap = {sequence_id: phmap.get()[sequence_id]}
                retval.update(
                    fit_zernike(
                        _phmap, uref.get(), NZernike=pp.get().n_zernike, zkm=zkm, A=A
                    )
                )

            phmap.set(retval)

            p.set(len(sequence_ids), message="Done!", detail="")
            time.sleep(1.0)

    @render.plot(alt="RegMap-PTTF plot")
    @reactive.event(input.plot_all_cgvt, input.do_plot_3_cgvt)
    def plot_3_cgvt():
        req(pp.get())
        req(phmap.get())

        sequence_ids = pp.get().sequence_ids
        for seq in sequence_ids:
            if "residual" not in phmap.get()[seq].keys():
                return

        generic_plot(
            figure_regmap_no_pttf,
            plot_sag,
            phmap.get(),
            uref.get(),
            int(input.plot_regmap_no_pttf_imkey()),
            "RegMap-PTTF",
        )

    @reactive.effect
    @reactive.event(input.download_all_plots_cgvt, input.download_plot_3_cgvt)
    def download_regmap_no_pttf():
        req(pp.get())
        req(phmap.get())
        req(figure_regmap_no_pttf.get())
        modal_download("regmap_no_pttf", "png")

    @reactive.effect
    @reactive.event(input.download_regmap_no_pttf_png)
    def download_regmap_no_pttf_png():
        outfile: list[FileInfo] | None = input.save_regmap_no_pttf_png()
        save_generic_plot(figure_regmap_no_pttf, outfile)

    @render.plot(alt="Allpolys plot")
    @reactive.event(input.plot_all_cgvt, input.do_plot_4_cgvt)
    def plot_4_cgvt():
        req(pp.get())
        req(phmap.get())

        sequence_ids = pp.get().sequence_ids
        for seq in sequence_ids:
            if "residual" not in phmap.get()[seq].keys():
                return

        generic_plot(
            figure_allpolys,
            plot_allpolys,
            phmap.get(),
            sequence_ids,
            pp.get().plot_allpolys_seq_ref,
            pp.get().n_zernike,
            pp.get().plot_allpolys_colors,
        )

    @reactive.effect
    @reactive.event(input.download_all_plots_cgvt, input.download_plot_4_cgvt)
    def download_allpolys():
        req(pp.get())
        req(phmap.get())
        req(figure_allpolys.get())
        modal_download("allpolys", "png")

    @reactive.effect
    @reactive.event(input.download_allpolys_png)
    def download_allpolys_png():
        outfile: list[FileInfo] | None = input.save_allpolys_png()
        save_generic_plot(figure_allpolys, outfile)

    @render.plot(alt="Polys plot")
    @reactive.event(input.plot_all_cgvt, input.do_plot_5_cgvt)
    def plot_5_cgvt():
        req(pp.get())
        req(phmap.get())

        sequence_ids = pp.get().sequence_ids
        for seq in sequence_ids:
            if "residual" not in phmap.get()[seq].keys():
                return

        generic_plot(
            figure_polys,
            plot_polys,
            phmap.get(),
            sequence_ids,
            pp.get().plot_polys_seq_ref,
            pp.get().plot_polys_order,
            pp.get().plot_polys_colors,
        )

    @reactive.effect
    @reactive.event(input.download_all_plots_cgvt, input.download_plot_5_cgvt)
    def download_polys():
        req(pp.get())
        req(phmap.get())
        req(figure_polys.get())
        modal_download("polys", "png")

    @reactive.effect
    @reactive.event(input.download_polys_png)
    def download_polys_png():
        outfile: list[FileInfo] | None = input.save_polys_png()
        save_generic_plot(figure_polys, outfile)

    @reactive.effect
    @reactive.event(input.download_phmap)
    def download_phmap():
        req(pp.get())
        req(phmap.get())
        modal_download("phmap", "pkl")

    @reactive.effect
    @reactive.event(input.download_phmap_pkl)
    def download_phmap_pkl():
        outfile: list[FileInfo] | None = input.save_phmap_pkl()

        if outfile is None:
            outfile = pp.get().outpath

        path = os.path.join(pp.get().outpath, f"{outfile}")

        with ui.Progress(min=0, max=15) as p:
            p.set(message="Saving in progress", detail="")
            time.sleep(1.0)

            to_pickle(phmap.get(), path)

            p.set(15, message="Done!", detail="")
            time.sleep(1.0)

    @reactive.effect
    @reactive.event(input.open)
    def _():
        req(input.open())
        m = ui.modal(
            ui.input_file(
                id="open_ini",
                label=ui.markdown(
                    "Input files must be in the INI format.  \n"
                    "Example files can be found in the TIGRO [GitHub repository](https://github.com/arielmission-space/TIGRO)."
                ),
                accept=[".ini"],
                multiple=False,
                button_label="Browse",
            ),
            title="Open INI File",
            easy_close=True,
            footer=ui.markdown(
                "Note: you may only open one file per session.  \n"
                "Refresh the page to open a different file."
            ),
        )
        ui.modal_show(m)

    @reactive.effect
    @reactive.event(input.open_ini)
    def open_ini():
        req(input.open_ini())
        file: list[FileInfo] | None = input.open_ini()

        if file is None:
            return

        if not file[0]["name"].endswith(".ini"):
            print("Invalid file")
            return

        if config.get().endswith(".ini") and config.get() != file[0]["name"]:
            return
            # await session.send_custom_message("refresh", "")

        config.set(file[0]["datapath"])
        pp.set(Parser(config=config.get()))

        full_refresh()

    @reactive.effect
    @reactive.event(input.save)
    def _():
        req(pp.get())
        req(input.save())
        m = ui.modal(
            ui.input_text(
                id="save_ini",
                label="Save As",
                value="filename.ini",
                placeholder="filename.ini",
            ),
            ui.input_action_button("download_ini", "Save"),
            title="Save INI File",
            easy_close=True,
        )
        ui.modal_show(m)

    @reactive.effect
    @reactive.event(input.download_ini)
    def download_ini():
        req(input.download_ini())
        outfile: list[FileInfo] | None = input.save_ini()

        if outfile is None:
            return

        path = os.path.join(pp.get().outpath, f"{outfile}")

        with ui.Progress(min=0, max=15) as p:
            p.set(message="Saving in progress", detail="")
            time.sleep(1.0)

            update_ini(input, path)

            p.set(15, message="Done!", detail="")
            time.sleep(1.0)

    @reactive.effect
    @reactive.event(input.close)
    async def _():
        await session.close()

    @reactive.effect
    @reactive.event(input.docs)
    def _():
        req(input.docs())
        m = ui.modal(
            ui.markdown(
                """
                Click [here](https://tigro.readthedocs.io/en/latest/) to access the TIGRO documentation.
                """
            ),
            title="Documentation",
            easy_close=True,
        )
        ui.modal_show(m)

    @reactive.effect
    @reactive.event(input.about)
    def _():
        req(input.about())
        m = ui.modal(
            ui.markdown(
                f"SOFTWARE: TIGRO UI v{__version__}  \n"
                f"AUTHOR: {__author__}  \n"
                f"LICENSE: {__license__}  \n"
            ),
            title="About",
            easy_close=True,
        )
        ui.modal_show(m)


app = App(app_ui, server, debug=True)
