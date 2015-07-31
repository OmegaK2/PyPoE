"""
Path     scripts/ggpkui.py
Name     GGPK User Interface
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

# Default Imports
import sys

# 3rd-Party Imports
from PySide.QtCore import *
from PySide.QtGui import *

# Package Imports
from PyPoE.ui.ggpk_viewer.core import MainWindow

# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
    translator = QTranslator()
    translator.load('i18n/en_US')
    app = QApplication(sys.argv)
    app.installTranslator(translator)
    frame = MainWindow(app)
    frame.run()