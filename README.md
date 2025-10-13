# Reskinner: Dynamic Theme Manager for PySimpleGUI

[![PyPI Version](https://img.shields.io/pypi/v/reskinner?style=flat-square)](https://pypi.org/project/reskinner/)
[![Python Versions](https://img.shields.io/pypi/pyversions/reskinner?style=flat-square&logo=python)](https://pypi.org/project/reskinner/)
[![License](https://img.shields.io/pypi/l/reskinner?style=flat-square)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Downloads](https://static.pepy.tech/personalized-badge/psg-reskinner?period=total&units=international_system&left_color=grey&right_color=yellowgreen&left_text=downloads)](https://pepy.tech/project/psg-reskinner)
[![GitHub issues](https://img.shields.io/github/issues/definite-d/psg_reskinner)](https://github.com/definite-d/psg_reskinner/issues)
![GitHub forks](https://img.shields.io/github/forks/definite-d/psg_reskinner?logo=github&style=flat)
[![GitHub stars](https://img.shields.io/github/stars/definite-d/psg_reskinner)](https://github.com/definite-d/psg_reskinner/stargazers)


### V4 Release
With the release of Version 4.0.0, the project is now officially known as "Reskinner". This is a re-write, focusing on 
improvements to the structure and API of the project.

#### Biggest changes
- Full support for [FreeSimpleGUI](https://github.com/spyoungtech/FreeSimpleGUI) is here. Thanks to [@deajan](https://github.com/deajan) for the contribution and bringing it to my notice.
- The entire project has been rewritten from scratch for better maintainability, extensibility, and performance.
- The `animated_reskin` function is no more... because the `reskin` function itself has animation parameters baked in now.
- The API for `reskin` has been improved to require only 2 parameters; the window, and the desired theme.
- The project's minimum supported Python version is now 3.8.
- Mentions of `HSV` interpolation in the code have been corrected; it's `HSL`.

<p align="center">
  <img src="https://github.com/definite-d/psg_reskinner/blob/main/res/demo.gif" alt="Reskinner Demo">
</p>

Reskinner is a powerful library for PySimpleGUI and FreeSimpleGUI, enabling dynamic theme switching at runtime without window recreation. It provides a seamless way to update your application's look and feel on the fly.

## Features

- Dynamic theme switching without window recreation
- Supports both PySimpleGUI and FreeSimpleGUI
- Easy integration with existing applications
- Precise control over theme transitions with animations and 3 supported interpolation modes.
- Lightweight and dependency-minimal

## Installation

### Using pip (PyPI)

```bash
# For PySimpleGUI
pip install "reskinner[psg]"

# For FreeSimpleGUI
pip install "reskinner[fsg]"
```

### Using uv

```bash
# Install uv if not already installed
pip install uv

# For PySimpleGUI
uv add reskinner[psg]

# For FreeSimpleGUI
uv add reskinner[fsg]
```

## Quick Start

```python
from random import choice
import PySimpleGUI as sg  # or import FreeSimpleGUI as sg
from reskinner import reskin

# Create a simple window
layout = [
    [sg.Text("Hello, Reskinner!")],
    [sg.Button("Change Theme"), sg.Button("Exit")]
]

window = sg.Window("Reskinner Demo", layout)

themes = sg.theme_list()
current_theme = sg.theme()

def change_theme():
    new_theme = choice([t for t in themes if t != current_theme])
    reskin(window=window, new_theme=new_theme, theme_function=sg.theme)
    return new_theme

while True:
    event, values = window.read()
    
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
        
    if event == "Change Theme":
        current_theme = change_theme()

window.close()
```

## Documentation

### Core Function

#### `reskin`
```python
from reskinner import reskin
import PySimpleGUI as sg

# Apply a new theme instantly
reskin(window=my_window, new_theme="DarkBlue3", theme_function=sg.theme)
```

## Advanced Usage

### Custom Interpolation

Reskinner supports three different interpolation modes for theme transitions; `hsl`, `hue`, and `rgb` (default):

```python
from reskinner import reskin
import PySimpleGUI as sg

# Smooth, animated color transition using HSL interpolation
reskin(
    window=window,
    new_theme="DarkAmber",
    theme_function=sg.theme,
    duration_in_milliseconds=800,
    interpolation_mode="hsl",
)
```

### Element-Specific Filtering

Customize whether specific elements are styled during reskinning:

```python
from reskinner import reskin
import PySimpleGUI as sg

# Skip elements you don't want to restyle
reskin(
    window=window,
    new_theme="LightGreen",
    theme_function=sg.theme,
    element_filter=lambda e: e.key != "skip_me"
)
```


## Compatibility

- Python 3.8+
- PySimpleGUI 4.60.0+ or FreeSimpleGUI 5.0.0+ *(Tkinter variant __only__; Reskinner doesn't support \*Qt, \*Wx, or \*Web variants)*
- Tkinter (included with Python)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The PySimpleGUI and FreeSimpleGUI communities
- All contributors who have helped improve Reskinner

## FAQs
### How does it work?

Reskinner runs through each element in a window, then by relying on the `element.widget`
interface to access the underlying Tkinter object, it applies style changes to the window.

### What's the story behind psg_reskinner?

Like [Unda](https://github.com/definite-d/unda), I created Reskinner to be a part/feature of a desktop application which
I'm developing, however, I decided to open-source it, as I imagined other developers would find such functionality
useful in their projects as well.

Development began on Monday 15th August 2022.

### Why is it called Reskinner?

I didn't want it to go against the built-in conventions of `theme` and `look_and_feel` that PySimpleGUI has.
