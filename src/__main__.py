def main():
    """
    Main Function.

    Gets called when the module is run instead of imported.
    """
    # % START DEMO % #
    from random import choice as rc

    from .__version__ import __version__
    from .reskinner import reskin
    from .sg import sg

    right_click_menu = [
        "",
        [["Hi", ["Next Level", ["Deeper Level", ["a", "b", "c"]], "Hoho"]], "There"],
    ]

    window_layout = [
        [sg.Titlebar("Reskinner Demo")],
        [sg.Text("Hello!", font=("Helvetica", 20))],
        [sg.Text("You are currently running the Reskinner demo.")],
        [sg.Text("The theme of this window changes every 2 seconds.")],
        [sg.Text("Changing to:")],
        [
            sg.Button(
                "DarkBlue3",
                k="current_theme",
                font=("Helvetica", 16),
                right_click_menu=right_click_menu,
            )
        ],
        [
            sg.Text(f"Reskinner v{__version__}", font=("Helvetica", 8), pad=(0, 0)),
            sg.Push(),
        ],
    ]

    window = sg.Window(
        "Reskinner Demo",
        window_layout,
        element_justification="center",
        keep_on_top=True,
    )

    def _reskin_job():
        themes = sg.theme_list()
        themes.remove(sg.theme())
        new = rc(themes)
        window["current_theme"].update(new)
        reskin(
            window=window,
            new_theme=new,
            theme_function=sg.theme,
            lf_table=sg.LOOK_AND_FEEL_TABLE,
            duration=450,
            interpolation_mode="hsl",
        )
        window.TKroot.after(2000, _reskin_job)

    started = False

    try:
        while True:
            e, v = window.read(timeout=2000)

            if e in (None, "Exit"):
                window.Close()
                break

            if not started:
                _reskin_job()
                started = True
    except KeyboardInterrupt:
        print("Goodbye!")
    except Exception as e:
        raise e
    finally:
        window.close()

    # % END DEMO % #
    return


if __name__ == "__main__":
    main()
