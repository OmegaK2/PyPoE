"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/file/specification/__init__.py                         |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

.. autofunction:: load
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import importlib
from importlib.machinery import SourceFileLoader

# 3rd-party

# self
from PyPoE.poe.constants import VERSION

# =============================================================================
# Globals
# =============================================================================

__all__ = ['load']

# =============================================================================
# Globals
# =============================================================================


def load(path=None, version=VERSION.DEFAULT, reload=False, validate=None):
    """
    Loads a specification from a python module that can be used for the dat
    files.
    The file must implement the classes from
    :py:mod:`PyPoE.poe.file.specification.fields` and expose the specification
    with a variable "specification" for this to work properly.

    Since this function is using python imports specifications are
    automatically cached once loaded. If using a cached version is not desired
    set the reload parameter to True.

    .. warning::
        Please note that many usages of the reload function will cause a memory
        leak since python does not remove old modules from it's cache.

    Parameters
    ----------
    path :  str
        If specified, read the specified python module as specification
    version : constants.VERSION
        Version of the game to load the specification for; only works if
        path is not specified.
    reload : bool
        Whether to reload the specified specification.
    validate : bool or None
        Whether additional validation will be run on the Specification.
        By default (None), this will only occur when custom specifications are
        loaded and not when default specifications are loaded.

    Returns
    -------
    :class:`ConfigObj`
        returns the ConfigObj of the read file.


    Raises
    ------
    ValueError
        if version passed is not valid
    SpecificationError
        if validation is enabled and any issues occur
    """
    if path is None:
        if validate is None:
            validate = False

        if version in (VERSION.STABLE, VERSION.BETA, VERSION.ALPHA):
            module = importlib.import_module(
                'PyPoE.poe.file.specification.data.%s' %
                str(version).split('.')[1].lower()
            )
        else:
            raise ValueError(
                'Unknown version or version currently not supported: %s' %
                version
            )
    else:
        if validate is None:
            validate = True

        module = SourceFileLoader('', path).load_module()

    if reload:
        importlib.reload(module)

    if validate:
        module.specification.validate()

    return module.specification
