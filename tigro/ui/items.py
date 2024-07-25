from shiny import ui

from tigro.ui.shared import nested_div
from tigro.ui.shared import menu_panel


menu_items = [
    ui.nav_menu("File", menu_panel("open"), menu_panel("save"), menu_panel("close")),
    ui.nav_menu("Help", menu_panel("docs"), menu_panel("about")),
]

system_sidebar = [
    ui.accordion_panel("System Explorer", nested_div("general")),
]

CGVt_sidebar = [
    ui.accordion_panel("Analysis", nested_div("cgvt_sidebar_analysis")),
    ui.accordion_panel("Plots", nested_div("cgvt_sidebar_plots")),
]

ZeroG_sidebar = [
    ui.accordion_panel("Analysis", nested_div("zerog_sidebar_analysis")),
    ui.accordion_panel("Plots", nested_div("zerog_sidebar_plots")),
]
