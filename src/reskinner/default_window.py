from FreeSimpleGUI import _convert_window_to_tk, InitializeResults
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
    sg.Button: sg.Button(size=(1, 1)),
    sg.ButtonMenu: sg.ButtonMenu("", sg.MENU_RIGHT_CLICK_EDITME_EXIT, size=(1, 1)),
    sg.Canvas: sg.Canvas(size=(1, 1)),
    sg.Checkbox: sg.Checkbox("", size=(1, 1)),
    sg.Column: sg.Column([[sg.Text()]], scrollable=True, size=(1, 1)),
    sg.Combo: sg.Combo([""], size=(1, 1)),
    sg.Frame: sg.Frame("", [[sg.Text(size=(1, 1))]], size=(1, 1)),
    sg.Graph: sg.Graph((1, 1), (0, 0), (1, 1)),
    sg.HorizontalSeparator: sg.HorizontalSeparator(),
    sg.Input: sg.Input(size=(1, 1)),
    sg.Image: sg.Image(size=(1, 1)),
    sg.Listbox: sg.Listbox([""], size=(1, 1)),
    sg.Menu: sg.Menu([["File", ["Exit"]], ["Edit", ["Edit Me"]]], size=(1, 1)),
    sg.Multiline: sg.Multiline(size=(1, 1)),
    sg.OptionMenu: sg.OptionMenu([""], size=(1, 1)),
    sg.Pane: sg.Pane([sg.Column([[sg.Text(size=(1, 1))]], size=(1, 1))]),
    sg.ProgressBar: sg.ProgressBar(0, size=(1, 1)),
    sg.Radio: sg.Radio("", 0, size=(1, 1)),
    sg.Sizegrip: sg.Sizegrip(),
    sg.Slider: sg.Slider(size=(1, 1)),
    sg.Spin: sg.Spin([0], size=(1, 1)),
    sg.StatusBar: sg.StatusBar("", size=(1, 1)),
    sg.TabGroup: sg.TabGroup([[sg.Tab("", [[sg.Text()]], key="tab")]], size=(1, 1)),
    sg.Table: sg.Table([["asdf"]], size=(1, 1)),
    sg.Text: sg.Text(size=(1, 1)),
    sg.Tree: sg.Tree(_tree_data, [""], num_rows=1),
    sg.VerticalSeparator: sg.VerticalSeparator(),
}

# A completely invisible window (on most platforms), which should at worst 
# flash the default window, then show a small line at the top-right of the 
# left display.
DEFAULT_WINDOW: sg.Window = sg.Window(
    "",
    [[element] for element in DEFAULT_ELEMENTS.values()],
    size=(0, 0),
    no_titlebar=True,
    finalize=True,
    element_padding=(0, 0),
    alpha_channel=0,
    location=(-1, -1),
)

DEFAULT_WINDOW.hide()
DEFAULT_ELEMENTS["tab"] = DEFAULT_WINDOW["tab"]
sg.theme(_previous_theme)
