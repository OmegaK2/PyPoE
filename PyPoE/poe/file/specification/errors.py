"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/file/specification/errors.py                           |
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

.. autoclass:: SpecificationError

.. autoclass:: SpecificationError.ERRORS

.. autoclass:: SpecificationWarning
"""

# =============================================================================
# Imports
# =============================================================================

# Python
from enum import IntEnum

# 3rd-party

# self

# =============================================================================
# Globals
# =============================================================================

__all__ = ['SpecificationError', 'SpecificationWarning']

# =============================================================================
# Exceptions & Warnings
# =============================================================================


class SpecificationError(ValueError):
    """
    SpecificationErrors are raised to indicate there is a problem with the
    specification compared to the data.

    Unlike most errors, they are raised with an error code and the error
    message. The error code can be used to capture specific errors more
    accurately.
    """

    class ERRORS(IntEnum):
        """
        Numeric meaning:

        * 1xxx - indicates issues with format of fields
        * 2xxx - indicates issues with format of virtual fields
        * 3xxx - indicates issues at runtime

        Attributes
        ----------
        INVALID_FOREIGN_KEY_FILE
            Foreign key file does not exist
        INVALID_FOREIGN_KEY_ID
            Foreign key with the specified id does not exist
        INVALID_ARGUMENT_COMBINATION
            Invalid combination of multiple arguments; i.e. when they can't be
            used together
        INVALID_ENUM_NAME
            Enum does not exist in :py:mod:`PyPoE.poe.constants`
        VIRTUAL_KEY_EMPTY
            Virtual key does not have fields defined
        VIRTUAL_KEY_DUPLICATE
            Virtual key is a duplicate of a regular key
        VIRTUAL_KEY_INVALID_KEY
            Invalid fields specified for the virtual key
        VIRTUAL_KEY_INVALID_DATA_TYPE
            Invalid data type(s) in the target fields
        RUNTIME_MISSING_SPECIFICATION
            No specification found in the specification format used for the
            function call
        RUNTIME_MISSING_FOREIGN_KEY
            A single foreign key reference could not be resolved
        RUNTIME_ROWSIZE_MISMATCH
            The row size in the specification doesn't match the real data row
            size
        """
        INVALID_FOREIGN_KEY_FILE = 1000
        INVALID_FOREIGN_KEY_ID = 1001
        INVALID_ARGUMENT_COMBINATION = 1002
        INVALID_ENUM_NAME = 1003
        VIRTUAL_KEY_EMPTY = 2000
        VIRTUAL_KEY_DUPLICATE = 2001
        VIRTUAL_KEY_INVALID_KEY = 2002
        VIRTUAL_KEY_INVALID_DATA_TYPE = 2003
        RUNTIME_MISSING_SPECIFICATION = 3000
        RUNTIME_MISSING_FOREIGN_KEY = 3001
        RUNTIME_ROWSIZE_MISMATCH = 3002

    def __init__(self, code, msg):
        super().__init__()
        self.code = self.ERRORS(code)
        self.msg = msg

    def __str__(self):
        return '%s: %s' % (repr(self.code), self.msg)


class SpecificationWarning(UserWarning):
    pass