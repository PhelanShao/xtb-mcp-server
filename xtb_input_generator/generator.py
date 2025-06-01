import os
from pathlib import Path
from . import structure_utils # Import structure conversion utilities

# Define the base path for resource files, relative to the location of generator.py
# We expect the resources folder to be at the same level as the xtb_input_generator folder
DEFAULT_RESOURCE_PATH_RELATIVE = "../resources"

class XTBInputGenerator:
    def __init__(self, resource_base_path: str | Path | None = None):
        """
        Initializes the XTBInputGenerator.

        Args:
            resource_base_path (str | None): The base path where resource files are located.
                                             If None, the default path relative to this file will be used.
        """
        if resource_base_path is None:
            # Get the directory of the current file (generator.py)
            current_dir = Path(__file__).parent
            self.resource_path = (current_dir / DEFAULT_RESOURCE_PATH_RELATIVE).resolve()
        else:
            self.resource_path = Path(resource_base_path).resolve()

        if not self.resource_path.is_dir():
            # This error should be caught during server startup or logged
            print(f"Warning: Resource path {self.resource_path} does not exist or is not a directory.")
            # In a real application, this might raise an exception

        self.templates = self._load_all_templates()
        self.parameter_docs = self._load_parameter_docs()
        # self.validators = self._init_validators() # 验证器将在后续任务中实现

    def _load_template_file(self, template_category: str, template_name: str) -> str | None:
        """Loads the content of a single template file."""
        file_path = self.resource_path / template_category / f"{template_name}.xtb_tpl"
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"Warning: Template file {file_path} not found.")
            return None
        except Exception as e:
            print(f"Warning: Error reading template file {file_path}: {e}")
            return None

    def _load_doc_file(self, doc_category: str, doc_name: str) -> str | None:
        """Loads the content of a single documentation file."""
        file_path = self.resource_path / doc_category / f"{doc_name}.md"
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"Warning: Documentation file {file_path} not found.")
            return None
        except Exception as e:
            print(f"Warning: Error reading documentation file {file_path}: {e}")
            return None

    def _load_all_templates(self) -> dict:
        """
        Loads all predefined xtb calculation templates.
        Template URI format: xtb://templates/{type}
        Example: xtb://templates/singlepoint
        """
        templates_data = {}
        template_dir = self.resource_path / "templates"
        if template_dir.is_dir():
            # Use rglob to find all .xtb_tpl files recursively
            for file_path in template_dir.rglob("*.xtb_tpl"):
                # Create a key based on the relative path from the template_dir
                # e.g., "singlepoint" or "sampling:metadynamics"
                relative_path = file_path.relative_to(template_dir)
                if relative_path.parent == Path("."): # Top-level template
                    template_key = relative_path.stem
                else: # Template in a subdirectory
                    template_key = f"{relative_path.parent.name}:{relative_path.stem}"
                
                # We need to pass the correct category and name to _load_template_file
                # Category would be "templates/sampling" or "templates"
                # Name would be "metadynamics" or "singlepoint"
                category_for_load = "templates"
                name_for_load = template_key # Default to the key itself if no colon
                if ":" in template_key:
                    parent_dir_name, stem_name = template_key.split(":", 1)
                    category_for_load = Path("templates") / parent_dir_name
                    name_for_load = stem_name
                else: # top level template
                    category_for_load = Path("templates")
                    name_for_load = template_key


                # _load_template_file expects category as a string relative to self.resource_path
                # and name without extension.
                # Example: self.resource_path / "templates" / "singlepoint.xtb_tpl"
                # Example: self.resource_path / "templates" / "sampling" / "metadynamics.xtb_tpl"
                
                # Correctly form the path parts for _load_template_file
                path_parts = list(relative_path.parts) # e.g., ['sampling', 'metadynamics.xtb_tpl'] or ['singlepoint.xtb_tpl']
                actual_name = Path(path_parts[-1]).stem # 'metadynamics' or 'singlepoint'
                
                if len(path_parts) > 1:
                    actual_category_path = Path("templates") / Path(*path_parts[:-1]) # 'templates/sampling'
                else:
                    actual_category_path = Path("templates") # 'templates'

                content = self._load_template_file(str(actual_category_path), actual_name)

                if content:
                    templates_data[template_key] = content
        return templates_data

    def _load_parameter_docs(self) -> dict:
        """
        Loads all predefined xtb parameter documentation.
        Documentation URI format: xtb://parameters/{param_set}
        Example: xtb://parameters/gfn2
        """
        docs_data = {}
        params_dir = self.resource_path / "parameters"
        if params_dir.is_dir():
            for file_path in params_dir.glob("*.md"):
                doc_name = file_path.stem # e.g., "gfn2"
                content = self._load_doc_file("parameters", doc_name)
                if content:
                    docs_data[doc_name] = content
        return docs_data

    def get_mcp_resource(self, uri: str) -> str | None:
        """
        Retrieves resource content based on MCP URI.
        MCP URI format: xtb://{category}/{identifier}
        Examples: xtb://templates/singlepoint, xtb://parameters/gfn2

        Args:
            uri (str): The MCP URI of the resource.
        
        Returns:
            str | None: The resource content as a string, or None if not found.
        """
        if not uri.startswith("xtb://"):
            return None

        parts = uri.replace("xtb://", "").split("/")
        if len(parts) != 2:
            return None

        category, identifier = parts
        print(f"Debug: Requesting resource category='{category}', identifier='{identifier}'") # Debug info

        if category == "templates":
            # Identifier might be "sampling:metadynamics" or "singlepoint"
            return self.templates.get(identifier)
        elif category == "sampling": # Handling xtb://sampling/metadynamics
            # We expect identifier to be like "metadynamics"
            # The key in self.templates would be "sampling:metadynamics"
            return self.templates.get(f"sampling:{identifier}")
        elif category == "wavefunction": # Handling xtb://wavefunction/orbitals
            # Identifier would be "orbitals"
            # Key in self.templates would be "wavefunction:orbitals"
            return self.templates.get(f"wavefunction:{identifier}")
        elif category == "advanced": # Handling xtb://advanced/oniom
            # Identifier would be "oniom"
            # Key in self.templates would be "advanced:oniom"
            return self.templates.get(f"advanced:{identifier}")
        elif category == "parameters":
            return self.parameter_docs.get(identifier)
        elif category == "formats":
            if identifier == "input": # Hardcoded handling for formats/input_spec.md
                return self._load_doc_file("formats", "input_spec")
        elif category == "help": # Handling xtb://help/faq
            # Identifier would be "faq"
            # These are .md files directly in resources/help/
            return self._load_doc_file("help", identifier)
        # Future expansion for more resource categories
        
        return None

    # --- MCP Tool Implementations (To be populated in future tasks) ---
    def generate_xtb_input_package(self, molecule_data: dict, calculation_type: str, method: str, settings: dict) -> dict:
        """
        Generates an input file package for xtb calculations.

        Args:
            molecule_data (dict): Contains molecular structure information.
                Expected keys: "format" (e.g., "xyz"), "content" (structure string),
                               "charge" (int), "multiplicity" (int).
            calculation_type (str): Type of calculation (e.g., "singlepoint", "optimization").
            method (str): xtb method (e.g., "gfn2", "gfn1").
            settings (dict): Other calculation settings (e.g., "solvent", "temperature").
        
        Returns:
            dict: A dictionary containing generated filenames and their content.
                  Example: {"structure.xyz": "...", ".xcontrolrc": "..."}
                  or {"error": "message"} on error.
        """
        files_to_return = {}
        warnings = []  # Initialize warnings list

        # 1. Process molecular structure data
        mol_format = molecule_data.get("format", "xyz").lower()
        mol_content = molecule_data.get("content")
        charge = molecule_data.get("charge", 0)
        # xtb uses unpaired electrons, multiplicity = 2S + 1 => S = (multiplicity - 1)/2
        # Unpaired electrons = 2S = multiplicity - 1
        spin_unpaired_electrons = molecule_data.get("multiplicity", 1) - 1


        if not mol_content:
            return {"error": "Molecular structure content ('content') not provided."}

        if mol_format != "xyz":
            # TODO: Use convert_structure_file_format for conversion in the future
            return {"error": f"Currently only 'xyz' format is supported for molecular structure input, received: {mol_format}"}
        
        files_to_return["structure.xyz"] = mol_content

        # 2. Select and populate the .xcontrolrc template
        template_key_map = {
            "singlepoint": "singlepoint",
            "optimization": "optimization",
            "frequency": "frequency",
            "scan": "scan",
            "md": "md",
        }
        calc_type_lower = calculation_type.lower()
        template_name = template_key_map.get(calc_type_lower)

        if not template_name:
            return {"error": f"Unsupported calculation type: {calculation_type}. Supported types: {list(template_key_map.keys())}"}

        xcontrol_template = self.templates.get(template_name)
        if not xcontrol_template:
            return {"error": f"Template '{template_name}' for calculation type '{calculation_type}' not found."}

        # 3. Prepare parameters for replacement
        # GFN version mapping
        gfn_version_map = {
            "gfn0": "0",
            "gfn1": "1",
            "gfn2": "2",
            "gfnff": "2"  # GFN-FF usually doesn't need a $gfn block, but using default here for generality
        }
        
        method_lower = method.lower()
        gfn_method_for_template = gfn_version_map.get(method_lower, "2")  # Default to GFN2
        
        if method_lower == "gfnff":
            # GFN-FF usually does not use the $gfn block, but rather --gfnff via command line
            # Or there might be a specific $gfnff block in .xcontrolrc (refer to xtb documentation)
            # This is simplified for now, can be improved later
            print("Warning: GFN-FF method selected, $gfn line in template might need adjustment or removal.")


        # Basic replacements
        # TODO: Use a more robust templating engine, e.g., Jinja2
        xcontrol_content = xcontrol_template
        xcontrol_content = xcontrol_content.replace("{charge}", str(charge))
        xcontrol_content = xcontrol_content.replace("{spin_multiplicity}", str(spin_unpaired_electrons)) # Use unpaired electron count
        xcontrol_content = xcontrol_content.replace("{gfn_version}", gfn_method_for_template) # Use mapped method string

        # Process settings
        solvent = settings.get("solvent", "none") # Default to gas phase
        temperature = settings.get("temperature", 298.15) # Default room temperature

        xcontrol_content = xcontrol_content.replace("{solvent}", str(solvent))
        xcontrol_content = xcontrol_content.replace("{temperature}", str(temperature))

        # Calculation type specific settings
        if calc_type_lower == "optimization":
            opt_level = settings.get("opt_level", "normal") # settings from generate_xtb_input tool
            max_opt_cycles = settings.get("max_opt_cycles", 200)
            xcontrol_content = xcontrol_content.replace("{opt_level}", str(opt_level))
            xcontrol_content = xcontrol_content.replace("{max_opt_cycles}", str(max_opt_cycles))
        elif calc_type_lower == "scan":
            # Scan usually requires an $opt block for optimization at each step
            opt_level = settings.get("opt_level", "normal")
            max_opt_cycles = settings.get("max_opt_cycles", 100) # Optimization in scan usually has fewer cycles
            xcontrol_content = xcontrol_content.replace("{opt_level}", str(opt_level))
            xcontrol_content = xcontrol_content.replace("{max_opt_cycles}", str(max_opt_cycles))
            
            scan_parameters_content = settings.get("scan_parameters")
            if scan_parameters_content:
                # If scan_parameters is a string, it's assumed to be the content of scan.inp
                if isinstance(scan_parameters_content, str):
                    files_to_return["scan.inp"] = scan_parameters_content
                    # Ensure .xcontrolrc includes $input "scan.inp"
                    if "$input \"scan.inp\"" not in xcontrol_content:
                        # Attempt to add to the end of the $scan block or end of file
                        # For simplicity, if not in template, append to end
                        # A more robust approach would be to ensure placeholders or specific locations in the template
                        if "# $input \"scan.inp\"" in xcontrol_content: # Commented out line in template
                             xcontrol_content = xcontrol_content.replace("# $input \"scan.inp\"", "$input \"scan.inp\"")
                        else: # Otherwise append to end
                             xcontrol_content += "\n$input \"scan.inp\""
                else: # TODO: Support generating scan.inp content from a dictionary
                    warnings.append("scan_parameters should be a string (scan.inp content) or a specific dictionary structure (not yet implemented).")
            # else: Template might contain inline scan definition

        elif calc_type_lower == "md":
            md_temperature = settings.get("md_temperature", temperature) # MD temperature, defaults to global temperature
            scc_temperature = settings.get("scc_temperature", md_temperature) # SCC temperature
            simulation_time_ps = settings.get("simulation_time_ps", 1.0)
            time_step_fs = settings.get("time_step_fs", 1.0)
            dump_frequency_fs = settings.get("dump_frequency_fs", time_step_fs * 10) # Output every 10 steps

            xcontrol_content = xcontrol_content.replace("{md_temperature}", str(md_temperature))
            xcontrol_content = xcontrol_content.replace("{scc_temperature}", str(scc_temperature))
            xcontrol_content = xcontrol_content.replace("{simulation_time_ps}", str(simulation_time_ps))
            xcontrol_content = xcontrol_content.replace("{time_step_fs}", str(time_step_fs))
            xcontrol_content = xcontrol_content.replace("{dump_frequency_fs}", str(dump_frequency_fs))
            # TODO: Populate optional MD parameters like thermostat, sccacc, velv

        # Handle general constraints
        constraints_content = settings.get("constraints")
        if constraints_content:
            if isinstance(constraints_content, str):
                files_to_return["constraints.inp"] = constraints_content
                # Ensure .xcontrolrc includes $constrain file=constraints.inp
                # (Usually the $constrain block itself is in the template, here it specifies an external file)
                # Alternatively, if the template has a $constrain block, content can be inserted directly
                # For simplicity, assume no $constrain block in template, or user will add manually
                # To automatically add $constrain file=..., more complex template processing is needed
                if "$constrain" not in xcontrol_content: # Very rough check
                    xcontrol_content += "\n$constrain\n  file=constraints.inp\n$end"
                elif "file=" not in xcontrol_content: # If $constrain exists but no file=
                     # This is imperfect logic, might need smarter insertion
                     pass # Not handled for now, relies on template or user
                else:
                    warnings.append("constraints should be a string (constraints.inp content).")


        # Remove untransformed placeholders (simple cleanup, should be handled by templating engine later)
        lines = xcontrol_content.splitlines()
        final_xcontrol_lines = []
        for line in lines:
            if "{" in line and "}" in line: # Contains untransformed placeholders
                # Check if it's a placeholder for an optional block, if so, remove the entire line
                # This is a very rough judgment, e.g., {optional_block_param}
                # A better approach is for the templating engine to support conditional blocks
                # For now: if it contains a placeholder and is not the start of a $ block, remove it
                if not line.strip().startswith("$"):
                    print(f"Warning: Removing line containing unparsed placeholder: '{line}'")
                    continue
            final_xcontrol_lines.append(line)
        xcontrol_content = "\n".join(final_xcontrol_lines)

        files_to_return[".xcontrolrc"] = xcontrol_content
        
        # 4. Generate run_xtb.sh script
        # Assume xtb is in PATH, structure file is structure.xyz, control file is .xcontrolrc
        run_script_content = f"""#!/bin/bash
# Basic script to run XTB calculation

# Ensure xtb is in your PATH
# Ensure structure.xyz and .xcontrolrc are in the current directory

xtb structure.xyz --input .xcontrolrc --chrg {charge} --uhf {spin_unpaired_electrons} -P $(nproc) --gfn {gfn_method_for_template} > xtb_output.log 2>&1

# Optional: add --gbsa {solvent} if solvent is used and not 'none'
# Optional: add --opt, --hess, --scan, --md flags if not fully controlled by .xcontrolrc
# (though best practice is to control via .xcontrolrc)

echo "XTB calculation started. Check xtb_output.log for progress."
"""
        if solvent and solvent.lower() != "none":
             # Simply append --gbsa to the command (might be redundant but harmless if $alpb is not in .xcontrolrc)
             run_script_content = run_script_content.replace(f"--gfn {gfn_method_for_template}", f"--gfn {gfn_method_for_template} --gbsa {solvent.lower()}")


        files_to_return["run_xtb.sh"] = run_script_content
        
        if warnings: # Add warnings to the returned dictionary
            files_to_return["warnings"] = warnings

        return files_to_return

    def validate_xtb_input_files(self, input_files: dict) -> dict:
        """
        Validates xtb input files (primarily .xcontrolrc and charge/spin information in structure files).

        Args:
            input_files (dict): Contains input file content.
                Expected keys:
                "structure_file_content" (str, optional): Molecular structure file content (e.g., XYZ).
                "xcontrol_content" (str): .xcontrolrc file content.
                "expected_charge" (int, optional): Expected molecular charge.
                "expected_multiplicity" (int, optional): Expected spin multiplicity.


        Returns:
            dict: Contains validation results {"is_valid": bool, "errors": [], "warnings": []}
        """
        errors = []
        warnings = []
        is_valid = True

        xcontrol_content = input_files.get("xcontrol_content")
        structure_content = input_files.get("structure_file_content") # Currently unused, can be used for structural sanity checks in the future
        
        expected_charge = input_files.get("expected_charge")
        expected_multiplicity = input_files.get("expected_multiplicity")

        if not xcontrol_content:
            errors.append("'.xcontrolrc' content not provided.")
            is_valid = False
            return {"is_valid": is_valid, "errors": errors, "warnings": warnings}

        # 1. Parse $chrg and $spin from .xcontrolrc
        xcontrol_charge = None
        xcontrol_spin_unpaired = None # xtb uses unpaired electron count

        for line in xcontrol_content.splitlines():
            line_stripped = line.strip()
            if line_stripped.startswith("$chrg"):
                try:
                    xcontrol_charge = int(line_stripped.split()[-1])
                except (ValueError, IndexError):
                    errors.append(f"Could not parse '$chrg' line: '{line_stripped}'")
                    is_valid = False
            elif line_stripped.startswith("$spin"):
                try:
                    xcontrol_spin_unpaired = int(line_stripped.split()[-1])
                except (ValueError, IndexError):
                    errors.append(f"Could not parse '$spin' line: '{line_stripped}'")
                    is_valid = False
            elif line_stripped.startswith("$uhf"): # $uhf is an alias for $spin
                try:
                    xcontrol_spin_unpaired = int(line_stripped.split()[-1])
                except (ValueError, IndexError):
                    errors.append(f"Could not parse '$uhf' line: '{line_stripped}'")
                    is_valid = False
        
        if xcontrol_charge is None:
            errors.append("'$chrg' definition not found in '.xcontrolrc'.")
            is_valid = False
        
        if xcontrol_spin_unpaired is None:
            errors.append("'$spin' or '$uhf' definition not found in '.xcontrolrc'.")
            is_valid = False

        # 2. Compare if expected values are provided
        if expected_charge is not None and xcontrol_charge is not None:
            if xcontrol_charge != expected_charge:
                errors.append(f"Charge in '.xcontrolrc' ({xcontrol_charge}) does not match expected charge ({expected_charge}).")
                is_valid = False
        
        if expected_multiplicity is not None and xcontrol_spin_unpaired is not None:
            expected_spin_unpaired = expected_multiplicity - 1
            if xcontrol_spin_unpaired != expected_spin_unpaired:
                errors.append(f"Unpaired electron count in '.xcontrolrc' ({xcontrol_spin_unpaired}) does not match expected spin multiplicity ({expected_multiplicity}, corresponding to {expected_spin_unpaired} unpaired electrons).")
                is_valid = False
        
        # 3. Check consistency of charge and spin multiplicity (basic rules)
        # A very rough check: odd number of electrons usually corresponds to doublet or higher odd multiplicity, even number of electrons usually corresponds to singlet or higher even multiplicity.
        # (Total electrons - Charge) % 2 == Unpaired electrons % 2
        # This check is complex and requires knowing the total number of electrons in the system, so it's skipped for now.
        # TODO: Implement more advanced charge/spin consistency checks, possibly requiring atomic number information.

        # 4. Basic syntax check (very preliminary)
        # Check for unclosed blocks (simple $... and $end counting)
        block_stack = []
        for line_num, line in enumerate(xcontrol_content.splitlines()):
            line_stripped = line.strip()
            if line_stripped.startswith("$") and not line_stripped.startswith(("$chrg", "$spin", "$uhf", "$gfn")): # Simple parameters are not pushed to stack
                # Exclude some known single-line directives that don't require $end
                known_single_line_directives = ["$alpb", "$gfnff"] # Can be extended
                is_single_line_directive = any(line_stripped.startswith(d) for d in known_single_line_directives)

                if not is_single_line_directive and line_stripped != "$end":
                    block_name = line_stripped.split()[0]
                    block_stack.append((block_name, line_num + 1))
                elif line_stripped == "$end":
                    if not block_stack:
                        errors.append(f"Excessive '$end' found on line {line_num + 1}.")
                        is_valid = False
                    else:
                        block_stack.pop()
        
        if block_stack:
            for block_name, line_num in block_stack:
                errors.append(f"Block '{block_name}' (starting on line {line_num}) did not find a corresponding '$end'.")
                is_valid = False
        
        # 5. Method and setting compatibility check (preliminary)
        gfn_version_in_control = None
        has_oniom_block = False
        has_embedding_block = False
        # ... Other specific blocks or parameters to check

        for line in xcontrol_content.splitlines():
            line_stripped = line.strip()
            if line_stripped.startswith("$gfn"):
                try:
                    gfn_version_in_control = line_stripped.split()[-1].lower()
                except IndexError:
                    pass # $gfn line format error, possibly caught earlier
            if line_stripped.startswith("$oniom"):
                has_oniom_block = True
            if line_stripped.startswith("$embedding"):
                has_embedding_block = True
            # ... 检查其他特定设置

        if has_oniom_block:
            # ONIOM is typically used with GFN2-xTB or GFN1-xTB, GFN0 might have limited support
            if gfn_version_in_control == "0":
                warnings.append("Warning: $oniom block used with GFN0-xTB, support might be limited or results suboptimal. GFN1 or GFN2 recommended.")
            if "gfnff" in gfn_version_in_control: # GFN-FF does not support ONIOM
                 errors.append("Error: $oniom block is incompatible with GFN-FF.")
                 is_valid = False
        
        if has_embedding_block:
            if "gfnff" in gfn_version_in_control:
                 errors.append("Error: $embedding block is incompatible with GFN-FF.")
                 is_valid = False
            # Other compatibility checks can be added

        # TODO: Add more validation rules, e.g., parameter value ranges.

        return {"is_valid": is_valid, "errors": errors, "warnings": warnings}

    def convert_structure_file_format(self, input_format: str, output_format: str, structure_data: str) -> dict:
        """
        Converts between different molecular structure formats.

        Args:
            input_format (str): Input structure format (e.g., "xyz", "coord").
            output_format (str): Output structure format (e.g., "xyz", "coord").
            structure_data (str): Original structure data string.

        Returns:
            dict: Contains "converted_content" and "output_filename_suggestion" or "error".
        """
        input_fmt = input_format.lower()
        output_fmt = output_format.lower()

        if input_fmt == output_fmt:
            return {
                "converted_content": structure_data,
                "output_filename_suggestion": f"structure.{output_fmt}",
                "message": "Input and output formats are the same, no conversion needed."
            }

        converted_content = None
        error_message = None
        output_filename_suggestion = f"structure_converted.{output_fmt}"

        if input_fmt == "xyz" and output_fmt == "coord":
            converted_content, error_message = structure_utils.xyz_to_coord_string(structure_data)
            if not error_message:
                 output_filename_suggestion = "coord" # TURBOMOLE default filename
        elif input_fmt == "coord" and output_fmt == "xyz":
            converted_content, error_message = structure_utils.coord_string_to_xyz(structure_data)
            if not error_message:
                output_filename_suggestion = "structure.xyz"
        elif input_fmt == "gaussian" and output_fmt == "xyz":
            converted_content, error_message = structure_utils.gaussian_to_xyz_string(structure_data)
            if not error_message:
                output_filename_suggestion = "structure_from_gaussian.xyz"
        # TODO: Support more conversion paths, e.g., via Open Babel (if available)
        # E.g.: xyz to vasp, gaussian to coord etc.
        else:
            return {"error": f"Conversion from '{input_fmt}' to '{output_fmt}' is not supported. Currently supported: xyz<->coord, gaussian->xyz."}

        if error_message:
            return {"error": f"Conversion failed: {error_message}"}
        
        if converted_content is None: # 双重检查，以防辅助函数返回 (None, None)
            return {"error": "An unknown error occurred during conversion, no content generated."}

        return {
            "converted_content": converted_content,
            "output_filename_suggestion": output_filename_suggestion
        }

    def generate_xcontrol_file(self, charge: int, spin_multiplicity: int, calculation_settings: dict) -> dict:
        """
        Generates the content of the .xcontrolrc file.

        Args:
            charge (int): Molecular charge.
            spin_multiplicity (int): Spin multiplicity.
            calculation_settings (dict): Contains calculation type and related parameters.
                Expected keys:
                "calculation_type": "singlepoint|optimization|frequency|scan|md"
                "method": "gfn0|gfn1|gfn2|gfnff" (for template selection or specific parameters)
                "solvent": "h2o", "none", etc. (optional)
                "temperature": float (optional)
                "optimization_settings": {"level": "normal", "maxcycle": 200} (optional, for optimization)
                # ... Other calculation type specific settings

        Returns:
            dict: Contains ".xcontrolrc" content or error message.
                  e.g., {"xcontrol_content": "...", "warnings": []} or {"error": "message"}
        """
        # xtb uses unpaired electrons: multiplicity = 2S + 1 => S = (multiplicity - 1)/2
        # Unpaired electrons = 2S = multiplicity - 1
        spin_unpaired_electrons = spin_multiplicity - 1

        calc_type = calculation_settings.get("calculation_type", "singlepoint").lower()
        method = calculation_settings.get("method", "gfn2").lower()
        
        content_lines = []
        warnings = []

        # 1. Basic parameters: $chrg, $spin, $gfn
        content_lines.append(f"$chrg {charge}")
        content_lines.append(f"$spin {spin_unpaired_electrons}")
        
        gfn_version_str = "2" # Default GFN2
        if method == "gfn0":
            gfn_version_str = "0"
        elif method == "gfn1":
            gfn_version_str = "1"
        elif method == "gfnff":
            warnings.append("GFN-FF method selected; $gfn block might be unnecessary or require specific $gfnff block.")
        # For GFN2 or unspecified method (defaults to GFN2), add $gfn 2
        if method == "gfn2" or method not in ["gfn0", "gfn1", "gfnff"]:
             content_lines.append(f"$gfn {gfn_version_str}")
        elif method in ["gfn0", "gfn1"]:
             content_lines.append(f"$gfn {gfn_version_str}")


        # 2. Solvent
        solvent = calculation_settings.get("solvent")
        if solvent and solvent.lower() != "none":
            content_lines.append(f"$alpb {solvent.lower()}")
        
        # 3. SCC block (usually requires temperature)
        temperature = calculation_settings.get("temperature", 298.15)
        scc_settings = calculation_settings.get("scc_settings", {})
        scc_maxiter = scc_settings.get("maxiter", 250)
        scc_etol = scc_settings.get("etol", "1.d-7")

        content_lines.append("$scc")
        content_lines.append(f"  temp={temperature}")
        content_lines.append(f"  maxiter={scc_maxiter}")
        content_lines.append(f"  etol={scc_etol}")
        content_lines.append("$end")

        # 4. Calculation type specific blocks
        if calc_type == "optimization":
            opt_settings = calculation_settings.get("optimization_settings", {})
            opt_level = opt_settings.get("level", "normal")
            opt_maxcycle = opt_settings.get("maxcycle", 200)
            content_lines.append("$opt")
            content_lines.append(f"  level={opt_level}")
            content_lines.append(f"  maxcycle={opt_maxcycle}")
            content_lines.append("$end")
        elif calc_type == "frequency":
            hess_settings = calculation_settings.get("hessian_settings", {})
            hess_temp = hess_settings.get("temperature", temperature)
            content_lines.append("$hess")
            content_lines.append(f"  temp={hess_temp}")
            content_lines.append("$end")
        elif calc_type == "singlepoint":
            pass
        
        # 5. Output control $write (basic)
        write_settings = calculation_settings.get("output_settings", {})
        write_json = write_settings.get("json", True)
        
        content_lines.append("$write")
        if write_json:
            content_lines.append("  json=true")
        content_lines.append("$end")

        return {"xcontrol_content": "\n".join(content_lines), "warnings": warnings}

    def explain_xtb_parameters_info(self, parameter_type: str, specific_parameter: str | None = None) -> dict:
        """
        Explains the meaning and usage recommendations for xtb parameters.

        Args:
            parameter_type (str): Parameter type (e.g., "globpar", "method", "gfn2", "gfn1", "gfn0").
                                  "globpar" refers to global parameters like $chrg, $spin.
                                  "gfn2", "gfn1", "gfn0" will attempt to load corresponding parameter documentation.
            specific_parameter (str, optional): Specific parameter name (e.g., "$chrg", "temp" in $scc).

        Returns:
            dict: Contains "explanation" (str) or "error".
        """
        param_type_lower = parameter_type.lower()

        # Attempt to retrieve information from already loaded parameter documentation
        # (e.g., if parameter_type is "gfn2", "gfn1", "gfn0")
        if param_type_lower in self.parameter_docs:
            doc_content = self.parameter_docs[param_type_lower]
            if specific_parameter:
                # Attempt to find specific parameters in the documentation (simple text search)
                explanation_lines = []
                found_specific = False
                # Simple line-based search, looking for lines containing the parameter name and its vicinity
                # TODO: Can be improved with more intelligent Markdown parsing
                lines = doc_content.splitlines()
                for i, line in enumerate(lines):
                    if specific_parameter.lower() in line.lower():
                        found_specific = True
                        # Attempt to capture the title or code block where the parameter name is located
                        # This is a heuristic method, might not be perfect
                        start_index = max(0, i - 2) # Context lines
                        end_index = min(len(lines), i + 3) # Context lines
                        context_snippet = "\n".join(lines[start_index:end_index])
                        explanation_lines.append(f"Found relevant content for '{specific_parameter}':\n---\n{context_snippet}\n---")
                        # break # If only the first match is needed

                if found_specific:
                    return {"explanation": "\n".join(explanation_lines) + f"\n\nFor complete '{param_type_lower}' documentation, refer to resource xtb://parameters/{param_type_lower}"}
                else:
                    return {"explanation": f"No specific description for parameter '{specific_parameter}' found directly in '{param_type_lower}' documentation.\nHere is the general documentation for '{param_type_lower}':\n\n{doc_content}"}
            else:
                return {"explanation": f"General documentation for '{param_type_lower}':\n\n{doc_content}"}

        # If not a preloaded documentation type, provide a general explanation
        if param_type_lower == "globpar":
            if specific_parameter:
                sp_lower = specific_parameter.lower()
                if sp_lower == "$chrg":
                    return {"explanation": "$chrg: Defines the total charge of the system. E.g., '$chrg 0' for a neutral system."}
                elif sp_lower == "$spin" or sp_lower == "$uhf":
                    return {"explanation": f"{specific_parameter}: Defines the number of unpaired electrons in the system. E.g., '$spin 0' (or '$uhf 0') for 0 unpaired electrons (usually a singlet state)."}
                elif sp_lower == "$gfn":
                    return {"explanation": "$gfn: Specifies the GFN method version to use. E.g., '$gfn 2' uses GFN2-xTB."}
                elif sp_lower == "$alpb":
                    return {"explanation": "$alpb: Specifies the implicit solvent model. E.g., '$alpb h2o' uses the GBSA water model, '$alpb none' for gas phase."}
                # Can continue to add explanations for other global parameters
                else:
                    return {"explanation": f"No specific explanation found for global parameter '{specific_parameter}'. Please provide parameters like '$chrg', '$spin', etc."}
            else:
                return {"explanation": "Global parameters (globpar) are basic directives in xtb control files, such as $chrg (charge), $spin (spin/unpaired electrons), $gfn (method version), $alpb (solvent model), etc."}
        
        elif param_type_lower == "method":
            # For "method", can point to GFN0, GFN1, GFN2 documentation
            if specific_parameter:
                sp_lower = specific_parameter.lower()
                if sp_lower in ["gfn0", "gfn1", "gfn2"]:
                    if sp_lower in self.parameter_docs:
                        return {"explanation": f"Documentation for method '{sp_lower}':\n\n{self.parameter_docs[sp_lower]}"}
                    else:
                        # Attempt to load from self.parameter_docs (if not loaded before)
                        # But current design loads all in __init__
                        return {"error": f"Parameter documentation for method '{sp_lower}' not found. Please ensure 'resources/parameters/{sp_lower}.md' file exists."}
                else:
                    return {"explanation": f"Unsupported method explanation for '{specific_parameter}'. Please try 'gfn0', 'gfn1', or 'gfn2'."}
            else:
                return {"explanation": "xtb supports various semi-empirical methods, primarily GFN0-xTB, GFN1-xTB, GFN2-xTB, and GFN-FF. GFN2-xTB is currently the recommended general-purpose method. Use the $gfn keyword to specify the version, e.g., '$gfn 2'."}

        return {"error": f"Cannot explain parameter type '{parameter_type}'. Supported types include 'globpar', 'method', or loaded parameter sets (e.g., 'gfn0', 'gfn1', 'gfn2')."}

    def generate_enhanced_sampling_input_package(self, molecule_data: dict, method_settings: dict, sampling_method_type: str, sampling_params: dict) -> dict:
        """
        Generates input file package for enhanced sampling calculations.

        Args:
            molecule_data (dict): Same definition as in generate_xtb_input_package.
            method_settings (dict): Contains basic calculation method information (gfn_version, charge, multiplicity, solvent, temperature).
            sampling_method_type (str): Type of enhanced sampling method (e.g., "metadynamics", "pathfinder").
            sampling_params (dict): Parameters specific to the enhanced sampling method.
                For "metadynamics":
                    "collective_variables_definition" (str): Definition string for coord=... in the $metadyn block.
                    "md_temperature", "simulation_time_ps", "time_step_fs", etc. (MD parameters)
                    "thermostat_type" (str, optional)
                    "kpush_value", "alpha_factor", etc. (metadynamics parameters)
                For "pathfinder":
                    "path_nrun", "path_nopt", "path_kpush", "path_kpull"
                    "product_coord_file" (str): Product structure filename (e.g., "product.xyz")
                    "product_coord_content" (str, optional): Product structure file content, if provided, the file will be created.
                    "opt_level", "max_opt_cycles" (Optimization parameters)


        Returns:
            dict: A dictionary containing generated filenames and their content, or error information.
        """
        files_to_return = {}
        warnings = [] # Initialize warnings list

        # 1. Process molecular structure (similar to generate_xtb_input_package)
        mol_format = molecule_data.get("format", "xyz").lower()
        mol_content = molecule_data.get("content")
        charge = method_settings.get("charge", 0)
        spin_unpaired_electrons = method_settings.get("multiplicity", 1) - 1

        if not mol_content:
            return {"error": "Molecular structure content ('content') not provided."}
        if mol_format != "xyz":
            return {"error": f"Currently only 'xyz' format is supported for molecular structure input, received: {mol_format}"}
        files_to_return["structure.xyz"] = mol_content

        # 2. Get basic calculation parameters
        gfn_version = method_settings.get("gfn_version", "2").lower()
        solvent = method_settings.get("solvent", "none")
        temperature = method_settings.get("temperature", 298.15) # General temperature, MD/SCC might override

        # 3. Select template
        template_key = None
        sampling_method_lower = sampling_method_type.lower()
        if sampling_method_lower == "metadynamics":
            template_key = "sampling:metadynamics"
        elif sampling_method_lower == "pathfinder":
            template_key = "sampling:pathfinder"
        elif sampling_method_lower == "normal_mode_following":
            template_key = "sampling:normal_mode_following"
        else:
            return {"error": f"Unsupported enhanced sampling method: {sampling_method_type}. Supported: metadynamics, pathfinder, normal_mode_following."}

        xcontrol_template = self.templates.get(template_key)
        if not xcontrol_template:
            return {"error": f"Template '{template_key}' for enhanced sampling method '{sampling_method_type}' not found."}

        # 4. Populate template
        xcontrol_content = xcontrol_template
        xcontrol_content = xcontrol_content.replace("{charge}", str(charge))
        xcontrol_content = xcontrol_content.replace("{spin_multiplicity}", str(spin_unpaired_electrons))
        xcontrol_content = xcontrol_content.replace("{gfn_version}", gfn_version)
        xcontrol_content = xcontrol_content.replace("{solvent}", solvent)
        
        # General temperature, MD/SCC blocks might have more specific temperatures
        xcontrol_content = xcontrol_content.replace("{temperature}", str(temperature)) # Replace temperature in $scc

        if sampling_method_lower == "metadynamics":
            md_temp = sampling_params.get("md_temperature", temperature)
            sim_time_ps = sampling_params.get("simulation_time_ps", 10.0)
            time_step_fs = sampling_params.get("time_step_fs", 1.0)
            dump_freq_fs = sampling_params.get("dump_frequency_fs", time_step_fs * 100)
            thermostat = sampling_params.get("thermostat_type", "bussi") # Default bussi
            cv_def = sampling_params.get("collective_variables_definition", "# CVs not defined in input, ensure template or defaults are adequate.")
            if not cv_def.strip() or cv_def.startswith("#"):
                 warnings.append("Metadynamics: Collective variables definition is empty or commented out.")


            xcontrol_content = xcontrol_content.replace("{md_temperature}", str(md_temp))
            xcontrol_content = xcontrol_content.replace("{scc_temperature}", str(md_temp)) # SCC 通常与MD温度一致
            xcontrol_content = xcontrol_content.replace("{simulation_time_ps}", str(sim_time_ps))
            xcontrol_content = xcontrol_content.replace("{time_step_fs}", str(time_step_fs))
            xcontrol_content = xcontrol_content.replace("{dump_frequency_fs}", str(dump_freq_fs))
            xcontrol_content = xcontrol_content.replace("{thermostat_type}", thermostat)
            xcontrol_content = xcontrol_content.replace("{collective_variables_definition}", cv_def)
            
            # Optional Metadynamics Parameters - Replace placeholders in template
            # If parameters are not provided, placeholders will remain and subsequent cleanup steps will attempt to remove them
            meta_params_map = {
                "kpush_value": "{kpush_value}",
                "alpha_factor": "{alpha_factor}",
                "pace_value": "{pace_value}",
                "gaussian_height_kjmol": "{gaussian_height_kjmol}",
                "gaussian_width_au_or_deg": "{gaussian_width_au_or_deg}",
                "bias_factor": "{bias_factor}",
                "grid_spacing_for_hills": "{grh}",
                "hills_file_name": "{file}" # Note that in the template it's {hills_file_name}
            }
            # Correcting hills_file_name key for template
            if "hills_file_name" in sampling_params:
                 xcontrol_content = xcontrol_content.replace(meta_params_map["hills_file_name"], str(sampling_params["hills_file_name"]))


            for param_key, template_placeholder in meta_params_map.items():
                if param_key == "hills_file_name": continue # Already handled
                if param_key in sampling_params:
                    xcontrol_content = xcontrol_content.replace(template_placeholder, str(sampling_params[param_key]))
                else:
                    # If not provided, we might want to remove the line from template if it's optional
                    # This is handled by the generic placeholder cleanup later
                    pass


        elif sampling_method_lower == "pathfinder":
            xcontrol_content = xcontrol_content.replace("{path_nrun}", str(sampling_params.get("path_nrun", 1)))
            xcontrol_content = xcontrol_content.replace("{path_nopt}", str(sampling_params.get("path_nopt", 10)))
            xcontrol_content = xcontrol_content.replace("{path_kpush}", str(sampling_params.get("path_kpush", 0.05)))
            xcontrol_content = xcontrol_content.replace("{path_kpull}", str(sampling_params.get("path_kpull", 0.1)))
            
            product_file_name = sampling_params.get("product_coord_file", "product.xyz")
            xcontrol_content = xcontrol_content.replace("{product_coord_file}", product_file_name)
            
            if "product_coord_content" in sampling_params:
                files_to_return[product_file_name] = sampling_params["product_coord_content"]
            else:
                warnings.append(f"Pathfinder: 'product_coord_content' for '{product_file_name}' not provided. Ensure the file exists or path is correct.")


            opt_level = sampling_params.get("opt_level", "normal")
            max_opt_cycles = sampling_params.get("max_opt_cycles", 50)
            xcontrol_content = xcontrol_content.replace("{opt_level}", str(opt_level))
            xcontrol_content = xcontrol_content.replace("{max_opt_cycles}", str(max_opt_cycles))

        elif sampling_method_lower == "normal_mode_following":
            xcontrol_content = xcontrol_content.replace("{modef_n_points}", str(sampling_params.get("modef_n_points", 10)))
            xcontrol_content = xcontrol_content.replace("{modef_step_size}", str(sampling_params.get("modef_step_size", 0.2)))
            xcontrol_content = xcontrol_content.replace("{modef_mode_index}", str(sampling_params.get("modef_mode_index", 7))) # Default to mode 7 (lowest non-trivial)

            # Optional modef params
            if "modef_freq_threshold" in sampling_params:
                 xcontrol_content = xcontrol_content.replace("{modef_freq_threshold}", str(sampling_params["modef_freq_threshold"]))
            if "modef_projection_mode" in sampling_params:
                 xcontrol_content = xcontrol_content.replace("{modef_projection_mode}", str(sampling_params["modef_projection_mode"]))
            
            # Optimization params for mode following steps
            opt_level = sampling_params.get("opt_level", "normal")
            max_opt_cycles = sampling_params.get("max_opt_cycles", 30) # Usually fewer cycles for mode following steps
            xcontrol_content = xcontrol_content.replace("{opt_level}", str(opt_level))
            xcontrol_content = xcontrol_content.replace("{max_opt_cycles}", str(max_opt_cycles))


        # Clean up unfilled placeholders (rough)
        lines = xcontrol_content.splitlines()
        final_xcontrol_lines = []
        for line in lines:
            if "{" in line and "}" in line: # Contains untransformed placeholders
                # If the line starts with # (comment) or does not start with $ (not a directive), remove it
                if line.strip().startswith("#") or not line.strip().startswith("$"):
                    print(f"Warning: Removing line containing unparsed placeholder: '{line}'")
                    continue
                # For directive lines starting with $, if they contain placeholders, also warn and remove (unless it's a block definition itself)
                # This is a stricter cleanup, requires good template design
                # For now, keep lines starting with $, even if they have placeholders, as they might be block starts
                # A better approach is conditional rendering in the templating engine
                
            final_xcontrol_lines.append(line)
        xcontrol_content = "\n".join(final_xcontrol_lines)
        
        files_to_return[".xcontrolrc"] = xcontrol_content

        # Generate run_xtb.sh script
        run_script_content = f"""#!/bin/bash
xtb structure.xyz --input .xcontrolrc --chrg {charge} --uhf {spin_unpaired_electrons} -P $(nproc) --gfn {gfn_version} > xtb_output.log 2>&1
echo "XTB Enhanced Sampling ({sampling_method_type}) calculation started. Check xtb_output.log for progress."
"""
        if solvent and solvent.lower() != "none":
             run_script_content = run_script_content.replace(f"--gfn {gfn_version}", f"--gfn {gfn_version} --gbsa {solvent.lower()}")
        files_to_return["run_xtb.sh"] = run_script_content

        if warnings: # Add warnings to the return dictionary
            files_to_return["warnings"] = warnings
            
        return files_to_return

    def generate_wavefunction_analysis_input_package(self, molecule_data: dict, method_settings: dict, analysis_params: dict) -> dict:
        """
        Generates xtb input file package for wavefunction and electronic structure analysis.

        Args:
            molecule_data (dict): Same as generate_xtb_input_package.
            method_settings (dict): Contains gfn_version, charge, multiplicity, solvent, temperature.
            analysis_params (dict): Wavefunction analysis related parameters.
                Expected keys:
                "analysis_types" (list[str]): e.g., ["molecular_orbitals", "electron_density", "bond_orders"]
                "output_formats" (dict, optional): e.g., {"cube_files": true, "molden_format": true}
                "visualization_settings" (dict, optional): e.g., {"grid_spacing": 0.1}
                                                           (Primarily for $cube block)
                "specific_orbitals_to_plot" (list[int] or str, optional): e.g., [10, 11] or "HOMO,LUMO"

        Returns:
            dict: A dictionary containing generated filenames and their content, or error information.
        """
        files_to_return = {}
        warnings = [] # Initialize warnings

        # 1. Process molecular structure
        mol_format = molecule_data.get("format", "xyz").lower()
        mol_content = molecule_data.get("content")
        charge = method_settings.get("charge", 0)
        spin_unpaired_electrons = method_settings.get("multiplicity", 1) - 1

        if not mol_content:
            return {"error": "Molecular structure content ('content') not provided."}
        if mol_format != "xyz":
            return {"error": f"Currently only 'xyz' format is supported for molecular structure input, received: {mol_format}"}
        files_to_return["structure.xyz"] = mol_content

        # 2. Get basic calculation parameters
        gfn_version = method_settings.get("gfn_version", "2").lower()
        solvent = method_settings.get("solvent", "none")
        temperature = method_settings.get("temperature", 298.15)

        # 3. Select base template
        template_key = "wavefunction:orbitals"
        xcontrol_template = self.templates.get(template_key)
        if not xcontrol_template:
            return {"error": f"Base template '{template_key}' for wavefunction analysis not found."}

        # 4. Populate base template parameters
        xcontrol_content = xcontrol_template
        xcontrol_content = xcontrol_content.replace("{charge}", str(charge))
        xcontrol_content = xcontrol_content.replace("{spin_multiplicity}", str(spin_unpaired_electrons))
        xcontrol_content = xcontrol_content.replace("{gfn_version}", gfn_version)
        xcontrol_content = xcontrol_content.replace("{solvent}", solvent)
        xcontrol_content = xcontrol_content.replace("{temperature}", str(temperature)) # For $scc if present in template


        # 5. Modify $write and $cube blocks based on analysis_params
        write_directives = {"json=true"}
        cube_directives = [] # Store as list of strings like "cal=1"

        analysis_types = analysis_params.get("analysis_types", [])
        output_formats = analysis_params.get("output_formats", {})
        vis_settings = analysis_params.get("visualization_settings", {})

        for analysis in analysis_types:
            atype = analysis.lower()
            if atype == "molecular_orbitals":
                write_directives.add("mos=true")
                write_directives.add("orbital_energies=true")
            elif atype == "localized_molecular_orbitals":
                write_directives.add("lmo=true")
            elif atype == "electron_density":
                write_directives.add("density=true")
                if output_formats.get("cube_files", False):
                    cube_directives.append("cal=1")
            elif atype == "spin_density":
                write_directives.add("spin_density=true")
                if output_formats.get("cube_files", False):
                    cube_directives.append("cal=4")
            elif atype == "bond_orders":
                write_directives.add("wiberg=true")
            elif atype == "population_analysis":
                write_directives.add("mulliken=true")
                write_directives.add("charges=true")
            elif atype == "esp_charges":
                write_directives.add("esp=true")
                if output_formats.get("cube_files", False):
                     cube_directives.append("cal=5")
            elif atype == "fod":
                write_directives.add("fod=true")
        
        # Build $write block string
        write_block_content = "$write\n" + "\n".join([f"  {d}" for d in sorted(list(write_directives))]) + "\n$end"
        
        # Replace or append $write block
        # A more robust way would be to parse the template, but for now, simple replacement
        if "$write" in xcontrol_content:
            # Find the start of $write and its corresponding $end
            import re
            match = re.search(r"(\$write.*?\$end)", xcontrol_content, re.DOTALL | re.IGNORECASE)
            if match:
                xcontrol_content = xcontrol_content.replace(match.group(1), write_block_content)
            else: # $write found but no $end, append (less ideal)
                xcontrol_content += "\n" + write_block_content
                warnings.append("Original $write block in template was malformed (no $end); appended new $write block.")
        else:
            xcontrol_content += "\n" + write_block_content
        
        # Build $cube block string (if needed)
        if cube_directives or analysis_params.get("specific_orbitals_to_plot"):
            cube_block_lines = ["$cube"]
            cube_block_lines.append(f"  step={vis_settings.get('cube_grid_step', vis_settings.get('grid_spacing', 0.2))}")
            cube_block_lines.append(f"  pthr={vis_settings.get('cube_density_threshold', 1e-5)}")
            
            specific_orbitals = analysis_params.get("specific_orbitals_to_plot")
            if specific_orbitals:
                # Ensure cal=3 for MO plotting
                cube_directives = [d for d in cube_directives if not d.startswith("cal=")]
                cube_directives.append("cal=3")
                if isinstance(specific_orbitals, list) and all(isinstance(o, int) for o in specific_orbitals):
                    cube_block_lines.append(f"  mo={','.join(map(str, specific_orbitals))}")
                elif isinstance(specific_orbitals, str):
                    # Basic HOMO/LUMO parsing, assuming HOMO index is known or can be estimated
                    # This is a placeholder for a more complex HOMO/LUMO index determination
                    if specific_orbitals.lower() == "homo":
                        warnings.append("Plotting 'HOMO': Actual index needs to be determined by a pre-calculation or estimation. Using placeholder index -1.")
                        cube_block_lines.append("  mo=-1") # Placeholder, xtb might interpret -1 as HOMO
                    elif specific_orbitals.lower() == "lumo":
                        warnings.append("Plotting 'LUMO': Actual index needs to be determined. Using placeholder index -2.")
                        cube_block_lines.append("  mo=-2") # Placeholder
                    else:
                        warnings.append(f"String-based specific orbital plotting ('{specific_orbitals}') is not fully supported beyond simple HOMO/LUMO placeholders.")
                else: # min/max range
                    mo_min = vis_settings.get("orbital_range", [None,None])[0]
                    mo_max = vis_settings.get("orbital_range", [None,None])[1]
                    if mo_min is not None and mo_max is not None:
                         cube_block_lines.append(f"  mo={mo_min}-{mo_max}")


            # Add other cal= directives if not plotting specific MOs
            if not specific_orbitals:
                 cube_block_lines.extend([f"  {d}" for d in cube_directives])

            cube_block_lines.append("$end")
            cube_block_str = "\n".join(cube_block_lines)

            # Replace or append $cube block
            if "$cube" in xcontrol_content:
                match_cube = re.search(r"(\$cube.*?\$end)", xcontrol_content, re.DOTALL | re.IGNORECASE)
                if match_cube:
                    xcontrol_content = xcontrol_content.replace(match_cube.group(1), cube_block_str)
                else:
                    xcontrol_content += "\n" + cube_block_str
                    warnings.append("Original $cube block in template was malformed; appended new $cube block.")
            elif cube_directives: # Only add if there are directives
                xcontrol_content += "\n" + cube_block_str


        files_to_return[".xcontrolrc"] = xcontrol_content

        # Generate run_xtb.sh script
        run_script_content = f"""#!/bin/bash
xtb structure.xyz --input .xcontrolrc --chrg {charge} --uhf {spin_unpaired_electrons} -P $(nproc) --gfn {gfn_version} > xtb_output.log 2>&1
echo "XTB Wavefunction Analysis calculation started. Check xtb_output.log for progress."
"""
        if solvent and solvent.lower() != "none":
             run_script_content = run_script_content.replace(f"--gfn {gfn_version}", f"--gfn {gfn_version} --gbsa {solvent.lower()}")
        files_to_return["run_xtb.sh"] = run_script_content
        
        if warnings:
            files_to_return["warnings"] = warnings

        return files_to_return

    def generate_oniom_input_package(self, molecule_data: dict, method_settings: dict, oniom_params: dict) -> dict:
        """
        Generates input file package for ONIOM calculations.

        Args:
            molecule_data (dict): Same as generate_xtb_input_package.
            method_settings (dict): Contains gfn_version_high_level, total_charge, total_spin_multiplicity, solvent, temperature.
            oniom_params (dict): ONIOM calculation specific parameters.
                Expected keys:
                "qmatoms_definition" (str): QM atom definition (e.g., "qmatoms=1,2,3" or "qmfile=qm_atoms.list").
                "method_low_level" (str): Low-level method (e.g., "gfnff").
                "link_atoms_definition" (str, optional): Link atom definition string.
                "oniom_settings" (str, optional): Other settings string within the $oniom block.
                "opt_level" (str, optional): Optimization level.
                "max_opt_cycles" (int, optional): Maximum optimization cycles.
                "qm_atoms_list_content" (str, optional): If qmatoms_definition uses qmfile, this is the file content.

        Returns:
            dict: A dictionary containing generated filenames and their content, or error information.
        """
        files_to_return = {}
        warnings = []

        # 1. Process molecular structure
        mol_format = molecule_data.get("format", "xyz").lower()
        mol_content = molecule_data.get("content")
        if not mol_content:
            return {"error": "Molecular structure content ('content') not provided."}
        if mol_format != "xyz":
            return {"error": f"Currently only 'xyz' format is supported for molecular structure input, received: {mol_format}"}
        files_to_return["structure.xyz"] = mol_content

        # 2. Get basic calculation parameters
        gfn_version_high = method_settings.get("gfn_version_high_level", "2").lower()
        total_charge = method_settings.get("total_charge", 0)
        total_spin_multiplicity = method_settings.get("total_spin_multiplicity", 1) - 1 # to unpaired e-
        solvent = method_settings.get("solvent", "none")
        temperature = method_settings.get("temperature", 298.15)

        # 3. Select template
        template_key = "advanced:oniom"
        xcontrol_template = self.templates.get(template_key)
        if not xcontrol_template:
            return {"error": f"Template '{template_key}' for ONIOM calculation not found."}

        # 4. Populate template
        xcontrol_content = xcontrol_template
        xcontrol_content = xcontrol_content.replace("{gfn_version_high_level}", gfn_version_high)
        xcontrol_content = xcontrol_content.replace("{total_charge}", str(total_charge))
        xcontrol_content = xcontrol_content.replace("{total_spin_multiplicity}", str(total_spin_multiplicity))
        xcontrol_content = xcontrol_content.replace("{solvent}", solvent)
        xcontrol_content = xcontrol_content.replace("{temperature}", str(temperature)) # For $scc

        # ONIOM specific parameters
        xcontrol_content = xcontrol_content.replace("{qmatoms_definition}", oniom_params.get("qmatoms_definition", "# QM atoms not defined"))
        xcontrol_content = xcontrol_content.replace("{method_low_level}", oniom_params.get("method_low_level", "gfnff"))
        xcontrol_content = xcontrol_content.replace("{link_atoms_definition}", oniom_params.get("link_atoms_definition", "# Link atoms not defined"))
        xcontrol_content = xcontrol_content.replace("{oniom_settings}", oniom_params.get("oniom_settings", "# No additional ONIOM settings"))
        
        xcontrol_content = xcontrol_content.replace("{opt_level}", oniom_params.get("opt_level", "normal"))
        xcontrol_content = xcontrol_content.replace("{max_opt_cycles}", str(oniom_params.get("max_opt_cycles", 100)))

        # If qm_atoms.list content is provided
        if "qm_atoms_list_content" in oniom_params and "qmfile=" in oniom_params.get("qmatoms_definition", ""):
            # Extract filename from qmatoms_definition
            qmfile_directive = oniom_params.get("qmatoms_definition")
            try:
                # Assumes format like "qmfile=filename.list" or "qmfile = filename.list"
                qm_filename = qmfile_directive.split("=")[1].strip().replace("\"", "")
                files_to_return[qm_filename] = oniom_params["qm_atoms_list_content"]
            except IndexError:
                warnings.append(f"Could not parse qmfile filename from '{qmfile_directive}'. qm_atoms_list_content not written to file.")


        # Clean up unfilled placeholders (rough)
        lines = xcontrol_content.splitlines()
        final_xcontrol_lines = []
        for line in lines:
            if "{" in line and "}" in line:
                if line.strip().startswith("#") or not line.strip().startswith("$"):
                    print(f"警告: ONIOM - 移除包含未解析占位符的行: '{line}'")
                    continue
            final_xcontrol_lines.append(line)
        xcontrol_content = "\n".join(final_xcontrol_lines)

        files_to_return[".xcontrolrc"] = xcontrol_content

        # Generate run_xtb.sh script
        run_script_content = f"""#!/bin/bash
xtb structure.xyz --input .xcontrolrc --chrg {total_charge} --uhf {total_spin_multiplicity} -P $(nproc) --gfn {gfn_version_high} --oniom > xtb_output.log 2>&1
# Note: --oniom flag might be needed on command line depending on xtb version and .xcontrolrc setup
echo "XTB ONIOM calculation started. Check xtb_output.log for progress."
"""
        if solvent and solvent.lower() != "none":
             run_script_content = run_script_content.replace(f"--gfn {gfn_version_high}", f"--gfn {gfn_version_high} --gbsa {solvent.lower()}")
        files_to_return["run_xtb.sh"] = run_script_content
        
        if warnings:
            files_to_return["warnings"] = warnings

        return files_to_return

    def generate_spectroscopy_input_package(self, molecule_data: dict, method_settings: dict, spectroscopy_params: dict) -> dict:
        """
        Generates input file package for spectroscopic property calculations.

        Args:
            molecule_data (dict): Same as generate_xtb_input_package.
            method_settings (dict): Contains gfn_version, charge, multiplicity, solvent, temperature.
            spectroscopy_params (dict): Spectroscopy calculation specific parameters.
                Expected keys:
                "spectroscopy_types" (list[str]): e.g., ["ir", "uv_vis", "nmr", "stm"]. (Currently only preliminary support for "ir")
                "ir_settings" (dict, optional):
                    "temperature" (float, optional): Temperature for $hess and $scc.
                    "anharmonicity_flag" (bool, optional): Whether to enable ssc in $hess.
                (uv_vis_settings, stm_settings to be implemented later)

        Returns:
            dict: A dictionary containing generated filenames and their content, or error information.
        """
        files_to_return = {}
        warnings = []

        # 1. Process molecular structure
        mol_format = molecule_data.get("format", "xyz").lower()
        mol_content = molecule_data.get("content")
        if not mol_content:
            return {"error": "Molecular structure content ('content') not provided."}
        if mol_format != "xyz":
            return {"error": f"Currently only 'xyz' format is supported for molecular structure input, received: {mol_format}"}
        files_to_return["structure.xyz"] = mol_content

        # 2. Get basic calculation parameters
        gfn_version = method_settings.get("gfn_version", "2").lower()
        charge = method_settings.get("charge", 0)
        spin_unpaired_electrons = method_settings.get("multiplicity", 1) - 1
        solvent = method_settings.get("solvent", "none")
        # Temperature parameter prioritizes specific spectroscopy settings, otherwise uses global settings
        default_temp = method_settings.get("temperature", 298.15)

        # 3. Select template and process based on spectroscopy_types
        spec_types = spectroscopy_params.get("spectroscopy_types", [])
        if not spec_types or not isinstance(spec_types, list):
            return {"error": "'spectroscopy_types' list not provided or format is incorrect."}

        # --- Preliminary support for IR only ---
        if "ir" in [st.lower() for st in spec_types]:
            template_key = "advanced:spectroscopy_ir"
            xcontrol_template = self.templates.get(template_key)
            if not xcontrol_template:
                return {"error": f"Template '{template_key}' for IR spectroscopy calculation not found."}

            xcontrol_content = xcontrol_template
            xcontrol_content = xcontrol_content.replace("{charge}", str(charge))
            xcontrol_content = xcontrol_content.replace("{spin_multiplicity}", str(spin_unpaired_electrons))
            xcontrol_content = xcontrol_content.replace("{gfn_version}", gfn_version)
            xcontrol_content = xcontrol_content.replace("{solvent}", solvent)

            ir_settings = spectroscopy_params.get("ir_settings", {})
            hess_temp = ir_settings.get("temperature", default_temp)
            scc_temp = ir_settings.get("scc_temperature", hess_temp) # SCC temperature usually consistent with Hessian
            
            xcontrol_content = xcontrol_content.replace("{temperature}", str(hess_temp)) # For $hess block
            xcontrol_content = xcontrol_content.replace("{scc_temperature}", str(scc_temp)) # For $scc block

            if ir_settings.get("anharmonicity_flag", False):
                # Template might have # ssc={anharmonicity_flag}
                # Simple replacement or ensure $hess block contains ssc=true
                # Current template design is commented out, uncomment and set value if needed
                # This is a placeholder for more robust template modification
                if "# ssc={anharmonicity_flag}" in xcontrol_content:
                     xcontrol_content = xcontrol_content.replace("# ssc={anharmonicity_flag}", "  ssc=true")
                elif "ssc=" not in xcontrol_content: # If $hess block does not contain ssc
                     # Attempt to add to $hess block (very rough)
                     if "$hess" in xcontrol_content:
                          xcontrol_content = xcontrol_content.replace("$hess", "$hess\n  ssc=true")
            
            # Clean up placeholders
            lines = xcontrol_content.splitlines()
            final_xcontrol_lines = []
            for line in lines:
                if "{" in line and "}" in line:
                    if line.strip().startswith("#") or not line.strip().startswith("$"):
                        print(f"Warning: IR Spec - Removing line containing unparsed placeholder: '{line}'")
                        continue
                final_xcontrol_lines.append(line)
            xcontrol_content = "\n".join(final_xcontrol_lines)
            
            files_to_return[".xcontrolrc"] = xcontrol_content
            current_calc_type_for_run_script = "IR Spectroscopy (Hessian)"
            run_script_options = "--hess" # Default for IR

        elif "uv_vis" in [st.lower() for st in spec_types]:
            template_key = "advanced:spectroscopy_uv_vis"
            xcontrol_template = self.templates.get(template_key)
            if not xcontrol_template:
                return {"error": f"Template '{template_key}' for UV-Vis spectroscopy calculation not found."}

            xcontrol_content = xcontrol_template
            xcontrol_content = xcontrol_content.replace("{charge}", str(charge))
            xcontrol_content = xcontrol_content.replace("{spin_multiplicity}", str(spin_unpaired_electrons))
            
            effective_gfn_version = gfn_version
            if gfn_version == "0":
                warnings.append("GFN0-xTB is not recommended for UV-Vis (sTDA) calculations, results may be unreliable. GFN1 or GFN2 is suggested.")
            xcontrol_content = xcontrol_content.replace("{gfn_version}", effective_gfn_version)
            xcontrol_content = xcontrol_content.replace("{solvent}", solvent)
            xcontrol_content = xcontrol_content.replace("{temperature}", str(default_temp))

            uv_vis_settings = spectroscopy_params.get("uv_vis_settings", {})
            stda_nroots = uv_vis_settings.get("n_states", uv_vis_settings.get("stda_nroots", 10))
            xcontrol_content = xcontrol_content.replace("{stda_nroots}", str(stda_nroots))

            optional_stda_params = {
                "stda_max_iterations": "{stda_max_iterations}",
                "stda_energy_window": "{stda_energy_window}",
                "stda_ssc_correction": "{stda_ssc_correction}"
            }
            for param_key, placeholder in optional_stda_params.items():
                if param_key in uv_vis_settings:
                    xcontrol_content = xcontrol_content.replace(placeholder, str(uv_vis_settings[param_key]))
            
            lines = xcontrol_content.splitlines()
            final_xcontrol_lines = []
            for line in lines:
                is_optional_placeholder_line = False
                for placeholder in optional_stda_params.values():
                    if placeholder in line:
                        # Check if the original key (before _ έγινε) was in settings
                        original_key = placeholder.strip("{}") # e.g. "stda_max_iterations"
                        if original_key not in uv_vis_settings:
                            is_optional_placeholder_line = True
                            break
                if is_optional_placeholder_line:
                    print(f"Warning: UV-Vis Spec - Removing line containing unparsed optional parameter: '{line}'")
                    continue
                
                # General cleanup for other placeholders if any remain
                if "{" in line and "}" in line and (line.strip().startswith("#") or not line.strip().startswith("$")):
                     print(f"Warning: UV-Vis Spec - Removing line containing unparsed placeholder: '{line}'")
                     continue
                final_xcontrol_lines.append(line)
            xcontrol_content = "\n".join(final_xcontrol_lines)

            files_to_return[".xcontrolrc"] = xcontrol_content
            current_calc_type_for_run_script = "UV-Vis Spectroscopy (sTDA)"
            run_script_options = "--stda"

        else:
            return {"error": f"Currently supported spectroscopy types are 'ir', 'uv_vis'. Received types: {spec_types}"}
        
        # Generate run_xtb.sh script
        run_script_content = f"""#!/bin/bash
        xtb structure.xyz --input .xcontrolrc --chrg {charge} --uhf {spin_unpaired_electrons} -P $(nproc) --gfn {gfn_version} --hess > xtb_output.log 2>&1
        # {run_script_options} command line flags ensure corresponding calculations are executed
        echo "XTB {current_calc_type_for_run_script} calculation started. Check xtb_output.log for progress."
"""
        if solvent and solvent.lower() != "none":
             run_script_content = run_script_content.replace(f"--gfn {gfn_version}", f"--gfn {gfn_version} --gbsa {solvent.lower()}")
        files_to_return["run_xtb.sh"] = run_script_content

        if warnings:
            files_to_return["warnings"] = warnings
            
        return files_to_return

    def analyze_md_trajectory_results(self, trajectory_file_content: str, input_format: str, analysis_types: list[str], output_options: dict | None = None) -> dict:
        """
        Analyzes MD trajectories and enhanced sampling results (placeholder).
        Actual implementation may require external libraries such as MDAnalysis, NumPy, Matplotlib, etc.

        Args:
            trajectory_file_content (str): Content of the trajectory file (e.g., xtb.trj, or other common formats if supported).
            input_format (str): Format of the trajectory file (e.g., "xtb_trj", "dcd", "xyz_multi").
            analysis_types (list[str]): List of analysis types to perform
                                       (e.g., "free_energy_surface", "rmsd", "rdf").
            output_options (dict, optional): Output options (e.g., {"plots": true, "data_files": true}).

        Returns:
            dict: Contains analysis results or status.
        """
        print(f"调用: analyze_md_trajectory_results for format {input_format}, types: {analysis_types}")
        # TODO: Implement trajectory analysis logic. This is usually complex and may go beyond simple text processing.
        # - Parse trajectory file.
        # - Perform calculations based on analysis_types.
        # - Generate plots or data files.
        return {"status": "not_implemented_yet", "message": "Trajectory analysis is a complex feature requiring dedicated libraries."}

    # ... (Placeholders for other advanced tools) ...

