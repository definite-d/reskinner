# Reskinner Demos

This directory contains demonstration programs showcasing various features and capabilities of the Reskinner library.

## Available Demos

<details>
<summary><a href="https://github.com/definite-d/reskinner/blob/main/demos/all_elements.py">all_elements.py</a></summary>

Based on the standard PySimpleGUI All Elements Demo but customized for Reskinner-specific features. Shows how different GUI components appear and behave with custom theming.

</details>

<details>
<summary><a href="https://github.com/definite-d/reskinner/blob/main/demos/extended_layouts.py">extended_layouts.py</a></summary>

Shows how to create complex layouts and switch between different visual themes dynamically. Includes examples of advanced layout techniques.

</details>

<details>
<summary><a href="https://github.com/definite-d/reskinner/blob/main/demos/pin.py">pin.py</a></summary>

Specifically demonstrates the `sg.pin` element functionality and addresses the single pixel issue that can occur when using `shrink=True`. Includes interactive controls to toggle different pin behaviors.

</details>

<details>
<summary><a href="https://github.com/definite-d/reskinner/blob/main/demos/rounded_buttons.py">rounded_buttons.py</a></summary>

Demonstrates custom rounded button creation using PIL (Pillow) library with reskinner integration. Shows how to create visually appealing rounded buttons that work with theme switching. **Requires PIL/Pillow to be installed.**

</details>

<details>
<summary><a href="https://github.com/definite-d/reskinner/blob/main/demos/updated_table.py">updated_table.py</a></summary>

Shows how to work with table elements in Reskinner, including dynamic updates, extended selection modes, and theme integration. Demonstrates real-time data manipulation in table format.

</details>

## Running Demos

### Method 1: Interactive GUI Launcher

Run the demos module directly to launch a graphical selection interface:

```bash
python -m demos
```

This will open a window where you can select and run any available demo from a dropdown menu.

### Method 2: Command Line

Run a specific demo by name from the command line:

```bash
python -m demos <demo_name>
```

Example:

```bash
python -m demos all_elements
```

### Method 3: Direct Execution

Run individual demo files directly:

```bash
python demos/all_elements.py
```

## Requirements

- **Repository clone required**: These demos are not included in the PyPI distribution. You must clone the repository to access them:
  ```bash
  git clone https://github.com/definite-d/reskinner.git
  cd reskinner
  ```
- The demos automatically import the necessary modules from `reskinner`
- Some demos may require additional dependencies that are typically installed with Reskinner

## Troubleshooting

If you encounter issues running demos:

1. Ensure you're in the project root directory
2. Verify that the Reskinner library is properly installed
3. Check that all required dependencies are available
4. Some demos may require specific display configurations

## Contributing

When adding new demos:

1. Create a new Python file in this directory
2. Implement a `main()` function as the entry point
3. Follow the existing naming convention (lowercase with underscores)
4. Add a brief description to this README
5. Ensure the demo works with the launcher system by not starting with an underscore in the filename
