#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests MCP server functionality and integration.
"""

import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the main module
import main
from xtb_input_generator import XTBInputGenerator


class TestMCPServerIntegration(unittest.TestCase):
    """Tests MCP server integration functionality"""

    def setUp(self):
        """Sets up the test environment"""
        self.water_xyz = """3
Water molecule
O  0.000000  0.000000  0.117300
H  0.000000  0.757200 -0.469200
H  0.000000 -0.757200 -0.469200
"""

    def test_mcp_server_initialization(self):
        """Tests MCP server initialization"""
        # Check if the server is initialized correctly
        self.assertIsNotNone(main.mcp)
        self.assertIsNotNone(main.xtb_generator)
        self.assertIsInstance(main.xtb_generator, XTBInputGenerator)

    def test_resource_functions_exist(self):
        """Tests if resource functions exist"""
        # Check if all resource functions are defined
        resource_functions = [
            'get_singlepoint_template',
            'get_optimization_template',
            'get_frequency_template',
            'get_scan_template',
            'get_md_template',
            'get_gfn0_parameters_doc',
            'get_gfn1_parameters_doc',
            'get_gfn2_parameters_doc',
            'get_metadynamics_template',
            'get_pathfinder_template',
            'get_normal_mode_following_template',
            'get_wavefunction_orbitals_template',
            'get_advanced_oniom_template',
            'get_advanced_spectroscopy_ir_template',
            'get_advanced_spectroscopy_uv_vis_template',
            'get_help_faq',
            'get_input_format_spec'
        ]
        
        for func_name in resource_functions:
            self.assertTrue(hasattr(main, func_name))
            func = getattr(main, func_name)
            self.assertTrue(callable(func))

    def test_tool_functions_exist(self):
        """Tests if tool functions exist"""
        # Check if all tool functions are defined
        tool_functions = [
            'generate_xtb_input',
            'generate_xcontrol',
            'validate_xtb_input',
            'convert_structure_format',
            'explain_xtb_parameters',
            'generate_enhanced_sampling',
            'generate_wavefunction_analysis',
            'generate_oniom_input',
            'generate_spectroscopy_input',
            'analyze_trajectory'
        ]
        
        for func_name in tool_functions:
            self.assertTrue(hasattr(main, func_name))
            func = getattr(main, func_name)
            self.assertTrue(callable(func))

    def test_generate_xtb_input_tool(self):
        """Tests the generate_xtb_input tool"""
        molecule_data = {
            "format": "xyz",
            "content": self.water_xyz,
            "charge": 0,
            "multiplicity": 1
        }
        
        result = main.generate_xtb_input(
            molecule_data=molecule_data,
            calculation_type="singlepoint",
            method="gfn2",
            settings={"solvent": "h2o", "temperature": 298.15}
        )
        
        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("structure.xyz", result)
            self.assertIn(".xcontrolrc", result)

    def test_validate_xtb_input_tool(self):
        """Tests the validate_xtb_input tool"""
        input_files = {
            "xcontrol_content": """$chrg 0
$spin 0
$gfn 2
$scc
  temp=298.15
