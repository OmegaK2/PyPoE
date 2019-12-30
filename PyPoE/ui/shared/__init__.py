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
import os
import time

# 3rd-party
from PySide2.QtCore import *
from PySide2.QtWidgets import *

# self
from PyPoE.ui.shared.settings import SettingsWindow

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

    sig_log_message = Signal(str)

    def __init__(self, *args, app_name=NotImplemented, **kwargs):
        super().__init__(*args, **kwargs)

        self.NAME = app_name

        QCoreApplication.setApplicationName(app_name)
        QSettings.setDefaultFormat(QSettings.IniFormat)
        self.settings = QSettings()
        self.APP_ROOT_DIR = os.path.split(self.settings.fileName())[0]
        self.APP_DIR = os.path.join(self.APP_ROOT_DIR, app_name)
        if not os.path.exists(self.APP_DIR):
            os.makedirs(self.APP_DIR)

        # Setup logging
        self.sig_log_message.connect(self._write_log)

        # Still needs to be setup
        self.notification = QTextEdit(readOnly=True)
        self.notification.setFixedHeight(100)

        self.settings_window = SettingsWindow(parent=self)

    def _write_log(self, msg, notification=None):
        timef = time.strftime("%H:%M:%S - ")
        if notification is None:
            notification = msg
        self.statusBar().showMessage(timef + notification)
        self.notification.append(timef + msg)
        QApplication.instance().processEvents()

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
    app.setOrganizationName('PyPoE')
    app.installTranslator(translator)

    maininst = maincls(*args, **kwargs)
    maininst.show()

    sys.exit(app.exec_())
