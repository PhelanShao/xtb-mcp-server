# coding: utf-8
"""
Utility functions for molecular structure format conversion and processing.
"""

import warnings

def xyz_to_coord_string(xyz_content: str, title: str = "xtb_coord_file") -> tuple[str | None, str | None]:
    """
    Converts XYZ format string content to TURBOMOLE COORD format string.

    Args:
        xyz_content (str): XYZ format string.
        title (str): Title line for the COORD file.
    
    Returns:
        tuple: A tuple (coord_string, error_message). error_message is None on success.
    """
    lines = xyz_content.strip().splitlines()
    if not lines or len(lines) < 2:
        return None, "XYZ content is empty or has insufficient lines."

    try:
        num_atoms = int(lines[0].strip())
        if len(lines) != num_atoms + 2:
            return None, f"XYZ file atom count declaration ({num_atoms}) does not match actual atom lines ({len(lines) - 2})."
    except ValueError:
        return None, f"Could not parse atom count from the first line of XYZ file: '{lines[0]}'"

    coord_lines = [f"$coord    {title}"]
    for i in range(num_atoms):
        parts = lines[i + 2].strip().split()
        if len(parts) < 4:
            return None, f"XYZ file line {i + 3} has incorrect format: '{lines[i + 2]}'"
        
        element = parts[0].lower() # TURBOMOLE usually uses lowercase element symbols
        x, y, z = parts[1], parts[2], parts[3]
        # Attempt to format coordinates in TURBOMOLE style (e.g., 12.6f)
        try:
            coord_lines.append(f"{float(x):12.6f}  {float(y):12.6f}  {float(z):12.6f}      {element}")
        except ValueError:
            return None, f"Could not parse coordinates as float on XYZ file line {i + 3}: '{lines[i + 2]}'"
            
    coord_lines.append("$end")
    return "\n".join(coord_lines), None


def coord_string_to_xyz(coord_content: str, comment: str = "Converted from COORD") -> tuple[str | None, str | None]:
    """
    Converts TURBOMOLE COORD format string content to XYZ format string.

    Args:
        coord_content (str): COORD format string.
        comment (str): Comment for the second line of the XYZ file.
    
    Returns:
        tuple: A tuple (xyz_string, error_message). error_message is None on success.
    """
    lines = coord_content.strip().splitlines()
    if not lines:
        return None, "COORD content is empty."

    atom_lines = []
    in_coord_block = False
    for line_num, line in enumerate(lines):
        line_stripped = line.strip()
        if line_stripped.startswith("$coord"):
            in_coord_block = True
            # Title extraction can be done here, but not necessary for XYZ conversion
            continue
        if line_stripped.startswith("$end"):
            if in_coord_block: # Ensure it's the $end of a $coord block
                in_coord_block = False # Assume only one $coord block per file
                break # Stop reading atoms
            continue # $end of other blocks

        if in_coord_block:
            parts = line_stripped.split()
            if len(parts) >= 4: # x y z element ...
                # 检查前三个是否为数字
                try:
                    float(parts[0])
                    float(parts[1])
                    float(parts[2])
                    atom_lines.append(f"{parts[3].capitalize()}  {parts[0]}  {parts[1]}  {parts[2]}")
                except ValueError:
                    # May not be an atom line, e.g., $periodic 3
                    if not any(kw in line_stripped for kw in ["$periodic", "$rundimensions"]): # Ignore some known directives
                         return None, f"COORD file line {line_num + 1} is within a $coord block but cannot be parsed as atomic coordinates: '{line}'"
            elif line_stripped: # Non-empty line but insufficient parts
                 if not any(kw in line_stripped for kw in ["$periodic", "$rundimensions"]):
                    return None, f"COORD file line {line_num + 1} is within a $coord block but has insufficient parts: '{line}'"


    if not atom_lines:
        return None, "No valid atomic coordinate lines or $coord block found in COORD content."
    if in_coord_block: # 如果循环结束时 in_coord_block 仍为 True，说明 $coord 未正确闭合
        return None, "$coord block did not find a corresponding $end."


    xyz_output_lines = [str(len(atom_lines)), comment] + atom_lines
    return "\n".join(xyz_output_lines), None


