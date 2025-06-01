#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests the functionality of molecular structure format conversion tools.
"""

import unittest
import sys
import os

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xtb_input_generator.structure_utils import (
    xyz_to_coord_string,
    coord_string_to_xyz,
    gaussian_to_xyz_string
)


class TestStructureUtils(unittest.TestCase):
    """Tests structure conversion utilities"""

    def setUp(self):
        """Sets up test data"""
        self.valid_xyz = """3
Water molecule
O  0.000000  0.000000  0.117300
H  0.000000  0.757200 -0.469200
H  0.000000 -0.757200 -0.469200
"""

        self.valid_coord = """$coord    water_molecule
  0.000000    0.000000    0.117300      o
  0.000000    0.757200   -0.469200      h
  0.000000   -0.757200   -0.469200      h
$end
"""

        self.valid_gaussian = """%chk=water.chk
%mem=1GB
%nprocshared=4
#p opt freq b3lyp/6-31g(d)

Water optimization and frequency

0 1
O    0.00000000    0.00000000    0.11779000
H    0.00000000    0.76322600   -0.47115800
H    0.00000000   -0.76322600   -0.47115800

"""

    def test_xyz_to_coord_valid(self):
        """Tests valid XYZ to COORD conversion"""
        result, error = xyz_to_coord_string(self.valid_xyz)
        self.assertIsNone(error)
        self.assertIsNotNone(result)
        self.assertIn("$coord", result)
        self.assertIn("$end", result)
        self.assertIn("o", result.lower())
        self.assertIn("h", result.lower())

    def test_xyz_to_coord_invalid_atom_count(self):
        """Tests XYZ file with mismatched atom count"""
        invalid_xyz = """3
Water
O  0.000000  0.000000  0.117300
H  0.000000  0.757200 -0.469200
"""  # Only 2 atoms, but 3 declared
        result, error = xyz_to_coord_string(invalid_xyz)
        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn("atom count declaration", error)

    def test_xyz_to_coord_invalid_format(self):
        """Tests malformed XYZ file"""
        invalid_xyz = """3
Water
O  0.000000  0.000000
H  0.000000  0.757200 -0.469200
H  0.000000 -0.757200 -0.469200
"""  # First atom missing Z coordinate
        result, error = xyz_to_coord_string(invalid_xyz)
        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn("incorrect format", error)

    def test_xyz_to_coord_empty_content(self):
        """Tests empty content"""
        result, error = xyz_to_coord_string("")
        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn("empty", error)

    def test_coord_to_xyz_valid(self):
        """Tests valid COORD to XYZ conversion"""
        result, error = coord_string_to_xyz(self.valid_coord)
        self.assertIsNone(error)
        self.assertIsNotNone(result)
        lines = result.strip().split('\n')
        self.assertEqual(lines[0], "3")  # Atom count
        self.assertIn("O", lines[2])  # First atom is oxygen

    def test_coord_to_xyz_no_end(self):
        """Tests COORD file missing $end"""
        invalid_coord = """$coord
  0.000000    0.000000    0.117300      o
  0.000000    0.757200   -0.469200      h
"""
        result, error = coord_string_to_xyz(invalid_coord)
        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn("$end", error)

    def test_coord_to_xyz_no_coord_block(self):
        """Tests file without $coord block"""
        invalid_coord = """$title
water
$end
"""
        result, error = coord_string_to_xyz(invalid_coord)
        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn("No valid atomic coordinate", error)

    def test_gaussian_to_xyz_valid(self):
        """Tests valid Gaussian to XYZ conversion"""
        result, error = gaussian_to_xyz_string(self.valid_gaussian)
        self.assertIsNone(error)
        self.assertIsNotNone(result)
        lines = result.strip().split('\n')
        self.assertEqual(lines[0], "3")  # Atom count
        self.assertIn("O", lines[2])  # First atom is oxygen

    def test_gaussian_to_xyz_no_charge_spin(self):
        """Tests Gaussian file missing charge/spin line"""
        invalid_gaussian = """%chk=test.chk
#p b3lyp/6-31g

Title

O 0.0 0.0 0.0
H 0.0 0.0 1.0
"""
        result, error = gaussian_to_xyz_string(invalid_gaussian)
        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn("charge/spin", error)

    def test_gaussian_to_xyz_no_coordinates(self):
        """Tests Gaussian file without coordinates"""
        invalid_gaussian = """%chk=test.chk
#p b3lyp/6-31g

Title

0 1

"""
        result, error = gaussian_to_xyz_string(invalid_gaussian)
        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn("atomic coordinates", error)


class TestStructureUtilsEdgeCases(unittest.TestCase):
    """Tests edge cases and special formats"""

    def test_xyz_with_extra_columns(self):
        """Tests XYZ file with extra columns"""
        xyz_extra = """2
Test with extra data
O  0.0  0.0  0.0  1.0  extra_data
H  0.0  0.0  1.0  2.0  more_data
"""
        result, error = xyz_to_coord_string(xyz_extra)
        self.assertIsNone(error)
        self.assertIsNotNone(result)

    def test_coord_with_periodic(self):
        """Tests COORD file with periodic information"""
        coord_periodic = """$coord
$periodic 3
  0.000000    0.000000    0.000000      o
  0.000000    0.000000    1.000000      h
$end
"""
        result, error = coord_string_to_xyz(coord_periodic)
        self.assertIsNone(error)
        self.assertIsNotNone(result)

    def test_gaussian_without_empty_line(self):
        """Tests Gaussian file without empty line after charge/spin line"""
        gaussian_no_empty = """%chk=test.chk
#p b3lyp/6-31g

Title

0 1
C 0.0 0.0 0.0
H 0.0 0.0 1.0
"""
        result, error = gaussian_to_xyz_string(gaussian_no_empty)
        self.assertIsNone(error)
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()