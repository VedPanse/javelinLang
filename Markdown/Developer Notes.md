``` python
import os
from tkinter import *
from config_exec import get_properties

fs = open("py_executable.py", "w")
fs.write("""from tkinter import *

window = Tk()
window.geometry("300x200")
    
""")
fs.close()


EXTENSION: str = ".jv"
CONFIG_FILE: str = "config.cfg"
EXECUTABLE: str = "py_executable.py"
PROPERTIES_OFFERED = ["background-color", "color", "width", "height"]


def get_parse_file() -> list:
    """
    :return: list of .ui files
    """

    return [k for k in os.listdir() if k[-3:] == EXTENSION]


def get_parse_code(file_name: str) -> list:
    fs = open(file_name, "r")
    return fs.read().split("\n")


def write_to_executable(command: str) -> None:
    fs = open(EXECUTABLE, "a")
    fs.write(command + "\n")
    fs.close()
    
    
def println(command: str) -> str:
    to_print: str = command[command.index("->") + 2:].strip()

    variable_name: str = to_print[to_print.index("id="):].strip().split("id=")[1][1:-1]

    text_to_be_printed: str = to_print[:to_print.index("id=")].strip()[:-1]

    command_string: str = f"{variable_name} = Label(window, text={text_to_be_printed})\n{variable_name}.pack()\n"

    return command_string


def unpack_command(command: str) -> str:
    if "//" in command:
        command = command[:command.index("//")]
    space_less: str = command.replace(" ", "")[1:]


    if "println->" in space_less and space_less.index("println") == 0:
        return println(command)
        # TODO: Add code to append a window shell (create a text label and append to window)

    elif "window->" in space_less and space_less.index("window") == 0:
        print(space_less)
        
    else:
        raise Exception(f"Command not recognized: {command}")

    return "print(\"_____\")"


def get_defaults(parent_type: str) -> dict:
    defaults_dict_window = {
        "background-color": "white",
        "color": "black",
        "width": 800,
        "height": 800
    }
    
    if parent_type == "window":
        return defaults_dict_window
    



def get_all_properties() -> dict:
    properties: dict = get_properties()
    all_properties_for_this_element: dict = {}
    
    if 'window' in properties.keys():
        window_properties: dict = properties['window']
        
        for this_property in PROPERTIES_OFFERED:
            if this_property in list(window_properties.keys()):
                all_properties_for_this_element[this_property] = window_properties[this_property]
            else:
                all_properties_for_this_element[this_property] = get_defaults("window")[this_property]
        
    else:
        print("Window not found")
        
    return all_properties_for_this_element



def master(file_data: list) -> None:
    for command in [line for line in file_data if line.strip() != ""]:

        if command.strip()[0] != "!":
            write_to_executable(command)
        else:
            unpacked_command: str = unpack_command(command.strip())
            write_to_executable(unpacked_command)
            
    print(get_all_properties())

    write_to_executable("\nwindow.mainloop()")


def read_config() -> str:
    fs = open(CONFIG_FILE, "r")
    config_data = fs.read()
    fs.close()
    
    return config_data
    

def main() -> None:
    for file_name in get_parse_file():
        master(get_parse_code(file_name))

    exec(open("py_executable.py").read())



if __name__ == "__main__":
    main()

```

# Adding to property offerings
1. Change the constant list: PROPERTIES_OFFERED
2. Change get_defaults