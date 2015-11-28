"""


Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | tests/PyPoE/shared/test_mixins.py                                |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
-------------------------------------------------------------------------------



Agreement
-------------------------------------------------------------------------------

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python

# 3rd-party
import pytest

# self
from PyPoE.shared import mixins

# =============================================================================
# Setup
# =============================================================================


class Repr(mixins.ReprMixin):
    def __init__(self, a, b=42):
        self.a = a
        self._b = b
        self.extra = 1337


# =============================================================================
# Tests
# =============================================================================


class TestReprMixin:

    @pytest.fixture
    def r(self):
        return Repr(5)

    def test_defaults(self, r):
        assert repr(r) == 'Repr<%s>(a=5)' % hex(id(r))

    def test_private(self, r):
        r._REPR_PRIVATE_ATTRIBUTES = True
        assert repr(r) == 'Repr<%s>(a=5, b=42)' % hex(id(r))

    def test_override(self, r):
        r._REPR_ATTRIBUTES = {'b': 'extra'}
        assert repr(r) == 'Repr<%s>(a=5, b=1337)' % hex(id(r))

    def test_override_missing(self, r):
        r._REPR_ATTRIBUTES = {'b': 'extra'}
        r._REPR_IGNORE_MISSING_ATTRIBUTES = True
        assert repr(r) == 'Repr<%s>(b=1337)' % hex(id(r))

    def test_ingore(self, r):
        r._REPR_ATTRIBUTES_IGNORE = {'a'}
        assert repr(r) == 'Repr<%s>()' % hex(id(r))