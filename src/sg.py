prompt = """
Neither PySimpleGUI (https://github.com/PySimpleGUI/PySimpleGUI/) nor FreeSimpleGUI (https://github.com/spyoungtech/FreeSimpleGUI) are installed.

You should install one or the other with the `psg` and `fsg` optional dependency groups respectively, e.g.:
`pip install reskinner[psg]` for PySimpleGUI support.
"""

try:
    import PySimpleGUI as sg
except ImportError:
    try:
        import FreeSimpleGUI as sg
    except ImportError:
        raise EnvironmentError(prompt)

__all__ = ["sg"]