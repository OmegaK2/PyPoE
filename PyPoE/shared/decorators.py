"""
Path     PyPoE/shared/decorators.py
Name     Decorators
Version  1.0.0a0
Revision $Id$
Author   Omega_K2

INFO

Utility decorators.


AGREEMENT

See PyPoE/LICENSE


TODO

...
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

class DeprecationDecorator():
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

# =============================================================================
# Functions
# =============================================================================

def deprecated(*args, **kwargs):
    if len(args) == 1 and callable(args[0]):
        return DeprecationDecorator()(args[0])
    else:
        return DeprecationDecorator(*args, **kwargs)