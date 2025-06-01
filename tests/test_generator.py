#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests the core functionality of the XTB input generator.
"""

import unittest
import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xtb_input_generator import XTBInputGenerator


class TestXTBInputGenerator(unittest.TestCase):
    """Tests the XTB input generator"""

    def setUp(self):
        """Sets up the test environment"""
        # Create a temporary resource directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.resource_path = Path(self.temp_dir) / "resources"
        
        # Create basic directory structure
        (self.resource_path / "templates").mkdir(parents=True)
        (self.resource_path / "parameters").mkdir(parents=True)
        (self.resource_path / "formats").mkdir(parents=True)
        (self.resource_path / "help").mkdir(parents=True)
        
        # Create basic template files
        self._create_test_templates()
        self._create_test_docs()
        
        # Initialize the generator
        self.generator = XTBInputGenerator(resource_base_path=self.resource_path)
        
        # Test molecular data
        self.water_xyz = """3
Water molecule
O  0.000000  0.000000  0.117300
H  0.000000  0.757200 -0.469200
H  0.000000 -0.757200 -0.469200
"""

    def tearDown(self):
        """Cleans up the test environment"""
        shutil.rmtree(self.temp_dir)

    def _create_test_templates(self):
        """Creates template files for testing"""
        # Singlepoint calculation template
        singlepoint_template = """$chrg {charge}
$spin {spin_multiplicity}
$gfn {gfn_version}
$alpb {solvent}
$scc
  temp={temperature}
$end
$write
  json=true
$end
"""
        with open(self.resource_path / "templates" / "singlepoint.xtb_tpl", "w") as f:
            f.write(singlepoint_template)

        # Optimization calculation template
        optimization_template = """$chrg {charge}
$spin {spin_multiplicity}
$gfn {gfn_version}
$alpb {solvent}
$opt
  optlevel={opt_level}
  maxcycle={max_opt_cycles}
$end
$scc
  temp={temperature}
$end
$write
  json=true
$end
"""
        with open(self.resource_path / "templates" / "optimization.xtb_tpl", "w") as f:
            f.write(optimization_template)

        # Frequency calculation template
        frequency_template = """$chrg {charge}
$spin {spin_multiplicity}
$gfn {gfn_version}
$alpb {solvent}
$hess
$end
$scc
  temp={temperature}
$end
$write
  json=true
$end
"""
        with open(self.resource_path / "templates" / "frequency.xtb_tpl", "w") as f:
            f.write(frequency_template)

    def _create_test_docs(self):
        """Creates documentation files for testing"""
        # GFN2 parameter documentation
        gfn2_doc = """# GFN2-xTB Parameters

GFN2-xTB is the second generation of the GFN tight-binding method.

## Key Features
- Improved accuracy for organic molecules
- Better description of non-covalent interactions
- Support for elements H-Rn
"""
        with open(self.resource_path / "parameters" / "gfn2.md", "w") as f:
            f.write(gfn2_doc)

        # Input format specification
        input_spec = """# XTB Input Format Specification

## Structure Files
- XYZ format: Standard Cartesian coordinates
- COORD format: TURBOMOLE coordinate format

## Control Files
- .xcontrolrc: Main control file for XTB calculations
"""
        with open(self.resource_path / "formats" / "input_spec.md", "w") as f:
            f.write(input_spec)

        # FAQ documentation
        faq_doc = """# Frequently Asked Questions

## Q: How do I run a single point calculation?
A: Use the generate_xtb_input tool with calculation_type="singlepoint"

