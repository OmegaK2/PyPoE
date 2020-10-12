"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/file/shared/__init__.py                                |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Shared classes & functions for the file API. Used for exposing the same basic
API.

All file classes inherit the base classes defined here or in the other shared
file modules.

.. warning::
    None of the abstract classes found here should be instantiated directly.

See also:

* :mod:`PyPoE.poe.file.shared.cache`
* :mod:`PyPoE.poe.file.shared.keyvalues`

Agreement
===============================================================================

See PyPoE/LICENSE

.. todo::

    The abstract classes should probably actually be using python abc api.

Documentation
===============================================================================

Abstract Classes
-------------------------------------------------------------------------------

.. autoclass:: AbstractFileReadOnly

.. autoclass:: AbstractFile

.. autoclass:: AbstractFileSystemNode


Enums
-------------------------------------------------------------------------------

.. autoclass:: FILE_SYSTEM_TYPES

Exceptions & Warnings
-------------------------------------------------------------------------------

.. autoclass:: ParserError

.. autoclass:: ParserWarning
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import abc
import os
import re
from enum import IntEnum
from io import BytesIO
from typing import Union, List, Dict, Callable, Any

# self
from PyPoE.shared.mixins import ReprMixin

# =============================================================================
# Globals
# =============================================================================

__all__ = [
    'ParserError',
    'ParserWarning'
    'AbstractFileReadOnly',
    'AbstractFile',
    'FILE_SYSTEM_TYPES',
    'AbstractFileSystemNode',
]

# =============================================================================
# Exceptions
# =============================================================================


class ParserError(Exception):
    """
    This exception or subclasses of this exception are raised when general
    errors related to the parsing of files occur, such as malformed files.
    """
    pass


class ParserWarning(UserWarning):
    """
    This warning or subclasses of this warning are emitted when during the
    parsing process there are cases where issues are not severe enough to
    entirely fail the passing, but could pose serious problems.
    """
    pass


# =============================================================================
# ABS
# =============================================================================


class AbstractFileReadOnly(ReprMixin):
    """
    Abstract Base Class for reading.

    It provides common methods as well as methods that implementing classes
    should override.
    """
    def _read(self, buffer, *args, **kwargs):
        """
        Parameters
        ----------
        buffer : io.BytesIO
            The file/byte buffer
        """
        raise NotImplementedError()

    def get_read_buffer(self,
                        file_path_or_raw: Union[BytesIO, bytes, str],
                        function: Callable,
                        *args, **kwargs) -> Any:
        """
        Will attempt to open the given file_path_or_raw in read mode and pass
        the buffer to the specified function.
        The function must accept at least one keyword argument called 'buffer'.

        Parameters
        ----------
        file_path_or_raw
            file path, bytes or buffer to read from
        function
            function that will be called with the buffer keyword argument
        args
            Additional positional arguments to pass to the specified function
        kwargs
            Additional keyword arguments to pass to the specified function


        Returns
        -------
            Result of the function


        Raises
        ------
        TypeError
            if file_path_or_raw has an invalid type
        """
        if isinstance(file_path_or_raw, BytesIO):
            return function(*args, buffer=file_path_or_raw, **kwargs)
        elif isinstance(file_path_or_raw, bytes):
            return function(*args, buffer=BytesIO(file_path_or_raw), **kwargs)
        elif isinstance(file_path_or_raw, str):
            with open(file_path_or_raw, 'rb') as f:
                return function(*args, buffer=f, **kwargs)
        else:
            raise TypeError('file_path_or_raw must be a file path or bytes object')

    def read(self,
             file_path_or_raw: Union[BytesIO, bytes, str],
             *args,
             **kwargs) -> Any:
        """
        Reads the file contents into the specified path or buffer. This will
        also reset any existing contents of the file.

        If a buffer or bytes was given, the data will be read from the buffer
        or bytes object.

        If a file path was given, the resulting data will be read from the
        specified file.

        Parameters
        ----------
        file_path_or_raw
            file path, bytes or buffer to read from
        args
            Additional positional arguments
        kwargs
            Additional keyword arguments


        Returns
        -------
        object
            result of the read operation, if any


        Raises
        ------
        TypeError
            if file_path_or_raw has an invalid type
        """
        return self.get_read_buffer(file_path_or_raw, self._read, *args, **kwargs)


