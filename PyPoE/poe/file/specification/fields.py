"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/file/specification/fields.py                           |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Data fields to be used in the specifications

Agreement
===============================================================================

See PyPoE/LICENSE

General Information
===============================================================================

About .dat files.
-------------------------------------------------------------------------------

.dat files are basically a binary database. They have a fixed width data
section and a variable width data section.

The header of the file contains the number of rows and the size of the rows,
so we can determine with certainty how large it would be. Together this is
fixed size data section.

The variable size section starts with a magic keyword 0xBBbbBBbbBBbbBB and
then is just filled with the data (which can not be read properly without
understanding the fixed width section - all data is referenced).

Note that some of the .dat files have been purposefully stripped of their
rows and data so they can not be read.


Style Guide
-------------------------------------------------------------------------------
Fields should be named with a proper name. CamelCase should be used on the all
the keys.

Related values should be have a prefix which is separated by a underscore.
For example, if there are two columns one of which provides a list of Ids and
the other provides a list of Values, you'd do something like:

* MyValue_Ids
* MyValue_Values

If it is unknown what the field does, name it after the datatype and replace N:
    Index<N>
        for unknown strings (ref|string)
    Unknown<N>
        for unknown values (byte, short, int, long & unsigned variants)
    Data<N>
        for unknown data (ref|list)
    Flag<N>
        for unknown boolean values (bool)
    Key<N>
        for unknown keys (likely to be a key, ulong type)

If it is known what the field does
    <WhatAmI>
        Use a good name. For example ItemLevel if the key is item level
    <OtherDat>Key
        If you know this field references another dat file use this naming;
        for example WorldAreasKey
    <OtherDat>Keys
        Similar to above, but use this for a list of keys
    <EXT>File
        Use this for a ref|string that contains a file path
        Replace <EXT> with the extension of the file, for example:
        DDSFile for a file with the .dds extension
    Id
        Use this for primary key value. Usually also the first value in a row


Editing guide
-------------------------------------------------------------------------------
New file:
Use int or uint types if you have a new .dat and fill it up until the data
size (pad with short/byte if necessary).

Finding out the proper type:

- an int field followed by a all 0 field is usually an ulong reference key

  - this also applies to lists, i.e. a ref|list|uint with each entry followed
    by a zero is probably a ref|list|ulong instead (and a key).

- an int field with ever increasing numbers not larger then data section is
  a pointer to the data section. If preceeded by a value > 0, it may be a
  list; otherwise it may be a string

  - if the value is increasing but out of bounds, the int may be at the wrong
    position, i.e. preceeded by byte(s) or short.

- list and strings may be empty

  - multiple empty lists may point at the same position in the data
  - empty strings will still take up 4 bytes of space (the zero terminator)

- if you see there are gaps or overlapping values in data section, considering
  increasing/decreasing the type accordingly (i.e. from ref|uint to ref|ulong)

  - if that doesn't help, the key might not be a reference

Finding out the proper meaning:

- First of all, mind the game! A lot can be deducted from knowing the game
  well.
- Keep the name of the file in mind;

  - it's common for files to have references to other related files (i.e. a
    xxxMasterMission is most likely to contain a reference to Master.dat
    somewhere)
  - the values will usually relate the file name obviously; i.e. will contain
    stats/mods for the items, their visuals, and so on

    - often these are supplied as keys (or Key1, Key2, Value1, Value2 ...)

- Look at the minimum and maximum of the values; often they only have a
  specific range which can hint at their meaning

  - 0 to 100 can often be Level related
  - Values with a base line of 1000 (or more rarely 100) above 0 are often
    spawn chance or weighting related.

- Values often appear as pairs, for example:

  - Spawn Weight

    - ref|list|ulong -> Tags.dat keys
    - ref|list|int -> Values

  - Stats

   - ulong -> Stat key
   - int -> Value (sometimes 2x for min/max rollable range)


Regarding references/keys to other files:

- Generally for their type:

  - ulong if referencing another file
  - uint if referencing the same file
  - None (0xFEFEFEFE) is a pretty solid giveaway

