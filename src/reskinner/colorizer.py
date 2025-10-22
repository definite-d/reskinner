from __future__ import annotations

from functools import lru_cache
from tkinter import Frame as TKFrame
from tkinter import Menu as TKMenu
from tkinter import Widget
from tkinter.ttk import Style
from typing import Any, Callable, Dict, Optional, Tuple, TypeVar, Union
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from colour import Color  # type: ignore[import-untyped]

from .constants import LRU_MAX_SIZE, ElementName, ScrollbarColorKey
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
def _default_element_cget(element_name: str, attribute: str) -> Union[str, Widget]:
    """Get an element attribute using cget.

    Internal use only.

    :param element_name: The name of the element
    :type element_name: str
    :param attribute: The attribute to pass to the cget function
    :type attribute: str
    :return: The result of the cget function
    :rtype: Union[str, Widget]
    """
    return DEFAULT_ELEMENTS[element_name].widget[attribute]


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
        return _default_element_cget(ElementName.CHECKBOX, "selectcolor") or "black"
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
        f"set defaultcombo [ttk::combobox::PopdownWindow {DEFAULT_ELEMENTS['combo'].widget}]",
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

    def _configure(
        self,
        attributes_to_theme_dict_color_keys: ThemeConfiguration,
        func_to_apply_configurations: Callable,
        func_to_get_default_color: Callable,
    ):
        """
        Internal use only.

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
        self._configure(
            configuration,
            element.widget.configure,
            lambda attribute: _default_element_cget(
                ElementName.from_element(element),
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
        self._configure(
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
        self._configure(configuration, window.TKroot.configure, _default_window_cget)

    # Specific

    def parent_row_frame(
        self,
        parent_row_frame: TKFrame,
        configuration: ThemeConfiguration,
    ):
        self._configure(
            configuration,
            parent_row_frame.configure,
            getattr(DEFAULT_ELEMENTS["text"], "ParentRowFrame").cget,
        )

    def menu_entry(
        self,
        menu: TKMenu,
        index: int,
        configuration: ThemeConfiguration,
    ):
        self._configure(
            configuration,
            lambda **_configurations: menu.entryconfigure(index, _configurations),
            lambda attribute: _default_element_cget("menu", attribute),
        )

    def optionmenu_menu(
        self,
        optionmenu: sg.OptionMenu,
        configuration: ThemeConfiguration,
    ):
        self._configure(
            configuration,
            optionmenu.widget["menu"].configure,
            _default_element_cget(ElementName.OPTIONMENU, "menu").cget,
        )

    def scrollbar(
        self,
        style_name: str,
        default_style: str,
    ):
        self.style(
            style_name,
            {
                "troughcolor": ScrollbarColorKey.TROUGH.value,
                "framecolor": ScrollbarColorKey.FRAME.value,
                "bordercolor": ScrollbarColorKey.FRAME.value,
            },
            default_style,
        )
        self.map(
            style_name,
            {
                "background": {
                    "selected": ScrollbarColorKey.BACKGROUND.value,
                    "active": ScrollbarColorKey.ARROW.value,
                    "background": ScrollbarColorKey.BACKGROUND.value,
                    "!focus": ScrollbarColorKey.BACKGROUND.value,
                },
                "arrowcolor": {
                    "selected": ScrollbarColorKey.ARROW.value,
                    "active": ScrollbarColorKey.BACKGROUND.value,
                    "background": ScrollbarColorKey.BACKGROUND.value,
                    "!focus": ScrollbarColorKey.ARROW.value,
                },
            },
            default_style,
        )

    def recurse_menu(self, tkmenu: Union[TKMenu, Widget]):
        """
        Internal use only.

        New and improved logic to change the theme of menus; we no longer take the lazy route of
        re-declaring new menu elements with each theme change - a method which Tkinter has an upper limit
        on. Rather, we recursively find and reconfigure the individual Menu objects that make up menus and
        submenus.

        :param tkmenu: The Tkinter menu object.
        :return: None
        """

        # This fixes issue #8. Thank you, @richnanney for reporting!
        if tkmenu.index("end") is None:
            return

        for index in range(0, tkmenu.index("end") + 1):
            self.menu_entry(
                tkmenu,
                index,
                {
                    "foreground": "TEXT_INPUT",
                    "background": "INPUT",
                    "activeforeground": "INPUT",
                    "activebackground": "TEXT_INPUT",
                },
            )

        for child in tkmenu.children.values():
            if issubclass(type(child), TKMenu):
                self.recurse_menu(child)

    def scrollable_column(self, column: sg.Column):
        self._configure(
            {"background": "BACKGROUND"},
            column.TKColFrame.configure,
            DEFAULT_ELEMENTS["column"].TKColFrame.cget,
        )
        self._configure(
            {"background": "BACKGROUND"},
            getattr(column.TKColFrame, "canvas").children["!frame"].configure,
            getattr(DEFAULT_ELEMENTS["column"].TKColFrame, "canvas")
            .children["!frame"]
            .cget,
        )

    def combo(self, combo: sg.Combo):
        # Configuring the listbox (popdown) of the combo.

        combo.widget.tk.call(
            "eval", f"set popdown [ttk::combobox::PopdownWindow {combo.widget}]"
        )

        def _configure_combo_popdown(**kwargs):
            for attribute, value in kwargs.items():
                combo.widget.tk.call(
                    "eval", f"$popdown.f.l configure -{attribute} {value}"
                )

        self._configure(
            {
                "background": "INPUT",
                "foreground": "TEXT_INPUT",
                "selectforeground": "INPUT",
                "selectbackground": "TEXT_INPUT",
            },
            _configure_combo_popdown,
            _default_combo_popdown_cget,
        )

        # Configuring the combo itself.
        style_name = combo.widget["style"]
        self.style(
            style_name,
            {
                "selectforeground": "TEXT_INPUT",
                "selectbackground": "INPUT",
                "selectcolor": "TEXT_INPUT",
                "foreground": "TEXT_INPUT",
                "background": ("BUTTON", 1),
                "arrowcolor": ("BUTTON", 0),
            },
            _default_element_cget("combo", "style"),
        )
        self.map(
            style_name,
            {
                "foreground": {"readonly": "TEXT_INPUT"},
                "fieldbackground": {"readonly": "INPUT"},
            },
            _default_element_cget("combo", "style"),
            True,
        )

    def checkbox_or_radio(self, element: Union[sg.Checkbox, sg.Radio]):
        element_name = ElementName.from_element(element)
        toggle = (
            _get_checkbox_radio_selectcolor(
                self._color(
                    "BACKGROUND",
                    lambda: _default_element_cget(element_name, "selectcolor"),
                ),
                self._color(
                    "TEXT",
                    lambda: _default_element_cget(element_name, "selectcolor"),
                ),
            ),
        )
        element.widget.configure(
            {"selectcolor": toggle}
        )  # A rare case where we use the configure method directly.
        self.element(
            element,
            {
                "background": "BACKGROUND",
                "foreground": "TEXT",
                "activebackground": "BACKGROUND",
                "activeforeground": "TEXT",
            },
        )

    def table_or_tree(self, element: Union[sg.Table, sg.Tree]):
        style_name = element.widget["style"]
        element_name = ElementName.from_element(element)
        default_style = element.widget.winfo_class()
        self.style(
            style_name,
            {
                "foreground": "TEXT",
                "background": "BACKGROUND",
                "fieldbackground": "BACKGROUND",
                "fieldcolor": "TEXT",
            },
            default_style,
            fallback="white",
        )
        self.map(
            style_name,
            {
                "foreground": {
                    "selected": ("BUTTON", 0),
                },
                "background": {
                    "selected": ("BUTTON", 1),
                },
            },
            default_style,
            True,
            fallback="white",
        )
        self.style(
            f"{style_name}.Heading",
            {
                "foreground": "TEXT_INPUT",
                "background": "INPUT",
            },
            f"{default_style}.Heading",
        )

        if element_name == "table":
            self.map(
                f"{style_name}.Heading",
                {
                    "foreground": {"active": "INPUT"},
                    "background": {"active": "TEXT_INPUT"},
                },
                f"{default_style}.Heading",
                True,
            )

    def progressbar(self, element: sg.ProgressBar):
        style_name = element.ttk_style_name
        self.style(
            style_name,
            {"background": ("PROGRESS", 0), "troughcolor": ("PROGRESS", 1)},
            _default_element_cget("progressbar", "style"),
        )
