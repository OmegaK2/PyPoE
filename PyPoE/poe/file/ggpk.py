"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/file/ggpk.py                                           |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Support for reading .ggpk files.

A .ggpk file, namely content.ggpk, is a container containing a virtual directory
and file contents. It is basically just packing the files together without
compression.

Agreement
===============================================================================

See PyPoE/LICENSE

Documentation
===============================================================================

Public API
-------------------------------------------------------------------------------

.. autoclass:: GGPKFile

    .. automethod:: __getitem__


Internal API
-------------------------------------------------------------------------------

General
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: DirectoryNode

    .. automethod:: __getitem__

Records
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: GGPKRecord

.. autoclass:: DirectoryRecord

.. autoclass:: FileRecord

.. autoclass:: FreeRecord

Miscellaneous
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: BaseRecord

.. autoclass:: MixinRecord

.. autoclass:: DirectoryRecordEntry
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import io
import struct
import os
import warnings
from typing import Union, Dict

# 3rd Party

# self
from PyPoE.shared import InheritedDocStringsMeta
from PyPoE.shared.decorators import doc
from PyPoE.shared.mixins import ReprMixin
from PyPoE.poe.file.shared import AbstractFileReadOnly, \
    AbstractFileSystemNode, FILE_SYSTEM_TYPES, ParserError

# =============================================================================
# Globals
# =============================================================================

__all__ = ['GGPKFile']


# =============================================================================
# Functions
# =============================================================================

# =============================================================================
# Errors
# =============================================================================


class GGPKException(Exception):
    pass


class InvalidTagException(GGPKException):
    pass


# =============================================================================
# Classes
# =============================================================================


class BaseRecord(ReprMixin):
    """
    Attributes
    ----------
    _container : GGPKFile
        Parent GGPKFile
    length : int
        Length
    offset : int
        Starting offset in ggpk
    """
    tag = None

    __slots__ = ['_container', 'length', 'offset']

    def __init__(self, container, length, offset):
        self._container = container
        self.length = length
        self.offset = offset

    def read(self, ggpkfile):
        """
        Read this record's header for the given GGPKFile instance.

        Parameters
        ----------
        ggpkfile : GGPKFile
            GGPKFile instance
        """
        pass

    def write(self, ggpkfile):
        """
        Write this record's header for the given GGPKFile instance.

        Parameters
        ----------
        ggpkfile : GGPKFile
            GGPKFile instance
        """
        ggpkfile.write(struct.pack('<i', self.length))
        ggpkfile.write(self.tag)


class MixinRecord:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = ''
        self._name_length = 0

    @property
    def name(self):
        """
        Returns and sets the name of the file

        If setting, it also takes care of adjusting name_length accordingly.
        Returns name of the file.

        Returns
        -------
        str
            name of the file
        """
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        # Account for null bytes
        self._name_length = len(name) + 1


@doc(append=BaseRecord)
class GGPKRecord(BaseRecord):
    """
    The GGPKRecord is the master record of the file; it always contains two
    entries. First is the root directory, 2nd is a FreeRecord.

    Attributes
    ----------
    offsets : list[int]
        List of offsets for records
    """
    tag = 'GGPK'

    __slots__ = BaseRecord.__slots__.copy() + ['offsets']

    @doc(doc=BaseRecord.read)
    def read(self, ggpkfile):
        # Should be 2, TODO?
        records = struct.unpack('<i', ggpkfile.read(4))[0]
        self.offsets = []
        for i in range(0, records):
            self.offsets.append(struct.unpack('<q', ggpkfile.read(8))[0])

    @doc(doc=BaseRecord.write)
    def write(self, ggpkfile):
        # Write length & tag
        super().write(ggpkfile)
        # Should always be 2
        ggpkfile.write(struct.pack('<i', 2))
        for i in range(0, len(offsets)):
            ggpkfile.write(struct.unpack('<q', offsets[i]))


