from __future__ import annotations

from datetime import datetime, timedelta
from tkinter import TclError
from typing import Callable, Dict, Optional, TypeVar, Union
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
from warnings import warn

from .colorizer import Colorizer, ThemeDict
from .easing import EasingName
from .elements import ElementReskinner
from .sg import sg

# Type variable for PySimpleGUI elements
T = TypeVar("T", bound=sg.Element)

# Type alias for element filter function
ElementFilter = Callable[[T], bool]


def reskin(
    window: sg.Window,
    new_theme: str,
    element_filter: Optional[ElementFilter] = None,
    theme_function: Callable[..., str] = sg.theme,
    lf_table: Optional[Dict[str, ThemeDict]] = None,
    set_future: bool = True,
    reskin_background: bool = True,
    duration: float = 0,
    interpolation_mode: Literal["hsl", "hue", "rgb"] = "rgb",
    easing_function: Optional[Union[EasingName, Callable[[float], float]]] = None,
) -> None:
    """Apply a new theme to a PySimpleGUI or FreeSimpleGUI window with optional animation.

    This function enables dynamic theme switching for GUI windows built with
    either PySimpleGUI or FreeSimpleGUI, without the need to recreate
    or re-instantiate the window or its elements. It optionally supports smooth
    animated transitions using RGB, HSL, or hue-based color interpolation.

    :param window: The PySimpleGUI window to reskin
    :type window: sg.Window
    :param new_theme: Name of the theme to apply
    :type new_theme: str
    :param element_filter: Optional function to filter which elements to reskin
    :type element_filter: Optional[ElementFilter]
    :param theme_function: Function to get/set the current theme
    :type theme_function: Callable[..., str]
    :param lf_table: Look and feel table containing theme definitions
    :type lf_table: Optional[Dict[str, ThemeDict]]
    :param set_future: If True, set the theme for future windows
    :type set_future: bool
    :param reskin_background: If True, reskin the window background
    :type reskin_background: bool
    :param duration: Duration of animation in milliseconds (0 for instant)
    :type duration: float
    :param interpolation_mode: Color interpolation mode ("hsl", "hue", or "rgb")
    :type interpolation_mode: Literal["hsl", "hue", "rgb"]
    :param easing_function: Optional easing function or name used to shape the animation curve.
    :type easing_function: Optional[Union[EasingName, Callable[[float], float]]]

    :raises ValueError: If the specified theme is not found
    :raises TclError: For Tkinter-related errors
    :raises RuntimeError: If theme reskinning initialization fails
    """
    if lf_table is None:
        lf_table = sg.LOOK_AND_FEEL_TABLE

    if not isinstance(window, sg.Window):
        raise TypeError(f"Expected a PySimpleGUI Window, got {type(window).__name__}")

    if not isinstance(new_theme, str):
        raise TypeError(f"Theme name must be a string, got {type(new_theme).__name__}")
    try:
        old_theme = theme_function()
        old_theme_dict: Optional[ThemeDict] = lf_table.get(old_theme)
        new_theme_dict: Optional[ThemeDict] = lf_table.get(new_theme)

        if not old_theme_dict:
            raise ValueError(
                f"Current theme '{old_theme}' not found in look and feel table."
            )

        if not new_theme_dict:
            raise ValueError(
                f"Target theme '{new_theme}' not found in look and feel table."
            )

    except Exception as e:
        if not isinstance(e, (ValueError, TypeError)):
            raise RuntimeError(
                f"Failed to initialize theme reskinning: {str(e)}"
            ) from e
        raise

    # Disregard redundant calls
    if (old_theme == new_theme) and (new_theme_dict == old_theme_dict):
        return

    colorizer = Colorizer(
        old_theme_dict, new_theme_dict, interpolation_mode, easing_function
    )

    if duration:
        if not isinstance(duration, (int, float)) or duration < 0:
            raise ValueError("Duration must be a non-negative number")

        delta = timedelta(milliseconds=duration)
        start = datetime.now()
        end = start + delta

        try:
            while datetime.now() <= end:
                elapsed = datetime.now() - start
                colorizer.progress = min(
                    1.0, elapsed.total_seconds() / delta.total_seconds()
                )
                try:
                    _reskin(colorizer, window, element_filter, reskin_background)
                    window.refresh()  # Ensure UI updates during animation
                except TclError as e:
                    if "invalid command name" in str(e):
                        warn("Window was closed during reskinning")
                        return
                    raise  # Re-raise other TclErrors

                window.TKroot.update_idletasks()

        except Exception as e:
            warn(f"Error during animated reskin: {str(e)}")
            raise

    colorizer.progress = 1
    _reskin(colorizer, window, element_filter, reskin_background)

    if set_future:
        theme_function(new_theme)


def _reskin(
    colorizer: Colorizer,
    window: sg.Window,
    element_filter: Optional[ElementFilter] = None,
    reskin_background: bool = True,
) -> None:
    """Handles the actual reskinning of window elements.

    :param colorizer: Colorizer instance for handling color transformations
    :type colorizer: Colorizer
    :param window: Window to reskin
    :type window: sg.Window
    :param element_filter: Optional function to filter elements
    :type element_filter: Optional[ElementFilter]
    :param reskin_background: Whether to reskin the window background
    :type reskin_background: bool
    """
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
    """Toggle window transparency.

    :param window: Window to toggle transparency for
    :type window: sg.Window
    :raises AttributeError: If window doesn't support transparency
    :raises TclError: For Tkinter-related errors
    :raises ValueError: If the window background color is invalid
    """
    if not hasattr(window, "TKroot") or not hasattr(window, "set_transparent_color"):
        raise AttributeError("Window does not support transparency")

    try:
        window_bg = window.TKroot.cget("background")
        transparent_color = window.TKroot.attributes("-transparentcolor")
        window.set_transparent_color(window_bg if transparent_color == "" else "")
    except TclError as e:
        if "unknown color name" in str(e):
            raise ValueError(f"Invalid color value: {window_bg}") from e
        raise  # Re-raise other TclErrors
