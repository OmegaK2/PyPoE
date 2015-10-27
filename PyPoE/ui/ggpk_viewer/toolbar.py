"""
Toolbars for GGPKViewer

Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | PyPoE/ui/ggpk_viewer/toolbar.py                                  |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
-------------------------------------------------------------------------------

Contains various toolbars for use in the GGPKViewer application.

Agreement
-------------------------------------------------------------------------------

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# 3rd Party
from PySide.QtCore import *
from PySide.QtGui import *

# self
from PyPoE.poe.file import ggpk
from PyPoE.ui.shared.dialog import RegExSearchDialog

# =============================================================================
# Globals
# =============================================================================

__all__ = ['ContextToolbar']

# =============================================================================
# Classes
# =============================================================================

class ContextToolbar(QToolBar):
    """
    Context-related toolbar
    """
    def __init__(self, *args, **kwargs):
        QToolBar.__init__(self, *args, **kwargs)


        #self.setAllowedAreas(Qt.LeftToolBarArea | Qt.RightToolBarArea)
        self.action_extract = QAction(self, text=self.tr('Extract'))
        self.action_extract.setStatusTip(self.tr('Extract currently selected file or folder'))
        self.action_extract.triggered.connect(self._toolbar_extract)
        self.action_extract.setDisabled(True)
        self.addAction(self.action_extract)

        self.action_search = QAction(self, text=self.tr('Search'))
        self.action_search.setStatusTip(self.tr('Search currently selected folder'))
        self.action_search.triggered.connect(self._toolbar_search)
        self.action_search.setDisabled(True)
        self.addAction(self.action_search)

        self.setWindowTitle(self.tr('File Viewer Toolbar'))
        self.setOrientation(Qt.Horizontal)
        self.parent().addToolBar(Qt.TopToolBarArea, self)
        self.visibilityChanged.connect(self._adjust_view)

        self.regex_search = RegExSearchDialog(self)

    def _adjust_view(self, visibility):
        self.parent().menu_view.action_toggle_toolbar.setChecked(visibility)

    def _toolbar_extract(self):
        # returns list of columns
        indexes = self.parent().ggpk_view.selectedIndexes()
        # Shouldn't happen... TODO log
        if not indexes:
            return

        p = self.parent()
        target_dir = QFileDialog.getExistingDirectory(self, self.tr('Select directory to extract to'))
        p._write_log(self.tr('Extracting file(s) to "%s"...' % target_dir))
        node = indexes[0].internalPointer()
        node.extract_to(target_dir)
        p._write_log(self.tr('Done.'))

    def _toolbar_search(self):
        # returns list of columns
        indexes = self.parent().ggpk_view.selectedIndexes()
        # Shouldn't happen... TODO log
        if not indexes:
            return

        # Option should be greyed out, but make sure in case it is selected anyway
        node = indexes[0].internalPointer()

        if not isinstance(node.record, ggpk.DirectoryRecord):
            return

        ok = self.regex_search.exec_()

        # User canceled or (custom) regex error
        if not ok:
            return

        sdir = self.regex_search.option_search_directories.isChecked()

        self.parent()._write_log(self.tr('Started searching...'))
        result = node.search(self.regex_search.regex_compiled,
                             search_directories=sdir)
        if result:
            out = []
            stop = None if self.regex_search.option_full_path.isChecked() else node
            for item in result:
                p = item.get_parent(stop_at=stop, make_list=True)
                p = [n.name for n in p]
                out.append('/'.join(p))
            out.sort()
            outtext = '\n'.join(out)
        else:
            outtext = self.tr('No items found.')

        self.parent()._write_log(self.tr('Finished searching.'))

        self.parent().file_textbox.setText(outtext)

    def enable_file_actions(self, node):
        """
        :param DirectoryNode node:
        :return:
        """
        if isinstance(node.record, ggpk.DirectoryRecord):
            self.action_search.setEnabled(True)
        else:
            self.action_search.setEnabled(False)
        self.action_extract.setEnabled(True)