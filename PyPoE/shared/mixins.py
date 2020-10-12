"""
Shared Mixin Classes

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/shared/mixins.py                                           |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Shared Mixin classes.

Agreement
===============================================================================

See PyPoE/LICENSE

Documentation
===============================================================================

Classes
-------------------------------------------------------------------------------

.. autoclass:: ReprMixin

"""

# =============================================================================
# Imports
# =============================================================================

# Python
import inspect
from collections import OrderedDict

# 3rd-party

# self

# =============================================================================
# Globals
# =============================================================================

__all__ = ['ReprMixin']

# =============================================================================
# Classes
# =============================================================================


class ReprMixin:
    """
    Add to a class to get semi-universal repr of the form:

    ClassName<memoryaddr>(arg1=val1, ..., argn=valn, extrakey1=extraval1, ...,
    extrakeyn=extravaln)


    :cvar _REPR_PRIVATE_ATTRIBUTES: If set, also consider attributes with _
    :type _REPR_PRIVATE_ATTRIBUTES: bool

    :cvar _REPR_ARGUMENTS_IGNORE_MISSING: Whether to ignore missing attributes
    if _REPR_ARGUMENTS_TO_ATTRIBUTES is specified
    :type _REPR_ARGUMENTS_IGNORE_MISSING: bool

    :cvar _REPR_ARGUMENTS_TO_ATTRIBUTES: Match arguments against this directory
    and if found as key, use the value to determine the instance attribute
    to retrieve the value for the attribute
    :type _REPR_ARGUMENTS_TO_ATTRIBUTES: dict[str, str]

    :cvar _REPR_ARGUMENTS_IGNORE: Ignore these arguments entirely
    :type _REPR_ARGUMENTS_IGNORE: set

    :cvar _REPR_EXTRA_ATTRIBUTES: Adds those extra attributes, even if they are
    not __init__ arguments.
    The keys are used for the name displayed, the values for retrieving the
    attribute from the instance. If the value is None, the key is used instead.
    :type _REPR_EXTRA_ATTRIBUTES: OrderedDict[str, str]
    """

    _REPR_PRIVATE_ATTRIBUTES = False
    _REPR_ARGUMENTS_IGNORE_MISSING = False
    _REPR_ARGUMENTS_TO_ATTRIBUTES = {}
    _REPR_ARGUMENTS_IGNORE = set()
    _REPR_EXTRA_ATTRIBUTES = OrderedDict()

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
            if parameter.kind == inspect.Parameter.POSITIONAL_ONLY:
                continue

            if name in self._REPR_ARGUMENTS_IGNORE:
                continue

            test_private = True
            if self._REPR_ARGUMENTS_TO_ATTRIBUTES:
                if name in self._REPR_ARGUMENTS_TO_ATTRIBUTES:
                    name = self._REPR_ARGUMENTS_TO_ATTRIBUTES[name]
                    test_private = False
                elif self._REPR_ARGUMENTS_IGNORE_MISSING:
                    continue
            s = self.__get_repr_obj(name, test_private)

            if s is None:
                continue

            args.append('%s=%s' % (parameter.name, s))

        for k, v in self._REPR_EXTRA_ATTRIBUTES.items():
            args.append('%s=%s' % (k, self.__get_repr_obj(v or k, False)))

        return '%s<%s>(%s)' % (
            self.__class__.__name__,
            hex(id(self)),
            ', '.join(args),
        )

# =============================================================================
# Functions
# =============================================================================