- Offsets:

  - Usually the other dat file, starting at 0 (offset not needed, default)
  - If the file has been blanked or if it referencing a specific column,
    often it uses offset 1

- Finding out what they reference to:

  - if the keys is very small it's likely to refer to a file with little
    entries (like difficulty, master, etc), like wise for big keys.
  - based on what the file does related files can often be deducted
  - references to Tags.dat and Mods.dat are very common

- if possible, test the references out and see if they make sense

Lastly, I suppose you could also try to reverse engineer the PathOfExile.exe
and see whether you find any structs for the files.

Documentation
===============================================================================

.. autoclass:: Specification

.. autoclass:: File

.. autoclass:: Field

.. autoclass:: VirtualField

"""

# =============================================================================
# Imports
# =============================================================================

# Python
from collections import OrderedDict
from typing import Tuple

# 3rd-party

# self
from PyPoE.poe import constants
from PyPoE.shared.mixins import ReprMixin
from PyPoE.poe.file.specification.errors import SpecificationError

# =============================================================================
# Globals
# =============================================================================

__all__ = ['Specification', 'File', 'Field', 'VirtualField']

# =============================================================================
# Classes
# =============================================================================


class _Common:
    def as_dict(self) -> dict:
        """
        Returns
        -------
        dict
            Returns itself as dictionary without any class references
        """
        return {k: getattr(self, k) for k in self.__slots__}


class Specification(dict):
    """
    Specification file
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self):
        """
        Performs validation on the current data in the specification

        Raises
        ------
        SpecificationError
            Raised when any errors occur.

            See :py:mod:`PyPoE.poe.file.specification.errors` for details
            on errors and error codes.

        """
        for file_name, file in self.items():
            for field_name, field in file.fields.items():
                # Validation
                if field.key:
                    if field.key not in self:
                        raise SpecificationError(
                            SpecificationError.ERRORS.INVALID_FOREIGN_KEY_FILE,
                            '%(dat_file)s->%(field)s->key: %(other)s is not in '
                            'specification' % {
                                'dat_file': file_name,
                                'field': field_name,
                                'other': field.key,
                            }
                        )

                    other_key = field['key_id']
                    if other_key and other_key not in self[field.key]['fields']:
                        raise SpecificationError(
                            SpecificationError.ERRORS.INVALID_FOREIGN_KEY_ID,
                            '%(dat_file)s->%(field)s->key_id: %(other)s->'
                            '%(other_key)s not in specification' % {
                                'dat_file': file_name,
                                'field': field_name,
                                'other': field.key,
                                'other_key': other_key,
                            }
                        )

                if field.enum:
                    if field.key:
                        raise SpecificationError(
                            SpecificationError.ERRORS.INVALID_ARGUMENT_COMBINATION,
                            '%(dat_file)s->%(field)s->enum: Either key or enum can '
                            'be specified but never both.' % {
                                'dat_file': file_name,
                                'field': field_name,
                            }
                        )
                    if not hasattr(constants, field.enum):
                        raise SpecificationError(
                            SpecificationError.ERRORS.INVALID_ENUM_NAME,
                            '%(dat_file)s->%(field)s->enum: Invalid constant enum '
                            '""%(enum)s" specified'
                            % {
                                'dat_file': file_name,
                                'field': field_name,
                                'enum': field.enum,
                            }
                        )

            for field_name, virtual_field in file.virtual_fields.items():
                # Validation
                if field_name in file.fields:
                    raise SpecificationError(
                        SpecificationError.ERRORS.VIRTUAL_KEY_DUPLICATE,
                        '%(dat_file)s->virtual_fields->%(field)s use the same name '
                        'as a key specified in %(dat_file)s->fields' %
                        {
                            'dat_file': file_name,
                            'field': field_name,
                        }
                    )

                if not virtual_field.fields:
                    raise SpecificationError(
                        SpecificationError.ERRORS.VIRTUAL_KEY_EMPTY,
                        '%(dat_file)s->virtual_fields->%(field)s->fields is empty' %
                        {
                            'dat_file': file_name,
                            'field': field_name,
                        }
                    )

                for other_field in virtual_field.fields:
                    if other_field not in file.fields and \
                                    other_field not in file.virtual_fields:
                        raise SpecificationError(
                            SpecificationError.ERRORS.VIRTUAL_KEY_INVALID_KEY,
                            '%(dat_file)s->virtual_fields->%(field)s->fields: '
                            'Field "%(other_field)s" does not exist' %
                            {
                                'dat_file': file_name,
                                'field': field_name,
                                'other_field': other_field,
                            }
                        )
                    if virtual_field.zip and other_field in file.fields and \
                            not file.fields[other_field].type.startswith(
                                'ref|list'):
                        raise SpecificationError(
                            SpecificationError.ERRORS.VIRTUAL_KEY_INVALID_DATA_TYPE,
                            '%(dat_file)s->virtual_fields->%(field)s->zip: The zip '
                            'option requires "%(other_field)s" to be a list' %
                            {
                                'dat_file': file_name,
                                'field': field_name,
                                'other_field': other_field,
                            }
                        )

    def as_dict(self) -> dict:
        """
        Returns
        -------
        dict
            Returns itself as dictionary without any class references
        """
        return {
            k: v.as_dict() for k, v in self.items()
        }


