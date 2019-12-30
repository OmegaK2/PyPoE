"""
Setting menu related things

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/ui/shared/settings.py                                      |
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

Internal API
-------------------------------------------------------------------------------
"""

# =============================================================================
# Imports
# =============================================================================

# Python

# 3rd-party
from PySide2.QtCore import *
from PySide2.QtWidgets import *

# self

# =============================================================================
# Globals
# =============================================================================

__all__ = ['SettingsWindow', 'SettingFrame', 'Setting', 'BoolSetting']

# =============================================================================
# Classes
# =============================================================================


class SettingsWindow(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.action_open = QAction(self, text=self.tr('Settings'))
        self.action_open.setStatusTip(self.tr(
            'Opens the settings window'
        ))
        self.action_open.triggered.connect(self._action_open)

        self.setWindowTitle(self.tr('Settings'))

        self.base_layout = QHBoxLayout()
        self.setLayout(self.base_layout)

        self.section_list = QListView(parent=self)
        self.section_list.setMovement(QListView.Static)
        self.section_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # TODO: IDK how to capture keyboard selections.
        self.section_list.pressed.connect(self._selected)
        self.base_layout.addWidget(self.section_list)

        self.frame = QFrame(parent=self)
        self.frame.setMinimumHeight(300)
        self.frame.setMinimumWidth(500)
        self.base_layout.addWidget(self.frame)

        self.layout = QVBoxLayout()
        self.frame.setLayout(self.layout)

        self.current_frame = None

        self.sections = []
        self.changed = True

    def _selected(self, index):
        if not index.isValid():
            return

        if self.current_frame:
            self.layout.removeWidget(self.current_frame)

        self.layout.addWidget(self.sections[index.row()]['frame'])
        self.current_frame = self.sections[index.row()]['frame']

    def add_config_section(self, tr, qframe, order=0):
        self.sections.append({
            'text': tr,
            'frame': qframe,
            'order': order,
        })
        self.changed = True

    def _action_open(self):
        if self.changed:
            self.sections.sort(key=lambda x: x['order'])
            model = QStringListModel()
            model.setStringList([row['text'] for row in self.sections])
            self.section_list.setModel(model)
            self.section_list.setSelectionMode(
                QAbstractItemView.SingleSelection
            )
            self.changed = False

        self.exec_()


class SettingFrame(QFrame):
    KEY = NotImplemented

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = {}

    def _add_setting(self, setting):
        self.settings[setting.KEY] = setting

    def __getattr__(self, item):
        try:
            return self.settings[item].value
        except KeyError:
            raise AttributeError


class BaseSetting:
    KEY = NotImplemented
    DEFAULT = NotImplemented

    def __init__(self, parent, settings, *args, **kwargs):
        self.parent = parent
        self.settings = settings
        self.value = self.get()

    def setting_path(self):
        return '/'.join(
            (self.parent.KEY, self.KEY)
        )

    def _get_cast(self, value):
        raise NotImplementedError

    def _set_cast(self, value):
        raise NotImplementedError

    def get(self):
        v = self.settings.value(self.setting_path())

        if v is None:
            return self.DEFAULT

        return self._get_cast(v)

    def set(self, value=None):
        if value is None:
            value = self.value

        self.settings.setValue(
            self.setting_path(),
            self._set_cast(value),
        )


class BoolSetting(BaseSetting):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.checkbox = QCheckBox()
        self.checkbox.setChecked(self.value)
        self.checkbox.stateChanged.connect(self._update)

    def _get_cast(self, value):
        return bool(int(value))

    def _set_cast(self, value):
        return str(int(value))

    def _update(self, state):
        if state == Qt.Unchecked:
            self.value = False
        elif state == Qt.Checked:
            self.value = True
        else:
            raise ValueError('Invalid Qt::CheckState')

        self.set()


class ComboBoxSetting(BaseSetting):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.combobox = QComboBox()
        self.combobox.setEditable(False)
        self.combobox.currentIndexChanged.connect(self._update)
        self.data = {}

    def _set_data(self, data):
        v = self.value
        self.data = data
        for i, (text, value) in enumerate(data.items()):
            self.combobox.addItem(text)
            if value == v:
                self.combobox.setCurrentIndex(i)

    def _update(self, value):
        self.value = self.data[self.combobox.itemText(value)]
        self.set(self.value)
# =============================================================================
# Functions
# =============================================================================