if __name__ == '__main__':
    # For local testing of the XTBInputGenerator class
    # Ensure the resources folder is under the xtb-mcp-server directory
    # i.e., xtb-mcp-server/resources and xtb-mcp-server/xtb_input_generator
    generator = XTBInputGenerator(resource_base_path="../resources")
    
    print("\n--- Loaded Templates ---")
    for name, content_preview in generator.templates.items():
        print(f"- {name}: {content_preview[:50].replace(os.linesep, ' ')}...")
    
    print("\n--- Loaded Parameter Documentation ---")
    for name, content_preview in generator.parameter_docs.items():
        print(f"- {name}: {content_preview[:50].replace(os.linesep, ' ')}...")

    print("\n--- 测试 get_mcp_resource ---")
    sp_template = generator.get_mcp_resource("xtb://templates/singlepoint")
    print(f"xtb://templates/singlepoint: {sp_template[:70].replace(os.linesep, ' ') if sp_template else '未找到'}...")
    
    gfn2_docs = generator.get_mcp_resource("xtb://parameters/gfn2")
    print(f"xtb://parameters/gfn2: {gfn2_docs[:70].replace(os.linesep, ' ') if gfn2_docs else 'Not found'}...")

    input_spec = generator.get_mcp_resource("xtb://formats/input")
    print(f"xtb://formats/input: {input_spec[:70].replace(os.linesep, ' ') if input_spec else 'Not found'}...")

    non_existent = generator.get_mcp_resource("xtb://nonexistent/stuff")
    print(f"xtb://nonexistent/stuff: {non_existent}")