class File:
    """
    Represents a single file in the specification.

    Parameters
    ----------
    fields : OrderedDict
        OrderedDict containing the field name as key and a :class:`Field`
        instance as value
    virtual_fields : OrderedDict
        OrderedDict containing the field name as key and a
        :class:`VirtualField` instance as value
    columns :  OrderedDict
        Shortened list of columns excluding intermediate columns
    columns_zip :  OrderedDict
        Shortened list of columns excluding zipped columns
    columns_all :  OrderedDict
        Complete list of columns, including all intermediate and virtual columns
    columns_data :  OrderedDict
        List of all columns directly derived from the data
    columns_unique:  OrderedDict
        List of all unique columns (which are also considered indexable)
    """

    __slots__ = [
        'fields',
        'virtual_fields',
        'columns',
        'columns_all',
        'columns_data',
        'columns_unique',
        'columns_zip',
    ]

    def __init__(self,
                 fields: Tuple['Field', ...] = None,
                 virtual_fields: Tuple['VirtualField', ...] = None
                 ):
        """
        Parameters
        ----------
        fields
            OrderedDict containing the field name as key and a :class:`Field`
            instance as value
        virtual_fields
            OrderedDict containing the field name as key and a
            :class:`VirtualField` instance as value
        """
        if fields is None:
            fields = OrderedDict()
        else:
            fields = OrderedDict(((field.name, field) for field in fields))
        self.fields = fields
        if virtual_fields is None:
            virtual_fields = OrderedDict()
        else:
            virtual_fields = OrderedDict(((field.name, field) for field in virtual_fields))
        self.virtual_fields = virtual_fields

        # Set utility columns from the given data
        self.columns = OrderedDict()
        self.columns_unique = OrderedDict()

        for field_name, field in fields.items():
            self.columns[field_name] = None
            if field.unique:
                self.columns_unique[field_name] = None

        self.columns_all = OrderedDict(self.columns)
        self.columns_data = OrderedDict(self.columns)
        self.columns_zip = OrderedDict(self.columns)

        if virtual_fields:
            delete = set()
            delete_zip = set()

            for field_name, virtual_field in virtual_fields.items():
                self.columns[field_name] = None
                self.columns_all[field_name] = None
                self.columns_zip[field_name] = None
                if virtual_field.zip:
                    delete_zip.update(virtual_field.fields)

                delete.update(virtual_field.fields)

            for item in delete:
                try:
                    del self.columns[item]
                # TODO: This can happen when virtual keys are invalid, move from validator to here?
                except KeyError:
                    pass

            for item in delete_zip:
                del self.columns_zip[item]

    def __getitem__(self, item):
        return getattr(self, item)

    def as_dict(self) -> dict:
        """
        Returns
        -------
        dict
            Returns itself as dictionary without any class references
        """
        out = {}
        for k in self.__slots__:
            v = getattr(self, k)
            if k in ('fields', 'virtual_fields'):
                out[k] = OrderedDict([(ok, ov.as_dict()) for ok, ov in v.items()])
            else:
                out[k] = v
        return out


