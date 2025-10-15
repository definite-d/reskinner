from enum import Enum

try:
    from enum import StrEnum
except ImportError:
    # Python < 3.11
    from strenum import StrEnum

from .sg import sg

ALTER_MENU_ACTIVE_COLORS = True
DEFAULT_THEME_NAME = "GrayGrayGray"
LRU_MAX_SIZE = 10


class InterpolationMode(StrEnum):
    HSL = "hsl"
    HUE = "hue"
    RGB = "rgb"


class ElementName(StrEnum):
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
    TAB = "tab"
    TABGROUP = "tabgroup"
    TABLE = "table"
    TEXT = "text"
    TREE = "tree"
    VERTICALSEPARATOR = "verticalseparator"

    @staticmethod
    def from_element(element: sg.Element):
        return ElementName(type(element).__name__.lower())


NON_GENERIC_ELEMENTS = [
    ElementName.BUTTON,
    ElementName.HORIZONTALSEPARATOR,
    ElementName.LISTBOX,
    ElementName.MULTILINE,
    ElementName.PROGRESSBAR,
    ElementName.SIZEGRIP,
    ElementName.SPIN,
    ElementName.TABGROUP,
    ElementName.TABLE,
    ElementName.TEXT,
    ElementName.TREE,
    ElementName.VERTICALSEPARATOR,
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