class DirectoryRecordEntry(ReprMixin):
    """
    Attributes
    ----------
    hash :  int
        murmur2 32bit hash
    offset :  int
        offset in :class:`GGPKFile`
    """
    def __init__(self, hash, offset):
        """
        Parameters
        ----------
        hash :  int
            murmur2 32bit hash
        offset :  int
            offset in GGPKFile
        """
        self.hash = hash
        self.offset = offset


@doc(append=BaseRecord)
class DirectoryRecord(MixinRecord, BaseRecord):
    """
    Represents a directory in the virtual :class:`GGPKFile` file tree.

    Attributes
    ----------
    _name :  str
        Name of directory
    _name_length :  int
        Length of name
    _entries_length :  int
        Number of directory entries
    hash :  int
        SHA256 hash of file contents
    """

    tag = 'PDIR'

    __slots__ = BaseRecord.__slots__.copy() + ['_name', '_name_length', 'entries_length', 'hash', 'entries']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @doc(doc=BaseRecord.read)
    def read(self, ggpkfile):
        self._name_length = struct.unpack('<i', ggpkfile.read(4))[0]
        self.entries_length = struct.unpack('<i', ggpkfile.read(4))[0]  
        self.hash = int.from_bytes(ggpkfile.read(32), 'big')
        # UTF-16 2-byte width
        self._name = ggpkfile.read(2 * (self._name_length - 1)).decode('UTF-16_LE')
        # Null Termination
        ggpkfile.seek(2, os.SEEK_CUR)
        self.entries = []
        for i in range(0, self.entries_length):
            self.entries.append(DirectoryRecordEntry(
                hash=struct.unpack('<I', ggpkfile.read(4))[0],
                offset=struct.unpack('<q', ggpkfile.read(8))[0],
            ))

    @doc(doc=BaseRecord.write)
    def write(self, ggpkfile):
        # Error Checking & variable preparation
        if len(self.hash) != 32:
            raise ValueError('Hash must be 32 bytes, was %s bytes' % len(self.hash))
        if len(self.entries) != self.entries_length:
            raise ValueError('Numbers of entries must match with length')
        name_str = self._name.encode('UTF-16')
        # Write length & tag
        super().write(ggpkfile)
        ggpkfile.write(struct.pack('<i', self._name_length))
        ggpkfile.write(struct.pack('<i', self.entries_length))
        # Fixed 32-bytes
        ggpkfile.write(self.hash)
        ggpkfile.write(name_str)
        ggpkfile.write(struct.pack('<h', 0))
        # TODO: len(self.entries)
        for entry in self.entries:
            ggpkfile.write(struct.pack('<i', entry.hash))
            ggpkfile.write(struct.pack('<q', entry.offset))


