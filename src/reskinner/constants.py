from enum import Enum

from ._compat import StrEnum
from .sg import sg

ALTER_MENU_ACTIVE_COLORS = True
DEFAULT_THEME_NAME = "GrayGrayGray"
LRU_MAX_SIZE = 10


class InterpolationMode(StrEnum):
    HSL = "hsl"
    HUE = "hue"
    RGB = "rgb"


def is_element_type(element, element_class):
    """
    Check if an element is of a specific PySimpleGUI type (including subclasses).

    :param element: The element to check
    :param element_class: The PySimpleGUI class to check against (e.g., sg.Button)
    :return: True if the element is of that type
    """
    return isinstance(element, element_class)


NON_GENERIC_ELEMENTS = [
    sg.Button,
    sg.HorizontalSeparator,
    sg.Listbox,
    sg.Multiline,
    sg.ProgressBar,
    sg.Sizegrip,
    sg.Spin,
    sg.TabGroup,
    sg.Table,
    sg.Text,
    sg.Tree,
    sg.VerticalSeparator,
]

_COLOR_MAPPING = {
    "Background Color": "BACKGROUND",
    "Button Background Color": ("BUTTON", 1),
    "Button Text Color": ("BUTTON", 0),
    "Input Element Background Color": "INPUT",
    "Input Element Text Color": "TEXT_INPUT",
    "Text Color": "TEXT",
    "Slider Color": "SCROLL",
}


class ScrollbarColorKey(Enum):
    TROUGH = _COLOR_MAPPING[sg.ttk_part_mapping_dict["Trough Color"]]
    FRAME = _COLOR_MAPPING[sg.ttk_part_mapping_dict["Frame Color"]]
    BACKGROUND = _COLOR_MAPPING[sg.ttk_part_mapping_dict["Background Color"]]
    ARROW = _COLOR_MAPPING[sg.ttk_part_mapping_dict["Arrow Button Arrow Color"]]
