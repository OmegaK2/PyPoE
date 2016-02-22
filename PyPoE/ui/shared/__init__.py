"""
Shared UI code

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/ui/shared/__init__.py                                      |
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
import sys

# 3rd-party
from PySide.QtCore import *
from PySide.QtGui import *

# self

# =============================================================================
# Globals
# =============================================================================

__all__ = ['SharedMainWindow', 'main']

# =============================================================================
# Classes
# =============================================================================


class SharedMainWindow(QMainWindow):
    """
    Shared Window class for use in sub applications to be launched from the
    Launchpad.
    """

    name = ''

    def closeEvent(self, *args, **kwargs):
        p = self.parent()
        if p is None:
            return

        p.child_closed.emit(self)

# =============================================================================
# Functions
# =============================================================================


def main(maincls, *args, **kwargs):
    """
    Load translations/app and start the qt application.

    Parameters
    ----------
    maincls
        Class to instantiate with the given arguments and keywords
    """
    translator = QTranslator()
    translator.load('i18n/en_US')

    app = QApplication(sys.argv)
    app.installTranslator(translator)

    maininst = maincls(*args, **kwargs)
    maininst.show()

    sys.exit(app.exec_())