def gaussian_to_xyz_string(gaussian_content: str, comment: str = "Converted from Gaussian input") -> tuple[str | None, str | None]:
    """
    Extracts molecular coordinates from Gaussian input file content and converts them to XYZ format string.
    Only extracts the first encountered coordinate block (before the first Link0/Link1 command, or end of file).
    Does not handle charge and spin.

    Args:
        gaussian_content (str): String content of the Gaussian input file.
        comment (str): Comment for the second line of the XYZ file.
    
    Returns:
        tuple: A tuple (xyz_string, error_message). error_message is None on success.
    """
    lines = gaussian_content.strip().splitlines()
    atom_lines_xyz = []
    
    # State machine: 0=looking for charge and spin line, 1=looking for empty line, 2=reading coordinates
    state = 0
    charge_spin_line_found = False
    empty_line_after_charge_spin_found = False

    for line_num, line in enumerate(lines):
        line_stripped = line.strip()

        # Look for Link0/Link1 commands, indicating the end of a calculation section
        if line_stripped.lower().startswith("%link") or line_stripped.lower().startswith("--link1--"):
            break # Only process the first structure block

        if state == 0: # Looking for charge and spin line
            parts = line_stripped.split()
            if len(parts) == 2:
                try:
                    int(parts[0]) # Attempt to parse as charge
                    int(parts[1]) # Attempt to parse as spin multiplicity
                    charge_spin_line_found = True
                    state = 1 # Enter state to look for empty line
                    continue
                except ValueError:
                    pass # Not a charge/spin line
            # If an empty line is encountered before finding the charge/spin line, it might also be part of the format
            if not line_stripped and charge_spin_line_found: # Theoretically, an empty line shouldn't be encountered first
                 pass # Keep state 0 or 1
            elif not line_stripped: # Empty line after title
                state = 0 # Keep looking for charge/spin line, allow empty line after title
                continue


        if state == 1: # Looking for empty line after charge and spin line
            if not line_stripped: # Found empty line
                empty_line_after_charge_spin_found = True
                state = 2 # Enter state to read coordinates
                continue
            # If a line that looks like coordinates is encountered before finding an empty line, this might be an irregular format
            # But some programs might omit the empty line and start coordinates directly
            parts_check = line_stripped.split()
            if len(parts_check) == 4:
                try:
                    float(parts_check[1])
                    float(parts_check[2])
                    float(parts_check[3])
                    # Looks like a coordinate line, try to enter state 2 even without an empty line
                    empty_line_after_charge_spin_found = True # Assume empty line is omitted
                    state = 2
                    # Do not continue, let the state == 2 logic below process this line
                except ValueError:
                    pass # 不是坐标行

        if state == 2: # Reading coordinates
            if not line_stripped: # End of coordinate block (empty line encountered)
                break
            
            parts = line_stripped.split()
            if len(parts) >= 4: # Element X Y Z ...
                try:
                    # Ensure X, Y, Z are numbers
                    float(parts[1])
                    float(parts[2])
                    float(parts[3])
                    atom_lines_xyz.append(f"{parts[0].capitalize()}  {parts[1]}  {parts[2]}  {parts[3]}")
                except (ValueError, IndexError):
                    # If line starts with a digit, it might be a Z-matrix, currently not supported
                    if parts[0][0].isdigit():
                         return None, f"Possible Z-matrix detected in Gaussian input (line {line_num+1}), currently not supported."
                    # Otherwise, it might be a format error or end of coordinate block
                    warnings.warn(f"Gaussian input file line {line_num + 1} is in coordinate block but cannot be parsed as atomic coordinates: '{line}'")
                    # break # Stop reading coordinates if an unparseable line is encountered
            elif line_stripped: # Non-empty line but insufficient parts
                 warnings.warn(f"Gaussian input file line {line_num + 1} is in coordinate block but has insufficient parts: '{line}'")
                 # break

    if not charge_spin_line_found:
        return None, "No valid charge/spin line found in Gaussian input."
    # The check for empty_line_after_charge_spin_found can be relaxed, as some programs might omit it
    # if not empty_line_after_charge_spin_found:
    #     return None, "No empty line separator found after charge/spin line in Gaussian input."

    if not atom_lines_xyz:
        return None, "No atomic coordinates extracted from Gaussian input."

    xyz_output_lines = [str(len(atom_lines_xyz)), comment] + atom_lines_xyz
    return "\n".join(xyz_output_lines), None