## Q: What solvents are supported?
A: XTB supports GBSA implicit solvation for many common solvents.
"""
        with open(self.resource_path / "help" / "faq.md", "w") as f:
            f.write(faq_doc)

    def test_initialization(self):
        """Tests generator initialization"""
        self.assertIsNotNone(self.generator)
        self.assertTrue(self.generator.resource_path.exists())
        self.assertIn("singlepoint", self.generator.templates)
        self.assertIn("optimization", self.generator.templates)

    def test_get_mcp_resource_templates(self):
        """Tests MCP resource acquisition - Templates"""
        # Test singlepoint calculation template
        singlepoint = self.generator.get_mcp_resource("xtb://templates/singlepoint")
        self.assertIsNotNone(singlepoint)
        self.assertIn("$chrg", singlepoint)
        self.assertIn("$gfn", singlepoint)

        # Test non-existent template
        nonexistent = self.generator.get_mcp_resource("xtb://templates/nonexistent")
        self.assertIsNone(nonexistent)

    def test_get_mcp_resource_parameters(self):
        """Tests MCP resource acquisition - Parameter documentation"""
        gfn2_doc = self.generator.get_mcp_resource("xtb://parameters/gfn2")
        self.assertIsNotNone(gfn2_doc)
        self.assertIn("GFN2-xTB", gfn2_doc)

    def test_get_mcp_resource_formats(self):
        """Tests MCP resource acquisition - Format specification"""
        input_spec = self.generator.get_mcp_resource("xtb://formats/input")
        self.assertIsNotNone(input_spec)
        self.assertIn("XTB Input Format", input_spec)

    def test_get_mcp_resource_help(self):
        """Tests MCP resource acquisition - Help documentation"""
        faq = self.generator.get_mcp_resource("xtb://help/faq")
        self.assertIsNotNone(faq)
        self.assertIn("Frequently Asked Questions", faq)

    def test_generate_xtb_input_singlepoint(self):
        """Tests generating singlepoint calculation input"""
        molecule_data = {
            "format": "xyz",
            "content": self.water_xyz,
            "charge": 0,
            "multiplicity": 1
        }
        
        result = self.generator.generate_xtb_input_package(
            molecule_data=molecule_data,
            calculation_type="singlepoint",
            method="gfn2",
            settings={"solvent": "h2o", "temperature": 298.15}
        )
        
        self.assertNotIn("error", result)
        self.assertIn("structure.xyz", result)
        self.assertIn(".xcontrolrc", result)
        self.assertIn("run_xtb.sh", result)
        
        # Check .xcontrolrc content
        xcontrol = result[".xcontrolrc"]
        self.assertIn("$chrg 0", xcontrol)
        self.assertIn("$spin 0", xcontrol)
        self.assertIn("$gfn 2", xcontrol)
        self.assertIn("$alpb h2o", xcontrol)

    def test_generate_xtb_input_optimization(self):
        """Tests generating geometry optimization input"""
        molecule_data = {
            "format": "xyz",
            "content": self.water_xyz,
            "charge": 0,
            "multiplicity": 1
        }
        
        result = self.generator.generate_xtb_input_package(
            molecule_data=molecule_data,
            calculation_type="optimization",
            method="gfn2",
            settings={
                "solvent": "none",
                "temperature": 298.15,
                "opt_level": "tight",
                "max_opt_cycles": 100
            }
        )
        
        self.assertNotIn("error", result)
        xcontrol = result[".xcontrolrc"]
        self.assertIn("$opt", xcontrol)
        self.assertIn("optlevel=tight", xcontrol)
        self.assertIn("maxcycle=100", xcontrol)

    def test_generate_xtb_input_invalid_format(self):
        """Tests unsupported molecular format"""
        molecule_data = {
            "format": "pdb",  # Unsupported format
            "content": "some pdb content",
            "charge": 0,
            "multiplicity": 1
        }
        
        result = self.generator.generate_xtb_input_package(
            molecule_data=molecule_data,
            calculation_type="singlepoint",
            method="gfn2",
            settings={}
        )
        
        self.assertIn("error", result)
        self.assertIn("Currently only", result["error"])

    def test_generate_xtb_input_invalid_calculation_type(self):
        """Tests unsupported calculation type"""
        molecule_data = {
            "format": "xyz",
            "content": self.water_xyz,
            "charge": 0,
            "multiplicity": 1
        }
        
        result = self.generator.generate_xtb_input_package(
            molecule_data=molecule_data,
            calculation_type="invalid_type",
            method="gfn2",
            settings={}
        )
        
        self.assertIn("error", result)
        self.assertIn("Unsupported calculation type", result["error"])

    def test_generate_xtb_input_missing_content(self):
        """Tests missing molecular content"""
        molecule_data = {
            "format": "xyz",
            "content": "",  # Empty content
            "charge": 0,
            "multiplicity": 1
        }
        
        result = self.generator.generate_xtb_input_package(
            molecule_data=molecule_data,
            calculation_type="singlepoint",
            method="gfn2",
            settings={}
        )
        
        self.assertIn("error", result)
        self.assertIn("not provided", result["error"])

    def test_validate_xtb_input_valid(self):
        """Tests validation of valid input files"""
        xcontrol_content = """$chrg 0
