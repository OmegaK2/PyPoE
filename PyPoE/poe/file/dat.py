"""
Path     PyPoE/poe/file/dat.py
Name     Dat Reader Tool
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO

Toolkit for reading & writing GGG .dat files.

.dat files can be found in Data/ and are read by the class DatFile.
Unfortunately, there is no magic keyword for identifying the GGG .dat format,
so advise caution when trying to read dat files.

The GGG .dat format uses a fixed-width table and a variable-length data section.
In the fixed-width table, the number of rows is defined, however, the data
format stored has to be reverse-engineered and is currently not stored in the
file itself.
The data is a continuous amount of binary data; reading values form there is
generally done by pointers (int) or list pointers (size, int) from the
table-data.

A list of default specification is included with PyPoE; to reload those or load
other specifications, load_spec may be used.


AGREEMENT

See PyPoE/LICENSE


TODO

write?
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import struct
import os
import multiprocessing
from io import BytesIO

# 3rd Party Library
import configobj
import validate

# Library imports
from PyPoE import DAT_SPECIFICATION, DAT_SPECIFICATION_CONFIGSPEC

# =============================================================================
# Globals
# =============================================================================

_default_spec = None

# =============================================================================
# Classes
# =============================================================================

class SpecificationError(ValueError):
    pass

class DatValue(object):
    """
    Representation of a value found in a dat file.

    Dev notes:
    Must keep the init
    """

    # Very important to cut down the cost of class creation
    # In some dat files we may be creating millions of instances, simply using
    # slots can make a significant difference (~35% speedup)
    __slots__ = [
        'value', 'size', 'offset', 'parent', 'specification', 'children',
        'child',
    ]

    def __init__(self, value=None, offset=None, size=None, parent=None, specification=None):
        self.value = value
        self.size = size
        self.offset = offset
        self.parent = parent
        self.specification = specification
        self.children = None
        self.child = None

    def __repr__(self):
        #TODO: iterative vs recursive?
        if self.is_pointer:
            return repr(self.child)
        elif self.is_list:
            return repr([repr(dv) for dv in self.children])
        else:
            return 'DatValue(' + repr(self.value) +')'

    # Properties

    def _get_data_size(self):
        if self.is_list:
            if self.children:
                size = self.children[0].size * self.value[0]
            else:
                size = 0
        elif self.is_pointer:
            size = self.child.size
        else:
            raise TypeError('Only supported on data (pointer or list) DatValue instances')
        return size

    def _get_data_start_offset(self):
        if self.is_list:
            return self.value[1]
        elif self.is_pointer:
            return self.value
        else:
            raise TypeError('Only supported on data (pointer or list) DatValue instances')

    def _get_data_end_offset(self):
        return self._get_data_start_offset() + self._get_data_size()

    def _is_data(self):
        return self.parent is not None

    def _has_data(self):
        return self.is_list or self.is_pointer

    def _is_list(self):
        return self.children is not None

    def _is_pointer(self):
        return self.child is not None

    def _is_parsed(self):
        return not isinstance(self.value, bytes)

    data_size = property(fget=_get_data_size)
    data_start_offset = property(fget=_get_data_start_offset)
    data_end_offset = property(fget=_get_data_end_offset)
    is_data = property(fget=_is_data)
    has_data = property(fget=_has_data)
    is_list = property(fget=_is_list)
    is_pointer = property(fget=_is_pointer)
    is_parsed = property(fget=_is_parsed)

    # Public

    def get_value(self):
        #TODO: iterative vs recursive?
        if self.is_pointer:
            return self.child.get_value()
        elif self.is_list:
            return [dv.get_value() for dv in self.children]
        else:
            return self.value

class RecordList(list):

    __slots__ = ['parent', 'rowid']

    def __init__(self, parent, rowid):
        list.__init__(self)
        self.parent = parent
        self.rowid = rowid

    def _get_column_index(self, item):
        for i in range(0, len(self.parent.table_columns)):
             if self.parent.table_columns[i].name == item:
                return i
        raise IndexError("%s not in list" % item)

    def __getitem__(self, item):
        if isinstance(item, str):
            value = list.__getitem__(self, self._get_column_index(item))
            if isinstance(value, DatValue):
                value = value.get_value()
            return value
        return list.__getitem__(self, item)

    def __repr__(self):
        stuff = ["{%s: %s}" %  (self.parent.table_columns[i].name, self[i]) for i in range(0, len(self))]
        return '[{%s}]' % ', '.join(stuff)
    '''def find_all(self, key, value):
        row_index = self._get_column_index(key)
        values = []
        for row in self:
            if row[row_index] == value:
                values.append(value)
        return values'''

    def keys(self):
        return [s.name for s in self.parent.table_columns]

class DatFile(object):
    """
    
    Variables:
    data_parsed:
    table_data:
    table_length:
    table_record_length:
    table_rows:
    """
    _table_offset = 4
    _cast_table = {
        'bool': ['?', 1],
        'byte': ['b', 1],
        'ubyte': ['B', 1],
        'short': ['h', 2],
        'ushort': ['H', 2],
        'int': ['i', 4],
        'uint': ['I', 4],
        'long': ['q', 8],
        'ulong': ['Q', 8],
    }
    _data_magic_number = b'\xBB\xbb\xBB\xbb\xBB\xbb\xBB\xbb'
    
    def __init__(self, file_name, *args, read_file=None, read_raw=None):
        self._file_name = file_name
        self.data_parsed = []
        self.data_offset = 0
        self.file_length = 0
        self._file_raw = None
        self.table_data = []
        self.table_columns = []
        self.table_length = 0
        self.table_record_length = 0
        self.table_rows = 0

        if read_file and read_raw:
            raise ValueError('Only one of read_file and read_raw should be set.')

        if read_file:
            self.read_from_file(read_file)
        elif read_raw:
            self.read_from_raw(read_raw)

    def __iter__(self):
        return iter(self.table_data)

    def _get_cast_type(self, caststr):
        size = None
        cast = None
        remainder = ''
        if caststr in self._cast_table:
            cast_type = 1
            size = self._cast_table[caststr][1]
            cast = self._cast_table[caststr][0]
        elif caststr == 'string':
            cast_type = 2
        elif caststr.startswith('ref|list|'):
            cast_type = 3
            size = 8
            cast = 'II'
            remainder = caststr[9:]
        elif caststr.startswith('ref|'):
            cast_type = 4
            size = 4
            cast = 'I'
            remainder = caststr[4:]
        return remainder, (cast_type, size, cast)

    def _cast_from_spec(self, specification, casts, parent=None, offset=None, data=None, queue_data=None):
        #cast = casts[0]

        if casts[0][0] == 1:
            ivalue = data[0] if data else struct.unpack('<' + casts[0][2], self._file_raw[offset:offset+casts[0][1]])[0]
            
            if ivalue in (-0x1010102, 0xFEFEFEFE, -0x101010101010102, 0xFEFEFEFEFEFEFEFE):
                ivalue = -1
            
            value = DatValue(ivalue, offset, casts[0][1], parent, specification)
        elif casts[0][0] == 2:
            # Beginning of the sequence, +1 to adjust for it
            offset_new = self._file_raw.find(b'\x00\x00\x00\x00', offset)
            # Account for 0 size strings
            if offset == offset_new:
                string = ''
            else:
                # It's possible that a string ends in \x00 and the next starts
                # with \x00
                # UTF-16 must be at least a multiple of 2
                while ((offset_new-offset) % 2):
                    offset_new = self._file_raw.find(b'\x00\x00\x00\x00', offset_new+1)
                string = self._file_raw[offset:offset_new].decode('utf-16')
            # Store the offset including the null terminator
            value = DatValue(string, offset, offset_new-offset+4, parent, specification)

        elif casts[0][0] >= 3:
            data = data if data else struct.unpack('<' + casts[0][2], self._file_raw[offset:offset+casts[0][1]])
            data_offset = data[-1] + self.data_offset

            # Instance..
            value = DatValue(data[0] if casts[0][0] == 4 else data, offset, casts[0][1], parent, specification)

            if casts[0][0] == 3:
                value.children = []
                for i in range(0, data[0]):
                    '''if offset < self._data_offset_current:
                        print(self._data_offset_current, offset)
                        raise SpecificationError("Overlapping offset for cast %s:%s" % (parent.is_list, casts[0]))'''
                    value.children.append(self._cast_from_spec(specification, casts[1:], value, data_offset+i*casts[1:][0][1]))
            elif casts[0][0] == 4:
                value.child = self._cast_from_spec(specification, casts[1:], value, data_offset)
            self.data_parsed.append(value)
            
        # TODO
        #if parent:
        #    self._data_offset_current = offset
        #    self.data_parsed.append(value)
            
        return value

    def _process_row(self, rowid):
        offset = 4 + rowid * self.table_record_length
        row_data = RecordList(self, rowid)
        data_raw = self._file_raw[offset:offset+self.table_record_length]
        if self.tempspec:
            # Unpacking the entire row in one go will help breaking down the
            # function calls significantly
            row_unpacked = struct.unpack(self.row_cast, data_raw)
            i = 0
            for spec, casts in self.tempspec:
                if casts[0][0] == 3:
                    cell_data = row_unpacked[i:i+2]
                    i += 1
                else:
                    cell_data = (row_unpacked[i], )
                row_data.append(self._cast_from_spec(spec, casts, data=cell_data, offset=offset))
                offset += casts[0][1]
                i += 1
        else:
            unparsed = DatValue(value=data_raw, offset=offset, size=self.table_record_length)
            row_data.append(unparsed)
            offset += self.table_record_length

        return row_data

    def _process_return_data(self, data):
        self.table_data.append(data[0])
        self.data_parsed += data[1]

    def print_data(self):
        for row in d.table_data:
            print('Row: %s' % row.rowid)
            for k in row.keys():
                v = row[k]
                print('|- %s: %s' % (k, v))
    
    def read_from_file(self, path, specification=None):
        file_path = os.path.join(path, self._file_name)
        with open(file_path, mode='br') as datfile:
            raw = datfile.read()
        self.read_from_raw(raw, specification)
    
    def read_from_raw(self, raw, specification=None):
        """
        Specification as _ordered_ dictionary key:value format
        """
        # TODO consider memory issues for saving raw contents
        if isinstance(raw, bytes):
            self._file_raw = raw
        elif isinstance(raw, BytesIO):
            self._file_raw = raw.read()
        else:
            raise TypeError('Raw must be bytes or BytesIO instance, got %s' %
                            type)

        if specification is None:
            if self._file_name in _default_spec:
                specification = _default_spec[self._file_name]
        else:
            specification = specification[self._file_name]

        self.specification = specification

        # Jump to last byte to get length
        self.file_length = len(self._file_raw)

        self.data_offset = self._file_raw.find(self._data_magic_number)
        self._data_offset_current = 0

        if self.data_offset == -1:
            raise ValueError("Did not find data magic number")

        self.table_rows = struct.unpack('<I', self._file_raw[0:4])[0]
        self.table_length = self.data_offset - self._table_offset
        if self.table_rows > 0:
            self.table_record_length = self.table_length//self.table_rows
        elif self.table_rows == 0 and self.table_length == 0:
            self.table_record_length = 0
        else:
            #TODO
            raise ValueError("WTF")

        self.table_data = []
        self.table_columns = []

        # Parse the specification in a way that's faster to access
        self.tempspec = []
        if specification:
            self.row_cast = []
            size = 0
            for key in specification['fields']:
                k = specification['fields'][key]
                self.table_columns.append(k)
                casts = []
                remainder = k['type']
                while remainder:
                    remainder, cast_type = self._get_cast_type(remainder)
                    casts.append(cast_type)
                size += casts[0][1]

                self.tempspec.append((k, casts))
                self.row_cast.append(casts[0][2])

            if size != self.table_record_length:
                raise SpecificationError('Row size %s vs actual size %s' % (size, self.table_record_length))

            self.row_cast = '<' + ''.join(self.row_cast)

        else:
            s = configobj.Section(None, 0, None)
            s.name = 'Unparsed'
            self.table_columns.append(s)

        # Prepare data section
        self.data_parsed = list()

        for i in range(0, self.table_rows):
            self.table_data.append(self._process_row(i))

        '''with multiprocessing.Pool() as pool:
            pool.map(self._process_row, range(0, self.table_rows))'''

        '''try:
            self.table_data.append(q_table_data.get())
        except multiprocessing.queue.empty:
            pass'''

    def export_to_html(self, export_table=True, export_data=False):
        outstr = []
        if export_table:
            outstr.append('<table>')

            outstr.append('<thead>')
            outstr.append('<tr>')
            outstr.append('<th>')
            outstr.append('ROW')
            outstr.append('</th>')
            for key in self.specification['fields']:
                outstr.append('<th>')
                disp = self.specification['fields'][key]['display']
                if not disp:
                    disp = key
                outstr.append(disp)
                outstr.append('</th>')
            outstr.append('</tr>')
            outstr.append('</thead>')

            outstr.append('<tbody>')
            for row in self.table_data:
                outstr.append('<tr>')
                outstr.append('<th>')
                outstr.append(str(row.rowid))
                outstr.append('</th>')
                for dv in row:
                    outstr.append('<td>')
                    outstr.append(str(dv.get_value()))
                    outstr.append('</td>')
                outstr.append('</tr>')
            outstr.append('</tbody>')

            outstr.append('</table>')
        if export_data:
            outstr.append('<table>')

            outstr.append('<thead>')
            outstr.append('<tr>')
            outstr.append('</tr>')
            outstr.append('</thead>')

            outstr.append('<tbody>')
            outstr.append('</tbody>')

            outstr.append('</table>')
        return ''.join(outstr)

def load_spec(path=None):
    if path is None:
        path = DAT_SPECIFICATION
    spec = configobj.ConfigObj(infile=path, configspec=DAT_SPECIFICATION_CONFIGSPEC)
    spec.validate(validate.Validator())

    return spec

def reload_default_spec():
    global _default_spec
    _default_spec = load_spec()

# =============================================================================
# Init
# =============================================================================

reload_default_spec()
        
if __name__ == '__main__':
    from line_profiler import LineProfiler
    profiler = LineProfiler()
    #profiler.add_function(DatValue.__init__)
    profiler.add_function(DatFile._cast_from_spec)
    profiler.add_function(DatFile._process_row)
    #profiler.add_function(DatFile.read_from_file)
    #profiler.add_function(DatFile.read_from_raw)


    #profiler.run("d = DatFile('GrantedEffects.dat', read_file='C:/Temp/Data')")
    #profiler.print_stats()

    #print(d.table_data)
    import cProfile
    #cProfile.run("d = DatFile('GrantedEffectsPerLevel.dat', read_file='C:/Temp/Data')")

