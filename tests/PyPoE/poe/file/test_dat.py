"""
Path     PyPoE/tests/poe/file/test_dat.py
Name     Tests for PyPoE.poe.file.dat
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO

Tests for dat.py


AGREEMENT

See PyPoE/LICENSE


TODO

- more/better tests for DatFile
- RecordList tests
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os
import struct

# 3rd Party
import pytest
from configobj import ConfigObj

# self
from PyPoE.poe.file import dat

# =============================================================================
# Setup
# =============================================================================

cur_dir = os.path.split(os.path.realpath(__file__))[0]

test_data = data = [
    ('bool', '?', 1),
    ('byte', 'b', -2**7+1),
    ('ubyte', 'B', 2**8-1),
    ('short', 'h', -2**15+1),
    ('ushort', 'H', 2**16-1),
    ('int', 'i', -2**31+1),
    ('uint', 'I', 2**32-1),
    ('long', 'q', -2**63+1),
    ('ulong', 'Q', 2**64-1),
]

test_str = 'Hello world'
test_str_enc = test_str.encode('utf-16le') + b'\x00\x00\x00\x00'
test_list = [17418241, 777123, 0xFEFEFEFE]

# =============================================================================
# Tests
# =============================================================================

def test_load_spec():
    return dat.load_spec(os.path.join(cur_dir, 'dat_testspec.ini'))

def test_reload_default_spec():
    old = dat._default_spec
    dat.reload_default_spec()
    assert id(old) != id(dat._default_spec), 'Specification wasn\'t reloaded'

# DatValue instances are created by the script, so they don't contain any
# error checking upon creation themselves.
# Hence we just test for them working correctly with correct information.

def test_dat_value_basic():
    """
    Test for a basic DatValue instance.
    """
    dv = dat.DatValue(value=5, offset=0, size=4, parent=None, specification=None)

    # Function tests
    assert dv.get_value() == 5, 'Value should be identical'

    # Property Tests
    with pytest.raises(TypeError):
        dv.data_size
        dv.data_start_offset
        dv.data_end_offset
    assert dv.is_data == False, 'Should not be data'
    assert dv.has_data == False, 'Should not have any data'
    assert dv.is_pointer == False, 'Should not be a pointer'
    assert dv.is_list == False, 'Should not be a list'
    assert dv.is_parsed == True, 'Should count as parsed value'

def test_dat_value_raw():
    """
    Test for a basic DatValue instance with raw data.
    """
    dv = dat.DatValue(value=b'\x00\x00', offset=0, size=2, parent=None, specification=None)

    # Function tests
    assert dv.get_value() == b'\x00\x00', 'Value should be identical'

    # Property Tests
    with pytest.raises(TypeError):
        dv.data_size
        dv.data_start_offset
        dv.data_end_offset
    assert dv.is_data == False, 'Should not be data'
    assert dv.has_data == False, 'Should not have any data'
    assert dv.is_pointer == False, 'Should not be a pointer'
    assert dv.is_list == False, 'Should not be a list'
    assert dv.is_parsed == False, 'Should count as unparsed/binary value'

def test_dat_value_pointer():
    """
    Test for a pointer DatValue instance.
    """
    dv_data = dat.DatValue(value=5, offset=0, size=4, parent=None, specification=None)

    dv = dat.DatValue(value=8, offset=0, size=4, parent=None, specification=None)
    dv.child = dat.DatValue(value='test', offset=8, size=4*2+4, parent=dv, specification=None)

    # Function tests
    assert dv.get_value() == 'test', 'Value should be identical'

    # Property Tests
    assert dv.data_size == dv.child.size, 'Should return the size of the child'
    assert dv.data_start_offset == dv.value, 'Should return the dv.value, i.e. the pointer'
    assert dv.data_end_offset == dv.value + dv.data_size, 'Should be the pointer + sizeof(child)'
    assert dv.is_data == False, 'Should not be data'
    assert dv.has_data == True, 'Should have data'
    assert dv.is_pointer == True, 'Should be a pointer'
    assert dv.is_list == False, 'Should not be a list'
    assert dv.is_parsed == True, 'Should count as parsed value'

    # Child Property tests
    with pytest.raises(TypeError):
        dv.child.data_size
        dv.child.data_start_offset
        dv.child.data_end_offset
    assert dv.child.is_data == True, 'Should be data'
    assert dv.child.has_data == False, 'Should not have any data'
    assert dv.child.is_pointer == False, 'Should not be a pointer'
    assert dv.child.is_list == False, 'Should not be a list'
    assert dv.child.is_parsed == True, 'Should count as parsed value'

def test_dat_value_list():
    """
    Test for a list DatValue instance.
    """
    dv = dat.DatValue(value=(3, 8), offset=0, size=8, parent=None, specification=None)
    dv.children = [
        dat.DatValue(value=1, offset=8, size=4, parent=dv, specification=None),
        dat.DatValue(value=2, offset=12, size=4, parent=dv, specification=None),
        dat.DatValue(value=3, offset=16, size=4, parent=dv, specification=None),
    ]

    # Function tests
    assert dv.get_value() == [1,2,3], 'Value should be identical'

    # Property Tests
    assert dv.data_size == dv.value[0] * dv.children[0].size, 'Should return sizeof(self) + sizeof(child)'
    assert dv.data_start_offset == dv.value[1], 'Should return the dv.value, i.e. the pointer'
    assert dv.data_end_offset == dv.value[1] + dv.data_size, 'Should be the pointer + sizeof(child)'
    assert dv.is_data == False, 'Should not be data'
    assert dv.has_data == True, 'Should have data'
    assert dv.is_pointer == False, 'Should not be a pointer'
    assert dv.is_list == True, 'Should be a list'
    assert dv.is_parsed == True, 'Should count as parsed value'

    # Child property tests
    for i in range(0, len(dv.children)):
        child = dv.children[i]
        with pytest.raises(TypeError):
            child.data_size
            child.data_start_offset
            child.data_end_offset
        assert child.is_data == True, 'Should be data'
        assert child.has_data == False, 'Should not have any data'
        assert child.is_pointer == False, 'Should not be a pointer'
        assert child.is_list == False, 'Should not be a list'
        assert child.is_parsed == True, 'Should count as parsed value'


def test_dat_file():
    # One row
    temp_file = []
    baseptr = 8
    # One row
    temp_file.append(struct.pack('<I', 1))
    for item in test_data:
        temp_file.append(struct.pack('<' + item[1], item[2]))
    # ref|string -> int pointer
    temp_file.append(struct.pack('<i', baseptr))
    baseptr += len(test_str_enc)
    # ref|list -> int size, int pointer
    temp_file.append(struct.pack('<i', 3))
    temp_file.append(struct.pack('<i', baseptr))
    baseptr += 3*4
    # ref|ref|ref|int
    # The first reference in the data list
    temp_file.append(struct.pack('<i', baseptr))
    baseptr += 4

    # Magic number
    temp_file.append(b'\xBB\xbb\xBB\xbb\xBB\xbb\xBB\xbb')
    # Data
    temp_file.append(test_str_enc)
    for item in test_list:
        temp_file.append(struct.pack('<I', item))

    # ref|ref|ref|int
    # the two extra refs, and integer value
    for i in range(0, 2):
        temp_file.append(struct.pack('<i', baseptr))
        baseptr += 4
    temp_file.append(struct.pack('<i', 0x1337))
    baseptr += 4

    temp_file = b''.join(temp_file)

    spec = test_load_spec()

    df = dat.DatFile('TestSpec.dat')
    df.read_from_raw(temp_file, specification=spec)

    for row in df.table_data:
        for test in test_data:
            assert row[test[0]] == test[2], 'Value mismatch - int'
        assert row['ref|string'] == test_str, 'Value mismatch - string'
        l = row['ref|list|int']
        assert l[0] == test_list[0], 'Value mismatch - list'
        assert l[1] == test_list[1], 'Value mismatch - list'
        # 0xFEFEFEFE is a magic key, so return -1
        assert l[2] == -1, 'Value mismatch - list, special value'
        assert row['ref|ref|ref|int'] == 0x1337, 'Value mismatch - nested pointers'