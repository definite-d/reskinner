# Pin Elements Demo
# Demonstrates the single pixel issue with sg.pin when shrink=True

from reskinner import reskin, sg

THEME = "BrightColors"


def main():
    sg.theme(THEME)
    use_custom_titlebar = sg.running_trinket()

    Menu = sg.MenubarCustom if use_custom_titlebar else sg.Menu

    menudef = [["File", ["Exit"]], ["Demo", ["Toggle Shrink", "Toggle NoShrink", "Toggle Regular"]]]

    layout = [
        [Menu(menudef, key="-CUST MENUBAR-", pad=0)],
        [
            sg.Text("Pin Demo - Single Pixel Issue with shrink=True", font="_ 14 bold"),
        ],
        [
            sg.Text("Theme:"),
            sg.Combo(sg.theme_list(), default_value=sg.theme(), key="-THEME-", readonly=True, size=(15, 22), enable_events=True),
            sg.Text("When shrink=True, single pixel of old theme remains after reskinning", text_color="red"),
        ],
        [
            sg.pin(sg.Button("Shrink=True Button", key="-SHRINK_BTN-")),
            sg.pin(sg.Button("Shrink=False Button", key="-NOSHRINK_BTN-"), shrink=False),
            sg.Button("Regular Button", key="-REGULAR_BTN-"),
        ],
        [
            sg.pin(sg.Text("Shrink=True Text", key="-SHRINK_TEXT-")),
            sg.pin(sg.Text("Shrink=False Text", key="-NOSHRINK_TEXT-"), shrink=False),
            sg.Text("Regular Text", key="-REGULAR_TEXT-"),
        ],
        [
            sg.pin(sg.Input("Shrink=True Input", key="-SHRINK_INPUT-", size=20)),
            sg.pin(sg.Input("Shrink=False Input", key="-NOSHRINK_INPUT-", size=20), shrink=False),
            sg.Input("Regular Input", key="-REGULAR_INPUT-", size=20),
        ],
        [
            sg.StatusBar("Change theme to see the single pixel issue with shrink=True elements", key="-STATUS-"),
        ],
    ]

    window = sg.Window(
        "Pin Elements Demo",
        layout,
        finalize=True,
        right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT,
        use_custom_titlebar=use_custom_titlebar,
        resizable=True,
    )

    # Debug: Print element types to see what sg.pin() creates
    print("Element types in window:")
    for element in window.element_list():
        print(f"  {element.Key}: {type(element).__name__}")
        if hasattr(element, 'Widget') and hasattr(element.Widget, 'winfo_children'):
            print(f"    Children: {[type(child).__name__ for child in element.Widget.winfo_children()]}")

    # Event loop
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event == "-THEME-":
            new_theme = values["-THEME-"]
            window["-STATUS-"].update(f"Reskinning to {new_theme}...")
            window.refresh()
            reskin(window, new_theme)
            window["-STATUS-"].update(f"Reskinned to {new_theme} - Check for single pixel artifacts!")

        elif event == "Toggle Shrink":
            for key in ["-SHRINK_BTN-", "-SHRINK_TEXT-", "-SHRINK_INPUT-"]:
                window[key].update(visible=not window[key].visible)

        elif event == "Toggle NoShrink":
            for key in ["-NOSHRINK_BTN-", "-NOSHRINK_TEXT-", "-NOSHRINK_INPUT-"]:
                window[key].update(visible=not window[key].visible)

        elif event == "Toggle Regular":
            for key in ["-REGULAR_BTN-", "-REGULAR_TEXT-", "-REGULAR_INPUT-"]:
                window[key].update(visible=not window[key].visible)

    window.close()


if __name__ == "__main__":
    main()