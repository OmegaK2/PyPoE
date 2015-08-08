"""
Path     PyPoE/ui/ggpk_viewer/menu.py
Name     Menus for GGPKViewer
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO

Contains the Menus and related actions for the GGPKViewer


AGREEMENT

See PyPoE/LICENSE


TODO

...
"""

# =============================================================================
# Imports
# =============================================================================

# Python

# 3rd Party
from PySide.QtGui import *

# self
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

class FileMenu(QMenu):
    """
    Create file menu and handle related actions
    """
    def __init__(self, *args, **kwargs):
        QMenu.__init__(self, *args, **kwargs)

        # Get the paths and store them for efficiency
        self.poe_install_paths = PoEPath(PoEPath.VERSION_STABLE, PoEPath.DISTRIBUTOR_ALL).get_installation_paths()
        self.poe_install_paths = sorted(self.poe_install_paths, key=lambda item: item.version)

        self.action_open = QAction(self, text=self.tr('Open'))
        self.action_open.setStatusTip(self.tr('Open GGPK File'))
        self.action_open.triggered.connect(self._open_ggpk)
        self.addAction(self.action_open)

        self.setTitle(self.tr('File'))
        self.parent().menuBar().addMenu(self)

    def _ggpk_sort(self, args):
        node = args['node']
        sorter = lambda obj: (isinstance(obj.record, ggpk.FileRecord), obj.name)
        node.children = sorted(node.children, key=sorter)

    def _open_ggpk(self):
        # Use the first found path
        dir = self.poe_install_paths[0].path if self.poe_install_paths else '.'

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

        p._write_log(self.tr('Open GGPK file "%(file)s".') % {'file': file_path})
        p._write_log(self.tr('Reading GGPK records...'))
        ggpk_file = ggpk.GGPKFile(file_path)
        ggpk_file.read()

        p._write_log(self.tr('Building GGPK directory...'))
        ggpk_file.directory_build()
        ggpk_file.directory.walk(self._ggpk_sort)

        m = GGPKModel(ggpk_file.directory)

        p._write_log(self.tr('Viewing GGPK contents...'))
        p.ggpk_view.setModel(m)
        p.ggpk_view.show()

        p._write_log(self.tr('Done.'))

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