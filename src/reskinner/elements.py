from tkinter import Frame as TKFrame
from tkinter import Menu as TKMenu
from tkinter.ttk import Widget as TTKWidget
from typing import Callable, Dict, List, Tuple, Type, Union

from .colorizer import (
    Colorizer,
    ThemeConfiguration,
    _default_combo_popdown_cget,
    _default_element_cget,
    _get_checkbox_radio_selectcolor,
)
from .constants import ALTER_MENU_ACTIVE_COLORS, ScrollbarColorKey
from .default_window import DEFAULT_ELEMENTS
from .sg import sg


class ElementDispatcher:
    """Efficient element handler dispatcher with pre-computed type mappings."""

    def __init__(self):
        # Direct type mappings for O(1) lookup
        self._type_handlers: Dict[Type, List[Callable]] = {}
        # Conditional handlers for special cases
        self._conditional_handlers: List[Tuple[Callable, Callable]] = []
        # Generic handlers that apply to all elements
        self._generic_handlers: List[Callable] = []

    def register_generic(self, handler: Callable) -> None:
        """Register a handler that applies to all elements."""
        self._generic_handlers.append(handler)

    def register_conditional(self, condition: Callable, handler: Callable) -> None:
        """Register a handler with a custom condition."""
        self._conditional_handlers.append((condition, handler))

    def register_type(self, element_type: Type, handler: Callable) -> None:
        """Register a handler for a specific element type."""
        if element_type not in self._type_handlers:
            self._type_handlers[element_type] = []
        self._type_handlers[element_type].append(handler)

    def dispatch(self, element) -> None:
        """Dispatch element to all appropriate handlers."""
        # Apply generic handlers first
        for handler in self._generic_handlers:
            handler(element)

        # Apply conditional handlers
        for condition, handler in self._conditional_handlers:
            if condition(element):
                handler(element)

        # Apply type-specific handlers
        for type_class, handlers in self._type_handlers.items():
            if isinstance(element, type_class):
                for handler in handlers:
                    handler(element)


