"""
Tests for PyPoE.poe.file.idt

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | tests/PyPoE/poe/file/test_idt.py                                 |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Tests for PyPoE/tests/poe/file/test_idt.py

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os

# 3rd-party
import pytest
from tempfile import TemporaryDirectory

# self
from PyPoE.poe.file import idt

# =============================================================================
# Setup
# =============================================================================

cur_dir = os.path.split(os.path.realpath(__file__))[0]
idl_path = os.path.join(cur_dir, '_data', 'test.idt')

# =============================================================================
# Fixtures
# =============================================================================

data = {
    'version': 1,
    'image': 'Art/2DItems/Test.dds',
    'records': [
        {
            'name': 'Blade',
            'records': [
                {'x': 1, 'y': 1},
                {'x': 2, 'y': 2},
            ],
        },
        {
            'name': 'Handle',
            'records': [
                {'x': 1, 'y': 1},
                {'x': 2, 'y': 2},
                {'x': 3, 'y': 3},
                {'x': 4, 'y': 4},
            ],
        },
    ],
}

@pytest.fixture
def idt_file():
    return idt.IDTFile(data)


# =============================================================================
# Tests
# =============================================================================

class TestIDLFile:

    def eq(self, idt_file):
        assert idt_file.version == data['version']
        assert idt_file.image == data['image']
        for i, tex in enumerate(data['records']):
            assert idt_file.records[i].name == tex['name']
            for j, coord in enumerate(tex['records']):
                assert idt_file.records[i].records[j].x == coord['x']
                assert idt_file.records[i].records[j].y == coord['y']

    def test_init(self, idt_file):
        self.eq(idt_file)

    def test_read(self, idt_file):
        idt_file2 = idt.IDTFile()
        idt_file2.read(idl_path)

        self.eq(idt_file)

    def test_write(self, idt_file):
        idt_file2 = idt.IDTFile()

        with TemporaryDirectory() as d:
            tmp_path = os.path.join(d, 'test_write.idt')
            idt_file.write(tmp_path)
            idt_file2.read(tmp_path)

            self.eq(idt_file2)



