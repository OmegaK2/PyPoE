"""
Path     PyPoE/lib/__init__.py
Name     Library init
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO

Library Init

AGREEMENT

See PyPoE/LICENSE


TODO

...
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import platform
import os
import warnings

# =============================================================================
# Globals
# =============================================================================

__all__ = [
    'APP_DIR', 'DATA_DIR', 'DAT_SPECIFICATION', 'DAT_SPECIFICATION_CONFIGSPEC',
]
__version__ = '1.0.0a0'

# =============================================================================
# Functions
# =============================================================================

def _get_app_dir():
    osys = platform.system()
    if osys == 'Windows':
        vars = ['APPDATA']
        subdir = 'PyPoE'
    elif osys == 'Linux':
        vars = ['HOME', 'PWD']
        subdir = '.PyPoE'
    else:
        raise RuntimeError('Unsupported Operating System')

    dir = None
    for var in vars:
        if var not in os.environ:
            continue
        dir = os.environ[var]
        if not os.path.exists(dir):
            continue
        break

    if dir is None:
        raise RuntimeError('Home/user directory not found')

    dir = os.path.join(dir, subdir)
    if not os.path.exists(dir):
        os.mkdir(dir)

    return dir

# =============================================================================
# Init
# =============================================================================

warnings.simplefilter('default', DeprecationWarning)
APP_DIR = _get_app_dir()
DATA_DIR = os.path.join(os.path.dirname(__file__), '_data')
DAT_SPECIFICATION = os.path.join(DATA_DIR, 'dat.specification.ini')
DAT_SPECIFICATION_CONFIGSPEC = os.path.join(DATA_DIR,
                                            'dat.specification.configspec.ini')

