import importlib.util
import sys
from pathlib import Path
from re import compile

from reskinner import sg

# Match files ending with '.py' but not starting with underscore
PY_PATTERN = compile(r"^(?P<name>[^_]{2}.*)\.py$")
DEFAULT_ENTRY_PROMPT = "Select a demo..."


def python_file_filter(f):
    if not f.is_file():
        return False
    m = PY_PATTERN.match(f.name)
    if not m:
        return False
    print(m["name"])
    return m["name"]


def list_demo_files():
    folder = Path(__file__).parent
    files = filter(python_file_filter, folder.iterdir())
    return sorted(f.name for f in files)


def run_demo(file_name):
    demo_path = Path(__file__).parent / file_name
    if not demo_path.suffix == ".py":
        demo_path = demo_path.with_suffix(".py")
    if not demo_path.exists():
        print(f"Demo file not found: {demo_path}")
        return

    spec = importlib.util.spec_from_file_location(
        file_name.rstrip(".py"), str(demo_path)
    )
    if spec is None:
        print(f"Demo file not found: {demo_path}")
        return
        
    demo_module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(demo_module)
        demo_module.main()
    except Exception as e:
        print(f"Error running demo '{file_name}':\n{e}")


def show_gui_and_launch():
    demo_files = list_demo_files()
    if not demo_files:
        sg.popup("No demo files found.", title="Error")
        return

    layout = [
        [sg.Text("Reskinner Demos", font="sans-serif 18")],
        [sg.Text("Select a demo to run:")],
        [
            sg.Combo(
                demo_files,
                DEFAULT_ENTRY_PROMPT,
                key="chosen_demo",
                size=(40, len(demo_files)),
                enable_events=True,
            )
        ],
        [
            sg.Text("Alternatively, use", pad=0),
            sg.Text("python -m demos <demo_name>", relief="sunken"),
        ],
        [sg.Push(), sg.Button("Exit"), sg.Button("Run", key="run")],
    ]

    window = sg.Window("Demo Launcher", layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        if event == "run" and (values["chosen_demo"] != DEFAULT_ENTRY_PROMPT):
            selected_demo = values["chosen_demo"]
            window.close()
            run_demo(selected_demo)
            break

    window.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_demo(sys.argv[1])
    else:
        show_gui_and_launch()
