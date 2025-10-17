prompt = """
Neither PySimpleGUI (https://github.com/PySimpleGUI/PySimpleGUI/) nor FreeSimpleGUI (https://github.com/spyoungtech/FreeSimpleGUI) are installed.

You should install one or the other with the `psg` and `fsg` optional dependency groups respectively, e.g.:
`pip install reskinner[psg]` for PySimpleGUI support.
"""
SG_LIB = "psg"
try:
    import PySimpleGUI as sg
except ImportError:
    try:
        import FreeSimpleGUI as sg

        SG_LIB = "fsg"
    except ImportError:
        raise EnvironmentError(prompt)

__all__ = ["sg", "SG_LIB"]
