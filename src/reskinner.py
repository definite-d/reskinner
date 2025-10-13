from datetime import datetime, timedelta
from tkinter import TclError
from typing import Callable, Dict, Literal
from warnings import warn

from .elements import ElementReskinner
from src.colorizer import Colorizer, ThemeDict
from src.sg import sg


def reskin(
    window: sg.Window,
    new_theme: str,
    element_filter: Callable[[sg.Element], ...],
    theme_function: Callable = sg.theme,
    lf_table: Dict[str, ThemeDict] = sg.LOOK_AND_FEEL_TABLE,
    set_future: bool = True,
    reskin_background: bool = True,
    duration_in_milliseconds: float = 0,
    interpolation_mode: Literal["hsl", "hue", "rgb"] = "rgb",
) -> None:
    old_theme = theme_function()
    old_theme_dict: ThemeDict = lf_table.get(old_theme, None)
    new_theme_dict: ThemeDict = sg.LOOK_AND_FEEL_TABLE.get(new_theme, None)

    if not old_theme_dict:
        raise ValueError("Invalid `old_theme`; theme not found")
    elif not new_theme_dict:
        raise ValueError("Invalid `new_theme`; theme not found")

    # Disregard redundant calls
    if (old_theme == new_theme) and (new_theme_dict == old_theme_dict):
        return

    colorizer = Colorizer(old_theme_dict, new_theme_dict, interpolation_mode)

    if duration_in_milliseconds:
        delta = timedelta(milliseconds=duration_in_milliseconds)
        start = datetime.now()
        end = start
        while datetime.now() <= end:
            colorizer.progress = round((datetime.now() - start) / delta, 4)
            try:
                _reskin(colorizer, window, element_filter, reskin_background)
            except TclError:  # Closed window.
                warn("The window has already been closed.")
                return

    colorizer.progress = 1
    _reskin(colorizer, window, element_filter, reskin_background)

    if set_future:
        theme_function(new_theme)


def _reskin(
    colorizer: Colorizer,
    window: sg.Window,
    element_filter: Callable[[sg.Element], ...],
    reskin_background: bool = True,
):
    # Window level changes
    if reskin_background:
        colorizer.window(window, {"background": "BACKGROUND"})

    # Handle element filtering
    whitelist = (
        filter(element_filter, window.element_list())
        if element_filter is not None
        else window.element_list()
    )

    # Element reskinner instance
    element_reskinner = ElementReskinner(colorizer)

    # Per-element changes happen henceforth
    for element in whitelist:
        element_reskinner.reskin_element(element)


def toggle_transparency(window: sg.Window) -> None:
    window_bg = window.TKroot.cget("background")
    transparent_color = window.TKroot.attributes("-transparentcolor")
    window.set_transparent_color(window_bg if transparent_color == "" else "")
