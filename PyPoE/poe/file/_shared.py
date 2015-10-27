"""
Shared classes/functions

Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/file/_shared.py                                        |
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
    'AbstractFileReadOnly',
    'AbstractFile',
    'AbstractFileUnbuffered',
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
    def __init__(self):
        pass

    def _read(self, buffer, *args, **kwargs):
        raise NotImplementedError()

    def read(self, file_path_or_raw, *args, **kwargs):
        """
        Reads the file contents into the specified path or buffer. This will
        also reset any existing contents of the file.

        If a buffer or bytes was given, the data will be read from the buffer
        or bytes object.

        If a file path was given, the resulting data will be read from the
        specified file.

        :param file_path_or_raw: file path, bytes or buffer to write to
        :type file_path_or_raw: BytesIO, bytes, str
        :param args: Additional positional arguments
        :param kwargs: Additional keyword arguments
        :return: result of the read operation, if any

        :raises TypeError: if file_path_or_raw has an invalid type
        """
        if isinstance(file_path_or_raw, BytesIO):
            return self._read(file_path_or_raw, *args, **kwargs)
        elif isinstance(file_path_or_raw, bytes):
            return self._read(BytesIO(file_path_or_raw), *args, **kwargs)
        elif isinstance(file_path_or_raw, str):
            with open(file_path_or_raw, 'rb') as f:
                return self._read(f, *args, **kwargs)
        else:
            raise TypeError('file_path_or_raw must be a file path or bytes object')


class AbstractFile(AbstractFileReadOnly):
    """
    Abstract Base Class for reading and writing files.

    It provides common methods as well as methods that implementing classes
    should override.
    """

    def _write(self, buffer, *args, **kwargs):
        raise NotImplementedError()

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
        if isinstance(file_path_or_raw, BytesIO):
            return self._write(file_path_or_raw, *args, **kwargs)
        elif isinstance(file_path_or_raw, bytes):
            return self._write(BytesIO(file_path_or_raw), *args, **kwargs)
        elif isinstance(file_path_or_raw, str):
            with open(file_path_or_raw, 'wb') as f:
                return self._write(f, *args, **kwargs)
        else:
            raise TypeError('file_path_or_raw must be a file path or bytes object')