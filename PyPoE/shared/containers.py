"""
special containers

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/shared/containers.py                                       |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

special containers

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
from collections.abc import Iterable

# =============================================================================
# Globals
# =============================================================================

__all__ = ['Record', 'TypedContainerMeta', 'TypedContainerMixin', 'TypedList']

# =============================================================================
# Classes
# =============================================================================

class Record:
    def __str__(self):
        return repr(self)

    def __repr__(self):
        out = []
        for attr in self.__slots__:
            out.append('%s=%s' % (attr, repr(getattr(self, attr))))

        return '%s(%s)' % (self.__class__.__name__, ', '.join(out))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return object.__eq__(self, other)

        for attr in self.__slots__:
            if not getattr(self, attr) == getattr(other, attr):
                return False

        return True

    def __ne__(self, other):
        if not isinstance(other, self.__class__):
            return object.__eq__(self, other)

        for attr in self.__slots__:
            if not getattr(self, attr) != getattr(other, attr):
                return False

        return True


class TypedContainerMeta(type):
    def __new__(cls, name, bases, attrs):
        if 'ACCEPTED_TYPES' not in attrs:
            raise ValueError('ACCEPTED_TYPES is required.')

        if attrs['ACCEPTED_TYPES'] is None:
            raise ValueError('ACCEPTED_TYPES must not be None.')

        if isinstance(attrs['ACCEPTED_TYPES'], type):
            attrs['ACCEPTED_TYPES'] = (attrs['ACCEPTED_TYPES'], )
        elif isinstance(attrs['ACCEPTED_TYPES'], Iterable):
            for t in attrs['ACCEPTED_TYPES']:
                if not isinstance(t, type):
                    raise ValueError('Every type in ACCEPTED_TYPES Iterable must be a type')
        else:
            raise ValueError('ACCEPTED_TYPES must be a type or Iterable of types')

        return type.__new__(cls, name, bases, attrs)


class TypedContainerMixin:

    ACCEPTED_TYPES = None

    def _is_cls(self, obj):
        if not isinstance(obj, self.__class__):
            raise TypeError(
                '"%s" instance can only be added to another "%s" instance.' % (
                    self.__class__.__name__,
                    self.__class__.__name__,
                )
            )

    def _is_acceptable(self, obj):
        if not isinstance(obj, self.ACCEPTED_TYPES):
            raise TypeError('"%s" instance only accepts "%s" instances.' % (
                self.__class__.__name__,
                ', '.join([t.__name__ for t in self.ACCEPTED_TYPES]),
            ))


class TypedList(list, TypedContainerMixin):
    def __add__(self, other):
        self._is_cls(other)
        list.__add__(self, other)

    def __iadd__(self, other):
        self._is_cls(other)
        list.__iadd__(self, other)

    def __setitem__(self, key, value):
        self._is_acceptable(value)
        list.__setattr__(self, key, value)

    def append(self, p_object):
        self._is_acceptable(p_object)
        list.append(self, p_object)

    def extend(self, iterable):
        for item in iterable:
            self._is_acceptable(item)
        list.extend(self, iterable)

    def insert(self, index, p_object):
        self._is_acceptable(p_object)
        list.insert(self, p_object)