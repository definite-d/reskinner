from .constants import DEFAULT_THEME_NAME
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
    sg.Button: sg.Button(),
    sg.ButtonMenu: sg.ButtonMenu("", sg.MENU_RIGHT_CLICK_EDITME_EXIT),
    sg.Canvas: sg.Canvas(),
    sg.Checkbox: sg.Checkbox(""),
    sg.Column: sg.Column([[sg.Text()]], scrollable=True),
    sg.Combo: sg.Combo([""]),
    sg.Frame: sg.Frame("", [[sg.Text()]]),
    sg.Graph: sg.Graph((2, 2), (0, 2), (2, 0)),
    sg.HorizontalSeparator: sg.HorizontalSeparator(),  # 'image': sg.Image(),
    sg.Input: sg.Input(),
    sg.Image: sg.Image(),
    sg.Listbox: sg.Listbox([""]),
    sg.Menu: sg.Menu([["File", ["Exit"]], ["Edit", ["Edit Me"]]]),
    sg.Multiline: sg.Multiline(),
    sg.OptionMenu: sg.OptionMenu([""]),
    sg.Pane: sg.Pane([sg.Column([[sg.Text()]]), sg.Column([[sg.Text()]])]),
    sg.ProgressBar: sg.ProgressBar(0),
    sg.Radio: sg.Radio("", 0),
    sg.Sizegrip: sg.Sizegrip(),
    sg.Slider: sg.Slider(),
    sg.Spin: sg.Spin([0]),
    sg.StatusBar: sg.StatusBar(""),
    sg.TabGroup: sg.TabGroup([[sg.Tab("", [[sg.Text()]], key="tab")]]),
    sg.Table: sg.Table([["asdf"]]),
    sg.Text: sg.Text(),
    sg.Tree: sg.Tree(_tree_data, [""], num_rows=1),
    sg.VerticalSeparator: sg.VerticalSeparator(),
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
DEFAULT_WINDOW.close()
