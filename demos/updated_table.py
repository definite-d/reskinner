import FreeSimpleGUI as sg
from reskinner import reskin

SIMPLEGUI_DARK_THEME = "Dark"
SIMPLEGUI_THEME = "Reddit"

sg.theme(SIMPLEGUI_THEME)


def make_window() -> sg.Window:
    layout = [
        [sg.Button("-THEME-")],
        [
            sg.Table(
                values=[[]],
                headings=["A", "B", "C"],
                auto_size_columns=True,
                justification="left",
                key="snapshot-list",
                select_mode="extended",
                size=(None, 10),
                expand_x=True,
                expand_y=True,
            )
        ],
    ]

    window = sg.Window(
        "Window Title",
        layout,
        use_default_focus=False,
        font="_ 15",
        metadata=0,
        size=(400, 300),
    )

    return window


snapshot_list = [
    ["Row 1", "Data", "More Data"],
    ["Row 2", "Data", "More Data"],
    ["Row 3", "Data", "More Data"],
    ["Row 4", "Data", "More Data"],
    ["Row 5", "Data", "More Data"],
]


def main():
    window = make_window()
    window.finalize()

    window["snapshot-list"].update(snapshot_list)

    while not window.is_closed():
        event, values = window.read()  # wake every hour
        print(event, values)
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        if event == "-THEME-":
            reskin(
                window=window,
                new_theme=SIMPLEGUI_DARK_THEME
                if (sg.theme() == SIMPLEGUI_THEME)
                else SIMPLEGUI_THEME,
            )
            continue


if __name__ == "__main__":
    main()
