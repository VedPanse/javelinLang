import os
from config_exec import get_properties

EXECUTABLE = "py_executable.py"
EXTENSION = ".jv"
CONFIG_FILE = ""

PROPERTIES_OFFERED = ["background-color", "color", "width", "height", "title"]
LABEL_PROPERTIES_OFFERED = ["color", "font-size", "background-color", "text-align", "font-family", "left", "right",
                            "bottom", "top"]

# Set the default CONFIG_FILE
CONFIG_FILE_DEFAULT = CONFIG_FILE


def get_parse_file() -> list:
    """
    :return: list of .jv files
    """
    return [k for k in os.listdir() if k.endswith(EXTENSION)]


def get_parse_code(file_name: str) -> list:
    with open(file_name, "r") as fs:
        return fs.read().split("\n")


def write_to_executable(command: str) -> None:
    with open(EXECUTABLE, "a") as fs:
        fs.write(command + "\n")


def handle_properties(properties: dict) -> None:
    if 'window' in properties:
        window_props = properties['window']
        for prop in PROPERTIES_OFFERED:
            if prop in window_props:
                value = window_props[prop]
                if prop == "background-color":
                    write_to_executable(f"window.configure(bg='{value}')")
                elif prop == "width":
                    write_to_executable(f"window.geometry('{value}x800')")
                elif prop == "height":
                    write_to_executable(f"window.geometry('800x{value}')")
                elif prop == "title":
                    write_to_executable(f"window.title('{value}')")
        del properties['window']

    for variable_name, attributes in properties.items():
        for prop, value in attributes.items():
            if prop in LABEL_PROPERTIES_OFFERED:
                if prop == "font-size":
                    font_size = value.split('px')[0]  # Extract the font size without 'px' suffix
                    write_to_executable(f"{variable_name}.config(font=('', {font_size}))")
                elif prop == "background-color":
                    write_to_executable(f"{variable_name}.config(bg='{value}')")
                elif prop == "text-align":
                    anchor = {'left': 'w', 'center': 'center', 'right': 'e'}.get(value.lower(), 'w')
                    write_to_executable(f"{variable_name}.config(anchor='{anchor}')")
                elif prop == "font-family":
                    write_to_executable(f"{variable_name}.config(font=('', 12, '{value}'))")  # Assume font size 12
                elif prop == "color":
                    write_to_executable(f"{variable_name}.config(fg='{value}')")
                elif prop == "position":
                    x, y = value.split(',')
                    write_to_executable(f"{variable_name}.place(x={x.strip()}, y={y.strip()})")


def println(command: str) -> str:
    to_print: str = command[command.index("->") + 2:].strip()
    variable_name: str = to_print[to_print.index("id="):].strip().split("id=")[1][1:-1]
    text_to_be_printed: str = to_print[:to_print.index("id=")].strip()[:-1]
    command_string: str = f"{variable_name} = Label(window, text={text_to_be_printed}, fg='black')\n{variable_name}.place(x=4, y=4)\n"
    return command_string


def unpack_command(command: str) -> str:
    if "//" in command:
        command = command[:command.index("//")]

    space_less: str = command.replace(" ", "")

    if "!println->" in space_less and space_less.index("!println") == 0:
        return println(command)
    elif "#CONFIG" in space_less:
        global CONFIG_FILE
        CONFIG_FILE = space_less.split(" ", 1)[1]
    else:
        raise Exception(f"Command not recognized: {command}")


def get_defaults(parent_type: str) -> dict:
    defaults_dict_window = {
        "background-color": "white",
        "color": "black",
        "width": 800,
        "height": 800,
        "title": "javelinLang"
    }

    if parent_type == "window":
        return defaults_dict_window


def get_all_properties() -> dict:
    properties: dict = get_properties()

    all_properties_for_this_element: dict = {}

    if 'window' in properties:
        window_properties = properties['window']
        window_props: dict = {}
        for this_property in PROPERTIES_OFFERED:
            if this_property in window_properties:
                window_props[this_property] = window_properties[this_property]
            else:
                window_props[this_property] = get_defaults("window")[this_property]
        all_properties_for_this_element['window'] = window_props
        del properties['window']

    for variable_list, attributes in properties.items():
        variable_list: list = variable_list.split(",")  # Split the variable list by comma
        for variable_name in variable_list:
            all_properties_for_this_element[variable_name.strip()] = attributes

    return all_properties_for_this_element


def master(file_data: list) -> None:
    global CONFIG_FILE
    for command in [line for line in file_data if line.strip() != ""]:
        if "#CONFIG" in command.strip():
            CONFIG_FILE = command.strip().split(" ", 1)[1]

        if command.strip()[0] != "!":
            write_to_executable(command)
        else:
            unpacked_command: str = unpack_command(command.strip())
            write_to_executable(unpacked_command)

    handle_properties(get_all_properties())
    write_to_executable("\nwindow.mainloop()")


def read_config() -> str:
    with open(CONFIG_FILE, "r") as fs:
        return fs.read()


def main() -> None:
    # Write initial setup to py_executable.py
    with open(EXECUTABLE, "w") as fs:
        fs.write("from tkinter import *\n\nwindow = Tk()\n")

    # Process .jv files
    for file_name in get_parse_file():
        file_data = get_parse_code(file_name)
        master(file_data)

    # TODO: position elements

    exec(open("py_executable.py").read())


if __name__ == "__main__":
    main()
