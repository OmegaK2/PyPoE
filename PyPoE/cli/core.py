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

# 3rd Party
from colorama import Fore, Style

# =============================================================================
# Globals
# =============================================================================

__all__ = ['run']

err_fmt = Style.BRIGHT + Fore.RED + '%s' + Style.RESET_ALL
warn_fmt = Style.BRIGHT + Fore.YELLOW + '%s' + Style.RESET_ALL

# =============================================================================
# Classes
# =============================================================================

class OutputHook(object):
    def __init__(self):
        self._orig_format_warning = warnings.formatwarning
        warnings.formatwarning = self.format_warning

    def format_warning(self, message, category, filename, lineno, line=None):
        kwargs = {
            'message': message,
            'category': category.__name__,
            'filename': filename,
            'lineno': lineno,
            'line': line,
        }
        f = "%(filename)s:%(lineno)s:\n%(category)s: %(message)s\n" % kwargs
        return warn_fmt % f


# =============================================================================
# Functions
# =============================================================================

def run(parser, config):
    OutputHook()
    args = parser.parse_args()
    if hasattr(args, 'func'):
        try:
            code = args.func(args)
        except Exception as e:
            print(err_fmt % traceback.format_exc())
            code = -1
    else:
        parser.print_help()
        code = 0

    config.write()
    sys.exit(code)