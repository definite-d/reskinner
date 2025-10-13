from typing import Callable, Optional

from .colorizer import Colorizer, ThemeDict
from .sg import sg


def _reskin(c: Colorizer):
    # Disregard redundant calls
    if c.new_theme_dict == c.old_theme_dict:
        return

    # Window level changes
    if reskin


def reskin(old_theme, new_theme):
    old_theme_dict: ThemeDict = sg.LOOK_AND_FEEL_TABLE[old_theme]
    new_theme_dict: ThemeDict = sg.LOOK_AND_FEEL_TABLE[new_theme]
    c = Colorizer(old_theme_dict, new_theme_dict)
