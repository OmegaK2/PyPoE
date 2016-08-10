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

Exceptions & Warnings
-------------------------------------------------------------------------------

.. autoclass:: ParserError

.. autoclass:: ParserWarning
"""

# =============================================================================
# Imports
# =============================================================================

# Python
from io import BytesIO

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

    def get_read_buffer(self, file_path_or_raw, function, *args, **kwargs):
        """
        Will attempt to open the given file_path_or_raw in read mode and pass
        the buffer to the specified function.
        The function must accept at least one keyword argument called 'buffer'.

        Parameters
        ----------
        file_path_or_raw : BytesIO | bytes | str
            file path, bytes or buffer to read from
        args :
            Additional positional arguments to pass to the specified function
        kwargs :
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

        Parameters
        ----------
        file_path_or_raw : BytesIO | bytes | str
            file path, bytes or buffer to read from
        args :
            Additional positional arguments
        kwargs :
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

    def get_write_buffer(self, file_path_or_raw, function, *args, **kwargs):
        """
        Will attempt to open the given file_path_or_raw in write mode and pass
        the buffer to the specified function.
        The function must accept at least one keyword argument called 'buffer'.

        Parameters
        ----------
        file_path_or_raw : BytesIO | bytes | str
            file path, bytes or buffer to write to
        args :
            Additional positional arguments to pass to the specified function
        kwargs :
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

    def write(self, file_path_or_raw, *args, **kwargs):
        """
        Write the contents of file to the specified path or buffer.

        If a buffer or bytes was given, a buffer object with the new data should
        be returned.

        If a file path was given, the resulting data should be written to the
        specified file.

        Parameters
        ----------
        file_path_or_raw : BytesIO | bytes | str
            file path, bytes or buffer to write to
        args :
            Additional positional arguments
        kwargs :
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