if __name__ == '__main__':
    import warnings # Add import
    # Test XYZ to COORD
    xyz_data_ok = """3
Water
O  0.000000  0.000000  0.117300
H  0.000000  0.757200 -0.469200
H  0.000000 -0.757200 -0.469200
"""
    xyz_data_bad_count = "2\nWater\nO 0 0 0\nH 0 0 1\nH 0 1 0"
    xyz_data_bad_format = "3\nWater\nO 0 0\nH 0 0 1\nH 0 1 0"

    coord_out, err = xyz_to_coord_string(xyz_data_ok)
    if err:
        print(f"XYZ to COORD Error: {err}")
    else:
        print("--- XYZ to COORD OK ---")
        print(coord_out)

    _, err = xyz_to_coord_string(xyz_data_bad_count)
    print(f"\nXYZ to COORD (bad_count) Error: {err}")
    
    _, err = xyz_to_coord_string(xyz_data_bad_format)
    print(f"\nXYZ to COORD (bad_format) Error: {err}")

    # Test COORD to XYZ
    coord_data_ok = """
$coord    title from test
  0.000000    0.000000    0.117300      o
  0.000000    0.757200   -0.469200      h
  0.000000   -0.757200   -0.469200      h
$end
"""
    coord_data_no_end = "$coord\n 0 0 0 o"
    coord_data_bad_atom = "$coord\n 0 0 o\n$end"

    xyz_out, err = coord_string_to_xyz(coord_data_ok)
    if err:
        print(f"\nCOORD to XYZ Error: {err}")
    else:
        print("\n--- COORD to XYZ OK ---")
        print(xyz_out)

    _, err = coord_string_to_xyz(coord_data_no_end)
    print(f"\nCOORD to XYZ (no_end) Error: {err}")

    _, err = coord_string_to_xyz(coord_data_bad_atom)
    print(f"\nCOORD to XYZ (bad_atom) Error: {err}")

    # Test Gaussian to XYZ
    gaussian_data_ok = """%chk=water.chk
%mem=1GB
%nprocshared=4
#p opt freq b3lyp/6-31g(d)

Water optimization and frequency

0 1
O    0.00000000    0.00000000    0.11779000
H    0.00000000    0.76322600   -0.47115800
H    0.00000000   -0.76322600   -0.47115800

"""
    gaussian_data_no_empty_line = """%chk=test.chk
#p b3lyp/6-31g

Title

0 1
C 0.0 0.0 0.0
H 0.0 0.0 1.09
H 1.0279 0.0 -0.3633
H -0.5140 0.8902 -0.3633
H -0.5140 -0.8902 -0.3633
"""
    gaussian_data_no_charge_spin = """%chk=test.chk
#p b3lyp/6-31g
Title
C 0.0 0.0 0.0
"""
    gaussian_data_zmat = """%chk=test.chk
#p b3lyp/6-31g
Title
0 1
C
H 1 1.09
H 1 1.09 2 109.47
"""


    xyz_g_out, err_g = gaussian_to_xyz_string(gaussian_data_ok)
    if err_g:
        print(f"\nGaussian to XYZ Error: {err_g}")
    else:
        print("\n--- Gaussian to XYZ OK ---")
        print(xyz_g_out)

    xyz_g_out_no_empty, err_g_no_empty = gaussian_to_xyz_string(gaussian_data_no_empty_line)
    if err_g_no_empty:
        print(f"\nGaussian to XYZ (no_empty_line) Error: {err_g_no_empty}")
    else:
        print("\n--- Gaussian to XYZ (no_empty_line) OK ---")
        print(xyz_g_out_no_empty)
        
    _, err_g_no_cs = gaussian_to_xyz_string(gaussian_data_no_charge_spin)
    print(f"\nGaussian to XYZ (no_charge_spin) Error: {err_g_no_cs}")

    _, err_g_zmat = gaussian_to_xyz_string(gaussian_data_zmat)
    print(f"\nGaussian to XYZ (zmat) Error: {err_g_zmat}")