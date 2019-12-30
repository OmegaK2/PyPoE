"""
QT classes for handling GGPK files

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/ui/shared/file/ggpk.py                                     |
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

Documentation
===============================================================================

Public API
-------------------------------------------------------------------------------

Interal API
-------------------------------------------------------------------------------
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os
from functools import wraps

# 3rd-party
from PySide2.QtCore import *
from PySide2.QtWidgets import *

# self
from PyPoE.poe.constants import DISTRIBUTOR, VERSION
from PyPoE.poe.path import PoEPath
from PyPoE.poe.file.ggpk import GGPKFile

# =============================================================================
# Globals
# =============================================================================

__all__ = []

# =============================================================================
# Classes
# =============================================================================


class GGPKOpenAction(QAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setText(self.tr('Open GGPK'))
        self.setStatusTip(self.tr('Open a content.ggpk file'))
        self.triggered.connect(self._open_ggpk)

    def _get_version(self):
        return VERSION.DEFAULT

    def _open_ggpk(self):
        """

        Returns
        -------
        GGPKThread or None
            Returns GGPKThread if successful, none otherwise
        """
        # TODO replace with config / last path
        paths = PoEPath(version=self._get_version(),
                        distributor=DISTRIBUTOR.GGG).get_installation_paths()

        # Use the first found path
        if paths:
            dir = os.path.join(paths[0].path, 'content.ggpk')
        else:
            dir = '.'

        p = self.parent()

        file = QFileDialog.getOpenFileName(
            p,
            self.tr("Open GGPK"),
            dir,
            self.tr("GGPK Files (*.ggpk)")
        )
        # User Aborted
        if not file[0]:
            return

        file_path = file[0]

        return GGPKThread(file_path, parent=p)


class GGPKThread(QThread):
    sig_update_progress = Signal(str, int)

    def __init__(self, file_path, *args, **kwargs):
        QThread.__init__(self, *args, **kwargs)
        self._file_path = file_path
        self.ggpk_file = None
        self._size = 0

        self.sig_update_progress.connect(self._progress_updater)

        self.progress_bar = GGPKProgressDialog('')

    def _progress_ggpk(self, func):
        """
        Hook for GGPKFile._read_record
        """
        fm = self.parent()

        @wraps(func)
        def temp(*args, **kwargs):
            if not self._size:
                self._size = kwargs['ggpkfile'].seek(0, os.SEEK_END)
                kwargs['ggpkfile'].seek(0, os.SEEK_SET)
            else:
                #kwargs['offset'])

                self.progress_bar.sig_progress.emit(
                    int(kwargs['offset'] / self._size * 100)
                )

            return func(*args, **kwargs)

        return temp

    def _progress_updater(self, title, max, *args, **kwargs):
        p = self.parent().parent()

        p._write_log(title)
        #self.progress_bar = GGPKProgressDialog(title, max, *args, **kwargs)
        self.progress_bar.setLabelText(title)
        self.progress_bar.setWindowTitle(title)
        self.progress_bar.setMaximum(max)
        self.progress_bar.setValue(0)

    def run(self):
        fm = self.parent()
        p = fm.parent()

        p.sig_log_message.emit(self.tr('Open GGPK file "%(file)s".') % {'file': self._file_path})

        self.sig_update_progress.emit(self.tr('Reading GGPK records...'), 100)
        ggpk_file = GGPKFile()
        # Hook the function for progress bar
        ggpk_file._read_record = self._progress_ggpk(ggpk_file._read_record)
        ggpk_file.read(self._file_path)
        # Finished
        self.progress_bar.sig_progress.emit(100)

        p.sig_log_message.emit(self.tr('Building GGPK directory...'))
        ggpk_file.directory_build()

        self.ggpk_file = ggpk_file


class GGPKProgressDialog(QProgressDialog):
    sig_progress = Signal(int)

    def __init__(self, title, maximum=100, *args, **kwargs):
        QProgressDialog.__init__(self, *args, **kwargs)

        self.setWindowTitle(title)
        self.setLabelText(title)
        self.setMinimum(0)
        self.setMaximum(maximum)
        self.setCancelButton(None)
        self.setMinimumWidth(250)
        #self.setMinimumSize(300, 50)
        self.show()

        self.sig_progress.connect(self.setValue)

# =============================================================================
# Functions
# =============================================================================