class ElementReskinner:
    def __init__(self, colorizer: Colorizer):
        """
        Initializes an ElementReskinner instance.

        :param colorizer: The Colorizer instance to use for reskinning
        :type colorizer: Colorizer
        """
        self._titlebar_row_frame = "Not Set"
        self.colorizer: Colorizer = colorizer
        self._dispatcher = ElementDispatcher()
        self._register_handlers()

    def _register_handlers(self) -> None:
        """Register all element handlers."""
        # Generic handlers that apply to all elements
        self._dispatcher.register_generic(self._handle_generic_tweaks)
        self._dispatcher.register_generic(self._handle_right_click_menus)
        self._dispatcher.register_generic(self._handle_ttk_scrollbars)

        # Conditional handlers for special cases
        self._dispatcher.register_conditional(
            lambda e: e.metadata == sg.TITLEBAR_METADATA_MARKER,
            self._reskin_custom_titlebar,
        )
        self._dispatcher.register_conditional(
            lambda e: (
                self._titlebar_row_frame != "Not Set"
                and hasattr(e, 'widget')
                and str(e.widget).startswith(f"{self._titlebar_row_frame}.")
            ),
            self._reskin_titlebar_child,
        )

        # Type-specific handlers
        self._dispatcher.register_type(sg.Column, self._reskin_column)
        self._dispatcher.register_type(sg.Button, self._reskin_button)
        self._dispatcher.register_type(sg.ButtonMenu, self._reskin_buttonmenu)
        self._dispatcher.register_type(sg.Canvas, self._reskin_canvas)
        self._dispatcher.register_type(sg.Combo, self._reskin_combo)
        self._dispatcher.register_type(sg.Frame, self._reskin_frame)
        self._dispatcher.register_type(sg.Listbox, self._reskin_listbox)
        self._dispatcher.register_type(sg.Menu, self._reskin_menu)
        self._dispatcher.register_type(sg.ProgressBar, self._reskin_progressbar)
        self._dispatcher.register_type(sg.OptionMenu, self._reskin_optionmenu)
        self._dispatcher.register_type(sg.Sizegrip, self._reskin_sizegrip)
        self._dispatcher.register_type(sg.Slider, self._reskin_slider)
        self._dispatcher.register_type(sg.Spin, self._reskin_spin)
        self._dispatcher.register_type(sg.TabGroup, self._reskin_tabgroup)

        # Multi-type handlers
        self._dispatcher.register_type(sg.Checkbox, self._reskin_checkbox)
        self._dispatcher.register_type(sg.Radio, self._reskin_checkbox)
        self._dispatcher.register_type(sg.HorizontalSeparator, self._reskin_separator)
        self._dispatcher.register_type(sg.VerticalSeparator, self._reskin_separator)
        self._dispatcher.register_type(sg.Input, self._reskin_input)
        self._dispatcher.register_type(sg.Multiline, self._reskin_input)
        self._dispatcher.register_type(sg.Text, self._reskin_text)
        self._dispatcher.register_type(sg.StatusBar, self._reskin_text)
        self._dispatcher.register_type(sg.Table, self._reskin_table)
        self._dispatcher.register_type(sg.Tree, self._reskin_table)

    def _handle_generic_tweaks(self, element: sg.Element) -> None:
        """Handle generic tweaks that apply to most elements."""
        if (
            getattr(element, "ParentRowFrame", False)
            and element.metadata != sg.TITLEBAR_METADATA_MARKER
        ):
            self._parent_row_frame(element.ParentRowFrame, {"background": "BACKGROUND"})

        if element.widget and "background" in element.widget.keys() and element.widget.cget("background"):
            self.colorizer.element(element, {"background": "BACKGROUND"})

    def _handle_right_click_menus(self, element: sg.Element) -> None:
        """Handle right-click menus."""
        # Thanks for pointing this out @dwelden!
        if element.TKRightClickMenu:
            self._recurse_menu(element.TKRightClickMenu)

    def _handle_ttk_scrollbars(self, element: sg.Element) -> None:
        """Handle TTK scrollbars."""
        if getattr(element, "vsb_style_name", False):
            self._scrollbar(element.vsb_style_name, "Vertical.TScrollbar")
        if getattr(element, "hsb_style_name", False):
            self._scrollbar(element.hsb_style_name, "Horizontal.TScrollbar")
        if getattr(
            element, "ttk_style_name", False
        ) and element.ttk_style_name.endswith("TScrollbar"):
            if getattr(element, "Scrollable", False):
                digit, rest = (
                    getattr(element, "ttk_style_name")
                    .replace("Horizontal", "Vertical")
                    .split("_", 1)
                )
                digit = str(int(digit) - 1)
                vertical_style = f"{digit}_{rest}"
                self._scrollbar(vertical_style, "TScrollbar")
            self._scrollbar(element.ttk_style_name, "TScrollbar")

    def reskin_element(self, element: sg.Element):
        """
        Reskin an element.

        :param element: The PySimpleGUI element to reskin
        :type element: sg.Element
        """
        self._dispatcher.dispatch(element)

    # Specific Elements

    def _reskin_custom_titlebar(self, element: sg.Element):
        self.colorizer.element(element, {"background": ("BUTTON", 1)})
        if element.ParentRowFrame:
            self._parent_row_frame(
                element.ParentRowFrame, {"background": ("BUTTON", 1)}
            )
        self._titlebar_row_frame = str(element.ParentRowFrame)

    def _reskin_titlebar_child(self, element: sg.Element):
        self._parent_row_frame(element.ParentRowFrame, {"background": ("BUTTON", 1)})
        self.colorizer.element(element, {"background": ("BUTTON", 1)})
        if "foreground" in element.widget.keys():
            self.colorizer.element(element, {"foreground": ("BUTTON", 0)})

    def _reskin_button(self, element: sg.Button):
        if issubclass(element.widget.__class__, TTKWidget):  # For Ttk Buttons.
            style = element.widget.cget("style")
            self.colorizer.style(
                style,
                {
                    "background": ("BUTTON", 1),
                    "foreground": ("BUTTON", 0),
                },
                "TButton",
            )
            self.colorizer.map(
                style,
                {
                    "background": {
                        "pressed": ("BUTTON", 0),
                        "active": ("BUTTON", 0),
                    },
                    "foreground": {
                        "pressed": ("BUTTON", 1),
                        "active": ("BUTTON", 1),
                    },
                },
                "TButton",
            )
        else:  # For regular buttons.
            self.colorizer.element(
                element,
                {
                    "background": ("BUTTON", 1),
                    "foreground": ("BUTTON", 0),
                    "activebackground": ("BUTTON", 0),
                    "activeforeground": ("BUTTON", 1),
                },
            )

    def _reskin_buttonmenu(self, element: sg.ButtonMenu):
        self.colorizer.element(
            element,
            {
                "background": ("BUTTON", 1),
                "foreground": ("BUTTON", 0),
                "activebackground": ("BUTTON", 0),
                "activeforeground": ("BUTTON", 1),
            },
        )
        if getattr(element, "TKMenu", False):
            self._recurse_menu(element.TKMenu)

    def _reskin_canvas(self, element: sg.Canvas):
        self.colorizer.element(element, {"highlightbackground": "BACKGROUND"})

    def _reskin_column(self, element: sg.Column):
        # Apply background color to the Column's frame
        self.colorizer.configure(
            {"background": "BACKGROUND"},
            element.TKColFrame.configure,
            element.TKColFrame.cget
        )
        
        # Handle scrollable column inner frame if it exists
        canvas = getattr(element.TKColFrame, "canvas", None)
        if canvas and hasattr(canvas, "children") and "!frame" in canvas.children:
            self.colorizer.configure(
                {"background": "BACKGROUND"},
                canvas.children["!frame"].configure,
                getattr(DEFAULT_ELEMENTS[sg.Column].TKColFrame, "canvas")
                .children.get("!frame")
                .cget
                if "!frame"
                in getattr(
                    DEFAULT_ELEMENTS[sg.Column].TKColFrame, "canvas", {}
                ).children
                else lambda _: "white",
            )
        
        if self._is_pin_created_column(element):
            # Apply background to all child frames for columns created by sg.pin to fix the single pixel issue.
            for child in element.TKColFrame.winfo_children():
                if child.winfo_class() == 'Frame':
                    if self._is_empty_pin_frame(child):
                        self.colorizer.configure(
                            {"background": "BACKGROUND"},
                            child.configure,
                            child.cget
                        )

    def _reskin_combo(self, element: sg.Combo):
        # Configuring the listbox (popdown) of the combo.
        element.widget.tk.call(
            "eval", f"set popdown [ttk::combobox::PopdownWindow {element.widget}]"
        )

        def _configure_combo_popdown(**kwargs):
            for attribute, value in kwargs.items():
                element.widget.tk.call(
                    "eval", f"$popdown.f.l configure -{attribute} {value}"
                )

        self.colorizer.configure(
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
        style_name = element.widget["style"]
        self.colorizer.style(
            style_name,
            {
                "selectforeground": "TEXT_INPUT",
                "selectbackground": "INPUT",
                "selectcolor": "TEXT_INPUT",
                "foreground": "TEXT_INPUT",
                "background": ("BUTTON", 1),
                "arrowcolor": ("BUTTON", 0),
            },
            _default_element_cget(sg.Combo, "style"),
        )
        self.colorizer.map(
            style_name,
            {
                "foreground": {"readonly": "TEXT_INPUT"},
                "fieldbackground": {"readonly": "INPUT"},
            },
            _default_element_cget(sg.Combo, "style"),
            True,
        )

    def _reskin_frame(self, element: sg.Frame):
        self.colorizer.element(element, {"foreground": "TEXT"})

    def _reskin_listbox(self, element: sg.Listbox):
        self.colorizer.element(
            element,
            {
                "foreground": "TEXT_INPUT",
                "background": "INPUT",
                "selectforeground": "INPUT",
                "selectbackground": "TEXT_INPUT",
            },
        )

    def _reskin_menu(self, element: sg.Menu):
        self._recurse_menu(element.widget)

    def _reskin_progressbar(self, element: sg.ProgressBar):
        style_name = element.ttk_style_name
        self.colorizer.style(
            style_name,
            {"background": ("PROGRESS", 0), "troughcolor": ("PROGRESS", 1)},
            _default_element_cget(sg.ProgressBar, "style"),
        )

    def _reskin_optionmenu(self, element: sg.OptionMenu):
        self._optionmenu_menu(
            element,
            {
                "foreground": "TEXT_INPUT",
                "background": "INPUT",
            },
        )
        if ALTER_MENU_ACTIVE_COLORS:
            self._optionmenu_menu(
                element,
                {"activeforeground": "INPUT", "activebackground": "TEXT_INPUT"},
            )
        self.colorizer.element(
            element, {"foreground": "TEXT_INPUT", "background": "INPUT"}
        )

    def _reskin_sizegrip(self, element: sg.Sizegrip):
        sizegrip_style = element.widget.cget("style")
        self.colorizer.style(sizegrip_style, {"background": "BACKGROUND"}, "TSizegrip")

    def _reskin_slider(self, element: sg.Slider):
        self.colorizer.element(element, {"foreground": "TEXT", "troughcolor": "SCROLL"})

    def _reskin_spin(self, element: sg.Spin):
        self.colorizer.element(
            element,
            {
                "background": "INPUT",
                "foreground": "TEXT_INPUT",
                "buttonbackground": "INPUT",
            },
        )

    def _reskin_tabgroup(self, element: sg.TabGroup):
        style_name = element.widget.cget("style")
        self.colorizer.style(style_name, {"background": "BACKGROUND"}, "TNotebook")
        self.colorizer.style(
            f"{style_name}.Tab",
            {"background": "INPUT", "foreground": "TEXT_INPUT"},
            "TNotebook.Tab",
        )
        self.colorizer.map(
            f"{style_name}.Tab",
            {
                "foreground": {"pressed": ("BUTTON", 1), "selected": "TEXT"},
                "background": {"pressed": ("BUTTON", 0), "selected": "BACKGROUND"},
            },
            f"{style_name}.Tab",
            False,
        )

    def _reskin_checkbox(self, element: Union[sg.Checkbox, sg.Radio]):
        element_type = type(element)
        toggle = (
            _get_checkbox_radio_selectcolor(
                self.colorizer._color(
                    "BACKGROUND",
                    lambda: _default_element_cget(element_type, "selectcolor"),
                ),
                self.colorizer._color(
                    "TEXT",
                    lambda: _default_element_cget(element_type, "selectcolor"),
                ),
            ),
        )
        element.widget.configure(
            {"selectcolor": toggle}
        )  # A rare case where we use the configure method directly.
        self.colorizer.element(
            element,
            {
                "background": "BACKGROUND",
                "foreground": "TEXT",
                "activebackground": "BACKGROUND",
                "activeforeground": "TEXT",
            },
        )

    def _reskin_separator(
        self, element: Union[sg.HorizontalSeparator, sg.VerticalSeparator]
    ):
        style_name = element.widget.cget("style")
        self.colorizer.style(style_name, {"background": "BACKGROUND"}, "TSeparator")

    def _reskin_input(self, element: Union[sg.Input, sg.Multiline]):
        self.colorizer.element(
            element,
            {
                "foreground": "TEXT_INPUT",
                "background": "INPUT",
                "selectforeground": "INPUT",
                "selectbackground": "TEXT_INPUT",
                "insertbackground": "TEXT_INPUT",
            },
        )

    def _reskin_text(self, element: Union[sg.Text, sg.StatusBar]):
        self.colorizer.element(
            element,
            {
                "background": "BACKGROUND",
                "foreground": "TEXT",
            },
        )

    def _reskin_table(self, element: Union[sg.Table, sg.Tree]):
        style_name = element.widget["style"]
        element_type = type(element)
        default_style = element.widget.winfo_class()
        self.colorizer.style(
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
        self.colorizer.map(
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
        self.colorizer.style(
            f"{style_name}.Heading",
            {
                "foreground": "TEXT_INPUT",
                "background": "INPUT",
            },
            f"{default_style}.Heading",
        )

        if element_type == sg.Table:
            self.colorizer.map(
                f"{style_name}.Heading",
                {
                    "foreground": {"active": "INPUT"},
                    "background": {"active": "TEXT_INPUT"},
                },
                f"{default_style}.Heading",
                True,
            )

    def _parent_row_frame(
        self,
        parent_row_frame: TKFrame,
        configuration: ThemeConfiguration,
    ):
        self.colorizer.configure(
            configuration,
            parent_row_frame.configure,
            getattr(DEFAULT_ELEMENTS[sg.Text], "ParentRowFrame").cget,
        )

    def _recurse_menu(self, tkmenu):
        """
        Internal use only.

        New and improved logic to change the theme of menus; we no longer take the lazy route of
        re-declaring new menu elements with each theme change - a method which Tkinter has an upper limit
        on. Rather, we recursively find and reconfigure the individual Menu objects that make up menus and
        submenus.

        :param tkmenu: The Tkinter menu object.
        :return: None
        """
        end_menu_index = tkmenu.index("end")

        # This fixes issue #8. Thank you, @richnanney for reporting!
        if end_menu_index is None:
            return

        for index in range(0, end_menu_index + 1):
            self._menu_entry(
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
                self._recurse_menu(child)

    def _scrollable_column(self, column: sg.Column):
        self.colorizer.configure(
            {"background": "BACKGROUND"},
            column.TKColFrame.configure,
            DEFAULT_ELEMENTS[sg.Column].TKColFrame.cget,
        )
        # Handle the inner frame if it exists
        canvas = getattr(column.TKColFrame, "canvas", None)
        if canvas and hasattr(canvas, "children") and "!frame" in canvas.children:
            self.colorizer.configure(
                {"background": "BACKGROUND"},
                canvas.children["!frame"].configure,
                getattr(DEFAULT_ELEMENTS[sg.Column].TKColFrame, "canvas")
                .children.get("!frame")
                .cget
                if "!frame"
                in getattr(
                    DEFAULT_ELEMENTS[sg.Column].TKColFrame, "canvas", {}
                ).children
                else lambda _: "white",
            )

    def _is_pin_created_column(self, element: sg.Column) -> bool:
        """Check if this column was created by sg.pin() by examining its structure."""
        # sg.pin() creates columns with no key (None) and specific layout structure
        return element.Key is None and hasattr(element, 'TKColFrame')

    def _is_empty_pin_frame(self, frame) -> bool:
        """Check if this frame is an empty column created by sg.pin(shrink=True)."""
        try:
            # Empty pin frames have minimal children (usually just the empty column structure)
            children = frame.winfo_children()
            return len(children) <= 1  # Empty or nearly empty frames
        except Exception:
            return False

    def _menu_entry(
        self,
        menu: TKMenu,
        index: int,
        configuration: ThemeConfiguration,
    ):
        configuration = dict(
            filter(
                lambda item: item[0] in menu.entryconfigure(index).keys(),
                configuration.items(),
            )
        )
        # Filter the configs for menu entries that don't accept the full config dict. Fixes issue #11.
        # Brought back in v4.0.2 after its omission caused a regression leading to issue #22.
        self.colorizer.configure(
            configuration,
            lambda **_configurations: menu.entryconfigure(index, _configurations),
            lambda attribute: _default_element_cget(sg.Menu, attribute),
        )

    def _optionmenu_menu(
        self,
        optionmenu: sg.OptionMenu,
        configuration: ThemeConfiguration,
    ):
        self.colorizer.configure(
            configuration,
            optionmenu.widget["menu"].configure,
            _default_element_cget(sg.OptionMenu, "menu").cget,
        )

    def _scrollbar(
        self,
        style_name: str,
        default_style: str,
    ):
        self.colorizer.style(
            style_name,
            {
                "troughcolor": ScrollbarColorKey.TROUGH.value,
                "framecolor": ScrollbarColorKey.FRAME.value,
                "bordercolor": ScrollbarColorKey.FRAME.value,
            },
            default_style,
        )
        self.colorizer.map(
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
