from enum import StrEnum

from .sg import sg


DEFAULT_ANIMATED_RESKIN_DURATION = 450
DISABLED_COLOR = "#A3A3A3"
DEFAULT_THEME_NAME = "GrayGrayGray"


class InterpolationMode(StrEnum):
    HSL = "hsl"
    HUE = "hue"
    RGB = "rgb"


class SGElement(StrEnum):
    BUTTON = "button"
    BUTTONMENU = "buttonmenu"
    CANVAS = "canvas"
    CHECKBOX = "checkbox"
    COLUMN = "column"
    COMBO = "combo"
    FRAME = "frame"
    GRAPH = "graph"
    HORIZONTALSEPARATOR = "horizontalseparator"
    IMAGE = "image"
    INPUT = "input"
    LISTBOX = "listbox"
    MENU = "menu"
    MULTILINE = "multiline"
    OPTIONMENU = "optionmenu"
    PANE = "pane"
    PROGRESSBAR = "progressbar"
    RADIO = "radio"
    SIZEGRIP = "sizegrip"
    SLIDER = "slider"
    SPIN = "spin"
    STATUSBAR = "statusbar"
    TABGROUP = "tabgroup"
    TABLE = "table"
    TEXT = "text"
    TREE = "tree"
    VERTICALSEPARATOR = "verticalseparator"


NON_GENERIC_ELEMENTS = [
    SGElement.BUTTON,
    SGElement.HORIZONTALSEPARATOR,
    SGElement.LISTBOX,
    SGElement.MULTILINE,
    SGElement.PROGRESSBAR,
    SGElement.SIZEGRIP,
    SGElement.SPIN,
    SGElement.TABGROUP,
    SGElement.TABLE,
    SGElement.TEXT,
    SGElement.TREE,
    SGElement.VERTICALSEPARATOR,
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
    TROUGH = _COLOR_MAPPING[sg.ttk_part_mapping_dict["Trough Color"]]
    FRAME = _COLOR_MAPPING[sg.ttk_part_mapping_dict["Frame Color"]]
    BACKGROUND = _COLOR_MAPPING[sg.ttk_part_mapping_dict["Background Color"]]
    ARROW = _COLOR_MAPPING[sg.ttk_part_mapping_dict["Arrow Button Arrow Color"]]
