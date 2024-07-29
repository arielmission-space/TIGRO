import time

from htmltools import Tag
from starlette.requests import Request as StarletteRequest
from faicons import icon_svg
from shiny import App
from shiny import ui
from shiny import reactive
from shiny import req
from shiny.types import FileInfo

from tigro import __author__
from tigro import __version__
from tigro import __license__

from tigro.classes.parser import Parser
from tigro.io.load import load_phmap

from tigro.ui.items import menu_items
from tigro.ui.items import system_sidebar
from tigro.ui.elems import app_elems
from tigro.ui.shared import refresh_ui
from tigro.ui.shared import nested_div


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
            ),
        ),
        ui.nav_panel(
            "ZeroG",
            ui.layout_columns(
                ui.card(nested_div("zerog_analysis"), full_screen=True),
                ui.card(nested_div("zerog_plots"), full_screen=True),
            ),
        ),
        fillable="TIGRO UI",
        id="navbar",
        title=ui.popover(
            [
                "TIGRO UI",
                icon_svg("circle-info").add_class("ms-2"),
            ],
            ui.markdown("blabla"),
            placement="right",
        ),
        window_title="TIGRO UI",
        # selected="System",
    )


def server(input, output, session):
    config = reactive.value("config")
    pp = reactive.value({})
    phmap = reactive.value({})
    outpath = reactive.value("outpath")

    # @reactive.calc
    # def api_call():
    #     req(config.get().sections())
    #     # other req here

    #     # myvalue = input.myvalue()
    #     # get inputs here

    #     with ui.Progress(min=1, max=15) as p:
    #         p.set(message="API call in progress", detail="")

    #         # api call here

    #         p.set(15, message="Done!", detail="")
    #         time.sleep(1.0)

    @reactive.effect
    @reactive.event(input.run_step1_system, input.run_step1_cgvt, input.run_step1_zerog)
    def load_sequences():

        sequence_ids = pp.get().sequence_ids
        retval = {}
        with ui.Progress(min=-1, max=len(sequence_ids)) as p:
            p.set(message="Loading sequences", detail="")
            time.sleep(1.0)

            # phmap = load_phmap(pp.get().datapath, sequence_ids)
            for i, sequence_id in enumerate(sequence_ids):
                retval.update(load_phmap(pp.get().datapath, [sequence_id]))
                p.set(i, message=f"Loading sequence {sequence_id}", detail="")

            p.set(len(sequence_ids), message="Done!", detail="")
            time.sleep(1.0)

        phmap.set(retval)

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
