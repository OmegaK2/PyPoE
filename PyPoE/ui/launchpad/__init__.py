"""
Launchpad

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/ui/launchpad/__init__.py                                   |
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
from PySide2.QtCore import *
from PySide2.QtWidgets import *

# self
from PyPoE.ui.shared import main

# =============================================================================
# Globals
# =============================================================================

__all__ = ['LaunchpadMainWindow', 'launchpad_main']

# =============================================================================
# Classes
# =============================================================================

class LaunchpadMainWindow(QMainWindow):

    child_closed = Signal(QWidget)

    def __init__(self, apps, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.apps = apps

        self.child_closed.connect(self._handle_closed_child)

        self.setWindowTitle(self.tr('PyPoE UI Launchpad'))

        frame = QFrame(parent=self)
        layout = QVBoxLayout()
        frame.setLayout(layout)

        layout.addWidget(QLabel(self.tr('Choose an application to start')))

        self.buttons = []
        self.instances = []
        for i, qmainwindow_cls in enumerate(apps):
            button = QPushButton(qmainwindow_cls.NAME)
            button.clicked.connect(self._wrap_clicked(i))
            layout.addWidget(button)
            self.buttons.append(button)
            self.instances.append(None)

        self.setCentralWidget(frame)

    def _wrap_clicked(self, i):
        def wrapped():
            return self.run_application(i)
        return wrapped

    def _handle_closed_child(self, qwidget):
        for i, item in enumerate(self.instances):
            if item == qwidget:
                break

        self.buttons[i].setEnabled(True)
        self.buttons[i].setText(qwidget.NAME)

    def run_application(self, i):
        self.buttons[i].setEnabled(False)
        self.buttons[i].setText(self.buttons[i].text() + self.tr(' (Running)'))
        qmainwindow = self.apps[i](parent=self)
        qmainwindow.show()
        qmainwindow.activateWindow()

        self.instances[i] = qmainwindow

# =============================================================================
# Functions
# =============================================================================


def launchpad_main(*args, **kwargs):
    main(LaunchpadMainWindow, *args, **kwargs)