from htmltools import Tag
from starlette.requests import Request as StarletteRequest
from faicons import icon_svg
from shiny import App
from shiny import ui


def app_ui(request: StarletteRequest) -> Tag:
    return ui.page_navbar(
        ui.nav_spacer(),
        ui.nav_panel(
            "CGVt",
            ui.layout_sidebar(
                ui.sidebar(

                ),
                ui.card(
                    full_screen=True,
                ),
            ),
        ),
        ui.nav_panel(
            "ZeroG",
            ui.layout_sidebar(
                ui.sidebar(

                ),
                ui.card(
                    full_screen=True,
                ),
            )
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
    )


def server(input, output, session):
    pass


app = App(app_ui, server, debug=False)
