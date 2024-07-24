from shiny import ui


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
    ]

    return (general_elems,)
