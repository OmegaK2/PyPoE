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

# =============================================================================
# Setup
# =============================================================================

DDS_UNCOMPRESSED = 'Art/Textures/Characters/Adventurer/' \
                   'adventurerPalid_colour.dds'
DDS_COMPRESSED = 'Art/2DArt/BuffIcons/AssassinsMark.dds'

# =============================================================================
# Tests
# =============================================================================


# These tests will raise errors if something is wrong, like decompression
# errors
class TestDDSExtract:
    def test_uncompressed(self, file_system):
        file_system.extract_dds(file_system.get_file(DDS_UNCOMPRESSED))

    def test_compressed(self, file_system):
        file_system.extract_dds(file_system.get_file(DDS_COMPRESSED))

    def test_reference(self, file_system):
        data = b'*' + DDS_COMPRESSED.encode('ascii')
        file_system.extract_dds(data)
