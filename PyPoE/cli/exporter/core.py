"""
Exporter Core

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/core.py                                       |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Exporter main function(s) and entry point.

The following calls are equivalent:

.. code-block:: none

    pypoe_exporter
    python PyPoE/cli/exporter/core.py


Agreement
===============================================================================

See PyPoE/LICENSE

Documentation
===============================================================================

.. autofunction:: main
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import argparse

# 3rd party

# self
from PyPoE.shared.config.validator import IntEnumValidator
from PyPoE.poe.constants import VERSION, DISTRIBUTOR
from PyPoE.cli.core import run
from PyPoE.cli.handler import ConfigHandler, SetupHandler
from PyPoE.cli.exporter import config
from PyPoE.cli.exporter.dat import DatHandler
from PyPoE.cli.exporter.wiki.core import WikiHandler

# =============================================================================
# Classes
# =============================================================================


# =============================================================================
# Functions
# =============================================================================


def setup_config():
    config.validator.functions.update({
        'is_version': IntEnumValidator(
            enum=VERSION,
        ),
        'is_distributor': IntEnumValidator(
            enum=DISTRIBUTOR,
        )
    })

    config.add_option('version', 'is_version(default=%s)' %
                      VERSION.DEFAULT.value)
    config.add_option('distributor', 'is_distributor(default=%s)' %
                      DISTRIBUTOR.DEFAULT.value)
    config.add_option(
        'ggpk_path', 'is_file(default="", exists=True, allow_empty=True)'
    )
    config.add_option('language',
                      'option("English", "French", "German", "Portuguese",'
                      '"Russian", "Spanish", "Thai", "Simplified Chinese",'
                      '"Traditional Chinese", "Korean", default="English")')


def main():
    """
    Entry point for the CLI PyPoE exporter
    """
    # Setup
    main_parser = argparse.ArgumentParser()
    main_sub = main_parser.add_subparsers()

    setup_config()

    DatHandler(main_sub)
    WikiHandler(main_sub)
    # In that order..
    SetupHandler(main_sub, config)
    ConfigHandler(main_sub, config)

    # Execute
    run(main_parser, config)

if __name__ == '__main__':
    main()
