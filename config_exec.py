def get_properties(config_path) -> dict:
    fs = open(config_path, "r")
    config_data: list[str] = fs.readlines()
    fs.close()

    PROPERTIES = {}

    current_section = None
    current_properties = {}

    for line in config_data:
        line = line.strip()

        # Ignore comments
        if "//" in line:
            line = line.split("//")[0].strip()

        # Check for section headers
        if line.startswith("!"):
            if current_section:
                PROPERTIES[current_section] = current_properties
                current_properties = {}

            current_section = line.split("->")[0].strip("!").strip()
            if current_section.startswith("[") and current_section.endswith("]"):
                current_section = current_section[1:-1]
            else:
                current_section = current_section
        elif ":" in line:
            key, value = map(str.strip, line.split(":", 1))
            current_properties[key] = value

    # Adding the last section after the loop
    if current_section:
        PROPERTIES[current_section] = current_properties

    return PROPERTIES

