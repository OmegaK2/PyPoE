"""
Path     PyPoE/poe/file/_shared.py
Name     Shared classes/functions
Version  1.0.0a0
Revision $Id$
Author   [#OMEGA]- K2

INFO

Shared classes & functions for the file API. Used for exposing the same basic
API.


AGREEMENT

See PyPoE/LICENSE


TODO

...
"""

# =============================================================================
# Imports
# =============================================================================

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

# =============================================================================
# ABS
# =============================================================================

class AbstractFileReadOnly(object):
    def __init__(self):
        pass

    def _read(self, buffer, *args, **kwargs):
        raise NotImplementedError()

    def read(self, file_path_or_raw, *args, **kwargs):
        if isinstance(file_path_or_raw, BytesIO):
            return self._read(file_path_or_raw)
        elif isinstance(file_path_or_raw, bytes):
            return self._read(BytesIO(file_path_or_raw))
        elif isinstance(file_path_or_raw, str):
            with open(file_path_or_raw, 'rb') as f:
                return self._read(f)
        else:
            raise TypeError('file_path_or_raw must be a file path or bytes object')


class AbstractFile(AbstractFileReadOnly):

    def _write(self, buffer, *args, **kwargs):
        raise NotImplementedError()

    def write(self, file_path_or_raw, *args, **kwargs):
        if isinstance(file_path_or_raw, BytesIO):
            return self._write(file_path_or_raw)
        elif isinstance(file_path_or_raw, bytes):
            return self._write(BytesIO(file_path_or_raw))
        elif isinstance(file_path_or_raw, str):
            with open(file_path_or_raw, 'wb') as f:
                return self._write(f)
        else:
            raise TypeError('file_path_or_raw must be a file path or bytes object')