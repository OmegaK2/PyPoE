"""
Path     PyPoE/cli/core.py
Name     CLI Core
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO

CLI Core


AGREEMENT

See PyPoE/LICENSE


TODO

Virtual Terminal?
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import sys
import traceback
import warnings
from enum import Enum

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
    default = Style.RESET_ALL
    error = Style.BRIGHT + Fore.RED
    warning = Style.BRIGHT + Fore.YELLOW

class OutputHook(object):
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

    config.write()
    sys.exit(code)


def console(message, msg=Msg.default, rtr=False):
    f = msg.value + message + Msg.default.value
    if rtr:
        return f
    else:
        print(f)

