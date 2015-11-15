"""
Decorators

Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | PyPoE/shared/decorators.py                                       |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
-------------------------------------------------------------------------------

Utility decorators.

Agreement
-------------------------------------------------------------------------------

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import functools
import warnings

# 3rd-party

# self

# =============================================================================
# Globals
# =============================================================================

__all__ = ['deprecated']

# =============================================================================
# Classes
# =============================================================================

class DeprecationDecorator(object):
    def __init__(self, message='Use of %(func)s is deprecated'):
        self.message = message

    def __call__(self, function):
        @functools.wraps(function)
        def deprecated_function(*args, **kwargs):
            warnings.warn(
                self.message % {
                    'func': function.__name__,
                }, DeprecationWarning, stacklevel=2,
            )

            return function(*args, **kwargs)

        return deprecated_function


class DocStringDecorator(object):
    """
    Decorator for docstring modifications.
    """
    def __init__(self, prepend='', append='', doc=None):
        """
        :param prepend: String to prepend to the docstring
        :type prepend: str

        :param append: String to append to the doctsting
        :type append: str

        :param doc: Docstring to use. If an object that doesn't inherit from str
        is supplied, use object's docstring.
        :type doc: None, str or object
        """
        self.append = append
        self.prepend = prepend
        self.doc = doc

    def __call__(self, function):
        @functools.wraps(function)
        def deprecated_function(*args, **kwargs):
            return function(*args, **kwargs)

        if self.doc is None:
            docs = deprecated_function.__doc__
        elif isinstance(self.doc, str):
            docs = self.doc
        else:
            docs = self.doc.__doc__

        if docs is None:
            docs = ''

        docs = self.prepend + docs + self.append

        if docs != '':
            deprecated_function.__doc__ = docs

        return deprecated_function

# =============================================================================
# Functions
# =============================================================================

def _make_callable(cls):
    @functools.wraps(cls)
    def call(*args, **kwargs):
        if len(args) == 1 and callable(args[0]):
            return cls()(args[0])
        else:
            return cls(*args, **kwargs)
    return call

deprecated = _make_callable(DeprecationDecorator)
doc = _make_callable(DocStringDecorator)
