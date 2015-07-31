"""
Path     scripts/pypoe_exporter.py
Name     Export data from ggpk files
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO

Exports data from ggpk and dat files.


AGREEMENT

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# 3rd Party
from colorama import init

# self
from PyPoE.cli.exporter.core import main

# =============================================================================
# Setup
# =============================================================================

if __name__ == '__main__':
    init()
    main()
