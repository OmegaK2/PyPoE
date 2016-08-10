"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | genmodules.py                                                    |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================



Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os
import re

# 3rd-party

# self
import PyPoE

# =============================================================================
# Globals
# =============================================================================

__all__ = []

# =============================================================================
# Classes
# =============================================================================

# =============================================================================
# Functions
# =============================================================================

if __name__ == '__main__':
    curdir = os.path.split(__file__)[0]

    outpaths = []

    for dirpath, dirnames, filenames in os.walk(PyPoE.DIR):
        for item in list(dirnames):
            if item.startswith('.') or item.startswith('__pycache'):
                dirnames.remove(item)

        for item in list(filenames):
            if item.startswith('.') or not item.endswith('.py'):
                filenames.remove(item)

        pypoe_path = dirpath.replace(PyPoE.DIR, 'PyPoE').strip('\\/')
        for filename in filenames:
            path = re.split(r'\\|/', os.path.join(pypoe_path, filename))
            if path[-1] == '__init__.py':
                del path[-1]

            path[-1] = path[-1].replace('.py', '')

            outpaths.append('.'.join(path))

    outpaths.sort()
    with open(os.path.join(curdir, 'source', 'autosummary.rst'), 'w') as f:
        f.write('.. autosummary::\n')
        f.write('    :toctree: _autosummary\n    \n')
        for path in outpaths:
            f.write('    %s\n' % path)
