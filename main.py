from mcp.server.fastmcp import FastMCP
from xtb_input_generator import XTBInputGenerator # Import XTBInputGenerator

# Create MCP server instance
# "XTBInputGeneratorServer" is the name of our server
# Server description and instructions can be added here
mcp = FastMCP(
    name="XTBInputGeneratorServer",
    instructions="""
    This server provides tools and resources for generating xtb quantum chemistry calculation input files.
    - Use 'generate_xtb_input' to create a complete input package.
    - Access templates like 'xtb://templates/singlepoint' for specific calculation types.
    """
)

# --- Initialize XTB Input Generator ---
# XTBInputGenerator handles its own resource path logic
# By default, it looks for a "resources" folder located at the same level as xtb_input_generator
xtb_generator = XTBInputGenerator()

# --- Resource Definitions ---
# Resource functions will now be delegated to the xtb_generator instance

@mcp.resource("xtb://templates/singlepoint")
def get_singlepoint_template() -> str:
    """
    Provides the template for an XTB single point calculation.
    """
    content = xtb_generator.get_mcp_resource("xtb://templates/singlepoint")
    return content if content else "Error: Singlepoint template not found or error loading."

@mcp.resource("xtb://templates/optimization")
def get_optimization_template() -> str:
    """
    Provides the template for an XTB geometry optimization calculation.
    """
    content = xtb_generator.get_mcp_resource("xtb://templates/optimization")
    return content if content else "Error: Optimization template not found or error loading."

@mcp.resource("xtb://templates/frequency")
def get_frequency_template() -> str:
    """
    Provides the template for an XTB frequency calculation.
    """
    content = xtb_generator.get_mcp_resource("xtb://templates/frequency")
    return content if content else "Error: Frequency template not found or error loading."

@mcp.resource("xtb://templates/scan")
def get_scan_template() -> str:
    """
    Provides the template for an XTB scan calculation.
    """
    content = xtb_generator.get_mcp_resource("xtb://templates/scan")
    return content if content else "Error: Scan template not found or error loading."

@mcp.resource("xtb://templates/md")
def get_md_template() -> str:
    """
    Provides the template for an XTB molecular dynamics (MD) calculation.
    """
    content = xtb_generator.get_mcp_resource("xtb://templates/md")
    return content if content else "Error: MD template not found or error loading."

@mcp.resource("xtb://parameters/gfn0")
def get_gfn0_parameters_doc() -> str:
    """
    Provides documentation for GFN0-xTB parameters.
    """
    content = xtb_generator.get_mcp_resource("xtb://parameters/gfn0")
    return content if content else "Error: GFN0 parameters document not found or error loading."

@mcp.resource("xtb://parameters/gfn1")
def get_gfn1_parameters_doc() -> str:
    """
    Provides documentation for GFN1-xTB parameters.
    """
    content = xtb_generator.get_mcp_resource("xtb://parameters/gfn1")
    return content if content else "Error: GFN1 parameters document not found or error loading."

@mcp.resource("xtb://sampling/metadynamics")
def get_metadynamics_template() -> str:
    """
    Provides the template for an XTB metadynamics calculation.
    """
    content = xtb_generator.get_mcp_resource("xtb://sampling/metadynamics")
    return content if content else "Error: Metadynamics template not found or error loading."

@mcp.resource("xtb://sampling/pathfinder")
def get_pathfinder_template() -> str:
    """
    Provides the template for an XTB reaction path search using Pathfinder.
    Note: $path keyword might be version-specific in xtb.
    """
    content = xtb_generator.get_mcp_resource("xtb://sampling/pathfinder")
    return content if content else "Error: Pathfinder template not found or error loading."

@mcp.resource("xtb://sampling/normal_mode_following")
def get_normal_mode_following_template() -> str:
    """
    Provides the template for an XTB normal mode following calculation.
    """
    content = xtb_generator.get_mcp_resource("xtb://sampling/normal_mode_following")
    return content if content else "Error: Normal Mode Following template not found or error loading."

@mcp.resource("xtb://wavefunction/orbitals")
def get_wavefunction_orbitals_template() -> str:
    """
    Provides the template for XTB wavefunction analysis, focusing on orbital output.
    """
    content = xtb_generator.get_mcp_resource("xtb://wavefunction/orbitals")
    return content if content else "Error: Orbitals template not found or error loading."

@mcp.resource("xtb://parameters/gfn2")
def get_gfn2_parameters_doc() -> str:
    """
    Provides documentation for GFN2-xTB parameters.
    """
    content = xtb_generator.get_mcp_resource("xtb://parameters/gfn2")
    return content if content else "Error: GFN2 parameters document not found or error loading."

