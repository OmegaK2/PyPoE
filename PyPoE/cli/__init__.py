"""
Path     PyPoE/cli/__init__.py
Name     CLI Package Init
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO

CLI Package init


AGREEMENT

See PyPoE/LICENSE


TODO

Excepthook?
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import warnings

# 3rd Party
from colorama import init

# self
from PyPoE.cli.core import console, Msg

# =============================================================================
# Globals
# =============================================================================

__all__ = ['Color']

# =============================================================================
# Bugfixes
# =============================================================================
# pywikibot hooks into the output and we really don't want that
_orig_show_warning = warnings.showwarning
try:
    import pywikibot
except:
    pass
init()

# =============================================================================
# Imports
# =============================================================================

class OutputHook(object):
    def __init__(self):
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
        _orig_show_warning(*args, **kwargs)

# =============================================================================
# Init
# =============================================================================

OutputHook()