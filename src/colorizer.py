from tkinter.ttk import Style
from tkinter import Frame as TKFrame, Menu as TKMenu, Widget
from typing import Dict, Union, Tuple, Callable
from colour import Color
from functools import lru_cache

from .constants import ElementName, ScrollbarColorKey
from .default_window import DEFAULT_ELEMENTS, DEFAULT_WINDOW
from .sg import sg

ThemeDict = Dict[str, Union[str, int, Tuple[str, str]]]
ThemeDictColorKey = Union[str, Tuple[str, int]]
ThemeConfiguration = Dict[str, ThemeDictColorKey]


def _is_valid_color(color: str) -> bool:
    """
    Internal use only.

    Checks if a color is valid or not

    :param color: A color string to be checked.
    :return: True or False.
    """
    if not color:
        return False
    try:
        Color(color).get_hex_l()
    except ValueError:
        return False
    else:
        return True


def _normalize_tk_color(tk_color) -> str:
    """
    Internal use only.

    Converts TK system colors to regular hex colors.

    :param tk_color: The TK color to be converted.
    :return: A hex color string.
    """
    result = Color()
    result.set_rgb(tuple(x / 65535 for x in DEFAULT_WINDOW.TKroot.winfo_rgb(tk_color)))
    return result.get_hex_l()


@lru_cache
def _safe_color(
    value: Union[str, type(sg.COLOR_SYSTEM_DEFAULT)],
    default_color: str,
) -> str:
    """
    Internal use only.

    If the value is a valid color, we return that. Otherwise, we return the default color.

    :param value: The value to check for safety.
    :param default_color: The expected default color.
    :return: A TK-safe color, no matter what the input value is.
    """
    if _is_valid_color(value):
        return value
    return _normalize_tk_color(default_color)


def _default_window_cget(attribute: str):
    """
    Internal use only.

    Shortcut function that calls the cget function of the default window.

    :param attribute: The attribute to pass to the cget function.
    :return: The result of the cget function.
    """
    return DEFAULT_WINDOW.TKroot[attribute]


def _default_element_cget(element_name: str, attribute: str):
    """
    Internal use only.

    Shortcut function that calls the cget function of a default element.

    :param element_name: The name of the element.
    :param attribute: The attribute to pass to the cget function.
    :return: The result of the cget function.
    """
    return DEFAULT_ELEMENTS[element_name].widget[attribute]


def _run_progressbar_computation(theme_dict: ThemeDict):
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


def _get_checkbox_radio_selectcolor(background_color, text_color) -> str:
    # PySimpleGUI's color conversion functions give different results than those of the colour module, so I can't
    # use the color module's functionality for everything here.
    if not all([_is_valid_color(background_color), _is_valid_color(text_color)]):
        return _default_element_cget(ElementName.CHECKBOX, "selectcolor") or "black"
    background_color: str = Color(background_color).get_hex_l()
    text_color: str = Color(text_color).get_hex_l()
    # TODO: Get the actual locations of these functions.
    background_hsl: Tuple[float, float, float] = _hex_to_hsl(background_color)
    text_hsl: Tuple[float, float, float] = _hex_to_hsl(text_color)
    l_delta: float = (
        abs(text_hsl[2] - background_hsl[2])
        / 10
        * (1 if text_hsl[2] < background_hsl[2] else -1)
    )
    rgb_ = _hsl_to_rgb(
        background_hsl[0], background_hsl[1], background_hsl[2] + l_delta
    )
    result: str = sg.rgb(*rgb_)
    return result


@lru_cache
def _get_combo_popdown_default(attribute):
    DEFAULT_WINDOW.TKroot.tk.call(
        "eval",
        f"set defaultcombo [ttk::combobox::PopdownWindow {DEFAULT_ELEMENTS['combo'].widget}]",
    )
    return DEFAULT_WINDOW.TKroot.tk.call("eval", f"$defaultcombo.f.l cget -{attribute}")


@lru_cache
def _get_combo_listbox_default(attribute):
    DEFAULT_WINDOW.TKroot.tk.call(
        "eval",
        f"set defaultcombo [ttk::combobox::PopdownWindow {DEFAULT_ELEMENTS['combo'].widget}]",
    )
    return DEFAULT_WINDOW.TKroot.tk.call("eval", f"$defaultcombo.f.l cget -{attribute}")


class Colorizer:
    def __init__(
        self,
        theme_dict: ThemeDict,
        styler: Union[Style, None] = None,
    ):
        self.theme_dict = _run_progressbar_computation(theme_dict)
        self.styler = styler if styler else Style()

    def _get_color_by_themedict_color_key(self, key: ThemeDictColorKey):
        if isinstance(key, str):
            return self.theme_dict[key]
        elif isinstance(key, tuple):
            key, index = key
            return self.theme_dict[key][index]
        else:
            raise ValueError("Invalid themedict key")

    def _configure(
        self,
        attributes_to_themedict_color_keys: ThemeConfiguration,
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
            attribute: _safe_color(
                self._get_color_by_themedict_color_key(theme_dict_color_key),
                func_to_get_default_color(attribute),
            )
            for attribute, theme_dict_color_key in attributes_to_themedict_color_keys.items()
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
                    _safe_color(
                        self._get_color_by_themedict_color_key(v),
                        self.styler.lookup(
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

    def combo_popdown(
        self,
        combo: sg.Combo,
        configuration: ThemeConfiguration,
    ):
        combo.widget.tk.call(
            "eval", f"set popdown [ttk::combobox::PopdownWindow {combo.widget}]"
        )

        def _configure_combo_popdown(**kwargs):
            command = "$popdown.f.l configure"
            for attribute, value in kwargs.items():
                command += f" -{attribute} {value}"
            combo.widget.tk.call("eval", command)

        self._configure(
            configuration, _configure_combo_popdown, _get_combo_popdown_default
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
        # Configuring the listbox of the combo.

        combo.widget.tk.call(
            "eval", f"set popdown [ttk::combobox::PopdownWindow {combo.widget}]"
        )

        def _configure_combo_listbox(**kwargs):
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
            _configure_combo_listbox,
            _get_combo_listbox_default,
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
        toggle = _get_checkbox_radio_selectcolor(
            _safe_color(
                self._get_color_by_themedict_color_key("BACKGROUND"),
                _default_element_cget(element_name, "selectcolor"),
            ),
            _safe_color(
                self._get_color_by_themedict_color_key("TEXT"),
                _default_element_cget(element_name, "selectcolor"),
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
                # "text": "TEXT",
            },
        )

    def table_or_tree(self, element: Union[sg.Table, sg.Tree]):
        style_name = element.widget["style"]
        element_name = ElementName.from_element(element)
        default_style = _default_element_cget(element_name, "style")
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
