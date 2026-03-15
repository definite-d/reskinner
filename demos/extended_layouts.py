import FreeSimpleGUI as sg
from reskinner import reskin

SIMPLEGUI_DARK_THEME = "Dark"
SIMPLEGUI_THEME = "Reddit"

sg.theme(SIMPLEGUI_THEME)


def _make_row(text: str):
    return [sg.Text(f"- {text}")]


def _theme_is_light() -> bool:
    return sg.theme() == SIMPLEGUI_THEME


def main():
    layout = [
        [sg.Text("Extended Layout Demo", font="_ 16")],
        [
            sg.Text(
                'Type in a value and click "Add Item" '
                "to extend the column below with text"
            )
        ],
        [
            sg.Column(
                [],
                size=(None, 200),
                expand_x=True,
                scrollable=True,
                vertical_scroll_only=True,
                key="container",
            )
        ],
        [
            sg.Input(key="data", expand_x=True),
            sg.Button(
                "Add Item",
                key="add",
                bind_return_key=True,
            ),
        ],
        [sg.pin(sg.Text(key="warning", visible=False))],
        [sg.Button("Toggle Theme", key="toggle_theme")],
    ]

    window: sg.Window = sg.Window("Extended layouts demo", layout)
    data: set[str] = set()

    container: sg.Column = window["container"]
    warning: sg.Text = window["warning"]

    def _warn(message: str, timeout=3000):
        locked = warning.metadata == "locked"

        warning.metadata = "locked"
        warning.update(
            f"Warning: {message}",
            text_color="red" if _theme_is_light() else "#FF9A9A",
            visible=True,
        )

        def _try_hide():
            warning.update(visible=False)
            warning.metadata = None

        if window.TKroot and not locked:
            window.TKroot.after(timeout, _try_hide)

    while not window.was_closed():
        e, v = window.read()

        if e == "add":
            if v["data"]:
                if v["data"] not in data:
                    window.extend_layout(container, [_make_row(v["data"])])
                    container.contents_changed()
                    data.add(v["data"])
                    window["data"].update(value="")
                else:
                    _warn(f"{v['data']} already added.")
            else:
                _warn("No data to add.")

        elif e == "toggle_theme":
            new_theme = SIMPLEGUI_DARK_THEME if _theme_is_light() else SIMPLEGUI_THEME
            reskin(window, new_theme)
