"""
Exporter Core

Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/core.py                                       |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
-------------------------------------------------------------------------------

Exporter main function(s).

Agreement
-------------------------------------------------------------------------------

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import argparse

# self
from . import config
from PyPoE.poe.constants import VERSION, DISTRIBUTOR
from PyPoE.cli.core import run
from PyPoE.cli.handler import ConfigHandler, SetupHandler
from PyPoE.cli.exporter.dat import DatHandler
from PyPoE.cli.exporter.wiki.core import WikiHandler

# =============================================================================
# class
# =============================================================================

# =============================================================================
# Functions
# =============================================================================


def main():
    # Setup
    main_parser = argparse.ArgumentParser()
    main_sub = main_parser.add_subparsers()

    spec = 'integer(min=%(min)s, max=%(max)s, default=%(default)s)'
    kwargs = {
        'min': 1,
        'max': VERSION.ALL.value,
        'default': VERSION.DEFAULT.value,
    }
    config.add_option('version', spec % kwargs)

    kwargs = {
        'min': 1,
        'max': DISTRIBUTOR.ALL.value,
        'default': DISTRIBUTOR.DEFAULT.value,
    }
    config.add_option('distributor', spec % kwargs)

    DatHandler(main_sub)
    WikiHandler(main_sub)
    # In that order..
    SetupHandler(main_sub, config)
    ConfigHandler(main_sub, config)

    # Execute
    run(main_parser, config)

if __name__ == '__main__':
    main()
