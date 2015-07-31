"""
Path     PyPoE/shared/config/validator.py
Name     Additional validators 
Version  1.0.0
Revision $Id$
Author   [#OMEGA]- K2

INFO

Additional validators for configobj and validate.


AGREEMENT

See PyPoE/LICENSE


TODO

...
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os

# 3rd Party
from validate import ValidateError, is_boolean

# =============================================================================
# Globals
# =============================================================================

__all__ = ['is_directory', 'is_file', 'functions']

# =============================================================================
# Functions
# =============================================================================

def _exists(value, exists):
    if not isinstance(exists, bool):
        # Raises VdtTypeError on fail
        exists = is_boolean(exists)
    if exists and not os.path.exists(value):
        raise ValidateError('Path "%s" does not exist.' % value)

def is_file(value, *args, exists=True, **kwargs):
    _exists(value, exists)
    if not os.path.isfile(value):
        raise ValidateError('"%s" is not a file.' % value)
    return value
    
def is_directory(value, *args, exists=True, **kwargs):
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
