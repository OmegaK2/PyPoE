"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/file/dat.py                                            |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================


Agreement
===============================================================================

See PyPoE/LICENSE


Documentation
===============================================================================
"""

# =============================================================================
# Imports
# =============================================================================

# python
import struct
import os
import pprint
from collections import defaultdict
from enum import IntEnum
from tempfile import TemporaryDirectory

# 3rd party
from fnvhash import fnv1a_64

try:
    import cffi
except ImportError:
    cffi = None

# self
from PyPoE.poe.file.shared import AbstractFileReadOnly

# =============================================================================
# Setup
# =============================================================================

if cffi:
    ffi = cffi.FFI()
    ffi.cdef("""int Ooz_Decompress(uint8_t const* src_buf, int src_len, 
            uint8_t* dst, size_t dst_size, int, int, int, uint8_t*, size_t, 
            void*, void*, void*, size_t, int);""")
    try:
        ooz = ffi.dlopen(r'C:\Code\Scripts\PoE\ooz\libooz.dll')
    except OSError:
        cffi = None
        ooz = None
else:
    ooz = None

# =============================================================================
# Classes
# =============================================================================


class ENCODE_TYPES_HEX(IntEnum):
    NONE = 0xCC07
    LZHLW = 0x8C00
    LZNIB = 0x8C01
    LZB16 = 0x8C02
    LZBLW = 0x8C03
    LZA = 0x8C04
    LZNA = 0x8C05
    KRAKEN = 0x8C06
    LZH = 0x8C07
    # 8, 9?
    MERMAID = 0x8C0A
    SELKIE = MERMAID
    HYDRA = MERMAID

    BITKNIT = 0x8C0B
    LEVIATHAN = 0x8C0C


class ENCODE_TYPES(IntEnum):
    LZH = 0
    LZHLW = 1
    LZNIB = 2
    NONE = 3
    LZB16 = 4
    LZBLW = 5
    LZA = 6
    LZNA = 7
    KRAKEN = 8
    MERMAID = 9
    BITKNIT = 10
    SELKIE = 11
    HYDRA = 12
    LEVIATHAN = 13


class Bundle(AbstractFileReadOnly):
    def __init__(self):
        self.encoder = None
        self.unknown = None
        self.size_decompressed = None
        self.size_compressed = None
        self.entry_count = None
        self.chunk_size = None
        self.unknown3 = None
        self.unknown4 = None
        self.unknown5 = None
        self.unknown6 = None
        self.chunks = None
        self.data = {}
        self.is_decompressed = defaultdict(lambda: False)

    def read(self, raw):
        if isinstance(raw, bytes):
            self._file_raw = raw
        elif isinstance(raw, BytesIO):
            self._file_raw = raw.read()
        else:
            raise TypeError('Raw must be bytes or BytesIO instance, got %s' %
                            type)

        self.uncompressed_size, self.data_size, self.head_size = \
            struct.unpack_from('<III', raw, offset=0)
        offset = 12

        data = struct.unpack_from('<IIQQIIIIII', raw, offset=offset)
        offset += 48

        self.encoder = ENCODE_TYPES(data[0])
        self.unknown = data[1]
        self.size_decompressed = data[2]
        self.size_compressed = data[3]
        self.entry_count = data[4]
        self.chunk_size = data[5]
        self.unknown3 = data[6]
        self.unknown4 = data[7]
        self.unknown5 = data[8]
        self.unknown6 = data[9]

        self.chunks = struct.unpack_from(
            '<%sI' % self.entry_count, raw, offset=offset)
        offset += self.entry_count*4

        for i in range(0, self.entry_count):
            offset2 = offset + self.chunks[i]
            self.data[i] = raw[offset:offset2]

            offset = offset2

    def decompress(self, start=0, end=None):
        if not self.data:
            raise ValueError()

        if end is None:
            end = self.entry_count

        last = self.entry_count - 1
        if ooz:
            for i in range(start, end):
                if self.is_decompressed[i]:
                    continue

                if i != last:
                    size = self.chunk_size
                else:
                    size = self.size_decompressed % self.chunk_size

                out = ffi.new('uint8_t[]', size)
                rtrcode = ooz.Ooz_Decompress(
                    self.data[i],  # src_buff
                    len(self.data[i]),  # src_len
                    out,  # dst
                    size,  # dst_size
                    0,
                    0,
                    0,
                    ffi.cast('uint8_t *', 0),
                    0,
                    ffi.cast('void *', 0),
                    ffi.cast('void *', 0),
                    ffi.cast('void *', 0),
                    0,
                    0,
                )

                if rtrcode == 0:
                    raise ValueError('Decode error - returned 0 bytes')

                self.data[i] = ffi.buffer(out)
                self.is_decompressed[i] = True
        else:
            tempdir = 'C:/temp/x/'
            with TemporaryDirectory() as tempdir:
                for i in range(start, end):
                    if self.is_decompressed[i]:
                        continue

                    fn = '%s/chunk%s' % (tempdir, i)

                    with open('%s.in' % fn, 'wb') as f:
                        if i != last:
                            size = 262144
                        else:
                            size = self.size_decompressed % 262144
                        f.write(struct.pack('<Q', size))
                        f.write(self.data[i])

                    os.system('ooz -d %(fn)s.in %(fn)s.out' % {'fn': fn})

                    with open('%s.out' % fn, 'rb') as f:
                        self.data[i] = f.read()
                    self.is_decompressed[i] = True


class PATH_TYPES(IntEnum):
    DIR = 1
    FILE = 2


class Index(Bundle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bundles = {}
        self.files = {}
        self.directories = {}
        self.directory_data = None

    def get_dir_info(self, path):
        return self.files[self.get_hash(path, type=PATH_TYPES.DIR)]

    def get_file_info(self, path):
        return self.files[self.get_hash(path, type=PATH_TYPES.FILE)]

    def get_hash(self, path, type=None):
        if isinstance(path, str):
            path = path.encode('utf-8')
        elif not isinstance(path, bytes):
            raise TypeError('path must be a string')

        if path.endswith(b'/'):
            if type is None:
                type = PATH_TYPES.DIR
            path = path.strip(b'/')
        # If type wasn't set before, assume this is a file
        if type == PATH_TYPES.FILE or type is None:
            path = path.lower()
        path += b'++'

        return fnv1a_64(path)

    def read(self, raw):
        super().read(raw)
        self.decompress()
        raw = b''.join(self.data.values())

        bundle_count = struct.unpack_from('<I', raw)[0]
        offset = 4

        for i in range(0, bundle_count):
            bundle = {}

            name_length = struct.unpack_from('<I', raw, offset=offset)[0]
            offset += 4

            bundle['name'] = struct.unpack_from(
                '%ss' % name_length, raw, offset=offset)[0]
            offset += name_length

            bundle['size'] = struct.unpack_from('<I', raw, offset=offset)[0]
            offset += 4

            self.bundles[i] = bundle

        file_count = struct.unpack_from('<I', raw, offset=offset)[0]
        offset += 4

        for i in range(0, file_count):
            data = struct.unpack_from('<QIII', raw, offset=offset)
            offset += 20

            self.files[data[0]] = {
                'bundle': self.bundles[data[1]],
                'file_offset': data[2],
                'file_size': data[3],
            }

        count = struct.unpack_from('<I', raw, offset=offset)[0]
        offset += 4
        for i in range(0, count):
            data = struct.unpack_from('<QIII', raw, offset=offset)
            offset += 20

            self.directories[data[0]] = {
                'offset': data[1],
                'size': data[2],
                'unknown2': data[3],
                'paths': None,
            }

        directory_bundle = Bundle()
        directory_bundle.read(raw[offset:])
        directory_bundle.decompress()
        self.directory_data = b''.join(directory_bundle.data.values())

        for path in self.directories.values():
            path['paths'] = self._make_paths(
                self.directory_data[path['offset']:path['offset'] + path['size']]
            )

    def _make_paths(self, raw):
        temp = []
        paths = []
        base = False
        offset = 0
        rawlen = len(raw)-4
        while offset <= rawlen:
            index = struct.unpack_from('<I', raw, offset=offset)[0]
            offset += 4

            if index == 0:
                base = not base
                if base:
                    temp = []
                continue
            else:
                index -= 1

            end_offset = raw.find(b'\x00', offset)
            string = raw[offset:end_offset]
            offset = end_offset+1

            try:
                string = temp[index] + string
            except IndexError:
                pass  # this is a new string
                pass  # this is a new string

            if base:
                temp.append(string)
            else:
                paths.append(string)

        return paths

if __name__ == '__main__':
    ind = Index()
    with open('C:/Temp/Bundles2/_.index.bin', 'rb') as f:
        ind.read(f.read())

    print(ind['Metadata/minimap_colours.txt'])

    '''b.decompress()
    for var in dir(b):
        if var.startswith('_'):
            continue
        print(var, getattr(b, var))
    '''

    #pprint.pprint(Index._make_paths(None, b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00Art/Microtransactions/spell/arc/crimson/models/\x00\x01\x00\x00\x00crimson\x00\x02\x00\x00\x00impact.a\x00\x02\x00\x00\x00arcvaalbuff.a\x00\x02\x00\x00\x00arc.a\x00\x00\x00\x00\x00\x01\x00\x00\x00rig_b722958b.smd\x00\x03\x00\x00\x00md\x00\x03\x00\x00\x00st\x00\x04\x00\x00\x00md\x00\x04\x00\x00\x00st\x00\x02\x00\x00\x00arc.sm\x00\x05\x00\x00\x00md\x00\x05\x00\x00\x00st\x00\x00\x00\x00\x00\x01\x00\x00\x00Art/Microtransactions/spell/arc/crimson/textures/\x00\x01\x00\x00\x00buff_\x00\x01\x00\x00\x00core_\x00\x01\x00\x00\x00dark_ink_3.\x00\x01\x00\x00\x00flash.\x00\x01\x00\x00\x00impact_\x00\x01\x00\x00\x00light\x00\x01\x00\x00\x00red_sparks.\x00\x01\x00\x00\x00thunder_flash.\x00\x07\x00\x00\x00ning_\x00\n\x00\x00\x00bolts.\x00\n\x00\x00\x00random.\x00\x07\x00\x00\x00_gradient.\x00\x07\x00\x00\x00_strong.\x00\x07\x00\x00\x00_sub.\x00\x06\x00\x00\x00flash\x00\x06\x00\x00\x00trail.\x00\x10\x00\x00\x00_sub.\x00\x03\x00\x00\x00trail.\x00\x03\x00\x00\x00mini.\x00\x03\x00\x00\x00mini_impact.\x00\x02\x00\x00\x00light.\x00\x02\x00\x00\x00trail.\x00\x00\x00\x00\x00\t\x00\x00\x00dds\x00\t\x00\x00\x00mat\x00\x08\x00\x00\x00dds\x00\x08\x00\x00\x00mat\x00\x0c\x00\x00\x00dds\x00\x0c\x00\x00\x00mat\x00\n\x00\x00\x00orb.dds\x00\n\x00\x00\x00orb.mat\x00\x0b\x00\x00\x00dds\x00\x0b\x00\x00\x00mat\x00\x0f\x00\x00\x00dds\x00\x0f\x00\x00\x00mat\x00\x0e\x00\x00\x00dds\x00\x0e\x00\x00\x00mat\x00\r\x00\x00\x00dds\x00\r\x00\x00\x00mat\x00\x11\x00\x00\x00dds\x00\x11\x00\x00\x00mat\x00\x12\x00\x00\x00dds\x00\x12\x00\x00\x00mat\x00\x10\x00\x00\x00.dds\x00\x10\x00\x00\x00.mat\x00\x05\x00\x00\x00dds\x00\x05\x00\x00\x00mat\x00\x04\x00\x00\x00dds\x00\x04\x00\x00\x00mat\x00\x13\x00\x00\x00dds\x00\x13\x00\x00\x00mat\x00\x03\x00\x00\x00sub.dds\x00\x03\x00\x00\x00subc.mat\x00\x15\x00\x00\x00dds\x00\x15\x00\x00\x00mat\x00\x14\x00\x00\x00dds\x00\x14\x00\x00\x00mat\x00\x17\x00\x00\x00dds\x00\x17\x00\x00\x00mat\x00\x02\x00\x00\x00sub.dds\x00\x02\x00\x00\x00sub.mat\x00\x16\x00\x00\x00dds\x00\x16\x00\x00\x00mat\x00')

    #              )