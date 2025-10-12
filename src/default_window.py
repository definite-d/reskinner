from .sg import sg
from .constants import DEFAULT_THEME_NAME, SGElement


_previous_theme = sg.theme()
sg.theme(DEFAULT_THEME_NAME)

_tree_data = sg.TreeData()
_tree_data.Insert(
    "",
    "_A_",
    "Tree Item 1",
    [1234],
)

DEFAULT_ELEMENTS = {
    SGElement.BUTTON: sg.Button(),
    SGElement.BUTTONMENU: sg.ButtonMenu("", sg.MENU_RIGHT_CLICK_EDITME_EXIT),
    SGElement.CANVAS: sg.Canvas(),
    SGElement.CHECKBOX: sg.Checkbox(""),
    SGElement.COLUMN: sg.Column([[sg.Text()]], scrollable=True),
    SGElement.COMBO: sg.Combo([""]),
    SGElement.FRAME: sg.Frame("", [[sg.Text()]]),
    SGElement.GRAPH: sg.Graph((2, 2), (0, 2), (2, 0)),
    SGElement.HORIZONTALSEPARATOR: sg.HorizontalSeparator(),  # 'image': sg.Image(),
    SGElement.INPUT: sg.Input(),
    SGElement.IMAGE: sg.Image(),
    SGElement.LISTBOX: sg.Listbox([""]),
    SGElement.MENU: sg.Menu([["File", ["Exit"]], ["Edit", ["Edit Me"]]]),
    SGElement.MULTILINE: sg.Multiline(),
    SGElement.OPTIONMENU: sg.OptionMenu([""]),
    SGElement.PANE: sg.Pane([sg.Column([[sg.Text()]]), sg.Column([[sg.Text()]])]),
    SGElement.PROGRESSBAR: sg.ProgressBar(0),
    SGElement.RADIO: sg.Radio("", 0),
    SGElement.SIZEGRIP: sg.Sizegrip(),
    SGElement.SLIDER: sg.Slider(),
    SGElement.SPIN: sg.Spin([0]),
    SGElement.STATUSBAR: sg.StatusBar(""),
    SGElement.TABGROUP: sg.TabGroup([[sg.Tab("", [[sg.Text()]], key="tab")]]),
    SGElement.TABLE: sg.Table([["asdf"]]),
    SGElement.TEXT: sg.Text(),
    SGElement.TREE: sg.Tree(_tree_data, [""], num_rows=1),
    SGElement.VERTICALSEPARATOR: sg.VerticalSeparator(),
}

# A completely invisible window, which should at worst show a
# small line at the top-right of the left display if
# viewed on a Raspberry Pi with multiple monitors. Unlikely.
DEFAULT_WINDOW = sg.Window(
    "",
    [[element] for element in DEFAULT_ELEMENTS.values()],
    size=(1, 1),
    no_titlebar=True,
    alpha_channel=0,
    location=(-1, -1),
).finalize()

DEFAULT_ELEMENTS["tab"] = DEFAULT_WINDOW["tab"]
sg.theme(_previous_theme)
