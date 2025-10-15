from tkinter.ttk import Widget as TTKWidget
from typing import Union

from .colorizer import Colorizer
from .constants import ALTER_MENU_ACTIVE_COLORS, ElementName
from .sg import sg


class ElementReskinner:
    def __init__(self, colorizer: Colorizer):
        """
        Initializes an ElementReskinner instance.

        :param colorizer: The Colorizer instance to use for reskinning
        :type colorizer: Colorizer
        """
        self._titlebar_row_frame = "Not Set"
        self.colorizer: Colorizer = colorizer

    def reskin_element(self, element: sg.Element):
        """
        Reskin an element based on its type.

        :param element: The PySimpleGUI element to reskin
        :type element: sg.Element
        """

        element_name = ElementName.from_element(element)

        # Generic tweaks
        if (
            getattr(element, "ParentRowFrame", False)
            and element.metadata != sg.TITLEBAR_METADATA_MARKER
        ):
            self.colorizer.parent_row_frame(
                element.ParentRowFrame, {"background": "BACKGROUND"}
            )

        if "background" in element.widget.keys() and element.widget.cget("background"):
            self.colorizer.element(element, {"background": "BACKGROUND"})

        # Right Click Menus (thanks for pointing this out @dwelden!)
        if element.TKRightClickMenu:
            self.colorizer.recurse_menu(element.TKRightClickMenu)

        # TTK Scrollbars
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

        # Python 3.7-compatible match/case.
        element_specific_reskin_function = {
            (element.metadata == sg.TITLEBAR_METADATA_MARKER): self._titlebar_row_frame,
            (
                str(element.widget).startswith(f"{self._titlebar_row_frame}.")
            ): self._reskin_titlebar_child,
            (
                (element_name == ElementName.COLUMN)
                and (getattr(element, "TKColFrame", "Not Set") != "Not Set")
            ): self._reskin_scrollable_column,
            (element_name == ElementName.BUTTON): self._reskin_button,
            (element_name == ElementName.BUTTONMENU): self._reskin_buttonmenu,
            (element_name == ElementName.CANVAS): self._reskin_canvas,
            (element_name == ElementName.COMBO): self._reskin_combo,
            (element_name == ElementName.FRAME): self._reskin_frame,
            (element_name == ElementName.LISTBOX): self._reskin_listbox,
            (element_name == ElementName.MENU): self._reskin_menu,
            (element_name == ElementName.PROGRESSBAR): self._reskin_progressbar,
            (element_name == ElementName.OPTIONMENU): self._reskin_optionmenu,
            (element_name == ElementName.SIZEGRIP): self._reskin_sizegrip,
            (element_name == ElementName.SLIDER): self._reskin_slider,
            (element_name == ElementName.SPIN): self._reskin_spin,
            (element_name == ElementName.TABGROUP): self._reskin_tabgroup,
            (
                element_name in (ElementName.CHECKBOX, ElementName.RADIO)
            ): self._reskin_checkbox,
            (
                element_name
                in (ElementName.HORIZONTALSEPARATOR, ElementName.VERTICALSEPARATOR)
            ): self._reskin_separator,
            (
                element_name in (ElementName.INPUT, ElementName.MULTILINE)
            ): self._reskin_input,
            (
                element_name in (ElementName.TEXT, ElementName.STATUSBAR)
            ): self._reskin_text,
            (element_name in (ElementName.TABLE, ElementName.TREE)): self._reskin_table,
        }.get(True, False)

        if element_specific_reskin_function:
            element_specific_reskin_function(element)

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