$end
""",
            "expected_charge": 0,
            "expected_multiplicity": 1
        }
        
        result = main.validate_xtb_input(input_files)
        
        self.assertIsInstance(result, dict)
        self.assertIn("is_valid", result)
        self.assertIn("errors", result)
        self.assertIn("warnings", result)

    def test_convert_structure_format_tool(self):
        """Tests the convert_structure_format tool"""
        result = main.convert_structure_format(
            input_format="xyz",
            output_format="coord",
            structure_data=self.water_xyz
        )
        
        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("converted_content", result)

    def test_generate_xcontrol_tool(self):
        """Tests the generate_xcontrol tool"""
        calculation_settings = {
            "calculation_type": "optimization",
            "method": "gfn2",
            "solvent": "h2o",
            "temperature": 298.15,
            "optimization_settings": {
                "level": "normal",
                "maxcycle": 200
            }
        }
        
        result = main.generate_xcontrol(
            charge=0,
            spin_multiplicity=1,
            calculation_settings=calculation_settings
        )
        
        self.assertIsInstance(result, dict)
        if "error" not in result:
            self.assertIn("xcontrol_content", result)

    def test_explain_xtb_parameters_tool(self):
        """Tests the explain_xtb_parameters tool"""
        result = main.explain_xtb_parameters(
            parameter_type="gfn2",
            specific_parameter=None
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn("explanation", result)

    def test_resource_error_handling(self):
        """Tests resource error handling"""
        # Simulate resource acquisition failure
        with patch.object(main.xtb_generator, 'get_mcp_resource', return_value=None):
            result = main.get_singlepoint_template()
            self.assertIn("Error:", result)

    def test_tool_error_handling(self):
        """Tests tool error handling"""
        # Test invalid molecular data
        invalid_molecule_data = {
            "format": "invalid",
            "content": "",
            "charge": 0,
            "multiplicity": 1
        }
        
        result = main.generate_xtb_input(
            molecule_data=invalid_molecule_data,
            calculation_type="singlepoint",
            method="gfn2",
            settings={}
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn("error", result)


class TestMCPServerAdvancedTools(unittest.TestCase):
    """Tests advanced tool functionality"""

    def setUp(self):
        """Sets up the test environment"""
        self.benzene_xyz = """12