class AbstractFile(AbstractFileReadOnly):
    """
    Abstract Base Class for reading and writing files.

    It provides common methods as well as methods that implementing classes
    should override.
    """

    def _write(self, buffer, *args, **kwargs):
        """
        Parameters
        ----------
        buffer : io.BytesIO
            The file/byte buffer
        """
        raise NotImplementedError()

    def get_write_buffer(self,
                         file_path_or_raw: Union[BytesIO, bytes, str],
                         function: Callable,
                         *args, **kwargs) -> Any:
        """
        Will attempt to open the given file_path_or_raw in write mode and pass
        the buffer to the specified function.
        The function must accept at least one keyword argument called 'buffer'.

        Parameters
        ----------
        file_path_or_raw
            file path, bytes or buffer to write to
        args
            Additional positional arguments to pass to the specified function
        kwargs
            Additional keyword arguments to pass to the specified function


        Returns
        -------
        object
            Result of the function


        Raises
        ------
        TypeError
            if file_path_or_raw has an invalid type
        """
        if isinstance(file_path_or_raw, BytesIO):
            return function(*args, buffer=file_path_or_raw, **kwargs)
        elif isinstance(file_path_or_raw, bytes):
            return function(*args, buffer=BytesIO(file_path_or_raw), **kwargs)
        elif isinstance(file_path_or_raw, str):
            with open(file_path_or_raw, 'wb') as f:
                return function(*args, buffer=f, **kwargs)
        else:
            raise TypeError('file_path_or_raw must be a file path or bytes object')

    def write(self,
              file_path_or_raw: Union[BytesIO, bytes, str],
              *args,
              **kwargs) -> Any:
        """
        Write the contents of file to the specified path or buffer.

        If a buffer or bytes was given, a buffer object with the new data should
        be returned.

        If a file path was given, the resulting data should be written to the
        specified file.

        Parameters
        ----------
        file_path_or_raw
            file path, bytes or buffer to write to
        args
            Additional positional arguments
        kwargs
            Additional keyword arguments


        Returns
        -------
        object
            result of the write operation, if any


        Raises
        ------
        TypeError
            if file_path_or_raw has an invalid type
        """
        return self.get_write_buffer(file_path_or_raw, self._write, *args, **kwargs)


class FILE_SYSTEM_TYPES(IntEnum):
    ROOT = -1
    DISK = 0
    BUNDLE = 1
    GGPK = 2


