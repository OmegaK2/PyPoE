"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | test_validator.py                                                |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================



Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os
from enum import IntEnum

# 3rd-party
import pytest
from validate import ValidateError

# self
from PyPoE.shared.config import validator

# =============================================================================
# Setup
# =============================================================================


class MyIntEnum(IntEnum):
    a = 1
    b = 2
    c = 3

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope='module')
def int_enum_tester():
    return validator.IntEnumValidator(enum=MyIntEnum, default=MyIntEnum.a)


@pytest.fixture(scope='module')
def file_path():
    return __file__


@pytest.fixture(scope='module')
def dir_path():
    return os.path.split(__file__)[0]


# =============================================================================
# Tests
# =============================================================================


class TestIntEnumValidator:
    values = (
        (1, MyIntEnum.a),
        ('a', MyIntEnum.a),
        ('1', MyIntEnum.a),
        # Will be written as this value into config
        ('MyIntEnum.a', MyIntEnum.a),
    )

    fvalues = (
        ('4', '4 (str) is out of range and should fail'),
        ('2.0', '2.0 (str) is not a valid integer'),
        (4, '4 (int) is out of range and should fail'),
        (2.0, '2.0 (float) is not a valid integer'),
    )


    def test_init(self, int_enum_tester):
        with pytest.raises(TypeError):
            validator.IntEnumValidator(enum=int)
            validator.IntEnumValidator(enum=MyIntEnum, default=5)
            validator.IntEnumValidator(enum=MyIntEnum, default='c')
            validator.IntEnumValidator(enum=MyIntEnum, default=int)

    @pytest.mark.parametrize('value,expected', values)
    def test_success(self, int_enum_tester, value, expected):
        assert int_enum_tester(value) == expected

    @pytest.mark.parametrize('value,errmsg', fvalues)
    def test_fail(self, int_enum_tester, value, errmsg):
        with pytest.raises(ValidateError):
            int_enum_tester(value)


class TestIsFile:
    def test_success(self, file_path):
        assert validator.is_file(file_path) == file_path

    @pytest.mark.xfail(ValidateError)
    def test_fail(self, dir_path):
        validator.is_file(dir_path)


class TestIsDirectory:
    def test_success(self, dir_path):
        assert validator.is_directory(dir_path) == dir_path

    @pytest.mark.xfail(ValidateError)
    def test_fail(self, file_path):
        validator.is_directory(file_path)
