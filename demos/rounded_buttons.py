# Rounded Buttons Demo
# Demonstrates custom rounded button creation with PIL and reskinner integration

try:
    from PIL import Image, ImageDraw
except ImportError:
    print(
        "Error: PIL/Pillow is required for this demo. "
        "Install with: `uv add --group dev Pillow`"
    )
    exit(1)

from io import BytesIO

from reskinner import reskin, sg

THEME = "BrightColors"

_custom_button_fg = {}


def _is_custom_button(element):
    return (
        hasattr(element, "ButtonColor")
        and element.ButtonColor != (None, None)
        and hasattr(element, "ImageData")
        and element.ImageData
    )


def _before_element(element, colorizer):
    if _is_custom_button(element):
        _custom_button_fg[element.Key] = element.ButtonColor[0]


def _after_element(element, colorizer):
    if element.key in _custom_button_fg:
        theme_bg = colorizer.color("BACKGROUND", lambda: "#000000")
        fg = _custom_button_fg[element.Key]
        element.widget.configure(
            foreground=fg,
            background=theme_bg,
            activebackground=theme_bg,
            activeforeground=fg,
        )


def round_corner(radius, fill):
    """Create a rounded corner image"""
    corner = Image.new("RGBA", (radius, radius), (0, 0, 0, 0))
    draw = ImageDraw.Draw(corner)
    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=fill)
    return corner


def round_rectangle(size, radius, fill):
    """Create a rounded rectangle image"""
    width, height = size
    rectangle = Image.new("RGBA", size, fill)
    corner = round_corner(radius, fill)
    rectangle.paste(corner, (0, 0))
    rectangle.paste(corner.rotate(90), (0, height - radius))
    rectangle.paste(corner.rotate(180), (width - radius, height - radius))
    rectangle.paste(corner.rotate(270), (width - radius, 0))
    return rectangle


def image_to_data(image):
    """Convert PIL image to bytes for PySimpleGUI"""
    with BytesIO() as output:
        image.save(output, format="PNG")
        return output.getvalue()


def RoundedButton(text, btn_width=100, btn_height=30, radius=30, **kwargs):
    """Create a rounded button using PIL images"""
    kwargs.pop("image_data", None)
    kwargs.pop("border_width", None)

    img = round_rectangle((btn_width, btn_height), radius, sg.theme_button_color()[1])
    button_color = (sg.theme_text_color(), sg.theme_background_color())

    return sg.Button(
        text,
        button_type=sg.BUTTON_TYPE_READ_FORM,
        image_data=image_to_data(img),
        button_color=button_color,
        border_width=0,
        **kwargs,
    )


def main():
    sg.theme(THEME)
    use_custom_titlebar = sg.running_trinket()

    Menu = sg.MenubarCustom if use_custom_titlebar else sg.Menu

    menudef = [
        ["File", ["Exit"]],
        ["Demo", ["Toggle Theme"]],
    ]

    layout = [
        [Menu(menudef, key="-CUST MENUBAR-", pad=0)],
        [sg.Text("Rounded Buttons Demo", font="_ 14 bold")],
        [sg.Text("Custom rounded buttons created with PIL")],
        [sg.Text("Click 'Toggle Theme' to see reskinning in action")],
        [sg.Push()],
        [
            RoundedButton(
                "Small Button", btn_width=80, btn_height=30, radius=15, key="btn_small"
            )
        ],
        [
            RoundedButton(
                "Medium Button",
                btn_width=120,
                btn_height=40,
                radius=20,
                key="btn_medium",
            )
        ],
        [
            RoundedButton(
                "Large Button", btn_width=200, btn_height=60, radius=30, key="btn_large"
            )
        ],
        [sg.Push()],
        [sg.Button("Exit", key="Exit")],
    ]

    window = sg.Window("Rounded Buttons Demo", layout, finalize=True)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event == "Toggle Theme":
            current_theme = sg.theme()
            new_theme = "Dark" if current_theme != "Dark" else THEME
            reskin(
                window,
                new_theme,
                before_element=_before_element,
                after_element=_after_element,
            )

    window.close()


if __name__ == "__main__":
    main()
