from tkinter.ttk import Widget as TTKWidget
from typing import Callable, Dict, List, Tuple, Type, Union

from .colorizer import Colorizer
from .constants import ALTER_MENU_ACTIVE_COLORS, is_element_type
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
        element_type = type(element)
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
            self._reskin_custom_titlebar
        )
        self._dispatcher.register_conditional(
            lambda e: str(e.widget).startswith(f"{self._titlebar_row_frame}."),
            self._reskin_titlebar_child
        )
        self._dispatcher.register_conditional(
            lambda e: (is_element_type(e, sg.Column) and (getattr(e, "TKColFrame", "Not Set") != "Not Set")),
            self._reskin_scrollable_column
        )
        
        # Type-specific handlers
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
            self.colorizer.parent_row_frame(
                element.ParentRowFrame, {"background": "BACKGROUND"}
            )

        if "background" in element.widget.keys() and element.widget.cget("background"):
            self.colorizer.element(element, {"background": "BACKGROUND"})

    def _handle_right_click_menus(self, element: sg.Element) -> None:
        """Handle right-click menus."""
        # Thanks for pointing this out @dwelden!
        if element.TKRightClickMenu:
            self.colorizer.recurse_menu(element.TKRightClickMenu)

    def _handle_ttk_scrollbars(self, element: sg.Element) -> None:
        """Handle TTK scrollbars."""
        if getattr(element, "vsb_style_name", False):
            self.colorizer.scrollbar(element.vsb_style_name, "Vertical.TScrollbar")
        if getattr(element, "hsb_style_name", False):
            self.colorizer.scrollbar(element.hsb_style_name, "Horizontal.TScrollbar")
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
                self.colorizer.scrollbar(vertical_style, "TScrollbar")
            self.colorizer.scrollbar(element.ttk_style_name, "TScrollbar")

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
            self.colorizer.parent_row_frame(
                element.ParentRowFrame, {"background": ("BUTTON", 1)}
            )
        self.titlebar_row_frame = str(element.ParentRowFrame)

    def _reskin_titlebar_child(self, element: sg.Element):
        self.colorizer.parent_row_frame(
            element.ParentRowFrame, {"background": ("BUTTON", 1)}
        )
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
            self.colorizer.recurse_menu(element.TKMenu)

    def _reskin_canvas(self, element: sg.Canvas):
        self.colorizer.element(element, {"highlightbackground": "BACKGROUND"})

    def _reskin_scrollable_column(self, element: sg.Column):
        if hasattr(
            element.TKColFrame, "canvas"
        ):  # This means the column is scrollable.
            self.colorizer.scrollable_column(element)

    def _reskin_combo(self, element: sg.Combo):
        self.colorizer.combo(element)

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
        self.colorizer.recurse_menu(element.widget)

    def _reskin_progressbar(self, element: sg.ProgressBar):
        self.colorizer.progressbar(element)

    def _reskin_optionmenu(self, element: sg.OptionMenu):
        self.colorizer.optionmenu_menu(
            element,
            {
                "foreground": "TEXT_INPUT",
                "background": "INPUT",
            },
        )
        if ALTER_MENU_ACTIVE_COLORS:
            self.colorizer.optionmenu_menu(
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
        self.colorizer.checkbox_or_radio(element)

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
        self.colorizer.table_or_tree(element)
