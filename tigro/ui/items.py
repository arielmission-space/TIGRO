from shiny import ui

from tigro.ui.shared import nested_div
from tigro.ui.shared import menu_panel


menu_items = [
    ui.nav_menu("File", menu_panel("open"), menu_panel("save"), menu_panel("close")),
    ui.nav_menu("Help", menu_panel("docs"), menu_panel("about")),
]
