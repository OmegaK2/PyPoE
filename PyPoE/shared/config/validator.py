"""
Additional validators 

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/shared/config/validator.py                                 |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Additional validators for configobj and validate.

Validator Function Generators
-------------------------------------------------------------------------------

.. autoclass:: IntEnumValidator

  .. automethod:: __call__

Validator Functions
-------------------------------------------------------------------------------

.. autofunction:: is_file

.. autofunction:: is_directory

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os
from enum import IntEnum

# 3rd Party
from validate import ValidateError, is_boolean

# =============================================================================
# Globals
# =============================================================================

__all__ = ['IntEnumValidator', 'is_directory', 'is_file', 'functions']


# =============================================================================
# Classes
# =============================================================================


class IntEnumValidator:
    """
    Class to create a dynamic validator for IntEnum classes
    """
    def __init__(self, enum, default=None):
        """

        Parameters
        ----------
        enum : :py:class:`enum.IntEnum`
            base enum class for this validator
        default : :py:class:`enum.IntEnum` | int | None
            default attribute of the enum
        Raises
        ------
        TypeError
            if enum is not an :py:class:`enum.IntEnum` class
        TypeError
            if default parameter is of invalid type

        """
        if not issubclass(enum, IntEnum):
            raise TypeError('enum must be an IntEnum subclass')
        self._enum = enum

        if default is None:
            self._default = None
        elif isinstance(default, enum):
            self._default = default
        elif isinstance(default, int):
            self._default = enum(int)
        else:
            raise TypeError('default must be a subtype of default')
        self._default = None

    def _get_enum_from_val(self, value):
        """
        Parameters
        ----------
        value : object
            the value to pass to the enum class from class creation

        Returns
        -------
        IntEnum
            IntEnum instance based on the class upon class creation

        Raises
        ------
        ValidateError
            if the the value isn't a member of the IntEnum class
        """
        try:
            return self._enum(value)
        except ValueError:
            raise ValidateError(
                '%s The value is not accepted by the enum.' %
                self._enum.__name__
            )

    def __call__(self, value):
        """
        Parameters
        ----------
        value : object
            The value to validate

        Returns
        -------
        IntEnum
            the int enum instance if successfully validated or None

        Raises
        ------
        ValidateError
            if the the value can't be validated
        """
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                # If the value was stored, it will be stored as
                # MyEnum.attribute
                #
                # This will get rid of the class portion for casting if present
                if value.startswith(self._enum.__name__ + '.'):
                    value = value[len(self._enum.__name__) + 1:]
                try:
                    value = getattr(self._enum, value)
                except AttributeError:
                    raise ValidateError(
                        'The value is neither an integer or a valid %s ' \
                        'attribute' % self._enum.__name__
                    )
            else:
                value = self._get_enum_from_val(value)
        elif isinstance(value, int):
            value = self._get_enum_from_val(value)
        elif value is None:
            return self._default
        else:
            raise ValidateError('Invalid type')

        return value


# =============================================================================
# Functions
# =============================================================================


def _exists(value, exists):
    if not isinstance(exists, bool):
        # Raises VdtTypeError on fail
        exists = is_boolean(exists)
    if exists and not os.path.exists(value):
        raise ValidateError('Path "%s" does not exist.' % value)


def is_file(value, *args, exists=True, allow_empty=False, **kwargs):
    """
    Checks whether the value is a valid file path (and optionally whether it
    exists).

    Parameters
    ----------
    value : object
        The value to validate
    exists : bool
        whether the file is required to exist to pass the validation check
    allow_empty : bool
        whether empty strings are allowed

    Returns
    -------
    IntEnum
        the int enum instance if successfully validated or None

    Raises
    ------
    ValidateError
        if the the value can't be validated
    """
    if allow_empty and value == '':
        return ''
    else:
        _exists(value, exists)
        if not os.path.isfile(value):
            raise ValidateError('"%s" is not a file.' % value)
        return value


def is_directory(value, *args, exists=True, allow_empty=False, **kwargs):
    """
    Checks whether the value is a valid directory path (and optionally whether
    it exists).

    Parameters
    ----------
    value : object
        The value to validate
    exists : bool
        whether the directory is required to exist to pass the validation check
    allow_empty : bool
        whether empty strings are allowed

    Returns
    -------
    IntEnum
        the int enum instance if successfully validated or None

    Raises
    ------
    ValidateError
        if the the value can't be validated
    """
    if allow_empty and value == '':
        return ''
    else:
        _exists(value, exists)
        if not os.path.isdir(value):
            raise ValidateError('"%s" is not a directory.' % value)
        return value

# =============================================================================
# Globals
# =============================================================================

functions = {
    'is_file': is_file,
    'is_directory': is_directory,
}
