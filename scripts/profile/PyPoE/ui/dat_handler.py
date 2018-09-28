"""


Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | scripts/profile/PyPoE/ui/dat_handler.py                          |
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
import cProfile
#from line_profiler import LineProfiler

from PySide2.QtCore import *
from PySide2.QtWidgets import *

# self
from PyPoE.ui.shared.file.handler import DatStyle
from PyPoE.ui.shared.file.manager import FileDataManager

# =============================================================================
# Globals
# =============================================================================

__all__ = []

# =============================================================================
# Classes
# =============================================================================

# =============================================================================
# Functions
# =============================================================================
if __name__ == '__main__':
    '''profiler = LineProfiler(
        DatStyle.sizeHint,
        DatStyle._get_text,
        DatStyle._show_value,
    )'''
    translator = QTranslator()
    translator.load('i18n/en_US')
    app = QApplication(sys.argv)
    app.installTranslator(translator)
    frame = QMainWindow()

    f = 'CharacterStartItems.dat'
    with open('C:/Temp/Data/' + f, 'rb') as file:
        data = file.read()
    #for item in dir(o):
     #   print(item, getattr(o, item))
    fm = FileDataManager(None)
    h = fm.get_handler(f)
    #profiler.run('w = h.get_widget(data, f, parent=frame)')
    #profiler.print_stats()
    w = h.get_widget(data, f, parent=frame)
    frame.setCentralWidget(w)

    frame.show()
    app.exec_()
