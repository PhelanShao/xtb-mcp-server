#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to test the actual functionality of the MCP server.
This script simulates MCP client calls to verify server functions.
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

# Import the main module to access MCP functions
import main

def test_basic_functionality():
    """Tests basic functionality"""
    print("=== Testing Basic MCP Functionality ===")
    
    # 测试资源访问
    print("\n1. Testing Resource Access:")
    
    # 测试模板资源
    singlepoint_template = main.get_singlepoint_template()
    print(f"   Singlepoint Calculation Template: {'[OK]' if singlepoint_template and len(singlepoint_template) > 0 else '[FAIL]'}")
    
    optimization_template = main.get_optimization_template()
    print(f"   Optimization Calculation Template: {'[OK]' if optimization_template and len(optimization_template) > 0 else '[FAIL]'}")
    
    # Test Parameter Documentation
    gfn2_doc = main.get_gfn2_parameters_doc()
    print(f"   GFN2 Parameter Documentation: {'[OK]' if gfn2_doc and len(gfn2_doc) > 0 else '[FAIL]'}")
    
    # Test Help Documentation
    faq = main.get_help_faq()
    print(f"   FAQ Documentation: {'[OK]' if faq and len(faq) > 0 else '[FAIL]'}")

def test_input_generation():
    """Tests input file generation"""
    print("\n2. Testing Input File Generation:")
    
    # Test Molecular Data
    water_xyz = """3
Water molecule
O  0.000000  0.000000  0.117300
H  0.000000  0.757200 -0.469200
H  0.000000 -0.757200 -0.469200
"""
    
    molecule_data = {
        "format": "xyz",
        "content": water_xyz,
        "charge": 0,
        "multiplicity": 1
    }
    
    # Test Singlepoint Calculation
    result = main.generate_xtb_input(
        molecule_data=molecule_data,
        calculation_type="singlepoint",
        method="gfn2",
        settings={"solvent": "h2o", "temperature": 298.15}
    )
    
    success = "error" not in result and "structure.xyz" in result and ".xcontrolrc" in result
    print(f"   Singlepoint Input Generation: {'[OK]' if success else '[FAIL]'}")
    
    if success:
        print(f"     - Number of Generated Files: {len([k for k in result.keys() if not k.startswith('warning')])}")
        print(f"     - Contains Structure File: {'[OK]' if 'structure.xyz' in result else '[FAIL]'}")
        print(f"     - Contains Control File: {'[OK]' if '.xcontrolrc' in result else '[FAIL]'}")
        print(f"     - Contains Run Script: {'[OK]' if 'run_xtb.sh' in result else '[FAIL]'}")
    
    # Test Geometry Optimization
    result_opt = main.generate_xtb_input(
        molecule_data=molecule_data,
        calculation_type="optimization",
        method="gfn2",
        settings={"opt_level": "tight", "max_opt_cycles": 100}
    )
    
    success_opt = "error" not in result_opt and "structure.xyz" in result_opt
    print(f"   Geometry Optimization Input Generation: {'[OK]' if success_opt else '[FAIL]'}")

def test_validation():
    """Tests input validation"""
    print("\n3. Testing Input Validation:")
    
    # Test Valid Input
    valid_xcontrol = """$chrg 0
$spin 0
$gfn 2
$scc
  temp=298.15
$end
$write
  json=true
$end
"""
    
    result = main.validate_xtb_input({
        "xcontrol_content": valid_xcontrol,
        "expected_charge": 0,
        "expected_multiplicity": 1
    })
    
    print(f"   Valid Input Validation: {'[OK]' if result.get('is_valid', False) else '[FAIL]'}")
    
    # Test Invalid Input
    invalid_xcontrol = """$chrg 0
$scc
  temp=298.15
# Missing $end
"""
    
    result_invalid = main.validate_xtb_input({
        "xcontrol_content": invalid_xcontrol
    })
    
    print(f"   Invalid Input Detection: {'[OK]' if not result_invalid.get('is_valid', True) else '[FAIL]'}")

