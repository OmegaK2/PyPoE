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
from enum import Enum

# 3rd Party
from colorama import Style, Fore

# =============================================================================
# Globals
# =============================================================================

__all__ = ['Msg', 'run', 'console']

# =============================================================================
# Classes
# =============================================================================

class Msg(Enum):
    default = Style.RESET_ALL
    error = Style.BRIGHT + Fore.RED
    warning = Style.BRIGHT + Fore.YELLOW

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

