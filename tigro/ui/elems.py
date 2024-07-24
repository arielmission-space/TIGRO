from shiny import ui


def app_elems(config):
    general_elems = [
        ui.input_text(
            "project",
            "Project name",
            value=config["general"].get("project", "Template"),
        ),
        ui.input_text(
            "comment",
            "Comment",
            value=config["general"].get("comment", ""),
        ),
        ui.input_text(
            "version",
            "Version",
            value=config["general"].get("version", "1.0"),
        ),
    ]

    return (general_elems,)
