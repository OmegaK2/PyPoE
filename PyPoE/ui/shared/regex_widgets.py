"""
Regular Expression Widgets

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/ui/shared/regex_widgets.py                                 |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Contains various self-contained regular expression widgets

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

import re

# 3rd Party
from PySide2.QtCore import *
from PySide2.QtWidgets import *

# self

# =============================================================================
# Globals
# =============================================================================

__all__ = []

# =============================================================================
# Classes
# =============================================================================


class RegexFlagsBox(QGroupBox):
    """

    Detailed description of flags:
    https://docs.python.org/3/library/re.html#contents-of-module-re

    re.LOCALE is not supported, as it is deprecated in python 3.5
    """
    def __init__(self, default_flags=0, disabled_flags=re.DEBUG, *args, **kwargs):
        QGroupBox.__init__(self, *args, **kwargs)

        self.setTitle(self.tr('RegEx Options'))

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self._regex_flags = [
            {
                'flag': re.ASCII,
                'variable': 'option_ascii',
                'description': self.tr('ASCII'),
                'tooltip': self.tr(
                    'Make \\w, \\W, \\b, \\B, \\d, \\D, \\s and \\S perform '
                    'ASCII-only matching instead of full Unicode matching'
                ),
            },
            {
                'flag': re.DEBUG,
                'variable': 'option_debug',
                'description': self.tr('Debug'),
                'tooltip': self.tr(
                    'Display debug information about compiled expression.'
                ),
            },
            {
                'flag': re.IGNORECASE,
                'variable': 'option_ignore_case',
                'description': self.tr('Ignore case'),
                'tooltip': self.tr(
                    'Perform case-insensitive matching; expressions like [A-Z]'
                    ' will match lowercase letters, too. This is not affected '
                    'by the current locale and works for Unicode characters as'
                    ' expected.'
                ),
            },
            {
                'flag': re.MULTILINE,
                'variable': 'option_multiline',
                'description': self.tr('Multiline'),
                'tooltip': self.tr(
                    'When specified, the pattern character \'^\' matches at '
                    'the beginning of the string and at the beginning of each '
                    'line (immediately following each newline); and the '
                    'pattern character \'$\' matches at the end of the string '
                    'and at the end of each line (immediately preceding each '
                    'newline). By default, \'^\' matches only at the beginning '
                    'of the string, and \'$\' only at the end of the string '
                    'and immediately before the newline (if any) at the end '
                    'of the string.'
                ),

            },
            {
                'flag': re.DOTALL,
                'variable': 'option_dotall',
                'description': self.tr('Dotall'),
                'tooltip': self.tr(
                    'Make the \'.\' special character match any character at '
                    'all, including a newline; without this flag, \'.\' will '
                    'match anything except a newline.'
                ),
            },
            {
                'flag': re.VERBOSE,
                'variable': 'option_verbose',
                'description': self.tr('Verbose'),
                'tooltip': self.tr(
                    'This flag allows you to write regular expressions that '
                    'look nicer. Whitespace within the pattern is ignored, '
                    'except when in a character class or preceded by an '
                    'unescaped backslash, and, when a line contains a \'#\' '
                    'neither in a character class or preceded by an unescaped '
                    'backslash, all characters from the leftmost such \'#\' '
                    'through the end of the line are ignored.'
                ),
            },
        ]

        delete = []

        for flag_info in self._regex_flags:
            if flag_info['flag'] & disabled_flags:
                delete.append(flag_info)
            else:
                box = QCheckBox(flag_info['description'], parent=self)
                box.setToolTip(flag_info['tooltip'])
                self.layout.addWidget(box)
                setattr(self, flag_info['variable'], box)

        for item in delete:
            self._regex_flags.remove(item)

        self._default_flags = default_flags
        self.set_defaults()

    def get_flags(self):
        flags = 0
        for flag_info in self._regex_flags:
            if getattr(self, flag_info['variable']).isChecked():
                flags |= flag_info['flag']

        return flags

    def set_defaults(self, flags=None):
        flags = self._default_flags if flags is None else flags
        for flag_info in self._regex_flags:
            box = getattr(self, flag_info['variable'])
            if flag_info['flag'] & flags:
                box.setCheckState(Qt.CheckState.Checked)
            else:
                box.setCheckState(Qt.CheckState.Unchecked)


# =============================================================================
# Functions
# =============================================================================
