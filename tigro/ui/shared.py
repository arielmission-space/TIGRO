import numpy as np
import faicons as fa

from shiny import ui


card_header_class_ = "d-flex justify-content-between align-items-center"

ICONS = {
    "ellipsis": fa.icon_svg("ellipsis"),
    "open": fa.icon_svg("folder-open"),
    "save": fa.icon_svg("floppy-disk"),
    "close": fa.icon_svg("xmark"),
    "docs": fa.icon_svg("book-open-reader"),
    "about": fa.icon_svg("info"),
    "run": fa.icon_svg("play"),
}


def menu_panel(id):
    return ui.nav_panel(
        ui.input_action_button(
            id,
            id.capitalize(),
            icon=ICONS[id],
            width="100%",
        )
    )


def nested_div(id):
    return ui.div(
        {"id": f"{id}-editor"},
        ui.div(
            {"id": f"inserted-{id}-editor"},
        ),
    )


def fill_header(items):
    if not items:
        return ui.div()
    key = min(np.array(list(items.keys())))
    item = items[key]
    return ui.div(
        {"style": "display: flex;"},
        *[
            ui.column(
                subitem["width"],
                {"style": "text-align: center;"},
                ui.markdown(
                    f"**{subkey}**  \n" "___",
                ),
            )
            for _, (subkey, subitem) in enumerate(item.items())
        ],
    )


def fill_value(items, name, row, col):
    func = items[name]["f"]
    prefix = "" if "prefix" not in items[name] else items[name]["prefix"]
    theid = f"{prefix}{name}_{row}_{col}"
    if func in [ui.input_select]:
        return func(
            id=theid,
            label=items[name]["label"] if "label" in items[name] else "",
            choices=items[name]["choices"],
            selected=items[name]["selected"],
        )
    elif func in [ui.input_text, ui.input_checkbox]:
        return func(
            id=theid,
            label=items[name]["label"] if "label" in items[name] else "",
            value=items[name]["value"],
        )
    elif func in [ui.p]:
        return func(
            f"{items[name]['value']}",
        )
    elif func in [ui.navset_card_pill]:
        return func(
            ui.nav_panel(
                items[name]["title"],
                ui.div(
                    *[
                        fill_value(items[name]["value"], key, row, col)
                        for key in items[name]["value"].keys()
                    ],
                ),
            ),
            selected=False,
        )
    elif func in [ui.accordion]:
        return func(
            ui.accordion_panel(
                items[name]["title"],
                ui.div(
                    *[
                        fill_value(items[name]["value"], key, row, col)
                        for key in items[name]["value"].keys()
                    ],
                ),
            ),
            open=False,
        )
    elif func in [ui.card]:
        return func(
            ui.div(
                items[name]["title"],
                ui.div(
                    *[
                        fill_value(items[name]["value"], key, row, col)
                        for key in items[name]["value"].keys()
                    ],
                ),
            ),
            open=False,
        )


def fill_body(items):
    if not items:
        return [ui.div()]
    return [
        ui.div(
            {"style": "display: flex;"},
            *[
                ui.column(
                    subitem["width"],
                    {"style": "text-align: center;"},
                    fill_value(item, subkey, row + 1, col),
                )
                for col, (subkey, subitem) in enumerate(item.items())
            ],
        )
        for row, (key, item) in enumerate(items.items())
    ]


def refresh_ui(name, items, mode=None, key=""):
    ui.remove_ui(f"#inserted-{name}-editor")

    if mode == "dict":
        items = [fill_header(items), *fill_body(items)]

    elif mode == "nested-dict":
        key = list(items.keys())[0] if key == "" else key
        items = [fill_header(items[key]), *fill_body(items[key])]

    ui.insert_ui(
        ui.div(
            {"id": f"inserted-{name}-editor"},
            *items,
        ),
        selector=f"#{name}-editor",
        where="beforeEnd",
    )


def output_text_verbatim(id, placeholder=True):
    return ui.div(
        {"id": f"{id}-editor"},
        ui.div(
            {"id": f"inserted-{id}-editor"},
            ui.output_text_verbatim(
                id,
                placeholder=placeholder,
            ),
        ),
    )


def modal_download(id, ext):
    m = ui.modal(
        *[
            ui.input_text(
                id=f"save_{id}_{ext}",
                label="Save As",
                value=f"filename.{ext}",
                placeholder=f"filename.{ext}",
            ),
            ui.input_action_button(
                f"download_{id}_{ext}",
                "Save",
            ),
            # ui.output_text(f"download_{ext}_progress"),
        ],
        title=f"Save {id} to {ext.upper()} File",
        easy_close=True,
    )
    ui.modal_show(m)