@mcp.resource("xtb://advanced/oniom")
def get_advanced_oniom_template() -> str:
    """
    Provides the template for an XTB ONIOM calculation.
    """
    content = xtb_generator.get_mcp_resource("xtb://advanced/oniom")
    return content if content else "Error: ONIOM template not found or error loading."

@mcp.resource("xtb://advanced/spectroscopy_ir")
def get_advanced_spectroscopy_ir_template() -> str:
    """
    Provides the template for an XTB IR spectroscopy calculation (based on Hessian).
    """
    content = xtb_generator.get_mcp_resource("xtb://advanced/spectroscopy_ir")
    return content if content else "Error: IR Spectroscopy template not found or error loading."

@mcp.resource("xtb://advanced/spectroscopy_uv_vis")
def get_advanced_spectroscopy_uv_vis_template() -> str:
    """
    Provides the template for an XTB UV-Vis spectroscopy calculation (sTDA).
    """
    content = xtb_generator.get_mcp_resource("xtb://advanced/spectroscopy_uv_vis")
    return content if content else "Error: UV-Vis Spectroscopy template not found or error loading."

@mcp.resource("xtb://help/faq")
def get_help_faq() -> str:
    """
    Provides a list of Frequently Asked Questions about this XTB MCP server.
    """
    content = xtb_generator.get_mcp_resource("xtb://help/faq")
    return content if content else "Error: FAQ document not found or error loading."

@mcp.resource("xtb://formats/input")
def get_input_format_spec() -> str:
    """
    Provides the specification for XTB input formats.
    """
    content = xtb_generator.get_mcp_resource("xtb://formats/input")
    return content if content else "Error: Input format specification not found or error loading."

# --- Tool Definitions ---

@mcp.tool()
def generate_xtb_input(molecule_data: dict, calculation_type: str, method: str, settings: dict) -> dict:
    """
    Generates a complete XTB calculation input package.

    Args:
        molecule_data (dict): Information about the molecule.
            - format (str): e.g., "xyz", "coord".
            - content (str): The actual molecular structure data.
            - charge (int): Molecular charge.
            - multiplicity (int): Spin multiplicity.
        calculation_type (str): Type of calculation, e.g., "singlepoint", "optimization", "frequency".
        method (str): XTB method to use, e.g., "gfn2", "gfn1", "gfn0", "gfnff".
        settings (dict): Additional calculation settings.
            - solvent (str, optional): Solvent name (e.g., "h2o", "toluene"). Defaults to "none" (gas phase).
            - temperature (float, optional): Temperature in Kelvin. Defaults to 298.15.
            - opt_level (str, optional, for optimization): Optimization level. Defaults to "normal".
            - max_opt_cycles (int, optional, for optimization): Max optimization cycles. Defaults to 200.
            # Add other relevant settings as they are implemented

    Returns:
        dict: A dictionary containing filenames as keys and their content as values,
              e.g., {"structure.xyz": "...", ".xcontrolrc": "..."}.
              Returns {"error": "message"} if an error occurs.
    """
    return xtb_generator.generate_xtb_input_package(
        molecule_data=molecule_data,
        calculation_type=calculation_type,
        method=method,
        settings=settings
    )

@mcp.tool()
def generate_xcontrol(charge: int, spin_multiplicity: int, calculation_settings: dict) -> dict:
    """
    Generates the content for an .xcontrolrc file based on provided parameters.

    Args:
        charge (int): Molecular charge.
        spin_multiplicity (int): Spin multiplicity of the molecule.
        calculation_settings (dict): Dictionary containing detailed settings for the calculation.
            - calculation_type (str): e.g., "singlepoint", "optimization", "frequency".
            - method (str): e.g., "gfn2", "gfn1".
            - solvent (str, optional): Name of the solvent.
            - temperature (float, optional): Temperature in Kelvin.
            - optimization_settings (dict, optional): Settings for optimization.
                - level (str): Optimization level.
                - maxcycle (int): Maximum optimization cycles.
            - hessian_settings (dict, optional): Settings for Hessian calculation.
                - temperature (float): Temperature for thermochemical analysis.
            - output_settings (dict, optional): Settings for output.
                - json (bool): Whether to output JSON.

    Returns:
        dict: A dictionary with "xcontrol_content" (str) and "warnings" (list),
              or {"error": "message"} if an error occurs.
    """
    return xtb_generator.generate_xcontrol_file(
        charge=charge,
        spin_multiplicity=spin_multiplicity,
        calculation_settings=calculation_settings
    )

