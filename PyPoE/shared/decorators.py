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

# =============================================================================
# Functions
# =============================================================================

def deprecated(function):
    @functools.wraps(function)
    def deprecated_function(*args, **kwargs):
        warnings.warn(
            'Use of %s is deprecated' % function.__name__, DeprecationWarning
        )

        return function(*args, **kwargs)

    return deprecated_function