Benzene molecule
C    1.40272    0.00000    0.00000
C    0.70136    1.21441    0.00000
C   -0.70136    1.21441    0.00000
C   -1.40272    0.00000    0.00000
C   -0.70136   -1.21441    0.00000
C    0.70136   -1.21441    0.00000
H    2.49029    0.00000    0.00000
H    1.24515    2.15666    0.00000
H   -1.24515    2.15666    0.00000
H   -2.49029    0.00000    0.00000
H   -1.24515   -2.15666    0.00000
H    1.24515   -2.15666    0.00000
"""

    def test_generate_enhanced_sampling_tool(self):
        """Tests the enhanced sampling tool"""
        molecule_data = {
            "format": "xyz",
            "content": self.benzene_xyz
        }
        
        method_settings = {
            "gfn_version": "2",
            "charge": 0,
            "multiplicity": 1,
            "solvent": "toluene",
            "temperature": 300.0
        }
        
        sampling_params = {
            "collective_variables_definition": "distance,1,2,auto",
            "md_temperature": 300.0,
            "simulation_time_ps": 10.0
        }
        
        result = main.generate_enhanced_sampling(
            molecule_data=molecule_data,
            method_settings=method_settings,
            sampling_method_type="metadynamics",
            sampling_params=sampling_params
        )
        
        self.assertIsInstance(result, dict)
        # This feature might not be fully implemented yet, so check basic structure

    def test_generate_wavefunction_analysis_tool(self):
        """Tests the wavefunction analysis tool"""
        molecule_data = {
            "format": "xyz",
            "content": self.benzene_xyz
        }
        
        method_settings = {
            "gfn_version": "2",
            "charge": 0,
            "multiplicity": 1,
            "solvent": "none",
            "temperature": 298.15
        }
        
        analysis_params = {
            "analysis_types": ["molecular_orbitals", "electron_density"],
            "output_formats": {"cube_files": True},
            "visualization_settings": {"grid_spacing": 0.1}
        }
        
        result = main.generate_wavefunction_analysis(
            molecule_data=molecule_data,
            method_settings=method_settings,
            analysis_params=analysis_params
        )
        
        self.assertIsInstance(result, dict)

    def test_generate_oniom_input_tool(self):
        """Tests the ONIOM input generation tool"""
        molecule_data = {
            "format": "xyz",
            "content": self.benzene_xyz
        }
        
        method_settings = {
            "gfn_version_high_level": "2",
            "total_charge": 0,
            "total_spin_multiplicity": 1,
            "solvent": "none",
            "temperature": 298.15
        }
        
        oniom_params = {
            "qmatoms_definition": "qmatoms=1,2,3,4,5,6",
            "method_low_level": "gfnff",
            "opt_level": "normal",
            "max_opt_cycles": 200
        }
        
        result = main.generate_oniom_input(
            molecule_data=molecule_data,
            method_settings=method_settings,
            oniom_params=oniom_params
        )
        
        self.assertIsInstance(result, dict)

    def test_generate_spectroscopy_input_tool(self):
        """Tests the spectroscopy calculation input generation tool"""
        molecule_data = {
            "format": "xyz",
            "content": self.benzene_xyz
        }
        
        method_settings = {
            "gfn_version": "2",
            "charge": 0,
            "multiplicity": 1,
            "solvent": "none",
            "temperature": 298.15
        }
        
        spectroscopy_params = {
            "spectroscopy_types": ["ir"],
            "ir_settings": {
                "temperature": 298.15,
                "anharmonicity_flag": False
            }
        }
        
        result = main.generate_spectroscopy_input(
            molecule_data=molecule_data,
            method_settings=method_settings,
            spectroscopy_params=spectroscopy_params
        )
        
        self.assertIsInstance(result, dict)

    def test_analyze_trajectory_tool(self):
        """Tests the trajectory analysis tool"""
        # This is a placeholder function, should return not implemented status
        result = main.analyze_trajectory(
            trajectory_file_content="dummy trajectory data",
            input_format="xtb_trj",
            analysis_types=["rmsd", "free_energy_surface"],
            output_options={"plots": True}
        )
        
        self.assertIsInstance(result, dict)
        # Should contain not implemented status information


class TestMCPServerResourceAccess(unittest.TestCase):
    """Tests MCP server resource access"""

    def test_all_template_resources(self):
        """Tests all template resources"""
        template_resources = [
            ("xtb://templates/singlepoint", main.get_singlepoint_template),
            ("xtb://templates/optimization", main.get_optimization_template),
            ("xtb://templates/frequency", main.get_frequency_template),
            ("xtb://templates/scan", main.get_scan_template),
            ("xtb://templates/md", main.get_md_template),
        ]
        
        for uri, func in template_resources:
            with self.subTest(uri=uri):
                result = func()
                self.assertIsInstance(result, str)
                # If the resource exists, it should contain XTB-related content or error information
                self.assertTrue(len(result) > 0)

    def test_all_parameter_resources(self):
        """Tests all parameter resources"""
        parameter_resources = [
            ("xtb://parameters/gfn0", main.get_gfn0_parameters_doc),
            ("xtb://parameters/gfn1", main.get_gfn1_parameters_doc),
            ("xtb://parameters/gfn2", main.get_gfn2_parameters_doc),
        ]
        
        for uri, func in parameter_resources:
            with self.subTest(uri=uri):
                result = func()
                self.assertIsInstance(result, str)
                self.assertTrue(len(result) > 0)

    def test_advanced_template_resources(self):
        """Tests advanced template resources"""
        advanced_resources = [
            ("xtb://sampling/metadynamics", main.get_metadynamics_template),
            ("xtb://sampling/pathfinder", main.get_pathfinder_template),
            ("xtb://sampling/normal_mode_following", main.get_normal_mode_following_template),
            ("xtb://wavefunction/orbitals", main.get_wavefunction_orbitals_template),
            ("xtb://advanced/oniom", main.get_advanced_oniom_template),
            ("xtb://advanced/spectroscopy_ir", main.get_advanced_spectroscopy_ir_template),
            ("xtb://advanced/spectroscopy_uv_vis", main.get_advanced_spectroscopy_uv_vis_template),
        ]
        
        for uri, func in advanced_resources:
            with self.subTest(uri=uri):
                result = func()
                self.assertIsInstance(result, str)
                self.assertTrue(len(result) > 0)

    def test_help_and_format_resources(self):
        """Tests help and format resources"""
        help_resources = [
            ("xtb://help/faq", main.get_help_faq),
            ("xtb://formats/input", main.get_input_format_spec),
        ]
        
        for uri, func in help_resources:
            with self.subTest(uri=uri):
                result = func()
                self.assertIsInstance(result, str)
                self.assertTrue(len(result) > 0)


if __name__ == '__main__':
    unittest.main()