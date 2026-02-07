from __future__ import annotations

from functools import lru_cache
from tkinter import Frame as TKFrame
from tkinter import Menu as TKMenu
from tkinter import Widget
from tkinter.ttk import Style
from typing import Any, Callable, Dict, Optional, Tuple, TypeVar, Union

from colour import Color  # type: ignore[import-untyped]

from ._compat import Literal, Type
from .constants import LRU_MAX_SIZE, ScrollbarColorKey
from .default_window import DEFAULT_ELEMENTS, DEFAULT_WINDOW
from .easing import EasingName, ease
from .interpolation import INTERPOLATION_MODES, InterpolationMethod
from .sg import sg

# Type variables and aliases
T = TypeVar("T")
ColorType = Union[str, Tuple[float, float, float], Tuple[float, float, float, float]]
ThemeDict = Dict[str, Union[str, int, Tuple[str, str]]]
ThemeDictColorKey = Union[str, Tuple[str, int]]
ThemeConfiguration = Dict[str, ThemeDictColorKey]
ElementFilter = Callable[[sg.Element], bool]  # type: ignore[valid-type]


def _is_valid_color(color: str) -> bool:
    """Check if a color string is valid.

    :param color: The color string to validate
    :type color: str
    :return: True if the color is valid, False otherwise
    :rtype: bool
    """
    if not color or not isinstance(color, str):
        return False

    try:
        # Try to create a Color object and get its hex representation
        Color(color).get_hex_l()
        return True
    except (ValueError, AttributeError):
        return False


def _normalize_tk_color(tk_color: str) -> Color:
    """Convert a Tkinter color to a Color object.

    :param tk_color: The Tkinter color string to convert
    :type tk_color: str
    :return: A Color object representing the input color
    :rtype: Color
    :raises RuntimeError: If default window is not properly initialized
    :raises ValueError: If the color cannot be converted
    """
    if not hasattr(DEFAULT_WINDOW, "TKroot"):
        raise RuntimeError("Default window not properly initialized")

    try:
        # Get RGB values from Tkinter (0-65535 range)
        rgb = DEFAULT_WINDOW.TKroot.winfo_rgb(tk_color)
        # Convert to 0-1 range expected by Color
        normalized = tuple(x / 65535 for x in rgb)

        result = Color()
        result.set_rgb(normalized)
        return result
    except Exception as e:
        raise ValueError(f"Failed to normalize Tk color '{tk_color}': {e}") from e


@lru_cache(maxsize=LRU_MAX_SIZE)
def _safe_color(
    value: Union[str, type(sg.COLOR_SYSTEM_DEFAULT)],  # type: ignore[valid-type]
    default_color_function: Callable[[], str],
) -> Color:
    """Safely convert a color value to a Color object, with caching.

    :param value: The color value to convert
    :type value: Union[str, type(sg.COLOR_SYSTEM_DEFAULT)]
    :param default_color_function: Function to get default color if conversion fails
    :type default_color_function: Callable[[], str]
    :return: The converted Color object
    :rtype: Color
    """
    try:
        return Color(value)
    except ValueError:
        return _normalize_tk_color(default_color_function())


def _default_window_cget(attribute: str) -> Any:
    """Get a window attribute using cget.

    Internal use only.

    :param attribute: The attribute to pass to the cget function
    :type attribute: str
    :return: The result of the cget function
    :rtype: Any
    """
    return DEFAULT_WINDOW.TKroot[attribute]


@lru_cache(maxsize=LRU_MAX_SIZE)
def _default_element_cget(element_class: Type, attribute: str) -> Union[str, Widget]:
    """
    Get the default value for an element's attribute.

    Internal use only.

    :param element_class: The class of the element
    :type element_class: Type
    :param attribute: The attribute to pass to the cget function
    :type attribute: str
    :return: The result of the cget function
    :rtype: Union[str, Widget]
    """
    # Try to find the element in DEFAULT_ELEMENTS, checking base classes if needed
    for cls in element_class.__mro__:
        if cls in DEFAULT_ELEMENTS:
            return DEFAULT_ELEMENTS[cls].widget[attribute]

    # Fallback: try to create a temporary element
    try:
        temp_element = element_class()
        return temp_element.widget[attribute]
    except Exception:
        # Final fallback: return a reasonable default
        return "black"


def _run_progressbar_computation(theme_dict: ThemeDict) -> ThemeDict:
    """Compute progress bar colors based on theme settings.

    :param theme_dict: The theme dictionary to modify
    :type theme_dict: ThemeDict
    :return: The modified theme dictionary
    :rtype: ThemeDict
    """
    if theme_dict["PROGRESS"] == sg.DEFAULT_PROGRESS_BAR_COMPUTE:
        theme_dict = theme_dict.copy()
        if (
            theme_dict["BUTTON"][1] != theme_dict["INPUT"]
            and theme_dict["BUTTON"][1] != theme_dict["BACKGROUND"]
        ):
            theme_dict["PROGRESS"] = (theme_dict["BUTTON"][1], theme_dict["INPUT"])
        else:
            theme_dict["PROGRESS"] = (theme_dict["TEXT_INPUT"], theme_dict["INPUT"])
    return theme_dict