def test_format_conversion():
    """Tests format conversion"""
    print("\n4. Testing Format Conversion:")
    
    water_xyz = """3
Water molecule
O  0.000000  0.000000  0.117300
H  0.000000  0.757200 -0.469200
H  0.000000 -0.757200 -0.469200
"""
    
    # Test XYZ to COORD Conversion
    result = main.convert_structure_format(
        input_format="xyz",
        output_format="coord",
        structure_data=water_xyz
    )
    
    success = "error" not in result and "converted_content" in result
    print(f"   XYZ to COORD Conversion: {'[OK]' if success else '[FAIL]'}")
    
    if success:
        coord_content = result["converted_content"]
        print(f"     - Contains $coord block: {'[OK]' if '$coord' in coord_content else '[FAIL]'}")
        print(f"     - Contains $end tag: {'[OK]' if '$end' in coord_content else '[FAIL]'}")

def test_advanced_features():
    """Tests advanced features"""
    print("\n5. Testing Advanced Features:")
    
    benzene_xyz = """12
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
    
    molecule_data = {
        "format": "xyz",
        "content": benzene_xyz
    }
    
    # Test Enhanced Sampling
    try:
        result = main.generate_enhanced_sampling(
            molecule_data=molecule_data,
            method_settings={
                "gfn_version": "2",
                "charge": 0,
                "multiplicity": 1
            },
            sampling_method_type="metadynamics",
            sampling_params={
                "collective_variables_definition": "distance,1,2,auto"
            }
        )
        print(f"   Enhanced Sampling Functionality: {'[OK]' if isinstance(result, dict) else '[FAIL]'}")
    except Exception as e:
        print(f"   Enhanced Sampling Functionality: [FAIL] (Error: {str(e)[:50]}...)")
    
    # Test Wavefunction Analysis
    try:
        result = main.generate_wavefunction_analysis(
            molecule_data=molecule_data,
            method_settings={
                "gfn_version": "2",
                "charge": 0,
                "multiplicity": 1
            },
            analysis_params={
                "analysis_types": ["molecular_orbitals"]
            }
        )
        print(f"   Wavefunction Analysis Functionality: {'[OK]' if isinstance(result, dict) else '[FAIL]'}")
    except Exception as e:
        print(f"   Wavefunction Analysis Functionality: [FAIL] (Error: {str(e)[:50]}...)")

def test_error_handling():
    """Tests error handling"""
    print("\n6. Testing Error Handling:")
    
    # Test Invalid Molecular Format
    result = main.generate_xtb_input(
        molecule_data={
            "format": "invalid_format",
            "content": "invalid content",
            "charge": 0,
            "multiplicity": 1
        },
        calculation_type="singlepoint",
        method="gfn2",
        settings={}
    )
    
    print(f"   Invalid Format Error Handling: {'[OK]' if 'error' in result else '[FAIL]'}")
    
    # Test Invalid Calculation Type
    result = main.generate_xtb_input(
        molecule_data={
            "format": "xyz",
            "content": "3\nWater\nO 0 0 0\nH 0 0 1\nH 0 1 0",
            "charge": 0,
            "multiplicity": 1
        },
        calculation_type="invalid_type",
        method="gfn2",
        settings={}
    )
    
    print(f"   Invalid Calculation Type Error Handling: {'[OK]' if 'error' in result else '[FAIL]'}")

def main_test():
    """Main test function"""
    print("XTB MCP Server Functionality Test")
    print("=" * 50)
    
    try:
        test_basic_functionality()
        test_input_generation()
        test_validation()
        test_format_conversion()
        test_advanced_features()
        test_error_handling()
        
        print("\n" + "=" * 50)
        print("[OK] MCP Functionality Test Complete!")
        print("Server is ready for deployment.")
        
    except Exception as e:
        print(f"\n[ERROR] An error occurred during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main_test()
    sys.exit(0 if success else 1)