$spin 0
$gfn 2
$scc
  temp=298.15
$end
$write
  json=true
$end
"""
        
        result = self.generator.validate_xtb_input_files({
            "xcontrol_content": xcontrol_content,
            "expected_charge": 0,
            "expected_multiplicity": 1
        })
        
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["errors"]), 0)

    def test_validate_xtb_input_missing_charge(self):
        """Tests validation with missing charge definition"""
        xcontrol_content = """$spin 0
$gfn 2
$scc
  temp=298.15
$end
"""
        
        result = self.generator.validate_xtb_input_files({
            "xcontrol_content": xcontrol_content
        })
        
        self.assertFalse(result["is_valid"])
        self.assertTrue(any("$chrg" in error for error in result["errors"]))

    def test_validate_xtb_input_unmatched_blocks(self):
        """Tests unmatched blocks"""
        xcontrol_content = """$chrg 0
$spin 0
$scc
  temp=298.15
# Missing $end
"""
        
        result = self.generator.validate_xtb_input_files({
            "xcontrol_content": xcontrol_content
        })
        
        self.assertFalse(result["is_valid"])
        self.assertTrue(any("$end" in error for error in result["errors"]))

    def test_convert_structure_format_xyz_to_coord(self):
        """Tests XYZ to COORD format conversion"""
        result = self.generator.convert_structure_file_format(
            input_format="xyz",
            output_format="coord",
            structure_data=self.water_xyz
        )
        
        self.assertNotIn("error", result)
        self.assertIn("converted_content", result)
        self.assertIn("$coord", result["converted_content"])
        self.assertIn("$end", result["converted_content"])

    def test_convert_structure_format_unsupported(self):
        """Tests unsupported format conversion"""
        result = self.generator.convert_structure_file_format(
            input_format="pdb",
            output_format="xyz",
            structure_data="some content"
        )
        
        self.assertIn("error", result)
        self.assertIn("not supported", result["error"])


class TestXTBInputGeneratorAdvanced(unittest.TestCase):
    """Tests advanced features"""

    def setUp(self):
        """Sets up the test environment"""
        # Use default resource path
        self.generator = XTBInputGenerator()
        
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

    def test_generate_xcontrol_file(self):
        """Tests generating xcontrol file"""
        result = self.generator.generate_xcontrol_file(
            charge=0,
            spin_multiplicity=1,
            calculation_settings={
                "calculation_type": "optimization",
                "method": "gfn2",
                "solvent": "toluene",
                "temperature": 298.15,
                "optimization_settings": {
                    "level": "tight",
                    "maxcycle": 200
                }
            }
        )
        
        self.assertNotIn("error", result)
        self.assertIn("xcontrol_content", result)
        
        content = result["xcontrol_content"]
        self.assertIn("$chrg 0", content)
        self.assertIn("$spin 0", content)

    def test_explain_xtb_parameters(self):
        """Tests parameter explanation functionality"""
        result = self.generator.explain_xtb_parameters_info(
            parameter_type="gfn2",
            specific_parameter=None
        )
        
        # This function might return basic information or "not implemented" status
        self.assertIn("explanation", result)

    def test_large_molecule_handling(self):
        """Tests large molecule handling"""
        molecule_data = {
            "format": "xyz",
            "content": self.benzene_xyz,
            "charge": 0,
            "multiplicity": 1
        }
        
        result = self.generator.generate_xtb_input_package(
            molecule_data=molecule_data,
            calculation_type="singlepoint",
            method="gfn2",
            settings={"solvent": "none"}
        )
        
        self.assertNotIn("error", result)
        self.assertIn("structure.xyz", result)


if __name__ == '__main__':
    unittest.main()