# noinspection PyUnresolvedReferences
def _get_checkbox_radio_selectcolor(background_color, text_color) -> str:
    # PySimpleGUI's color conversion functions give different results than those of the colour module
    # due to floating point truncation, so I can't use the color module's functionality for everything here.
    if not all([_is_valid_color(background_color), _is_valid_color(text_color)]):
        return _default_element_cget(sg.Checkbox, "selectcolor") or "black"
    background_color: str = Color(background_color).get_hex_l()
    text_color: str = Color(text_color).get_hex_l()
    background_hsl: Tuple[float, float, float] = sg._hex_to_hsl(background_color)
    text_hsl: Tuple[float, float, float] = sg._hex_to_hsl(text_color)
    l_delta: float = (
        abs(text_hsl[2] - background_hsl[2])
        / 10
        * (1 if text_hsl[2] < background_hsl[2] else -1)
    )
    rgb_ = sg._hsl_to_rgb(
        background_hsl[0], background_hsl[1], background_hsl[2] + l_delta
    )
    result: str = sg.rgb(*rgb_)
    return result


@lru_cache(maxsize=LRU_MAX_SIZE)
def _default_combo_popdown_cget(attribute: str) -> str:
    """Get a combobox popdown attribute using cget.

    Internal use only.

    :param attribute: The attribute to retrieve
    :type attribute: str
    :return: The value of the requested attribute
    :rtype: str
    """
    DEFAULT_WINDOW.TKroot.tk.call(
        "eval",
        f"set defaultcombo [ttk::combobox::PopdownWindow {DEFAULT_ELEMENTS[sg.Combo].widget}]",
    )
    return DEFAULT_WINDOW.TKroot.tk.call("eval", f"$defaultcombo.f.l cget -{attribute}")


class Colorizer:
    def __init__(
        self,
        old_theme_dict: ThemeDict,
        new_theme_dict: ThemeDict,
        interpolation_mode: Literal["hsl", "hue", "rgb"] = "rgb",
        easing_function: Optional[Union[EasingName, Callable[[float], float]]] = None,
        progress: float = 0,
    ):
        self.old_theme_dict: ThemeDict = _run_progressbar_computation(old_theme_dict)
        self.new_theme_dict: ThemeDict = _run_progressbar_computation(new_theme_dict)
        self.progress: float = progress
        self.styler: Style = Style()
        self.interpolate: InterpolationMethod = INTERPOLATION_MODES[interpolation_mode]
        self.easing_function = easing_function

    def _color(
        self,
        key: ThemeDictColorKey,
        default_color_function: Callable[[], str],
    ) -> str:
        if isinstance(key, str):
            start, end = self.old_theme_dict[key], self.new_theme_dict[key]
        elif isinstance(key, tuple):
            key, index = key
            start, end = (
                self.old_theme_dict[key][index],
                self.new_theme_dict[key][index],
            )
        else:
            raise ValueError("Invalid theme_dict key")

        try:
            start = _safe_color(start, default_color_function)
            end = _safe_color(end, default_color_function)
        except ValueError:
            raise ValueError("The referenced theme_dict value is not a valid color.")

        return self.interpolate(
            start, end, ease(self.progress, self.easing_function)
        ).get_hex_l()

    def configure(
        self,
        attributes_to_theme_dict_color_keys: ThemeConfiguration,
        func_to_apply_configurations: Callable,
        func_to_get_default_color: Callable,
    ):
        """
        Configures the colors of anything (elements, widgets, styles etc.) safely by calling a config function and
        supplying processed colors.

        :return: None
        """
        _configurations = {
            attribute: self._color(
                theme_dict_color_key, lambda: func_to_get_default_color(attribute)
            )
            for attribute, theme_dict_color_key in attributes_to_theme_dict_color_keys.items()
        }
        func_to_apply_configurations(**_configurations)

    # Generic

    def element(
        self,
        element: sg.Element,
        configuration: ThemeConfiguration,
    ):
        self.configure(
            configuration,
            element.widget.configure,
            lambda attribute: _default_element_cget(
                type(element),
                attribute,
            ),
        )

    def style(
        self,
        style: str,
        configuration: ThemeConfiguration,
        default_style: str,
        fallback: str = "black",
    ):
        # if self.styler.configure(style) is None:
        #     raise ReskinnerException(f"`{style}` doesn't exist.")
        self.configure(
            configuration,
            lambda **kwargs: self.styler.configure(style, **kwargs),
            lambda attribute: self.styler.lookup(
                default_style, attribute, default=fallback
            ),
        )

    def map(
        self,
        style: str,
        configurations: Dict[str, ThemeConfiguration],
        default_style: str,
        pass_state: bool = False,
        fallback: str = "black",
    ) -> None:
        # if self.styler.configure(style) is None:
        #     raise ReskinnerException(f"`{style}` doesn't exist.")
        values = {
            configuration_key: [
                (
                    k,
                    self._color(
                        v,
                        lambda: self.styler.lookup(
                            default_style,
                            configuration_key,
                            [k] if pass_state else None,
                            fallback,
                        ),
                    ),
                )
                for k, v in configuration.items()
            ]
            for configuration_key, configuration in configurations.items()
        }
        self.styler.map(style, **values)

    def window(
        self,
        window: sg.Window,
        configuration: ThemeConfiguration,
    ):
        if window.TKroot:
            self.configure(
                configuration,
                window.TKroot.configure,
                _default_window_cget,
            )
