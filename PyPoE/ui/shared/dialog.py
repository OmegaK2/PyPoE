"""
Shared Dialog Prompts

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/ui/shared/dialog.py                                        |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Contains various self-contained dialog prompts for various tasks.

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import re

# 3rd Party
from PySide2.QtCore import *
from PySide2.QtWidgets import *

# self
from PyPoE.ui.shared.regex_widgets import RegexFlagsBox

# =============================================================================
# Imports
# =============================================================================

__all__ = ['RegExSearchDialog']

# =============================================================================
# Imports
# =============================================================================

class RegExSearchDialog(QDialog):
    def __init__(self, *args, **kwargs):
        QDialog.__init__(self, *args, **kwargs)

        self.setWindowTitle(self.tr('RegEx Search Dialog'))

        self.master_layout = QVBoxLayout()
        self.setLayout(self.master_layout)

        self.regex_box = RegexFlagsBox(default_flags=re.IGNORECASE)
        self.master_layout.addWidget(self.regex_box)

        self.option_group_box = QGroupBox(self.tr('Search Options', parent=self))
        self.master_layout.addWidget(self.option_group_box)

        self.option_group_box_layout = QVBoxLayout()
        self.option_group_box.setLayout(self.option_group_box_layout)

        self.option_search_directories = QCheckBox(self.tr('Search directory names', parent=self.option_group_box))
        self.option_group_box_layout.addWidget(self.option_search_directories)

        self.option_full_path = QCheckBox(self.tr('Show full path', parent=self.option_group_box))
        self.option_group_box_layout.addWidget(self.option_full_path)

        self.master_layout.addWidget(QLabel(self.tr('Enter Regular Expression:'), parent=self))

        self.regex_input = QLineEdit()
        self.master_layout.addWidget(self.regex_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Reset)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        b = self.button_box.button(QDialogButtonBox.Reset)
        b.clicked.connect(self.reset)

        self.master_layout.addWidget(self.button_box)

        # Set default states
        self.reset()

    def accept(self, *args, **kwargs):
        # Validate and store the regex
        try:
            self.regex_compiled = re.compile(self.regex_input.text(), self.regex_box.get_flags())
        except re.error as e:
            QMessageBox.critical(self, self.tr('RegEx Error'), self.tr('regular Expression error:\n %s') % e.args[0])
            # TODO: This may be unncessary. Actually should  accept even return rejected? No idea.
            return QDialog.Rejected

        return QDialog.accept(self, *args, **kwargs)

    def reset(self):
        """
        Set defaults and empty the input text
        """
        self.regex_compiled = re.compile('')
        self.regex_input.setText('')
        self.regex_box.set_defaults()
        self.option_search_directories.setCheckState(Qt.CheckState.Unchecked)
        self.option_full_path.setCheckState(Qt.CheckState.Checked)