@mcp.tool()
def validate_xtb_input(input_files: dict) -> dict:
    """
    Validates XTB input files, primarily .xcontrolrc content and charge/spin consistency.

    Args:
        input_files (dict): A dictionary containing the content of input files.
            - "xcontrol_content" (str): Content of the .xcontrolrc file.
            - "structure_file_content" (str, optional): Content of the molecular structure file.
            - "expected_charge" (int, optional): The expected molecular charge for validation.
            - "expected_multiplicity" (int, optional): The expected spin multiplicity for validation.

    Returns:
        dict: A dictionary with validation results:
              {"is_valid": bool, "errors": list[str], "warnings": list[str]}
    """
    return xtb_generator.validate_xtb_input_files(input_files=input_files)

@mcp.tool()
def convert_structure_format(input_format: str, output_format: str, structure_data: str) -> dict:
    """
    Converts molecular structure data between different formats.
    Currently supports XYZ to COORD and COORD to XYZ.

    Args:
        input_format (str): The format of the input structure_data (e.g., "xyz", "coord").
        output_format (str): The desired output format (e.g., "xyz", "coord").
        structure_data (str): The string content of the molecular structure.

    Returns:
        dict: A dictionary containing "converted_content" (str) and
              "output_filename_suggestion" (str) upon success,
              or {"error": "message"} if conversion fails or is not supported.
    """
    return xtb_generator.convert_structure_file_format(
        input_format=input_format,
        output_format=output_format,
        structure_data=structure_data
    )

@mcp.tool()
def explain_xtb_parameters(parameter_type: str, specific_parameter: str | None = None) -> dict:
    """
    Explains the meaning and usage of XTB parameters.

    Args:
        parameter_type (str): The type or category of the parameter.
                              Examples: "globpar", "method", "gfn2", "scc", "opt".
        specific_parameter (str, optional): The specific parameter name to explain.
                                           Examples: "$chrg", "temp" (within a block like $scc).

    Returns:
        dict: A dictionary containing the "explanation" (str) or an "error" (str) if not found.
    """
    return xtb_generator.explain_xtb_parameters_info(
        parameter_type=parameter_type,
        specific_parameter=specific_parameter
    )

# TODO: Define other tools here

@mcp.tool()
def generate_enhanced_sampling(molecule_data: dict, method_settings: dict, sampling_method_type: str, sampling_params: dict) -> dict:
    """
    Generates input files for an enhanced sampling calculation (e.g., Metadynamics, Pathfinder).

    Args:
        molecule_data (dict): Molecular structure information.
            - format (str): e.g., "xyz".
            - content (str): Structure data.
        method_settings (dict): Basic calculation method settings.
            - gfn_version (str): e.g., "2", "1", "0".
            - charge (int): Molecular charge.
            - multiplicity (int): Spin multiplicity.
            - solvent (str, optional): Solvent name.
            - temperature (float, optional): General temperature in Kelvin.
        sampling_method_type (str): Type of enhanced sampling (e.g., "metadynamics", "pathfinder").
        sampling_params (dict): Parameters specific to the chosen sampling method.
            For "metadynamics":
                - collective_variables_definition (str): String defining CVs for .xcontrolrc.
                - md_temperature (float, optional): MD temperature.
                - simulation_time_ps (float, optional): Simulation time in ps.
                - time_step_fs (float, optional): MD time step in fs.
                - dump_frequency_fs (float, optional): Trajectory dump frequency in fs.
                - thermostat_type (str, optional): e.g., "bussi".
                - (other metadynamics specific params like kpush_value, alpha_factor, etc.)
            For "pathfinder":
                - path_nrun (int, optional): Number of pathfinder runs.
                - path_nopt (int, optional): Number of path optimization points.
                - path_kpush (float, optional): Pushing force constant.
                - path_kpull (float, optional): Pulling force constant.
                - product_coord_file (str): Filename for product coordinates (e.g., "product.xyz").
                - product_coord_content (str, optional): Content for the product coordinate file.
                - opt_level (str, optional): Optimization level for path points.
                - max_opt_cycles (int, optional): Max optimization cycles for path points.

    Returns:
        dict: A dictionary containing filenames and their content, or an error message.
              May also include a "warnings" key with a list of warnings.
    """
    return xtb_generator.generate_enhanced_sampling_input_package(
        molecule_data=molecule_data,
        method_settings=method_settings,
        sampling_method_type=sampling_method_type,
        sampling_params=sampling_params
    )

