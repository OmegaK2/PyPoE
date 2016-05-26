"""
Tests for PyPoE.poe.file.idl

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | tests/PyPoE/poe/file/test_idl.py                                 |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Tests for PyPoE/poe/file/idl.py

Agreement
===============================================================================

See PyPoE/LICENSE

TODO
===============================================================================

- IDLFile:
-- __add__
-- __setitem__
-- insert
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
from PyPoE.poe.file.idl import IDLFile, IDLRecord

# =============================================================================
# Setup
# =============================================================================

cur_dir = os.path.split(os.path.realpath(__file__))[0]
idl_path = os.path.join(cur_dir, '_data', 'test.idl')
idl_path_result = os.path.join(cur_dir, '_data', 'test_write.idl')

# =============================================================================
# Fixtures
# =============================================================================

data = [
    ["Art/2DArt/Test1", "Art/Textures/Test.dds", 0, 0, 1, 1],
    ["Art/2DArt/Test2", "Art/Textures/Test.dds", 1, 0, 2, 1],
    ["Art/2DArt/Test3", "Art/Textures/Test.dds", 0, 1, 2, 2],
]


@pytest.fixture
def idl_file():
    return IDLFile()

@pytest.fixture
def idl_records():
    return [IDLRecord(*row) for row in data]

@pytest.fixture(params=data)
def idl_record(request):
    return IDLRecord(*request.param), request.param

@pytest.fixture
def idl_record_extra():
    return IDLRecord("Art/2DArt/Extra", "Art/Textures/Test.dds", 0, 2, 3, 3)

# =============================================================================
# Tests
# =============================================================================

class TestIDLRecord:
    def test_init(self, idl_record):
        record, d = idl_record

        for i, attr in enumerate(record.__slots__):
            assert getattr(record, attr) == d[i], 'Attribute %s mismatch' % attr

    def test_eq(self, idl_record, idl_record_extra):
        record, d = idl_record
        assert record == record, 'Record should be equal to itself'
        assert record == IDLRecord(*d), 'Record should be equal to record initialized with the same data'
        assert not record == idl_record_extra, 'Record should not be equal to record initialized with different data'
        assert not record == 5, 'Record should not be equal to other data types'

    def test_repr(self, idl_record):
        record, d = idl_record
        assert eval(repr(record)) == record, 'repr() should return an object that would create a valid IDLRecord'

class TestIDLFile:
    def test_init(self, idl_file):
        pass

    def test_append(self, idl_file, idl_records):
        # Should work and not raise any errors
        for record in idl_records:
            idl_file.append(record)
        # Should raise type error
        with pytest.raises(TypeError):
            idl_file.append(5)
            idl_file.append('test')
            idl_file.append(object())

    def test_read(self, idl_file, idl_records):
        idl_file.read(idl_path)

        for i, record in enumerate(idl_file):
            assert record == idl_records[i], 'The records read should match the testing records.'

    def test_write(self, idl_file, idl_records):
        for record in idl_records:
            idl_file.append(record)

        with TemporaryDirectory() as d:
            tmp_path = os.path.join(d, 'test_write.idl')
            idl_file.write(tmp_path)

            with open(tmp_path, 'rb') as f1:
                with open(idl_path_result, 'rb') as f2:
                    assert f1.read() == f2.read(), 'Written file should be equal to the write test file.'