class Field(_Common, ReprMixin):
    """
    Fields instances are used to tie a specific set of information to a
    column field.

    **Type Syntax**

    I've mostly adapted the Syntax from VisualGGPK2, but it may be subject to
    change to the python struct data types; for now they'll stay since bool is
    most certainly more readable then ?.

    Base types:
        bool
            8 bit integer value, first bit is 1 or 0 (cocered to True/False)
        byte
            8 bit integer value, signed
        ubyte
            8 bit integer value, unsigned
        short
            16 bit integer value, signed
        ushort
            16 bit integer value, unsigned
        int
            32 bit integer value, signed
        uint
            32 bit integer value, unsigned
        long
            64 bit integer value, signed
        ulong
            64 bit integer value, unsigned
        float
            32 bit floating point value, single precision
        double
            64 bit floating point value, double precision

    Variable/Pointer types:
        ref|<other>
            32 bit value, unsigned

            a pointer to the data section
        ref|list|<other>
            two 32 bit values, unsigned

            first value determines the size of the list

            second value is the pointer to the data section
        ref|string
            just like a normal reference, but it will parse as null terminated
            utf16_le encoded string

    """
    __slots__ = [
        'type', 'key', 'key_id', 'key_offset', 'enum', 'unique', 'file_path',
        'file_ext', 'display', 'display_type', 'description'
    ]

    def __init__(self,
                 type: str,
                 key: str = None,
                 key_id: str = None,
                 key_offset: int = 0,
                 enum: str = None,
                 unique: bool = False,
                 file_path: bool = False,
                 file_ext: str = None,
                 display: str = None,
                 display_type: str = None,
                 description: str = None,
                 name: str = None):
        """
        All parameters except type are optional.

        Parameters
        ----------
        type
            Required. The type. See Type Syntax above
        key
            Name of the .dat file that is reference. Must exist in the
            specification.
        key_id
            Name of the column in the other dat file that is referenced.

            This should be specified together with key, alone it does nothing.

            If the column is indexed (i.e. unique), this is fast.
        key_offset
            Offset at which the key of the other file starts.
            This generally useful when it's a key_id value, but the keys are
            numbered rowid+1 for example (so offset would be 1).

            This should be specified together with key, alone it does nothing.
        enum
            Enum from :py:mod:`PyPoE.poe.constants` to use for this field
        unique
            Whether each value contained in this file is unique.
        file_path
            Whether the entry is a file path. Please note this should also be
            set if there is no file extension.
        file_ext
            The extension of the file, if any.

            Most of the time this should be set together with file_path, unless
            there is no path given.
        display
            String to show instead of the field id when displaying this
        display_type
            Python formatter syntax for outputting the value
        description
            Description of what this field does
        name
            Name of the field
        """
        self.type = type
        self.key = key
        self.key_id = key_id
        self.key_offset = key_offset
        self.enum = enum
        self.unique = unique
        self.file_path = file_path
        self.file_ext = file_ext
        self.display = display
        self.display_type = display_type
        self.description = description
        self.name = name

        if display_type is None:
            if type == 'float':
                self.display_type = '{0:.6f}'
            else:
                self.display_type = '{0}'
        else:
            self.display_type = display_type

    def __getitem__(self, item):
        return getattr(self, item)


class VirtualField(_Common):
    """
    Virtual fields are based off other Field instances and provide additional
    convenience options such as grouping certain fields together.
    """
    __slots__ = ['name', 'fields', 'zip']

    def __init__(self,
                 name: str,
                 fields: Tuple[str, ...],
                 zip: bool = False):
        """

        Parameters
        ----------
        name

        fields
            List of fields to coerce into one field.
            All fields must be exist, but they can be either a regular or
            virtual field or combination of.
        zip
             Whether to zip the fields together.
             This option requires each of the referenced fields to be a list.
        """
        self.name = name
        self.fields = fields
        self.zip = zip

    def __getitem__(self, item):
        return getattr(self, item)
