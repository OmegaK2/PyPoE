"""
Shared Mixin Classes

Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | PyPoE/shared/mixins.py                                           |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
-------------------------------------------------------------------------------

Shared Mixin classes.

Agreement
-------------------------------------------------------------------------------

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import inspect

# 3rd-party

# self

# =============================================================================
# Globals
# =============================================================================

__all__ = ['ReprMixin']

# =============================================================================
# Classes
# =============================================================================


class ReprMixin(object):
    """
    Add to a class to get semi-universal repr of the form:

    ClassName<memoryaddr>(arg1=val1, ..., argn=valn)


    :cvar _REPR_PRIVATE_ATTRIBUTES: If set, also consider attributes with _
    :type _REPR_PRIVATE_ATTRIBUTES: bool

    :cvar _REPR_IGNORE_MISSING_ATTRIBUTES: In
    :type _REPR_IGNORE_MISSING_ATTRIBUTES: bool

    :cvar _REPR_ATTRIBUTES: In
    :type _REPR_ATTRIBUTES: dict[str, str]

    :cvar _REPR_ATTRIBUTES_IGNORE: In
    :type _REPR_ATTRIBUTES_IGNORE: set
    """

    _REPR_PRIVATE_ATTRIBUTES = False
    _REPR_IGNORE_MISSING_ATTRIBUTES = False
    _REPR_ATTRIBUTES = {}
    _REPR_ATTRIBUTES_IGNORE = set()

    def __get_repr_obj(self, name, test_private):
        if not hasattr(self, name):
            if test_private and self._REPR_PRIVATE_ATTRIBUTES:
                name = '_' + name
                if not hasattr(self, name):
                    return
            else:
                return

        return repr(getattr(self, name))

    def __repr__(self):
        args = []
        for name, parameter in inspect.signature(self.__init__).parameters.items():
            if parameter.kind != inspect.Parameter.POSITIONAL_OR_KEYWORD:
                continue

            if name in self._REPR_ATTRIBUTES_IGNORE:
                continue

            test_private = True
            if self._REPR_ATTRIBUTES:
                if name in self._REPR_ATTRIBUTES:
                    name = self._REPR_ATTRIBUTES[name]
                    test_private = False
                elif self._REPR_IGNORE_MISSING_ATTRIBUTES:
                    continue
            s = self.__get_repr_obj(name, test_private)

            if s is None:
                continue

            args.append('%s=%s' % (parameter.name, s))

        return '%s<%s>(%s)' % (
            self.__class__.__name__,
            hex(id(self)),
            ', '.join(args),
        )

# =============================================================================
# Functions
# =============================================================================
