"""
Tests for PyPoE.poe.file.dat

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | tests/PyPoE/poe/file/test_dat.py                                 |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Tests for dat.py

Agreement
===============================================================================

See PyPoE/LICENSE

TODO
===============================================================================

- more/better tests for DatFile
- RecordList tests
===============================================================================
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os
import struct

# 3rd Party
import pytest

# self
from PyPoE.poe.constants import MOD_DOMAIN
from PyPoE.poe.file import dat
from PyPoE.poe.file.specification import load

# =============================================================================
# Setup
# =============================================================================

spec_dir = os.path.join(
    os.path.split(os.path.realpath(__file__))[0], '_data', 'specifications'
)

test_data = data = [
    ('bool', '?', 1),
    ('byte', 'b', -2**7+1),
    ('ubyte', 'B', 2**8-2),
    ('short', 'h', -2**15+1),
    ('ushort', 'H', 2**16-2),
    ('int', 'i', -2**31+1),
    ('uint', 'I', 2**32-2),
    ('long', 'q', -2**63+1),
    ('ulong', 'Q', 2**64-2),
]

test_str = 'Hello world'
test_str_enc = test_str.encode('utf-16le') + b'\x00\x00\x00\x00'
test_list = [17418241, 777123, 0xFEFEFEFE]


@pytest.fixture(scope='module')
def testspec_dat_file():
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
    temp_file.append(dat.DAT_FILE_MAGIC_NUMBER)
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

    return b''.join(temp_file)


@pytest.fixture(scope='module')
def rr_temp_dir(tmpdir_factory):
    file_datas = (
        {
            'file_name': 'Main.dat',
            'data': (
                (0, 1, 0, 0, 10, 1),
                (1, 2, 1, 1, 20, 2),
                (2, 3, 3, 0xFEFEFEFE, 30, 3),
            )
        },
        {
            'file_name': 'Other.dat',
            'data': (
                (10, ),
                (20, ),
                (30, ),
            ),
        },
    )

    temp_dir = str(tmpdir_factory.mktemp('rrtest'))
    os.mkdir(os.path.join(temp_dir, 'Data'))

    for file_data in file_datas:
        with open(os.path.join(temp_dir, 'Data', file_data['file_name']),
                  'wb') as temp_file:
            temp_file.write(struct.pack('<I', len(file_data['data'])))
            for row in file_data['data']:
                for value in row:
                    temp_file.write(struct.pack('<I', value))
            temp_file.write(dat.DAT_FILE_MAGIC_NUMBER)

    return temp_dir


@pytest.fixture(scope='module')
def rr_instance(rr_temp_dir):
    return dat.RelationalReader(
        path_or_ggpk=rr_temp_dir,
        read_options={
            'specification': load(os.path.join(
                spec_dir, 'rr_test.py'
            )),
            'use_dat_value': False,
        },
    )

# =============================================================================
# Tests
# =============================================================================


def test_load():
    return load(os.path.join(spec_dir, 'dat_testspec.py'))


def test_reload_default_spec():
    old = dat._default_spec
    dat.set_default_spec(reload=True)
    assert id(old) != id(dat._default_spec), 'Specification wasn\'t reloaded'

#
# DatValue
#
# DatValue instances are created by the script, so they don't contain any
# error checking upon creation themselves.
# Hence we just test for them working correctly with correct information.


class TestDatValue:
    # Basic Data
    dv_basic = dat.DatValue(value=5, offset=0, size=4, parent=None, specification=None)
    dv_basic_int_negative = dat.DatValue(value=-42, offset=0, size=4, parent=None, specification=None)
    dv_basic_int_positive = dat.DatValue(value=1337, offset=0, size=4, parent=None, specification=None)
    dv_basic_str_test = dat.DatValue(value='test', offset=0, size=4*2+4, parent=None, specification=None)
    dv_basic_str_a = dat.DatValue(value='a', offset=0, size=1*2+4, parent=None, specification=None)
    dv_basic_str_z = dat.DatValue(value='z', offset=0, size=1*2+4, parent=None, specification=None)

    # Raw
    dv_raw = dat.DatValue(value=b'\x00\x00', offset=0, size=2, parent=None, specification=None)

    # Pointers
    dv_pointer = dat.DatValue(value=8, offset=0, size=4, parent=None, specification=None)
    dv_pointer.child = dat.DatValue(value='test', offset=8, size=4*2+4, parent=dv_pointer, specification=None)

    dv_pointer_int_negative = dat.DatValue(value=8, offset=0, size=4, parent=None, specification=None)
    dv_pointer_int_negative.child = dat.DatValue(value=-42, offset=8, size=4, parent=dv_pointer_int_negative, specification=None)

    dv_pointer_int_positive = dat.DatValue(value=8, offset=0, size=4, parent=None, specification=None)
    dv_pointer_int_positive.child = dat.DatValue(value=1337, offset=8, size=4, parent=dv_pointer_int_positive, specification=None)

    # Lists
    dv_list = dat.DatValue(value=(3, 8), offset=0, size=8, parent=None, specification=None)
    dv_list.children = [
        dat.DatValue(value=1, offset=8, size=4, parent=dv_list, specification=None),
        dat.DatValue(value=2, offset=12, size=4, parent=dv_list, specification=None),
        dat.DatValue(value=3, offset=16, size=4, parent=dv_list, specification=None),
    ]

    dv_list_reversed = dat.DatValue(value=(3, 8), offset=0, size=8, parent=None, specification=None)
    dv_list_reversed.children = [
        dat.DatValue(value=3, offset=8, size=4, parent=dv_list_reversed, specification=None),
        dat.DatValue(value=2, offset=12, size=4, parent=dv_list_reversed, specification=None),
        dat.DatValue(value=1, offset=16, size=4, parent=dv_list_reversed, specification=None),
    ]


    def test_instance_basic(self):
        """
        Test for a basic DatValue instance.
        """
        # Function tests
        assert self.dv_basic.get_value() == 5, 'Value should be identical'

        # Property Tests
        with pytest.raises(TypeError):
            self.dv_basic.data_size
            self.dv_basic.data_start_offset
            self.dv_basic.data_end_offset
        assert self.dv_basic.is_data == False, 'Should not be data'
        assert self.dv_basic.has_data == False, 'Should not have any data'
        assert self.dv_basic.is_pointer == False, 'Should not be a pointer'
        assert self.dv_basic.is_list == False, 'Should not be a list'
        assert self.dv_basic.is_parsed == True, 'Should count as parsed value'

    def test_instance_raw(self):
        """
        Test for a basic DatValue instance with raw data.
        """
        # Function tests
        assert self.dv_raw.get_value() == b'\x00\x00', 'Value should be identical'

        # Property Tests
        with pytest.raises(TypeError):
            self.dv_raw.data_size
            self.dv_raw.data_start_offset
            self.dv_raw.data_end_offset
        assert self.dv_raw.is_data == False, 'Should not be data'
        assert self.dv_raw.has_data == False, 'Should not have any data'
        assert self.dv_raw.is_pointer == False, 'Should not be a pointer'
        assert self.dv_raw.is_list == False, 'Should not be a list'
        assert self.dv_raw.is_parsed == False, 'Should count as unparsed/binary value'

    def test_instance_pointer(self):
        """
        Test for a pointer DatValue instance.
        """
        # Function tests
        assert self.dv_pointer.get_value() == 'test', 'Value should be identical'

        # Property Tests
        assert self.dv_pointer.data_size == self.dv_pointer.child.size, 'Should return the size of the child'
        assert self.dv_pointer.data_start_offset == self.dv_pointer.value, 'Should return the self.dv_pointer.value, i.e. the pointer'
        assert self.dv_pointer.data_end_offset == self.dv_pointer.value + self.dv_pointer.data_size, 'Should be the pointer + sizeof(child)'
        assert self.dv_pointer.is_data == False, 'Should not be data'
        assert self.dv_pointer.has_data == True, 'Should have data'
        assert self.dv_pointer.is_pointer == True, 'Should be a pointer'
        assert self.dv_pointer.is_list == False, 'Should not be a list'
        assert self.dv_pointer.is_parsed == True, 'Should count as parsed value'

        # Child Property tests
        with pytest.raises(TypeError):
            self.dv_pointer.child.data_size
            self.dv_pointer.child.data_start_offset
            self.dv_pointer.child.data_end_offset
        assert self.dv_pointer.child.is_data == True, 'Should be data'
        assert self.dv_pointer.child.has_data == False, 'Should not have any data'
        assert self.dv_pointer.child.is_pointer == False, 'Should not be a pointer'
        assert self.dv_pointer.child.is_list == False, 'Should not be a list'
        assert self.dv_pointer.child.is_parsed == True, 'Should count as parsed value'

    def test_instance_list(self):
        """
        Test for a list DatValue instance.
        """
        # Function tests
        assert self.dv_list.get_value() == [1,2,3], 'Value should be identical'

        # Property Tests
        assert self.dv_list.data_size == self.dv_list.value[0] * self.dv_list.children[0].size, 'Should return sizeof(self) + sizeof(child)'
        assert self.dv_list.data_start_offset == self.dv_list.value[1], 'Should return the self.dv_list.value, i.e. the pointer'
        assert self.dv_list.data_end_offset == self.dv_list.value[1] + self.dv_list.data_size, 'Should be the pointer + sizeof(child)'
        assert self.dv_list.is_data == False, 'Should not be data'
        assert self.dv_list.has_data == True, 'Should have data'
        assert self.dv_list.is_pointer == False, 'Should not be a pointer'
        assert self.dv_list.is_list == True, 'Should be a list'
        assert self.dv_list.is_parsed == True, 'Should count as parsed value'

        # Child property tests
        for i in range(0, len(self.dv_list.children)):
            child = self.dv_list.children[i]
            with pytest.raises(TypeError):
                child.data_size
                child.data_start_offset
                child.data_end_offset
            assert child.is_data == True, 'Should be data'
            assert child.has_data == False, 'Should not have any data'
            assert child.is_pointer == False, 'Should not be a pointer'
            assert child.is_list == False, 'Should not be a list'
            assert child.is_parsed == True, 'Should count as parsed value'

    # comprehensions are performed on the values, not the datvalues themselves

    types = ['__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__']
    cmp_tests = []

    # Basic Tests
    basic_tests = [
        [dv_basic_int_negative, dv_basic],
        [dv_basic, dv_basic_int_positive],
        [dv_basic_int_negative, 0],
        [dv_basic_int_negative, dv_pointer_int_positive],
        [dv_basic_str_a, dv_basic_str_z],
        [dv_basic_str_a, 'test'],
        [dv_basic_str_a, dv_pointer],
        [dv_list, dv_list_reversed],
        [dv_list, [8]],
    ]
    for item in zip(types, [True, True, False, True, False, False]):
        item = list(item)
        for vars in basic_tests:
            cmp_tests.append(item + vars)

    @pytest.mark.parametrize('cmp_type,result,a,b', cmp_tests)
    def test_cmp(self, cmp_type, result, a, b):
        assert getattr(a, cmp_type)(b) == result, '%s for %s and %s should return %s' % (cmp_type, a, b, result)


#
# DatFile tests
#

def test_dat_file(testspec_dat_file):
    spec = test_load()

    df = dat.DatFile('TestSpec.dat')
    dr = df.read(testspec_dat_file, specification=spec)

    for row in dr:
        for test in test_data:
            assert row[test[0]] == test[2], 'Value mismatch - int'
        assert row['ref|string'] == test_str, 'Value mismatch - string'
        l = row['ref|list|int']
        assert l[0] == test_list[0], 'Value mismatch - list'
        assert l[1] == test_list[1], 'Value mismatch - list'
        # 0xFEFEFEFE is a magic key, so return -1
        assert l[2] is None, 'Value mismatch - list, special value'
        assert row['ref|ref|ref|int'] == 0x1337, 'Value mismatch - nested pointers'


class TestSpecificationErrors:
    errors = (
        (
            'invalid_foreign_key_file.py',
            dat.SpecificationError.ERRORS.INVALID_FOREIGN_KEY_FILE,
        ),
        (
            'invalid_foreign_key_id.py',
            dat.SpecificationError.ERRORS.INVALID_FOREIGN_KEY_ID,
        ),
        (
            'invalid_argument_combination.py',
            dat.SpecificationError.ERRORS.INVALID_ARGUMENT_COMBINATION,
        ),
        (
            'invalid_enum_name.py',
            dat.SpecificationError.ERRORS.INVALID_ENUM_NAME,
        ),
        (
            'virtual_key_empty.py',
            dat.SpecificationError.ERRORS.VIRTUAL_KEY_EMPTY,
        ),
        (
            'virtual_key_duplicate.py',
            dat.SpecificationError.ERRORS.VIRTUAL_KEY_DUPLICATE,
        ),
        (
            'virtual_key_invalid_key.py',
            dat.SpecificationError.ERRORS.VIRTUAL_KEY_INVALID_KEY,
        ),
        (
            'virtual_key_invalid_data_type.py',
            dat.SpecificationError.ERRORS.VIRTUAL_KEY_INVALID_DATA_TYPE,
        ),

    )

    @pytest.mark.parametrize('file_name,error', errors)
    def test_validation_errors(self, file_name, error):
        with pytest.raises(dat.SpecificationError) as e:
            load(os.path.join(spec_dir, file_name))
        assert e.value.code == error

    def test_runtime_missing_specification(self, testspec_dat_file):
        df = dat.DatFile('TestSpec.dat')
        with pytest.raises(dat.SpecificationError) as e:
            dr = df.read(testspec_dat_file)
        assert e.value.code == \
               dat.SpecificationError.ERRORS.RUNTIME_MISSING_SPECIFICATION

    def test_runtime_rowsize_mismatch(self, rr_temp_dir):
        df = dat.DatFile('Main.dat')
        with pytest.raises(dat.SpecificationError) as e:
            dr = df.read(
                os.path.join(rr_temp_dir, 'Data', 'Main.dat'),
                specification=load(os.path.join(
                    spec_dir, 'runtime_rowsize_mismatch.py'
                )),
            )

        assert e.value.code == \
            dat.SpecificationError.ERRORS.RUNTIME_ROWSIZE_MISMATCH


    foreign_key_errors = (
        'runtime_missing_foreign_key1.py',
        'runtime_missing_foreign_key2.py',
    )

    @pytest.mark.parametrize('spec_name', foreign_key_errors)
    def test_runtime_missing_foreign_key(self, rr_temp_dir, spec_name):
        rr = dat.RelationalReader(
            path_or_ggpk=rr_temp_dir,
            raise_error_on_missing_relation=True,
            read_options={
                'specification': load(os.path.join(
                    spec_dir, spec_name
                )),
                'use_dat_value': False,
            },
        )
        with pytest.raises(dat.SpecificationError) as e:
            rr.get_file('Data/Main.dat')
        assert e.value.code == \
            dat.SpecificationError.ERRORS.RUNTIME_MISSING_FOREIGN_KEY


class TestRelationalReader():
    relations_expected = {
        'ForeignKey': [0, 1, 2],
        'ForeignKeyOffset': [0, 1, 2],
        'ForeignKeyNone': [0, 1, None],
        'ForeignKeyCellValue': [0, 1, 2],
    }

    @pytest.mark.parametrize('use_dat_value', (True, False))
    def test_relations(self, rr_temp_dir, use_dat_value):
        rr = dat.RelationalReader(
            path_or_ggpk=rr_temp_dir,
            read_options={
                'specification': load(os.path.join(
                    spec_dir, 'rr_test.py'
                )),
                'use_dat_value': use_dat_value,
            },
        )

        for column, values in self.relations_expected.items():
            for i, row in enumerate(rr['Main.dat']):
                expected = values[i]
                if expected is not None:
                    expected = rr['Other.dat'][expected]
                else:
                    expected = None

                assert row[column] == expected, 'Testing against expected row'

    enums_expected = {
        'ConstTest': (MOD_DOMAIN(1), MOD_DOMAIN(2), MOD_DOMAIN(3)),
    }

    @pytest.mark.parametrize('use_dat_value', (True, False))
    def test_enums(self, rr_temp_dir, use_dat_value):
        rr = dat.RelationalReader(
            path_or_ggpk=rr_temp_dir,
            read_options={
                'specification': load(os.path.join(
                    spec_dir, 'rr_test.py'
                )),
                'use_dat_value': use_dat_value,
            },
        )
        for column, values in self.enums_expected.items():
            for i, row in enumerate(rr['Main.dat']):
                assert row[column] == values[i], 'Testing against expected enum'

    def test_getitem(self, rr_instance):
        assert rr_instance['Main.dat'] == \
               rr_instance.get_file('Data/Main.dat').reader