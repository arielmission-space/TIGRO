from shiny import ui


def nested_div(id):
    return ui.div(
        {"id": f"{id}-editor"},
        ui.div(
            {"id": f"inserted-{id}-editor"},
        ),
    )