@mcp.tool()
def generate_wavefunction_analysis(molecule_data: dict, method_settings: dict, analysis_params: dict) -> dict:
    """
    Generates input files for XTB wavefunction and electronic structure analysis.

    Args:
        molecule_data (dict): Molecular structure information (format, content).
        method_settings (dict): Basic calculation settings (gfn_version, charge, multiplicity, solvent, temperature).
        analysis_params (dict): Parameters for the wavefunction analysis.
            - "analysis_types" (list[str]): Types of analysis to perform
              (e.g., "molecular_orbitals", "electron_density", "bond_orders", "esp_charges").
            - "output_formats" (dict, optional): Specifies output formats, e.g., {"cube_files": True}.
            - "visualization_settings" (dict, optional): Settings for visualization, e.g.,
              {"grid_spacing": 0.1, "density_threshold": 1e-4}.
            - "specific_orbitals_to_plot" (list[int] or str, optional): For MO plotting,
              e.g., [10, 11] or "HOMO,LUMO" (HOMO/LUMO support is basic).

    Returns:
        dict: A dictionary containing filenames and their content, or an error message.
              May include a "warnings" key with a list of warnings.
    """
    return xtb_generator.generate_wavefunction_analysis_input_package(
        molecule_data=molecule_data,
        method_settings=method_settings,
        analysis_params=analysis_params
    )

@mcp.tool()
def generate_oniom_input(molecule_data: dict, method_settings: dict, oniom_params: dict) -> dict:
    """
    Generates input files for an XTB ONIOM calculation.

    Args:
        molecule_data (dict): Molecular structure information.
        method_settings (dict): Basic calculation settings for the high-level region and overall system.
            - gfn_version_high_level (str): GFN version for the QM region.
            - total_charge (int): Total charge of the system.
            - total_spin_multiplicity (int): Total spin multiplicity.
            - solvent (str, optional): Solvent name.
            - temperature (float, optional): Temperature in Kelvin.
        oniom_params (dict): Parameters specific to the ONIOM calculation.
            - qmatoms_definition (str): Definition of QM atoms (e.g., "qmatoms=1,2,3" or "qmfile=qm_atoms.list").
            - method_low_level (str): Method for the low-level region (e.g., "gfnff").
            - link_atoms_definition (str, optional): Definitions for link atoms.
            - oniom_settings (str, optional): Additional settings for the $oniom block.
            - opt_level (str, optional): Optimization level.
            - max_opt_cycles (int, optional): Maximum optimization cycles.
            - qm_atoms_list_content (str, optional): Content for the QM atoms list file if qmfile is used.

    Returns:
        dict: A dictionary containing filenames and their content, or an error message.
              May also include a "warnings" key.
    """
    return xtb_generator.generate_oniom_input_package(
        molecule_data=molecule_data,
        method_settings=method_settings,
        oniom_params=oniom_params
    )

@mcp.tool()
def generate_spectroscopy_input(molecule_data: dict, method_settings: dict, spectroscopy_params: dict) -> dict:
    """
    Generates input files for XTB spectroscopy calculations.
    Currently, primary support is for IR spectroscopy (via Hessian calculation).

    Args:
        molecule_data (dict): Molecular structure information.
        method_settings (dict): Basic calculation settings (gfn_version, charge, multiplicity, solvent, temperature).
        spectroscopy_params (dict): Parameters for the spectroscopy calculation.
            - "spectroscopy_types" (list[str]): List of spectroscopy types, e.g., ["ir"].
            - "ir_settings" (dict, optional): Settings specific to IR calculations.
                - "temperature" (float, optional): Temperature for Hessian and SCC.
                - "anharmonicity_flag" (bool, optional): Flag for simple quasi-harmonic correction.
            # uv_vis_settings, stm_settings, etc., to be added for other types.

    Returns:
        dict: A dictionary containing filenames and their content, or an error message.
              May also include a "warnings" key.
    """
    return xtb_generator.generate_spectroscopy_input_package(
        molecule_data=molecule_data,
        method_settings=method_settings,
        spectroscopy_params=spectroscopy_params
    )

@mcp.tool()
def analyze_trajectory(trajectory_file_content: str, input_format: str, analysis_types: list[str], output_options: dict | None = None) -> dict:
    """
    Analyzes MD trajectory and enhanced sampling results. (Placeholder)
    Actual implementation will require dedicated analysis libraries.

    Args:
        trajectory_file_content (str): Content of the trajectory file.
        input_format (str): Format of the trajectory file (e.g., "xtb_trj", "dcd").
        analysis_types (list[str]): List of analysis types to perform
                                   (e.g., "free_energy_surface", "rmsd").
        output_options (dict, optional): Options for output generation (e.g., {"plots": True}).

    Returns:
        dict: Contains analysis results or status. Currently returns a 'not_implemented_yet' status.
    """
    return xtb_generator.analyze_md_trajectory_results(
        trajectory_file_content=trajectory_file_content,
        input_format=input_format,
        analysis_types=analysis_types,
        output_options=output_options
    )

if __name__ == "__main__":
    # Run MCP server
    # Defaults to STDIO transport
    # Other transports can be specified, e.g.:
    # mcp.run(transport="streamable-http", host="127.0.0.1", port=9000)
    mcp.run()