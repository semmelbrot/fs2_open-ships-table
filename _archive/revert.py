import re

def restore_original_ship_values(input_filepath, output_filepath):
    """
    Reads a spaceship game configuration file, restores specific ship values
    to their original (pre-mod) states based on a header comment section,
    and writes the modified content to an output file.

    Args:
        input_filepath (str): The path to the input text file.
        output_filepath (str): The path to the output text file.
    """
    with open(input_filepath, 'r') as f:
        lines = f.readlines()

    # Define the modifications and their original factors/values
    # These are derived from the "VELOCITY MOD" section
    modifications = {
        "Max Speed factor": {
            "keyword": "$Max Velocity",
            "index": 2,  # Affects only the Z component
            "operation": lambda x, factor: x / factor,
            "factor": 2.0,
            "comment_line": "Max Speed factor: 2.0 // Only the z factor has been modified"
        },
        "AB max speed": {
            "keyword": "+Aburn Max Vel",
            "index": 2,  # Affects only the Z component
            "operation": lambda x, factor: x / factor,
            "factor": 2.0,
            "comment_line": "AB max speed: 2.0"
        },
        "Max Overclock SPeed factor": {
            "keyword": "$Max Oclk Speed",
            "index": None, # Affects the whole value
            "operation": lambda x, factor: x / factor,
            "factor": 2.0,
            "comment_line": "Max Overclock SPeed factor: 2.0"
        },
        "Accel Factor": {
            "keyword": "$Forward accel",
            "index": None, # Affects the whole value
            "operation": lambda x, factor: x / factor,
            "factor": 1.25,
            "comment_line": "Accel Factor: 1.25   Slide Accel not changed"
        },
        "Decel Factor": {
            "keyword": "$Forward decel",
            "index": None, # Affects the whole value
            "operation": lambda x, factor: x / factor,
            "factor": 1.25,
            "comment_line": "Decel Factor: 1.25"
        },
        "AB Accel factor": {
            "keyword": "+Aburn For accel",
            "index": None, # Affects the whole value
            "operation": lambda x, factor: x / factor,
            "factor": 1.25,
            "comment_line": "AB Accel factor: 1.25"
        },
        "XYRotation Factor": {
            "keyword": "$Rotation time",
            "index": [0, 1],  # Affects X and Y components
            "operation": lambda x, factor: x / factor, # Multiply to revert because smaller value is faster
            "factor": 1.5,
            "comment_line": "XYRotation Factor: 1.5"
        }
    }

    output_lines = []
    in_ship_block = False
    ship_name_pattern = re.compile(r'^\$Name:\s+(.*)$')
    
    # Process lines to find ship definitions and apply reversals
    for i, line in enumerate(lines):
        # Check if we are inside a ship definition block
        if ship_name_pattern.match(line):
            in_ship_block = True
            output_lines.append(line)
            continue # Move to the next line to avoid processing the ship name line twice
        
        # If we are not in a ship block and the line is not a comment, just append it
        if not in_ship_block and not line.strip().startswith(';'):
            output_lines.append(line)
            continue

        # If we encounter a new ship name or the end of the file, it means the previous ship block ended
        # We need to re-evaluate this logic. The ship block processing needs to be self-contained for each ship.
        # A simpler approach is to iterate, and when a ship block starts, collect its lines
        # then process the collected lines and append them.

        # This simpler approach will just process line by line based on keywords
        modified = False
        for mod_name, mod_info in modifications.items():
            keyword = mod_info["keyword"]
            if keyword in line:
                try:
                    # Extract the current value(s)
                    parts = line.split(":", 1)
                    if len(parts) < 2:
                        continue # Skip lines that don't conform to "KEY: VALUE"
                    
                    value_str = parts[1].strip()
                    # Remove any inline comments
                    if ';;' in value_str:
                        value_str = value_str.split(';;')[0].strip()

                    current_values = [float(v) for v in value_str.replace(',', ' ').split() if v.strip()]

                    if not current_values:
                        continue

                    new_values = list(current_values) # Create a mutable copy

                    if mod_info["index"] is None: # Affects the whole value (single float)
                        if current_values: # Ensure there's a value to modify
                            new_values[0] = mod_info["operation"](current_values[0], mod_info["factor"])
                    elif isinstance(mod_info["index"], int): # Affects a specific index
                        if mod_info["index"] < len(current_values):
                            new_values[mod_info["index"]] = mod_info["operation"](current_values[mod_info["index"]], mod_info["factor"])
                    elif isinstance(mod_info["index"], list): # Affects multiple indices
                        for idx in mod_info["index"]:
                            if idx < len(current_values):
                                new_values[idx] = mod_info["operation"](current_values[idx], mod_info["factor"])
                    
                    # Reconstruct the line
                    if len(new_values) > 1:
                        # Format floats to reasonable precision, e.g., 3 decimal places
                        # Ensure the line maintains its original spacing where possible
                        original_indent = line.split(keyword)[0]
                        original_comment = ''
                        if ';;' in line:
                            original_comment = ';;' + line.split(';;', 1)[1]
                        
                        # Find the actual starting point of the values for formatting
                        match = re.search(r'^\s*[\$\+]\w+:\s*', line)
                        if match:
                            indent_after_keyword = ' ' * (len(match.group(0)) - len(keyword) - 1)
                        else:
                            indent_after_keyword = '' # Fallback

                        new_value_str = ", ".join([f"{v:.3f}".rstrip('0').rstrip('.') if '.' in f"{v:.3f}" else f"{int(v)}" for v in new_values])
                        line = f"{original_indent}{keyword}:{indent_after_keyword}{new_value_str} {original_comment}".strip() + "\n"
                    else:
                        # Single value, try to preserve original formatting
                        original_value_start_index = line.find(value_str)
                        if original_value_start_index != -1:
                            new_single_value = f"{new_values[0]:.3f}".rstrip('0').rstrip('.') if '.' in f"{new_values[0]:.3f}" else f"{int(new_values[0])}"
                            # Reconstruct line to preserve original spacing before and after the value
                            before_value = line[:original_value_start_index]
                            after_value = line[original_value_start_index + len(value_str):]
                            line = f"{before_value}{new_single_value}{after_value}"
                        else:
                             # Fallback if value string not found precisely (shouldn't happen often)
                            new_single_value = f"{new_values[0]:.3f}".rstrip('0').rstrip('.') if '.' in f"{new_values[0]:.3f}" else f"{int(new_values[0])}"
                            line = f"{parts[0]}: {new_single_value}{' ' + original_comment if original_comment else ''}\n"

                    modified = True
                    break # Only one modification per line is expected for simplicity

                except ValueError:
                    # Handle cases where value conversion fails (e.g., non-numeric data)
                    pass
                except IndexError:
                    # Handle cases where index is out of bounds for current_values
                    pass
        
        output_lines.append(line)

    with open(output_filepath, 'w') as f:
        f.writelines(output_lines)

    print(f"Original values restored and saved to '{output_filepath}'")

input_file = "inertia-shp.tbm" # Replace with your input file name
output_file = "inertia-shp-new.tbm" # Desired output file name
restore_original_ship_values(input_file, output_file)