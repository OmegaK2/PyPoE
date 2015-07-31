"""
Path     PyPoE/ui/shared/file/model.py
Name     Data Model for viewing files
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO

Contains the Menus and related actions for the GGPK Viewer


AGREEMENT

See PyPoE/LICENSE


TODO

...
"""

# =============================================================================
# Imports
# =============================================================================

# 3rd Party
from PySide.QtCore import *

# self
from PyPoE.poe.file.dat import DatFile

# =============================================================================
# Globals
# =============================================================================

__all__ = ['DatTableModel', 'DatDataModel', 'GGPKModel']

# =============================================================================
# Classes
# =============================================================================

class DatModelShared(QAbstractTableModel):
    """
    TODO: master should be a DatFrame... but circular dependencies
    """
    def __init__(self, dat_file, master, *args, **kwargs):
        QAbstractTableModel.__init__(self, *args, **kwargs)
        if not isinstance(dat_file, DatFile):
            raise TypeError('datfile must be a DatFile instance')
        self._dat_file = dat_file
        self._master = master

class DatTableModel(DatModelShared):
    def _sort_value(self, dat_value):
        if self._master.option_dereference_pointer.isChecked():
            if dat_value.is_list:
                return self._show_value(dat_value)
            elif dat_value.is_pointer:
                return dat_value.child.value
        if dat_value.is_list:
            return dat_value.value[1]
        return dat_value.value

    def rowCount(self, parent=QModelIndex()):
        return len(self._dat_file.table_data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._dat_file.table_columns) + 1

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None

        c = index.column()
        if c == 0:
            return self._dat_file.table_data[index.row()].rowid
        else:
            return self._dat_file.table_data[index.row()][c-1]

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            # Is a specification entry
            if section > 0:
                s = self._dat_file.table_columns[section-1]
                return s['display'].replace('\\n','\n') if s['display'] else s.name
            return self.tr('RowID')
        return None

    def sort(self, column, order=Qt.AscendingOrder):
        reverse = False if order != Qt.AscendingOrder else True
        if column > 0:
            sorter = lambda x: self._sort_value(x[column-1])
        else:
            sorter = lambda x: x.rowid
        self._dat_file.table_data.sort(key=sorter, reverse=reverse)
        self.dataChanged.emit(0,0)

class DatDataModel(DatModelShared):
    def __init__(self, *args, **kwargs):
        DatModelShared.__init__(self, *args, **kwargs)
        self._sections = [
            (self._master.tr('Offset\nStart'), self._show_start_offset),
            (self._master.tr('Offset\nEnd'), self._show_end_offset),
            (self._master.tr('Data\nSize'), self._show_size),
            (self._master.tr('Data'), self._show_data),
        ]

        self._data = []
        if len(self._dat_file.data_parsed) > 1:
            last = self._dat_file.data_parsed[0]
            self._data.append(last)
            # Remove duplicates for easier reading
            # TODO add option this?
            for item in self._dat_file.data_parsed[1:]:
                #if (last.data_start_offset == item.data_start_offset and
                #    last.data_end_offset == item.data_end_offset and
                #    last.data_start_offset == last.data_end_offset):
                #    continue

                self._data.append(item)
                last = item

    def _show_start_offset(self, dat_value):
        return dat_value.data_start_offset

    def _show_end_offset(self, dat_value):
        return dat_value.data_end_offset

    def _show_size(self, dat_value):
        return dat_value.data_size

    def _show_data(self, dat_value):
        return dat_value

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._sections)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None

        dv = self._data[index.row()]

        return self._sections[index.column()][1](dv)

    def headerData(self, section, orientation, role):
        if not self.rowCount():
            return None
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self._sections[section][0]
        return None

    def sort(self, column, order=Qt.AscendingOrder):
        reverse = False if order != Qt.AscendingOrder else True
        self._data.sort(key=lambda x: self._sections[column][1](x), reverse=reverse)
        self.dataChanged.emit(0,0)

class GGPKModel(QAbstractItemModel):
    def __init__(self, data=None):
        QAbstractItemModel.__init__(self)
        self.headers = (self.tr('Name'), self.tr('Size'), self.tr('Offset'))
        self._data = data

    def index(self, row, column, parent=QModelIndex()):
        if not parent.isValid():
            return self.createIndex(row, column, self._data)
        node = parent.internalPointer()
        return self.createIndex(row, column, node.children[row])

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        node = index.internalPointer()
        if node.parent is None:
            return QModelIndex()
        else:
            return self.createIndex(node.parent.children.index(node), 0, node.parent)

    def rowCount(self, parent=QModelIndex()):
        if not parent.isValid():
            # Root node is always row 1.
            return 0 if self._data is None else 1
        node = parent.internalPointer()
        return len(node.children)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None
        node = index.internalPointer()
        cid = index.column()
        if cid == 0:
            return node.name
        elif cid == 1:
            return str(node.record.length)
        elif cid == 2:
            # need to str or the program hangs for some reason
            return str(node.record.offset)
        #elif cid == 3:
        #    return str(node.hash)
        return None

    def headerData(self, section, orientation, role):
        if orientation != Qt.Horizontal:
            return None
        if role != Qt.DisplayRole:
            return None

        try:
            return self.headers[section]
        except IndexError:
            return None