@doc(append=BaseRecord)
class FileRecord(MixinRecord, BaseRecord):
    """
    Represents a file in the virtual :class:`GGPKFile` file tree.

    Attributes
    ----------
    _name :  str
        Name of file
    _name_length :  int
        Length of name
    hash :  int
        SHA256 hash of file contents
    data_start :  int
        starting offset of data
    data_length :  int
        length of data
    """

    tag = 'FILE'

    __slots__ = BaseRecord.__slots__.copy() + ['_name', '_name_length', 'hash', 'data_start', 'data_length']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def extract(self, buffer=None):
        """
        Extracts this file contents into a memory file object.

        Parameters
        ----------
        buffer : io.Bytes or None
            GGPKFile Buffer to use; if None, open the parent GGPKFile and use
            it as buffer.


        Returns
        -------
        io.BytesIO
            memory file buffer object
        """
        if buffer is None:
            return self._container.get_read_buffer(
                self._container._file_path_or_raw,
                self.extract,
            )

        # The buffer object is taken care of in get_read_buffer if it's a file
        buffer.seek(self.data_start)
        memfile = io.BytesIO()
        memfile.write(buffer.read(self.data_length))
        # Set the pointer to the beginning
        memfile.seek(0)
        return memfile

    def extract_to(self, directory, name=None):
        """
        Extracts the file to the given directory.
        
        Parameters
        ----------
        directory :  str
            the directory to extract the file to
        name : str or None
            the name of the file; if None use the file name as in the record.
        """
        name = self._name if name is None else name 
        path = os.path.join(directory, name)
        with open(path, 'bw') as exfile:
            # TODO Mem leak?
            exfile.write(self.extract().read())

    @doc(doc=BaseRecord.read)
    def read(self, ggpkfile):
        self._name_length = struct.unpack('<i', ggpkfile.read(4))[0]
        self.hash = int.from_bytes(ggpkfile.read(32), 'big')
        # UTF-16 2-byte width
        self._name = ggpkfile.read(2 * (self._name_length - 1)).decode('UTF-16')
        # Null Termination
        ggpkfile.seek(2, os.SEEK_CUR)
        self.data_start = ggpkfile.tell()
        # Length 4B - Tag 4B - STRLen 4B - Hash 32B + STR ?B  
        self.data_length = self.length - 44 - self._name_length * 2
        
        ggpkfile.seek(self.data_length, os.SEEK_CUR)

    @doc(doc=BaseRecord.write)
    def write(self, ggpkfile):
        # Error checking & variable preparation first
        if len(self.hash) != 32:
            raise ValueError('Hash must be 32 bytes, was %s bytes' % len(self.hash))
        
        name_str = self._name.encode('UTF-16')
        # Write length & tag
        super().write(ggpkfile)
        ggpkfile.write(struct.pack('<i', self._name_length))
        # Fixed 32-bytes
        ggpkfile.write(self.hash)
        ggpkfile.write(name_str)
        ggpkfile.write(struct.pack('<h', 0))
        
        #TODO: Write File Contents here?


@doc(append=BaseRecord)
class FreeRecord(BaseRecord):
    """
    Attributes
    ----------
    next_free : int
        offset of next :class:`FreeRecord`
    """
    tag = 'FREE'

    __slots__ = BaseRecord.__slots__.copy() + ['next_free']

    @doc(doc=BaseRecord.read)
    def read(self, ggpkfile):
        self.next_free = struct.unpack('<q', ggpkfile.read(8))[0]
        ggpkfile.seek(self.length -16, os.SEEK_CUR)

    @doc(doc=BaseRecord.write)
    def write(self, ggpkfile):
        # Write length & tag
        super().write(ggpkfile)
        ggpkfile.write(struct.pack('<q', self.next_free))


class DirectoryNode(AbstractFileSystemNode):
    """
    Attributes
    ----------
    children : list[DirectoryNode]
        list of parent :class:`DirectoryNode` instances (i.e. files and
        directories)
    parent : DirectoryNode
        parent :class:`DirectoryNode` or None if this is the root node
    record : :class:`DirectoryRecord` or :class:`FileRecord`
        associated record
    hash : str
        some kind of hash the game uses
    """

    __slots__ = ['record', 'hash'] + AbstractFileSystemNode.__slots__

    _REPR_ARGUMENTS_IGNORE = {'parent'}

    def __init__(self,
                 *args,
                 parent: 'DirectoryNode',
                 is_file: bool,
                 record: Union[DirectoryRecord, FileRecord],
                 hash: str,
                 **kwargs):
        super().__init__(
            *args,
            parent=parent,
            is_file=is_file,
            file_system_type=FILE_SYSTEM_TYPES.GGPK,
            **kwargs)
        self.record: Union[DirectoryRecord, FileRecord] = record
        self.hash: str = hash

    @property
    def name(self) -> str:
        return self.record.name

    @property
    def data(self) -> bytes:
        if self.is_file:
            return self.record.extract()
        else:
            raise ValueError('Only files can have their data extracted')
        

