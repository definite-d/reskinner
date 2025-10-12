from enum import StrEnum
from .sg import sg


DEFAULT_ANIMATED_RESKIN_DURATION = 450
DISABLED_COLOR = "#A3A3A3"

class InterpolationMode(StrEnum):
    HSL = 'hsv'
    HUE = 'hue'
    RGB = 'rgb'

class SGElement(StrEnum):
    BUTTON = "button",
    HORIZONTAL_SEPARATOR = "horizontalseparator",
    LISTBOX = "listbox",
    MULTILINE = "multiline",
    PROGRESSBAR = "progressbar",
    SIZEGRIP = "sizegrip",
    SPIN = "spin",
    TABGROUP = "tabgroup",
    TABLE = "table",
    TEXT = "text",
    TREE = "tree",
    VERTICAL_SEPARATOR = "verticalseparator",

NON_GENERIC_ELEMENTS = [
    SGElement.BUTTON,
    SGElement.HORIZONTAL_SEPARATOR,
    SGElement.LISTBOX,
    SGElement.MULTILINE,
    SGElement.PROGRESSBAR,
    SGElement.SIZEGRIP,
    SGElement.SPIN,
    SGElement.TABGROUP,
    SGElement.TABLE,
    SGElement.TEXT,
    SGElement.TREE,
    SGElement.VERTICAL_SEPARATOR,
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

class ScrollbarColorKey(StrEnum):
    TROUGH = _COLOR_MAPPING[ttk_part_mapping_dict["Trough Color"]]
    FRAME = _COLOR_MAPPING[ttk_part_mapping_dict["Frame Color"]]
    BACKGROUND = _COLOR_MAPPING[ttk_part_mapping_dict["Background Color"]]
    ARROW = _COLOR_MAPPING[ttk_part_mapping_dict["Arrow Button Arrow Color"]]
