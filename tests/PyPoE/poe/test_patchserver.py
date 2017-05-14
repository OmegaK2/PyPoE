"""
Tests for PyPoE.poe.patchserver

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | tests/PyPoE/poe/test_patchserver.py                              |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Tests for patchserver.py

Agreement
===============================================================================

See PyPoE/LICENSE

TODO
===============================================================================
Testing on live data is difficult, since we can't verify it was downloaded
correctly as the contents of the files may change. Perhaps find a good
candidate for testing.
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os
import re
from urllib.error import HTTPError
from tempfile import TemporaryDirectory

# 3rd-party
import pytest

# self
from PyPoE.poe import patchserver

# =============================================================================
# Setup
# =============================================================================

_TEST_URL = 'Data/Wordlists.dat'
_re_version = re.compile(r'[\d]+\.[\d]+\.[\d]+\.[\d]+', re.UNICODE)

# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture(scope='module')
def patch():
    return patchserver.Patch()

# =============================================================================
# Tests
# =============================================================================


class TestPatch(object):
    def test_dst_file(self, patch):
        with TemporaryDirectory() as temp:
            patch.download(
                file_path=_TEST_URL,
                dst_file=os.path.join(temp, 'test.txt'),
            )

    def test_dst_dir(self, patch):
        with TemporaryDirectory() as temp:
            patch.download(
                file_path=_TEST_URL,
                dst_dir=temp,
            )

    def test_missing_dst_error(self, patch):
        with pytest.raises(ValueError):
            patch.download(
                file_path=_TEST_URL,
            )

    def test_file_not_found(self, patch):
        with pytest.raises(HTTPError):
            patch.download_raw(
                file_path='THIS_SHOULD_NOT_EXIST.FILE',
            )

    def test_version(self, patch):
        assert _re_version.match(patch.version) is not None, 'patch.version ' \
            'result is expected to match the x.x.x.x format'

