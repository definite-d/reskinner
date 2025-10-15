# All Elements Demo
# Based on the default PySimpleGUI All Elements Demo, customized for specific use.

from reskinner import reskin, sg

THEME = "BrightColors"
NAME_SIZE = 23


def main():
    sg.theme(THEME)
    use_custom_titlebar = sg.running_trinket()

    def name(label):
        dots = NAME_SIZE - len(label) - 2
        return sg.Text(
            f"{label} {'•' * dots}",
            size=(NAME_SIZE, 1),
            justification="r",
            pad=(0, 0),
            font="Courier 10",
        )

    Menu = sg.MenubarCustom if use_custom_titlebar else sg.Menu

    # Tree data for Tree Element
    treedata = sg.TreeData()
    treedata.Insert("", "_A_", "Tree Item 1", [1234])
    treedata.Insert("", "_B_", "B", [])
    treedata.Insert("_A_", "_A1_", "Sub Item 1", ["can", "be", "anything"])

    layout_l = [
        [name("Text"), sg.Text("Text")],
        [name("Input"), sg.Input(size=15)],
        [name("Multiline"), sg.Multiline(size=(15, 2))],
        [
            name("Combo"),
            sg.Combo(
                sg.theme_list(),
                default_value=sg.theme(),
                size=(15, 22),
                enable_events=True,
                readonly=True,
                key="-COMBO-",
            ),
        ],
        [name("OptionMenu"), sg.OptionMenu(["OptionMenu"], size=(15, 2))],
        [name("Checkbox"), sg.Checkbox("Checkbox")],
        [name("Radio"), sg.Radio("Radio", 1)],
        [name("Spin"), sg.Spin(["Spin"], size=(15, 2))],
        [name("Button"), sg.Button("Button")],
        [
            name("ButtonMenu"),
            sg.ButtonMenu("ButtonMenu", sg.MENU_RIGHT_CLICK_EDITME_EXIT),
        ],
        [
            name("Slider"),
            sg.Slider((0, 10), orientation="h", size=(10, 15), key="slider"),
        ],
        [
            name("Listbox"),
            sg.Listbox(["Listbox", "Listbox 2"], no_scrollbar=True, size=(15, 2)),
        ],
        [name("Image"), sg.Image(sg.EMOJI_BASE64_HAPPY_THUMBS_UP)],
        [name("Graph"), sg.Graph((125, 50), (0, 0), (125, 50), key="-GRAPH-")],
    ]

    layout_r = [
        [
            name("Canvas"),
            sg.Canvas(background_color=sg.theme_button_color()[1], size=(125, 40)),
        ],
        [
            name("ProgressBar"),
            sg.ProgressBar(100, orientation="h", size=(10, 20), key="-PBAR-"),
        ],
        [
            name("Table"),
            sg.Table([[1, 2, 3], [4, 5, 6]], ["Col 1", "Col 2", "Col 3"], num_rows=2),
        ],
        [name("Tree"), sg.Tree(treedata, ["Heading"], num_rows=3)],
        [name("Horizontal Separator"), sg.HSep()],
        [name("Vertical Separator"), sg.VSep()],
        [name("Frame"), sg.Frame("Frame", [[sg.Text(size=15)]])],
        [name("Column"), sg.Column([[sg.Text(size=15)]])],
        [
            name("Tab, TabGroup"),
            sg.TabGroup(
                [[sg.Tab("Tab1", [[sg.Text(size=(15, 2))]]), sg.Tab("Tab2", [[]])]],
                right_click_menu=[[""], ["asdfe", "adsfasdfadfs", ";klhjlkjh"]],
            ),
        ],
        [
            name("Pane"),
            sg.Pane(
                [sg.Column([[sg.Text("Pane 1")]]), sg.Column([[sg.Text("Pane 2")]])]
            ),
        ],
        [name("Push"), sg.Push(), sg.Text("Pushed over")],
        [name("VPush"), sg.VPush()],
        [name("Sizer"), sg.Sizer(60, 60)],
        [name("StatusBar"), sg.StatusBar("StatusBar")],
        [name("Sizegrip"), sg.Sizegrip()],
    ]

    menudef = [["File", ["Exit"]], ["Edit", ["Edit Me"]]]

    layout = [
        [Menu(menudef, key="-CUST MENUBAR-", pad=0)],
        [
            sg.Text(
                "PySimpleGUI Elements - Use Combo to Change Themes",
                font="_ 14",
                justification="center",
                expand_x=True,
            )
        ],
        [
            sg.Checkbox(
                "Use Custom Titlebar & Menubar",
                default=use_custom_titlebar,
                enable_events=True,
                key="-USE CUSTOM TITLEBAR-",
                pad=0,
                tooltip="checkcheckcheck",
            )
        ],
        [sg.Column(layout_l, pad=0, scrollable=True), sg.Column(layout_r, pad=0)],
    ]

    window = sg.Window(
        "The PySimpleGUI Element List",
        [[sg.Column(layout, scrollable=True)]],
        finalize=True,
        right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT,
        use_custom_titlebar=use_custom_titlebar,
        resizable=True,
    )

    # Initial updates
    window["-PBAR-"].update(30)
    window["-GRAPH-"].draw_image(data=sg.EMOJI_BASE64_HAPPY_JOY, location=(0, 50))

    # Debug: print all element types in the window
    for element in sorted(set(type(el).__name__ for el in window.element_list())):
        print(element)

    # Event loop
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event == "-COMBO-":
            reskin(window, values["-COMBO-"], duration=200)

        elif event == "-USE CUSTOM TITLEBAR-":
            use_custom_titlebar = values["-USE CUSTOM TITLEBAR-"]
            sg.set_options(use_custom_titlebar=use_custom_titlebar)

        elif event == "Edit Me":
            sg.execute_editor(__file__)

        elif event == "Version":
            sg.popup_scrolled(
                __file__, sg.get_versions(), keep_on_top=True, non_blocking=True
            )

    window.close()


if __name__ == "__main__":
    main()
