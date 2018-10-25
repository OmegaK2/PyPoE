"""


Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/ui/shared/table_context_menus.py                           |
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

# 3rd-party
from PySide2.QtCore import *
from PySide2.QtWidgets import *

# self

# =============================================================================
# Globals
# =============================================================================

__all__ = ['TableContextReadOnlyMenu']

# =============================================================================
# Classes
# =============================================================================


class TableContextReadOnlyMenu(QMenu):
    def __init__(self, *args, **kwargs):
        QMenu.__init__(self, *args, **kwargs)

        qtableview = self.parent()
        qtableview.setContextMenuPolicy(Qt.CustomContextMenu)
        qtableview.customContextMenuRequested.connect(self.popup)

        self.action_copy = self.addAction("Copy", self.copy)

        self.point = None

    def _handle_data(self, data):
        return str(data)

    def copy(self, *args, **kwargs):
        qmodelindexlist = self.parent().selectionModel().selectedIndexes()

        rmin, rmax, cmin, cmax = 2**32, 0, 2**32, 0

        for qmodelindex in qmodelindexlist:
            rid = qmodelindex.row()
            cid = qmodelindex.column()

            rmin = min(rmin, rid)
            rmax = max(rmax, rid)
            cmin = min(cmin, cid)
            cmax = max(cmax, cid)

        # +1 to offset for the minimum size
        matrix = [[None for j in range(0, cmax-cmin+1)] for i in range(0, rmax-rmin+1)]

        for qmodelindex in qmodelindexlist:
            matrix[qmodelindex.row()-rmin][qmodelindex.column()-cmin] = self._handle_data(qmodelindex.data())

        # Transform the matrix into a string
        out = []
        for row in matrix:
            out.append('\t'.join(['' if cell is None else cell for cell in row]))

        QApplication.clipboard().setText('\n'.join(out))

    def popup(self, point, *args, **kwargs):
        self.point = point
        QMenu.popup(self, self.parent().mapToGlobal(point))


# =============================================================================
# Functions
# =============================================================================
