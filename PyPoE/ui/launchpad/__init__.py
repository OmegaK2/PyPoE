"""
Launchpad

Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | PyPoE/ui/launchpad/__init__.py                                   |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
-------------------------------------------------------------------------------



Agreement
-------------------------------------------------------------------------------

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

__all__ = []

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
        for i, qmainwindow in enumerate(apps):
            button = QPushButton(qmainwindow.name)
            button.clicked.connect(lambda: self.run_application(i))
            layout.addWidget(button)
            self.buttons.append(button)
            self.instances.append(None)

        self.setCentralWidget(frame)

    def _handle_closed_child(self, qwidget):
        for i, item in enumerate(self.instances):
            if item == qwidget:
                break

        self.buttons[i].setEnabled(True)
        self.buttons[i].setText(qwidget.name)

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

def main(apps):
    translator = QTranslator()
    translator.load('i18n/en_US')

    app = QApplication(sys.argv)
    app.installTranslator(translator)

    launchpad = LaunchpadMainWindow(apps)
    launchpad.show()

    return app.exec_()