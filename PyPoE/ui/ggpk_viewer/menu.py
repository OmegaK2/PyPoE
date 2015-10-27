"""
Menus for GGPKViewer

Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | PyPoE/ui/ggpk_viewer/menu.py                                     |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
-------------------------------------------------------------------------------

Contains the Menus and related actions for the GGPKViewer

Agreement
-------------------------------------------------------------------------------

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os
from functools import wraps

# 3rd Party
from PySide.QtCore import *
from PySide.QtGui import *

# self
from PyPoE.poe.constants import DISTRIBUTOR, VERSION
from PyPoE.poe.file import dat, ggpk
from PyPoE.poe.path import PoEPath
from PyPoE.ui.shared.file.model import GGPKModel

# =============================================================================
# Globals
# =============================================================================

__all__ = ['FileMenu', 'MiscMenu', 'ViewMenu']

# =============================================================================
# Classes
# =============================================================================

class GGPKThread(QThread):

    sig_update_progress = Signal(str, int)

    def __init__(self, file_path, *args, **kwargs):
        QThread.__init__(self, *args, **kwargs)
        self._file_path = file_path
        self.m = None
        self._size = 0

        self.sig_update_progress.connect(self._progress_updater)

        self.progress_bar = GGPKProgress('')

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

    def _ggpk_sort(self, args):
        node = args['node']
        sorter = lambda obj: (isinstance(obj.record, ggpk.FileRecord), obj.name)
        node.children = sorted(node.children, key=sorter)

    def _progress_updater(self, title, max, *args, **kwargs):
        p = self.parent().parent()

        p._write_log(title)
        #self.progress_bar = GGPKProgress(title, max, *args, **kwargs)
        self.progress_bar.setLabelText(title)
        self.progress_bar.setWindowTitle(title)
        self.progress_bar.setMaximum(max)
        self.progress_bar.setValue(0)

    def run(self):
        fm = self.parent()
        p = fm.parent()

        p.sig_log_message.emit(self.tr('Open GGPK file "%(file)s".') % {'file': self._file_path})

        self.sig_update_progress.emit(self.tr('Reading GGPK records...'), 100)
        ggpk_file = ggpk.GGPKFile()
        # Hook the function for progress bar
        ggpk_file._read_record = self._progress_ggpk(ggpk_file._read_record)
        ggpk_file.read(self._file_path)
        # Finished
        self.progress_bar.sig_progress.emit(100)

        ds = 0
        for item in ggpk_file.records.values():
            if isinstance(item, ggpk.DirectoryRecord):
                ds += 1

        p.sig_log_message.emit(self.tr('Building GGPK directory...'))
        ggpk_file.directory_build()

        p.sig_log_message.emit(self.tr('Sorting GGPK directory...'))
        ggpk_file.directory.walk(self._ggpk_sort)

        self.m = GGPKModel(ggpk_file.directory)

        p.sig_log_message.emit(self.tr('Viewing GGPK contents...'))
        fm.sig_update_ggpk.emit()

class GGPKProgress(QProgressDialog):
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


class FileMenu(QMenu):
    """
    Create file menu and handle related actions
    """
    sig_update_ggpk = Signal()
    def __init__(self, *args, **kwargs):
        QMenu.__init__(self, *args, **kwargs)

        # Get the paths and store them for efficiency
        self.poe_install_paths = PoEPath().get_installation_paths()
        self.poe_install_paths = sorted(self.poe_install_paths, key=lambda item: item.version)

        self.action_open = QAction(self, text=self.tr('Open'))
        self.action_open.setStatusTip(self.tr('Open GGPK File'))
        self.action_open.triggered.connect(self._open_ggpk)
        self.addAction(self.action_open)

        self.setTitle(self.tr('File'))
        self.parent().menuBar().addMenu(self)

        self.sig_update_ggpk.connect(self._update_ggpk_model)

    def _open_ggpk(self):
        # Use the first found path
        if self.poe_install_paths:
            dir = os.path.join(self.poe_install_paths[0].path, 'content.ggpk')
        else:
            dir = '.'

        file = QFileDialog.getOpenFileName(self, self.tr("Open GGPK"), dir, self.tr("GGPK Files (*.ggpk)"))
        # User Aborted
        if not file[0]:
            return

        p = self.parent()
        file_path = file[0]

        # Destroy the old object or we're massively memory-leaking
        # TODO for some reason 2 objects are still kept in memory
        p._reset_file_view(reset_hash=True)
        p.ggpk_view.model().deleteLater()
        p.ggpk_view.setModel(GGPKModel())

        self.t = GGPKThread(file_path, parent=self)
        self.t.start()

    def _update_ggpk_model(self):
        p = self.parent()
        p.ggpk_view.setModel(self.t.m)
        p.ggpk_view.show()

        p.sig_log_message.emit(self.tr('Done.'))




class ViewMenu(QMenu):
    """
    Create view menu and handle related actions
    """
    def __init__(self, *args, **kwargs):
        QMenu.__init__(self, *args, **kwargs)

        self.action_toggle_toolbar = QAction(self, text=self.tr('File Viewer Toolbar'), checkable=True)
        self.action_toggle_toolbar.setStatusTip(self.tr('Toggle file viewer toolbar'))
        self.action_toggle_toolbar.triggered.connect(self._toggle_view_toolbar)
        self.action_toggle_toolbar.setChecked(True)
        self.addAction(self.action_toggle_toolbar)

        self.setTitle(self.tr('View'))
        self.parent().menuBar().addMenu(self)

    def _toggle_view_toolbar(self):
        tb = self.parent().context_toolbar
        tb.setVisible(not tb.isVisible())

class MiscMenu(QMenu):
    """
    Create misc menu and handle related actions
    """
    def __init__(self, *args, **kwargs):
        QMenu.__init__(self, *args, **kwargs)

        self.action_reload_specifications = QAction(self, text=self.tr('Reload .dat specifications'))
        self.action_reload_specifications.setStatusTip(self.tr('Reloads the default .dat specifications.'))
        self.action_reload_specifications.triggered.connect(self._reload_specifications)
        self.addAction(self.action_reload_specifications)

        self.setTitle(self.tr('Misc'))
        self.parent().menuBar().addMenu(self)

    def _reload_specifications(self):
        p = self.parent()

        p._write_log(self.tr('Reloading default specification...'))
        dat.reload_default_spec()
        p._write_log('Done.')