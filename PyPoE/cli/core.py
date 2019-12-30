"""
CLI Core

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/core.py                                                |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

CLI core utility classes and functions.

Agreement
===============================================================================

See PyPoE/LICENSE

TODO-List
===============================================================================

- Virtual Terminal?
- console output formatting/linebreaks

Documentation
===============================================================================

Classes
-------------------------------------------------------------------------------

.. autoclass:: Msg

.. autoclass:: OutputHook

Functions
-------------------------------------------------------------------------------

.. autofunction:: run

.. autofunction:: console
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import sys
import traceback
import warnings
from enum import Enum
from time import strftime

# 3rd Party
from colorama import Style, Fore

# =============================================================================
# Globals
# =============================================================================

__all__ = ['Msg', 'OutputHook', 'run', 'console']

# =============================================================================
# Classes
# =============================================================================


class Msg(Enum):
    """
    Used for :py:func`console` function.

    Parameters
    ----------
    default
        default
    warning
        yellow warning message
    error
        red error message
    """
    default = Style.RESET_ALL
    error = Style.BRIGHT + Fore.RED
    warning = Style.BRIGHT + Fore.YELLOW


class OutputHook:
    """
    Warning hook to reformat / restyle warning messages properly.
    """
    def __init__(self, show_warning):
        self._orig_show_warning = show_warning
        self._orig_format_warning = warnings.formatwarning
        warnings.formatwarning = self.format_warning
        warnings.showwarning = self.show_warning

    def format_warning(self, message, category, filename, lineno, line=None):
        kwargs = {
            'message': message,
            'category': category.__name__,
            'filename': filename,
            'lineno': lineno,
            'line': line,
        }
        f = "%(filename)s:%(lineno)s:\n%(category)s: %(message)s\n" % kwargs
        return console(f, msg=Msg.warning, rtr=True)
    #
    def show_warning(self, *args, **kwargs):
        self._orig_show_warning(*args, **kwargs)

# =============================================================================
# Functions
# =============================================================================


def run(parser, config):
    """
    Run the CLI application with the given parser and config.

    It will take care of handling parsing the arguments and calling the
    appropriate function and print any tracebacks that occurred during the call.

    Saves config and exits the python client.

    .. warning::
        This function will exist the python client on completion

    Parameters
    ----------
    parser : argparse.ArgumentParser
        assembled argument parser for argument handling
    config : ConfigHelper
        config object to use for the CLI application wide config
    """
    args = parser.parse_args()
    if hasattr(args, 'func'):
        try:
            code = args.func(args)
        except Exception as e:
            console(traceback.format_exc(), msg=Msg.error)
            code = -1
    else:
        parser.print_help()
        code = 0

    config.validate(config.validator)
    config.write()
    sys.exit(code)


def console(message, msg=Msg.default, rtr=False, raw=False):
    """
    Send the specified messge to console

    Parameters
    ----------
    message : str
        Message to send
    msg : Msg
        Message type
    rtr : bool
        Return message instead of printing
    raw : bool
        Skip timestamp/colour formatting

    Returns
    -------
    None or str
        if rtr is specified returns formatted message, None otherwise
    """
    if raw:
        f = message
    else:
        f = msg.value + strftime('%X ') + message + Msg.default.value
    if rtr:
        return f
    else:
        print(f)

