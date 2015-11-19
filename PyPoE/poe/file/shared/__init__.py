"""
Shared classes/functions

Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/file/shared/__init__.py                                |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
-------------------------------------------------------------------------------

Shared classes & functions for the file API. Used for exposing the same basic
API.

Agreement
-------------------------------------------------------------------------------

See PyPoE/LICENSE

TODO
-------------------------------------------------------------------------------

The abstract classes should probably actually be using python abc api.
"""

# =============================================================================
# Imports
# =============================================================================

# Python
from io import BytesIO

# =============================================================================
# Globals
# =============================================================================

__all__ = [
    'ParserError',
    'ParserWarning'
    'AbstractFileReadOnly',
    'AbstractFile',
    'AbstractFileCache',
]

# =============================================================================
# Exceptions
# =============================================================================

class ParserError(Exception):
    pass

class ParserWarning(UserWarning):
    pass

# =============================================================================
# ABS
# =============================================================================

class AbstractFileReadOnly(object):
    """
    Abstract Base Class for reading.

    It provides common methods as well as methods that implementing classes
    should override.
    """
    def _read(self, buffer, *args, **kwargs):
        """
        :param buffer: The file/byte buffer
        :type buffer: io.BytesIO
        """
        raise NotImplementedError()

    def get_read_buffer(self, file_path_or_raw, function, *args, **kwargs):
        """
        Will attempt to open the given file_path_or_raw in read mode and pass
        the buffer to the specified function.
        The function must accept at least one keyword argument called 'buffer'.

        :param file_path_or_raw: file path, bytes or buffer to read from
        :type file_path_or_raw: BytesIO, bytes or str

        :param args: Additional positional arguments to pass to the specified
        function

        :param kwargs: Additional keyword arguments to pass to the specified
        function

        :return: Result of the function

        :raises TypeError: if file_path_or_raw has an invalid type
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

    def read(self, file_path_or_raw, *args, **kwargs):
        """
        Reads the file contents into the specified path or buffer. This will
        also reset any existing contents of the file.

        If a buffer or bytes was given, the data will be read from the buffer
        or bytes object.

        If a file path was given, the resulting data will be read from the
        specified file.

        :param file_path_or_raw: file path, bytes or buffer to read from
        :type file_path_or_raw: BytesIO, bytes or str

        :param args: Additional positional arguments

        :param kwargs: Additional keyword arguments

        :return: result of the read operation, if any

        :raises TypeError: if file_path_or_raw has an invalid type
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
        :param buffer: The file/byte buffer
        :type buffer: io.BytesIO
        """
        raise NotImplementedError()

    def get_write_buffer(self, file_path_or_raw, function, *args, **kwargs):
        """
        Will attempt to open the given file_path_or_raw in write mode and pass
        the buffer to the specified function.
        The function must accept at least one keyword argument called 'buffer'.

        :param file_path_or_raw: file path, bytes or buffer to write to
        :type file_path_or_raw: BytesIO, bytes or str

        :param args: Additional positional arguments to pass to the specified
        function

        :param kwargs: Additional keyword arguments to pass to the specified
        function

        :return: Result of the function

        :raises TypeError: if file_path_or_raw has an invalid type
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

    def write(self, file_path_or_raw, *args, **kwargs):
        """
        Write the contents of file to the specified path or buffer.

        If a buffer or bytes was given, a buffer object with the new data should
        be returned.

        If a file path was given, the resulting data should be written to the
        specified file.

        :param file_path_or_raw: file path, bytes or buffer to write to
        :type file_path_or_raw: BytesIO, bytes, str
        :param args: Additional positional arguments
        :param kwargs: Additional keyword arguments
        :return: result of the write operation, if any

        :raises TypeError: if file_path_or_raw has an invalid type
        """
        return self.get_write_buffer(file_path_or_raw, self._write, *args, **kwargs)


class AbstractFileCache(object):
    def __init__(self, path_or_ggpk=None, files=None, options=None):
        """
        Creates a new Relational Reader instance.

        See DatReader for details on the options available.

        :param path_or_ggpk: The path where the dat files are stored or a
        GGPKFile instance
        :type path_or_ggpk: :class:`GGPKFile` or str

        :raises TypeError: if path_or_ggpk not specified or invalid type
        :raises ValueError: if a GGPKFile was passed, but it was not parsed
        """
        if isinstance(path_or_ggpk, GGPKFile):
            if not path_or_ggpk.is_parsed:
                raise ValueError('The GGPK File must be parsed.')
            self._ggpk = path_or_ggpk
            self._path = None
        elif isinstance(path_or_ggpk, str):
            self._ggpk = None
            self._path = path_or_ggpk
        else:
            raise TypeError('path_or_ggpk must be a valid directory or GGPKFile')