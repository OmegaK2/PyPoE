"""
Toolbars for GGPKViewer

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/ui/ggpk_viewer/toolbar.py                                  |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Contains various toolbars for use in the GGPKViewer application.

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os

# 3rd Party
from PySide2.QtCore import *
from PySide2.QtWidgets import *

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
        self.action_extract.setStatusTip(self.tr(
            'Extract currently selected file or folder'
        ))
        self.action_extract.triggered.connect(self._toolbar_extract)
        self.action_extract.setDisabled(True)
        self.addAction(self.action_extract)

        self.action_search = QAction(self, text=self.tr('Search'))
        self.action_search.setStatusTip(self.tr(
            'Search currently selected folder'
        ))
        self.action_search.triggered.connect(self._toolbar_search)
        self.action_search.setDisabled(True)
        self.addAction(self.action_search)

        self.action_copy_path = QAction(self, text=self.tr('Copy path'))
        self.action_copy_path.setStatusTip(self.tr(
            'Copy the file path relative to content.ggpk root for the '
            'currently selected file or folder')
        )
        self.action_copy_path.triggered.connect(self._toolbar_copy_path)
        self.action_copy_path.setDisabled(True)
        #self.addAction(self.action_copy_path)

        self.setWindowTitle(self.tr('File Viewer Toolbar'))
        self.setOrientation(Qt.Horizontal)
        self.parent().addToolBar(Qt.TopToolBarArea, self)
        self.visibilityChanged.connect(self._adjust_view)

        self.regex_search = RegExSearchDialog(self)

    def _adjust_view(self, visibility):
        self.parent().menu_view.action_toggle_toolbar.setChecked(visibility)

    def _get_node(self):
        """
        Returns
        -------
        DirectoryNode
        """
        # returns list of columns
        indexes = self.parent().ggpk_view.selectedIndexes()
        # Shouldn't happen... TODO log
        if not indexes:
            return
        return indexes[0].internalPointer()

    def _toolbar_extract_dds(self, path, node):
        self.parent()._write_log(path)
        with open(path, 'rb') as f:
            data = f.read()
        if data[:4] == b'DDS ':
            return

        try:
            data = ggpk.extract_dds(
                data, path_or_file_system=node.record._container
            )
        except FileNotFoundError as e:
            self.parent()._write_log('Broken symbolic link.\n%s' % e)

        with open(path, 'wb') as f:
            f.write(data)

    def _toolbar_extract(self):
        node = self._get_node()
        if node is None:
            return

        p = self.parent()
        target_dir = QFileDialog.getExistingDirectory(
            self,
            self.tr('Select directory to extract to')
        )
        if not target_dir:
            return
        p._write_log(self.tr('Extracting file(s) to "%s"...' % target_dir))
        node.extract_to(target_dir)

        #TODO Fix double writing
        if self.parent().s_general.uncompress_dds:
            if isinstance(node.record, ggpk.DirectoryRecord):
                p._write_log(self.tr('Uncompressing DDS Files...'))
                for root, dirs, files in \
                        os.walk(os.path.join(target_dir, node.name)):
                    for file_name in files:
                        if file_name.endswith('.dds'):
                            self._toolbar_extract_dds(
                                os.path.join(root, file_name),
                                node
                            )
            elif isinstance(node.record, ggpk.FileRecord) and \
                    node.name.endswith('.dds'):
                p._write_log(self.tr('Uncompressing DDS File...'))
                self._toolbar_extract_dds(
                    os.path.join(target_dir, node.name),
                    node
                )

        p._write_log(self.tr('Done.'))

    def _toolbar_search(self):
        node = self._get_node()
        if node is None:
            return

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

    def _toolbar_copy_path(self):
        node = self._get_node()
        if node is None:
            return

        QApplication.clipboard().setText(node.get_path())

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
        self.action_copy_path.setEnabled(True)