class AbstractFileSystemNode(ReprMixin):
    __slots__ = ['parent', 'file_system_type', 'is_file', 'children']

    def __init__(self,
                parent: 'FileSystemNode',
                file_system_type: FILE_SYSTEM_TYPES,
                is_file: bool):
        self.parent: 'FileSystemNode' = parent
        self.file_system_type: FILE_SYSTEM_TYPES = file_system_type
        self.is_file: bool = is_file
        self.children: Dict[str, 'FileSystemNode'] = {}

    def __getitem__(self, item: str) -> 'AbstractFileSystemNode':
        """
        Return the the specified file or directory path.

        The path will accept valid paths for the current operating system,
        however I suggest using forward slashes ( / ) as they are supported on
        both Windows and Linux.

        Since the each node supports the same syntax, all these calls are
        equivalent:

        .. code-block:: python

            self['directory1']['directory2']['file.ext']
            self['directory1']['directory2/file.ext']
            self['directory1/directory2']['file.ext']
            self['directory1/directory2/file.ext']

        Parameters
        ----------
        item
            file path or file name

        Returns
        -------
            returns the :class:`AbstractFileSystemNode` of the specified item

        Raises
        ------
        FileNotFoundError
            if the specified item is not found
        """
        item = item.strip('/\\')
        if not item:
            return self

        path = []
        partial = item
        while partial:
            partial, result = os.path.split(partial)
            path.insert(0, result)

        obj = self
        while True:
            try:
                partial = path.pop(0)
            except IndexError:
                return obj

            for child in obj.children.values():
                if child.name == partial:
                    obj = child
                    break
            else:
                raise FileNotFoundError('%s/%s not found' % (
                    self.get_path(), item
                ))

    @property
    def data(self) -> bytes:
        """
        Returns the data contained within this object
        """
        raise NotImplementedError

    @property
    def name(self) -> str:
        """
        Returns the name associated with the stored record.

        Returns
        -------
            name of the file/directory
        """
        raise NotImplementedError

    @property
    def files(self) -> List['FileSystemNode']:
        """
        Returns a list of nodes which belong to files

        Returns
        -------
            list of :class:`AbstractFileSystemNode` instances which reference
            a file
        """
        return [child for child in self.children.values() if child.is_file]

    @property
    def directories(self) -> List['FileSystemNode']:
        """
        Returns a list of nodes which belong to directories

        Returns
        -------
            list of :class:`AbstractFileSystemNode` instances which reference
            a directory
        """
        return [child for child in self.children.values() if child.is_directory]

    @property
    def is_directory(self) -> bool:
        """
        Whether this node references a directory or file.
        """
        return not self.is_file

    def search(self,
               regex: re.Pattern,
               search_files: bool = True,
               search_directories: bool = True) -> \
            List['AbstractFileSystemNode']:
        """

        Parameters
        ----------
        regex
            compiled regular expression to use
        search_files
            Whether file instances should be searched
        search_directories
            Whether directory instances should be searched


        Returns
        -------
            List of matching :class:`AbstractFileSystemNode` instances
        """
        if isinstance(regex, str):
            regex = re.compile(regex)

        nodes = []

        # func = lambda n: nodes.append(n) if re.search(regex, n.name) else None
        # self.walk(func)

        q = []
        q.append(self)

        while len(q) > 0:
            node = q.pop()
            if ((search_files and node.is_file or
                 search_directories and node.is_directory)
                    and re.search(regex, node.name)):
                nodes.append(node)

            for child in node.children:
                q.append(child)

        return nodes

    def get_path(self) -> str:
        """
        Returns the full path

        Returns
        -------
            Full path
        """
        return '/'.join([n.name for n in self.get_parent(make_list=True)])

    def get_parent(self,
                   n: int = -1,
                   stop_at: Union['AbstractFileSystemNode', None] = None,
                   make_list: bool = False) -> 'AbstractFileSystemNode':
        """
        Gets the n-th parent or returns root parent if at top level.
        Negative values for n will iterate until the root is found.

        If the make_list keyword is set to True, a list of Nodes in the
        following form will be returned:

        [n-th parent, (n-1)-th parent, ..., self]

        Parameters
        ----------
        n
            Up to which depth to go to.
        stop_at
            :class:`AbstractFileSystemNode` instance to stop the iteration at
        make_list
            Return a list of :class:`AbstractFileSystemNode` instances instead of parent

        Returns
        -------
            Returns parent or root :class:`AbstractFileSystemNode` instance
        """
        nodes = []
        node = self
        while n != 0:
            if node.parent is None:
                break

            if node is stop_at:
                break

            if make_list:
                nodes.insert(0, node)
            node = node.parent
            n -= 1

        return nodes if make_list else node

    def walk(self, function: Callable):
        """
        .. todo::
            function = None -> generator like os.walk (dir, [dirs], [files])

        Walks over the nodes and it's sub nodes and executes the specified
        function.

        The function will be called with the following dictionary arguments:

        * node - :class:`AbstractFileSystemNode`
        * depth - Depth

        Parameters
        ----------
        function
            function to call when walking
        """
        q = []
        q.append({'node': self, 'depth': 0})

        while len(q) > 0:
            data = q.pop()
            function(**data)
            for child in data['node'].children.values():
                q.append({'node': child, 'depth': data['depth'] + 1})

        """for child in self.children:
            function(child)
            child.walk(function)"""

    def extract_to(self, target_directory: str):
        """
        Extracts the node and its contents (including sub-directories) to the
        specified target directory.

        Parameters
        ----------
        target_directory : str
            Path to directory where to extract to.
        """
        dir_path = os.path.join(target_directory, self.name)
        if self.is_directory:
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)

            for node in self.children.values():
                node.extract_to(dir_path)
        else:
            with open(dir_path, 'wb') as f:
                f.write(bytes(self))