class GGPKFile(AbstractFileReadOnly, metaclass=InheritedDocStringsMeta):
    """
    Representation of a .ggpk file.

    Attributes
    ----------
    directory : DirectoryNode
        root :class:`DirectoryNode` instance
    records : dict[int, BaseRecord]
        mapping of offset -> record instances
    """

    EXTENSION = '.ggpk'

    def __init__(self, *args, **kwargs):
        AbstractFileReadOnly.__init__(self, *args, **kwargs)
        self.directory: Union[DirectoryNode, None] = None
        self.records: Dict[int, BaseRecord] = {}

    def __getitem__(self, item: str) -> DirectoryNode:
        """
        Returns the specified node for the specified file path

        Parameters
        ----------
        item
            file path

        Returns
        -------
            the :class:`DirectoryNode` instance if found

        Raises
        ------
        ValueError
            if directory is not build
        FileNotFoundError
            if file was not found

        See Also
        --------
        DirectoryNode.__getitem__
        """
        if self.directory is None:
            raise ValueError('Directory not build')
        if item == 'ROOT':
            return self.directory

        return self.directory[item]

    #
    # Properties
    #

    def _is_parsed(self) -> bool:
        """
        Whether the directory has been built.
        """
        return self.directory is not None

    is_parsed = property(fget=_is_parsed)

    #
    # Private
    #

    def _read_record(self, records, ggpkfile, offset: int):
        length = struct.unpack('<i', ggpkfile.read(4))[0]
        tag = ggpkfile.read(4)
        
        '''for recordcls in recordsc:
            if recordcls.tag == tag:
                break

        record = recordcls(self, length, offset)'''

        if tag == b'FILE':
            record = FileRecord(self, length, offset)
        elif tag == b'FREE':
            record = FreeRecord(self, length, offset)
        elif tag == b'PDIR':
            record = DirectoryRecord(self, length, offset)
        elif tag == b'GGPK':
            record = GGPKRecord(self, length, offset)
        else:
            raise InvalidTagException(tag)

        record.read(ggpkfile)
        records[offset] = record

    def diff(self, other_ggpk, out_file=None):
        """
        Creates a list of file paths that differ between this GGPKFile instance
        and another GGPKFile instance.
        This will take into account new, deleted and changed files.

        Optionally writes this list to the specified out_file

        Parameters
        ----------
        other_ggpk : GGPKFile
            Other parsed GGPKFile instance to compare against
        out_file : str or None
            File to optionally write the output to.

        Returns
        -------
        list[str]
            List of new file paths
        list[str]
            List of deleted file paths
        list[str]
            List of changed file paths (different hash)

        Raises
        ------
        TypeError
            if other_ggpk is not a GGPKFile instance
        ValueError
            if any of the GGPKFile instances are not parsed
        ValueError
            if any of the GGPKFile instances do not have their directory build
        """
        if not isinstance(other_ggpk, GGPKFile):
            raise TypeError('other_ggpk must a parsed GGPK file instance')

        if not self.is_parsed or  not other_ggpk.is_parsed:
            raise ValueError('Both ggpk files must be parsed and have their '
                             'directory build.')

        data = [{'ggpk': self}, {'ggpk': other_ggpk}]

        for gdict in data:
            gdict['files'] = {}

            def add_file(node, depth):
                if not isinstance(node.record, FileRecord):
                    return
                gdict['files'][node.get_path()] = node.record.hash

            gdict['ggpk'].directory.walk(add_file)

            gdict['set'] = set(gdict['files'].keys())

        new_files = sorted(list(data[0]['set'].difference(data[1]['set'])))
        deleted_files = sorted(list(data[1]['set'].difference(data[0]['set'])))
        changed_files = []
        for fn in sorted(list(data[0]['set'].union(data[1]['set']))):
                try:
                    if data[0]['files'][fn] != data[1]['files'][fn]:
                        changed_files.append(fn)
                except KeyError:
                    pass

        if out_file:
            with open(out_file, 'w') as f:
                f.write('Diff between two ggpk files\n')
                f.write('\n')

                for header, k in (
                    ('New files', new_files),
                    ('Removed files', deleted_files),
                    ('Changed files', changed_files),
                ):
                    f.write('\n')
                    f.write('='*80)
                    f.write('\n')
                    f.write(header)
                    f.write('\n\n')
                    for fn in k:
                        f.write(fn)
                        f.write('\n')

        return new_files, deleted_files, changed_files

    def build_directory(self, parent: DirectoryNode = None) -> DirectoryNode:
        """
        Rebuilds the directory or the specified :class:`DirectoryNode`
        If the root directory is rebuild it will be stored in the directory
        object variable.
        
        Parameters
        ----------
        parent : :class:`DirectoryNode` or None
            parent :class:`DirectoryNode`. If None generate the root directory


        Returns
        -------
        DirectoryNode
            Returns the parent node or the root node if parent was None


        Raises
        ------
        ParserError
            if performed without calling .read() first
            if offsets pointing to records types which are not
            :class:`FileRecord` or :class:`DirectoryRecord`
        """
        if not self.records:
            raise ParserError('No records - perform .read() first')

        # Build Root directory
        if parent is None:
            ggpkrecord = self.records[0]
            for offset in ggpkrecord.offsets:
                record = self.records[offset]
                if isinstance(record, DirectoryRecord):
                    break
            if not isinstance(record, DirectoryRecord):
                raise ParserError('GGPKRecord does not contain a DirectoryRecord,\
                    got %s' % type(record))

            root = DirectoryNode(
                parent=None,
                is_file=False,
                record=record,
                hash=None,
            )

            self.directory = root
        else:
            root = parent

        l = []
        for entry in root.record.entries:
            l.append((entry.offset, entry.hash, root))

        try:
            while True:
                offset, hash, parent = l.pop()
                try:
                    record = self.records[offset]
                except KeyError:
                    pass
                else:
                    node = DirectoryNode(
                        parent=parent,
                        is_file=isinstance(record, FileRecord),
                        record=record,
                        hash=hash,
                    )
                    parent.children[record.name] = node

                    if node.is_directory:
                        for entry in record.entries:
                            l.append((entry.offset, entry.hash, node))
        except IndexError:
            pass

        return root

    directory_build = build_directory
        
    def _read(self, buffer, *args, **kwargs):
        """
        Reads the records from the file into object.records.
        """
        records = {}
        offset = 0
        size = buffer.seek(0, os.SEEK_END)

        # Reset Pointer
        buffer.seek(0, os.SEEK_SET)

        while offset < size:
            try:
                self._read_record(
                    records=records,
                    ggpkfile=buffer,
                    offset=offset,
                )
            except InvalidTagException as e:
                warnings.warn('Invalid tag %s - seeking next valid tag' % e.args)
                buffer.seek(offset)

                not_found = True
                # Offset by 3 so I can capture things in the middle of chunks
                offset -= 3
                while not_found:
                    chunk = buffer.read(4096)
                    # TODO: Maybe remove free and GGPK here for speedups
                    for bytestr in (b'FILE', b'PDIR', b'FREE', b'GGPK'):
                        index = chunk.find(bytestr)
                        if index == -1:
                            continue
                        else:
                            # The tag is preceeded by u32 length
                            offset = buffer.tell() - 4096 + index - 4
                            buffer.seek(offset)
                            not_found = False
                            break
                    else:
                        # Offset by 3 again to account for the size of 4
                        offset += 4093
                        buffer.seek(offset)
                        if len(chunk) < 4096:
                            break
            else:
                offset = buffer.tell()
        self.records = records

    @doc(prepend=AbstractFileReadOnly.read)
    def read(self, file_path_or_raw, *args, **kwargs):
        super().read(file_path_or_raw, *args, **kwargs)
        self._file_path_or_raw = file_path_or_raw


if __name__ == '__main__':
    import cProfile
    from line_profiler import LineProfiler
    profiler = LineProfiler()
    '''profiler.add_function(GGPKFile.read)
    profiler.add_function(GGPKFile._read_record)
    for record in recordsc:
        profiler.add_function(record.read)'''

    ggpk = GGPKFile()
    ggpk.read(r'M:\Path of Exile\Content.ggpk')
    ggpk.directory_build()
    print(ggpk[r'Bundles2\_.index.bin'].get_path())
    #profiler.run("ggpk.read()")

    #profiler.add_function(GGPKFile.directory_build)
    #profiler.add_function(DirectoryNode.__init__)
    #profiler.run("ggpk.directory_build()")
    #ggpk.directory.directories[2].extract_to('N:/')
    profiler.print_stats()
