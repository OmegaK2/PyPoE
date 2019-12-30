"""
Tests for PyPoE.poe.file.ggpk

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | tests/PyPoE/poe/file/test_ggpk.py                                |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Tests for ggpk.py

Agreement
===============================================================================

See PyPoE/LICENSE

.. todo::

    * The entire test I suppose
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os
from tempfile import TemporaryDirectory

# 3rd Party
import pytest

# self
from PyPoE.poe.file import ggpk

# =============================================================================
# Setup
# =============================================================================

DDS_UNCOMPRESSED = 'Art/Textures/Characters/Adventurer/' \
                   'adventurerPalid_colour.dds'
DDS_COMPRESSED = 'Art/2DArt/BuffIcons/AssassinsMark.dds'

# =============================================================================
# Tests
# =============================================================================


class TestGGPKFile:
    # This kinda tests it already by reading the global fixture
    def test_init(self, ggpkfile):
        assert ggpkfile.is_parsed == True


# These tests will raise errors if something is wrong, like decompression
# errors
class TestDDSExtract:
    def test_uncompressed(self, ggpkfile):
        data = ggpkfile[DDS_UNCOMPRESSED].record.extract().read()
        ggpk.extract_dds(data=data)

    def test_compressed(self, ggpkfile):
        data = ggpkfile[DDS_COMPRESSED].record.extract().read()
        ggpk.extract_dds(data=data)

    def test_reference_ggpk(self, ggpkfile):
        data = b'*' + DDS_COMPRESSED.encode('ascii')
        ggpk.extract_dds(data=data, path_or_ggpk=ggpkfile)

    def test_reference_path(self, ggpkfile):
        data = b'*' + DDS_COMPRESSED.encode('ascii')
        path = os.path.split(DDS_COMPRESSED)[0]
        with TemporaryDirectory() as tmp_dir:
            path = os.path.join(tmp_dir, path)
            os.makedirs(path)
            ggpkfile[DDS_COMPRESSED].record.extract_to(path)

            ggpk.extract_dds(data=data, path_or_ggpk=tmp_dir)
