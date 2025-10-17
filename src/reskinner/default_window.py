from .constants import DEFAULT_THEME_NAME, ElementName
from .sg import sg

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
    ElementName.BUTTON: sg.Button(),
    ElementName.BUTTONMENU: sg.ButtonMenu("", sg.MENU_RIGHT_CLICK_EDITME_EXIT),
    ElementName.CANVAS: sg.Canvas(),
    ElementName.CHECKBOX: sg.Checkbox(""),
    ElementName.COLUMN: sg.Column([[sg.Text()]], scrollable=True),
    ElementName.COMBO: sg.Combo([""]),
    ElementName.FRAME: sg.Frame("", [[sg.Text()]]),
    ElementName.GRAPH: sg.Graph((2, 2), (0, 2), (2, 0)),
    ElementName.HORIZONTALSEPARATOR: sg.HorizontalSeparator(),  # 'image': sg.Image(),
    ElementName.INPUT: sg.Input(),
    ElementName.IMAGE: sg.Image(),
    ElementName.LISTBOX: sg.Listbox([""]),
    ElementName.MENU: sg.Menu([["File", ["Exit"]], ["Edit", ["Edit Me"]]]),
    ElementName.MULTILINE: sg.Multiline(),
    ElementName.OPTIONMENU: sg.OptionMenu([""]),
    ElementName.PANE: sg.Pane([sg.Column([[sg.Text()]]), sg.Column([[sg.Text()]])]),
    ElementName.PROGRESSBAR: sg.ProgressBar(0),
    ElementName.RADIO: sg.Radio("", 0),
    ElementName.SIZEGRIP: sg.Sizegrip(),
    ElementName.SLIDER: sg.Slider(),
    ElementName.SPIN: sg.Spin([0]),
    ElementName.STATUSBAR: sg.StatusBar(""),
    ElementName.TABGROUP: sg.TabGroup([[sg.Tab("", [[sg.Text()]], key="tab")]]),
    ElementName.TABLE: sg.Table([["asdf"]]),
    ElementName.TEXT: sg.Text(),
    ElementName.TREE: sg.Tree(_tree_data, [""], num_rows=1),
    ElementName.VERTICALSEPARATOR: sg.VerticalSeparator(),
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
