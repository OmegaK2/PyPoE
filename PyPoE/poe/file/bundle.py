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

Enums
-------------------------------------------------------------------------------

.. autoclass: ENCODE_TYPES

.. authclass: ENCODE_TYPES_HEX

.. autoclass: PATH_TYPES

Classes
-------------------------------------------------------------------------------

.. autoclass: Bundle

.. autoclass: Index

Index Records
-------------------------------------------------------------------------------

.. autoclass: IndexRecord

.. autoclass: BundleRecord

.. autoclass: FileRecord

.. autoclass: DirectoryRecord
"""

# =============================================================================
# Imports
# =============================================================================

# python
import struct
import os
from enum import IntEnum
from io import BytesIO
from tempfile import TemporaryDirectory
from typing import List, Union

# 3rd party
from fnvhash import fnv1a_64

try:
    import cffi
except ImportError:
    cffi = None

# self
from PyPoE.shared.mixins import ReprMixin
from PyPoE.shared.decorators import doc
from PyPoE.poe.file.shared import AbstractFileReadOnly

# =============================================================================
# Setup
# =============================================================================

__all__ = [
    'ENCODE_TYPES', 'ENCODE_TYPES_HEX', 'PATH_TYPES',

    'IndexRecord', 'BundleRecord', 'FileRecord', 'DirectoryRecord',

    'Bundle', 'Index'
]

if cffi:
    ffi = cffi.FFI()
    ffi.cdef("""int Ooz_Decompress(uint8_t const* src_buf, int src_len, 
            uint8_t* dst, size_t dst_size, int, int, int, uint8_t*, size_t, 
            void*, void*, void*, size_t, int);""")
    try:
        ooz = ffi.dlopen(r'libooz.dll')
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
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

    def _read(self, buffer: BytesIO):
        if isinstance(self.data, bytes):
            raise ValueError('Bundle has been decompressed already')

        raw = buffer.read()

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

    def decompress(self, start: int = 0, end: int = None):
        """
        Decompresses this bundle's contents.

        This requires either the oozdll to be available or the ooz commandline
        tool.

        Parameters
        ----------
        start
            Start chunk
        end
            End chunk
        """
        if not self.data:
            raise ValueError()

        if end is None:
            end = self.entry_count

        last = self.entry_count - 1
        if ooz:
            for i in range(start, end):
                if i != last:
                    size = self.chunk_size
                else:
                    size = self.size_decompressed % self.chunk_size

                out = ffi.new('uint8_t[]', size+64)
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

                self.data[i] = ffi.buffer(out)[:-64]
        else:
            with TemporaryDirectory() as tempdir:
                for i in range(start, end):
                    fn = os.path.join(tempdir,'chunk%s' % i)

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

        self.data = b''.join(self.data.values())


class PATH_TYPES(IntEnum):
    DIR = 1
    FILE = 2


class IndexRecord(ReprMixin):
    SIZE = None


class BundleRecord(IndexRecord):
    """
    Attributes
    ----------
    parent : Index
    name : str
    size : int
    contents : Bundle
    BYTES : int
    """
    __slots__ = ['parent', 'name', 'size',  'contents', 'BYTES']

    _REPR_EXTRA_ATTRIBUTES = {x: None for x in __slots__}

    def __init__(self, raw: bytes, parent: 'Index', offset: int):
        self.parent = parent

        name_length = struct.unpack_from('<I', raw, offset=offset)[0]

        self.name = struct.unpack_from(
            '%ss' % name_length, raw, offset=offset+4)[0].decode()

        self.size = struct.unpack_from('<I', raw, offset=offset+4+name_length)[0]

        self.BYTES = name_length + 8

        self.contents = None

    @property
    def file_name(self) -> str:
        """
        Returns
        -------
        The full filename of this bundle file
        """
        return self.name + '.bundle.bin'

    @property
    def ggpk_path(self) -> str:
        """
        Returns
        -------
        The path relative to the content.ggpk
        """
        return 'Bundles2/' + self.file_name

    def read(self, file_path_or_raw: Union[str, bytes]):
        """
        Reads the contents of this bundle if they haven't been read already

        Parameters
        ----------
        file_path_or_raw
            see Bundle.read
        """
        if self.contents is None:
            self.contents = Bundle()
            self.contents.read(file_path_or_raw)
            self.contents.decompress()


class FileRecord(IndexRecord):
    """
    Attributes
    ----------
    parent: Index
    hash: int
    bundle: BundleRecord
    file_offset: int
    file_size: int
    """
    __slots__ = ['parent', 'hash', 'bundle', 'file_offset', 'file_size']

    _REPR_EXTRA_ATTRIBUTES = {x: None for x in __slots__}
    SIZE = 20

    def __init__(self, raw: bytes, parent: 'Index', offset: int):
        data = struct.unpack_from('<QIII', raw, offset=offset)

        self.parent = parent
        self.hash = data[0]
        self.bundle = parent.bundles[data[1]]
        self.file_offset = data[2]
        self.file_size = data[3]

    def get_file(self) -> bytes:
        """
        Returns the file contents associated with this record. For this to work
        the parent's bundle must loaded.

        Returns
        -------
        The contents of the file associated with this record.
        """
        return self.bundle.contents.data[
               self.file_offset:self.file_offset+self.file_size]


class DirectoryRecord(IndexRecord):
    """
    Attributes
    ----------
    parent: Index
    hash: int
    offset: int
    size: int
    unknown: int
    """
    __slots__ = ['parent', 'hash', 'offset', 'size', 'unknown', '_paths']

    _REPR_EXTRA_ATTRIBUTES = {x: None for x in __slots__}
    SIZE = 20

    def __init__(self, raw: bytes, parent: 'Index', offset:int):
        self.parent = parent
        data = struct.unpack_from('<QIII', raw, offset=offset)

        self.hash = data[0]
        self.offset = data[1]
        self.size = data[2]
        self.unknown = data[3]
        self._paths = None

    @property
    def paths(self) -> List[str]:
        """
        Returns
        -------
        A list of all files with their full paths (relative to the game root)
        contained within this directory
        """
        return [x.decode() for x in self._paths]

    @property
    def files(self) -> List[str]:
        """
        Returns
        -------
        A list of files contained in this directory.
        """
        return [x.rsplit('/', maxsplit=1)[-1] for x in self.paths]


class Index(Bundle):
    PATH = 'Bundles2/_.index.bin'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bundles = {}
        self.files = {}
        self.directories = {}

    def get_dir_record(self, path: Union[str, bytes]) -> DirectoryRecord:
        """
        Returns the directory record for the given directory path

        Parameters
        ----------
        path
            Directory path

        Returns
        -------
        DirectoryRecord
            The directory record for the given directory path

        Raises
        ------
        FileNotFoundError
            if the path is not valid
        """
        try:
            return self.directories[self.get_hash(path, type=PATH_TYPES.DIR)]
        except KeyError:
            raise FileNotFoundError()

    def get_file_record(self, path: Union[str, bytes]) -> FileRecord:
        """
        Returns the file record for the given file path

        Parameters
        ----------
        path
            File path

        Returns
        -------
        FileRecord
            The file record for the given file path

        Raises
        ------
        FileNotFoundError
            if the path is not valid
        """
        try:
            return self.files[self.get_hash(path, type=PATH_TYPES.FILE)]
        except KeyError:
            raise FileNotFoundError()

    def get_hash(self, path: Union[str, bytes], type: PATH_TYPES = None) -> int:
        """
        Calculates the 64 bit FNA1a hash value for a given path

        Parameters
        ----------
        path
            path to calculate the hash for
        type
            type of the path (i.e. whether this is a file or directory)

            if not given, it is attempted to infer from the path

        Returns
        -------
        Calculated 64bit FNV1a hash value
        """
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

    def _read(self, buffer: BytesIO):
        if self.bundles:
            raise ValueError('Index bundle has been read already.')
        super()._read(buffer)
        self.decompress()
        raw = self.data

        bundle_count = struct.unpack_from('<I', raw)[0]
        offset = 4

        for i in range(0, bundle_count):
            br = BundleRecord(raw, self, offset)

            self.bundles[i] = br
            offset += br.BYTES

        file_count = struct.unpack_from('<I', raw, offset=offset)[0]
        offset += 4

        for i in range(0, file_count):
            fr = FileRecord(raw, self, offset)
            self.files[fr.hash] = fr
            offset += fr.SIZE

        count = struct.unpack_from('<I', raw, offset=offset)[0]
        offset += 4
        for i in range(0, count):
            dr = DirectoryRecord(raw, self, offset)
            self.directories[dr.hash] = dr
            offset += dr.SIZE

        directory_bundle = Bundle()
        directory_bundle.read(raw[offset:])
        directory_bundle.decompress()

        for directory_record in self.directories.values():
            directory_record._paths = self._make_paths(
                directory_bundle.data[
                    directory_record.offset:
                    directory_record.offset + directory_record.size
                ]
            )

    def _make_paths(self, raw: bytes) -> List[bytes]:
        """

        Parameters
        ----------
        raw
            packed paths

        Returns
        -------
        A list of unpacked paths
        """
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
    ind.read('C:/Temp/Bundles2/_.index.bin')

    print(ind['Metadata/minimap_colours.txt'])

    '''b.decompress()
    for var in dir(b):
        if var.startswith('_'):
            continue
        print(var, getattr(b, var))
    '''

    #pprint.pprint(Index._make_paths(None, b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00Art/Microtransactions/spell/arc/crimson/models/\x00\x01\x00\x00\x00crimson\x00\x02\x00\x00\x00impact.a\x00\x02\x00\x00\x00arcvaalbuff.a\x00\x02\x00\x00\x00arc.a\x00\x00\x00\x00\x00\x01\x00\x00\x00rig_b722958b.smd\x00\x03\x00\x00\x00md\x00\x03\x00\x00\x00st\x00\x04\x00\x00\x00md\x00\x04\x00\x00\x00st\x00\x02\x00\x00\x00arc.sm\x00\x05\x00\x00\x00md\x00\x05\x00\x00\x00st\x00\x00\x00\x00\x00\x01\x00\x00\x00Art/Microtransactions/spell/arc/crimson/textures/\x00\x01\x00\x00\x00buff_\x00\x01\x00\x00\x00core_\x00\x01\x00\x00\x00dark_ink_3.\x00\x01\x00\x00\x00flash.\x00\x01\x00\x00\x00impact_\x00\x01\x00\x00\x00light\x00\x01\x00\x00\x00red_sparks.\x00\x01\x00\x00\x00thunder_flash.\x00\x07\x00\x00\x00ning_\x00\n\x00\x00\x00bolts.\x00\n\x00\x00\x00random.\x00\x07\x00\x00\x00_gradient.\x00\x07\x00\x00\x00_strong.\x00\x07\x00\x00\x00_sub.\x00\x06\x00\x00\x00flash\x00\x06\x00\x00\x00trail.\x00\x10\x00\x00\x00_sub.\x00\x03\x00\x00\x00trail.\x00\x03\x00\x00\x00mini.\x00\x03\x00\x00\x00mini_impact.\x00\x02\x00\x00\x00light.\x00\x02\x00\x00\x00trail.\x00\x00\x00\x00\x00\t\x00\x00\x00dds\x00\t\x00\x00\x00mat\x00\x08\x00\x00\x00dds\x00\x08\x00\x00\x00mat\x00\x0c\x00\x00\x00dds\x00\x0c\x00\x00\x00mat\x00\n\x00\x00\x00orb.dds\x00\n\x00\x00\x00orb.mat\x00\x0b\x00\x00\x00dds\x00\x0b\x00\x00\x00mat\x00\x0f\x00\x00\x00dds\x00\x0f\x00\x00\x00mat\x00\x0e\x00\x00\x00dds\x00\x0e\x00\x00\x00mat\x00\r\x00\x00\x00dds\x00\r\x00\x00\x00mat\x00\x11\x00\x00\x00dds\x00\x11\x00\x00\x00mat\x00\x12\x00\x00\x00dds\x00\x12\x00\x00\x00mat\x00\x10\x00\x00\x00.dds\x00\x10\x00\x00\x00.mat\x00\x05\x00\x00\x00dds\x00\x05\x00\x00\x00mat\x00\x04\x00\x00\x00dds\x00\x04\x00\x00\x00mat\x00\x13\x00\x00\x00dds\x00\x13\x00\x00\x00mat\x00\x03\x00\x00\x00sub.dds\x00\x03\x00\x00\x00subc.mat\x00\x15\x00\x00\x00dds\x00\x15\x00\x00\x00mat\x00\x14\x00\x00\x00dds\x00\x14\x00\x00\x00mat\x00\x17\x00\x00\x00dds\x00\x17\x00\x00\x00mat\x00\x02\x00\x00\x00sub.dds\x00\x02\x00\x00\x00sub.mat\x00\x16\x00\x00\x00dds\x00\x16\x00\x00\x00mat\x00')

    #              )