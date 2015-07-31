"""
Path     PyPoE/cli/exporter/core.py
Name     GGPK User Interface Classes
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO

Creates a qt User Interface to browse GGPK files.


AGREEMENT

See PyPoE/LICENSE


TODO

...
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import argparse
import sys

# self
from . import config
from PyPoE.poe.path import PoEPath
from PyPoE.cli.core import run
from PyPoE.cli.handler import ConfigHandler, SetupHandler
from PyPoE.cli.exporter.wiki import WikiHandler

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
        'min': min(PoEPath.VERSIONS),
        'max': PoEPath.VERSION_ALL,
        'default': PoEPath.VERSION_DEFAULT,
    }
    config.add_option('version', spec % kwargs)

    kwargs = {
        'min': min(PoEPath.DISTRIBUTORS),
        'max': PoEPath.DISTRIBUTOR_ALL,
        'default': PoEPath.DISTRIBUTOR_DEFAULT,
    }
    config.add_option('distributor', spec % kwargs)

    WikiHandler(main_sub)
    # In that order..
    SetupHandler(main_sub, config)
    ConfigHandler(main_sub, config)

    # Execute
    run(main_parser, config)
