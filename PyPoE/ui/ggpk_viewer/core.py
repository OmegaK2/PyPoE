"""
Path     PyPoE/ui/ggpk_viewer/core.py
Name     GGPK User Interface Classes
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO

Creates a qt User Interface to browse GGPK files.


AGREEMENT

See PyPoE/LICENSE


TODO

...
"""

# =============================================================================
# Imports
# =============================================================================

# Default Imports
import time
import sys
from traceback import format_exc

# Library Imports
from PySide.QtCore import *
from PySide.QtGui import *

# Package Imports
from PyPoE.poe.file import ggpk
from PyPoE.ui.shared.file.manager import FileDataManager
from PyPoE.ui.shared.file.model import GGPKModel
from PyPoE.ui.ggpk_viewer.toolbar import *
from PyPoE.ui.ggpk_viewer.menu import *

# =============================================================================
# Classes
# =============================================================================

class MainWindow(QMainWindow):

    sig_log_message = Signal(str)

    def __init__(self, app):
        self.app = app
        super(MainWindow, self).__init__()

        # Misc Variables set in other places
        self._last_node = None

        self._file_data_manager = FileDataManager(self)

        # Menu Bar
        self.menu_file = FileMenu(parent=self)
        self.menu_view = ViewMenu(parent=self)
        self.menu_misc = MiscMenu(parent=self)

        # Tool Bars
        self.context_toolbar = ContextToolbar(parent=self)

        # Central Widget
        self.master = QSplitter(parent=self)
        self.master.setOrientation(Qt.Vertical)
        self.work_area_splitter = QSplitter()
        self.master.addWidget(self.work_area_splitter)
        self.notification = QTextEdit(readOnly=True)
        self.notification.setFixedHeight(100)
        self.master.addWidget(self.notification)


        self.ggpk_view = QTreeView()
        self.ggpk_view.setModel(GGPKModel())
        self.ggpk_view.setColumnWidth(0, 200)
        self.ggpk_view.setColumnWidth(1, 75)
        self.ggpk_view.setColumnWidth(2, 80)
        #self.ggpk_view.setColumnWidth(3, 80)
        self.ggpk_view.setMinimumSize(370, 370)
        self.ggpk_view.clicked.connect(self._view_record)
        self.ggpk_view.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.ggpk_view.addAction(self.context_toolbar.action_extract)
        self.ggpk_view.addAction(self.context_toolbar.action_search)
        self.work_area_splitter.addWidget(self.ggpk_view)

        self.work_area_frame = QFrame()
        self.work_area_frame.setContentsMargins(0, 0, 0, 0)
        self.file_layout = QVBoxLayout()
        self.file_layout.setContentsMargins(0, 0, 0, 0)
        self.work_area_frame.setLayout(self.file_layout)
        self.work_area_splitter.addWidget(self.work_area_frame)

        # Create Info bar
        self.file_infobar_layout = QHBoxLayout()
        self.file_infobar_layout.setAlignment(Qt.AlignLeft)
        self.file_infobar = QFrame()
        self.file_infobar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.file_infobar.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.file_infobar.setLayout(self.file_infobar_layout)

        self.file_infobar_layout.addWidget(QLabel(self.tr('Name Hash:')))
        self.file_infobar_name_hash = QLineEdit(readOnly=True)
        #self.file_infobar_name_hash.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        self.file_infobar_name_hash.setFixedWidth(70)
        self.file_infobar_layout.addWidget(self.file_infobar_name_hash)

        self.file_infobar_layout.addWidget(QLabel(self.tr('File Hash:')))
        self.file_infobar_file_hash = QLineEdit(readOnly=True)
        self.file_infobar_file_hash.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        self.file_infobar_file_hash.setMinimumWidth(405)
        self.file_infobar_layout.addWidget(self.file_infobar_file_hash)

        # Add to the info bar to general file layout
        self.file_layout.addWidget(self.file_infobar)

        # Create Frame
        #self.file_frame_scroll = QScrollArea()
        #self.file_frame_scroll.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        #self.file_layout.addWidget(self.file_frame_scroll)


        self.file_frame = QFrame()
        self.file_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.file_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.file_layout.addWidget(self.file_frame)

        self.file_frame_layout = QVBoxLayout()
        self.file_frame_layout.setAlignment(Qt.AlignTop)
        self.file_frame.setLayout(self.file_frame_layout)

        #self.file_frame_scroll.setWidget(self.file_frame)
        #self.file_frame_scroll.setLayout(self.file_frame_layout)
        #self.file_frame_scroll.show()

        #
        self.file_textbox = QTextEdit(self)
        self.file_textbox.setText(self.tr("No file selected."))
        self.file_textbox.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.file_frame_layout.addWidget(self.file_textbox)

        # Setup the main window
        self.setCentralWidget(self.master)
        self.statusBar()
        self.setWindowTitle(self.tr('GGPK View'))

        #
        self.sig_log_message.connect(self._write_log)

    def _write_log(self, msg, notification=None):
        timef = time.strftime("%H:%M:%S - ")
        if notification is None:
            notification = msg
        self.statusBar().showMessage(timef + notification)
        self.notification.append(timef + msg)
        self.app.processEvents()

    def _reset_file_view(self, reset_hash=True):
        if reset_hash:
            self.file_infobar_file_hash.setText('')
            self.file_infobar_name_hash.setText('')
            self._last_node = None
        if hasattr(self, 'file_view'):
            self.file_frame_layout.removeWidget(self.file_view)
            self.file_view.deleteLater()
            del self.file_view

    def _view_record(self, index=QModelIndex()):
        node = index.internalPointer()
        self.context_toolbar.enable_file_actions(node)

        # Do nothing if the user spams clicks the same...
        if node is self._last_node:
            return

        self._last_node = node

        self.file_infobar_file_hash.setText(hex(node.record.hash)[2:].upper())
        self.file_infobar_name_hash.setText(str(node.hash))

        if isinstance(node.record, ggpk.DirectoryRecord):
            self.file_textbox.setText(self.tr("No file selected."))
            self.file_textbox.setVisible(True)
            if hasattr(self, 'file_view'):
                self.file_view.setVisible(False)
            return

        # Avoid extracting data until we actually need
        obj = self._file_data_manager.get_handler(node.record.name)
        if obj is None:
            self.file_textbox.setText(self.tr("File view not supported for this file type."))
            self.file_textbox.setVisible(True)
            self._reset_file_view(reset_hash=False)
            return


        try:
            qwidget = obj.get_widget(node.record.extract(), file_name=node.record.name, parent=self)
        except Exception as e:
            msg = self.tr("%(error)s occurred when trying to open %(file)s" % {
                'file': node.record.name,
                'error': e.__class__.__name__,
            })
            fullmsg = msg + ': \n\n' + format_exc()

            self.file_textbox.setText(fullmsg)
            self._write_log(fullmsg, msg)
            return


        self.file_textbox.setVisible(False)
        # Remove the old widget or we're heavily memory leaking
        self._reset_file_view(reset_hash=False)

        self.file_frame_layout.addWidget(qwidget)
        self.file_view = qwidget

        # Actually is a file record



    def run(self):
        self.show()
        self.app.exec_()

# =============================================================================
# Functions
# =============================================================================

def main():
    translator = QTranslator()
    translator.load('i18n/en_US')
    app = QApplication(sys.argv)
    app.installTranslator(translator)
    frame = MainWindow(app)
    frame.run()

if __name__ == '__main__':
    main()