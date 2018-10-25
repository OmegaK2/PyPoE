"""
Data Models for viewing files

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/ui/shared/file/model.py                                    |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Contains shared QT Models for displaying various GGG data.

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# 3rd Party
from PySide2.QtCore import *

# self
from PyPoE.poe.file.dat import DatFile, DatValue
from PyPoE.ui.shared.proxy_filter_model import FilterProxyModel

# =============================================================================
# Globals
# =============================================================================

__all__ = [
    'DatDataModel',
    'DatTableModel',
    'DatValueProxyModel',
    'GGPKModel',
]

# =============================================================================
# Classes
# =============================================================================


class DatModelShared(QAbstractTableModel):
    """
    TODO: master should be a DatFrame... but circular dependencies
    """
    def __init__(self, dat_file, *args, **kwargs):
        QAbstractTableModel.__init__(self, *args, **kwargs)
        if not isinstance(dat_file, DatFile):
            raise TypeError('datfile must be a DatFile instance')
        self._dat_file = dat_file


class DatTableModel(DatModelShared):
    def __init__(self, *args, **kwargs):
        DatModelShared.__init__(self, *args, **kwargs)

        self._columns = [(id, item['section']) for id, item in self._dat_file.reader.table_columns.items()]

    def rowCount(self, parent=QModelIndex()):
        return len(self._dat_file.reader.table_data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._dat_file.reader.table_columns) + 1

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None

        c = index.column()
        if c == 0:
            return self._dat_file.reader.table_data[index.row()].rowid
        else:
            return self._dat_file.reader.table_data[index.row()][c-1]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation != Qt.Horizontal:
            return None

        # Is a specification entry
        if section > 0:
            name, field = self._columns[section-1]
        else:
            field = None
            name = None

        if role == Qt.DisplayRole:
            if field:
                return field.display.replace('\\n', '\n') if field.display \
                    else name
            else:
                return self.tr('RowID')
        elif role == Qt.ToolTipRole and field:
            return field.description

        return None


class DatDataModel(DatModelShared):
    def __init__(self, *args, **kwargs):
        DatModelShared.__init__(self, *args, **kwargs)
        self._sections = [
            (self.tr('Offset\nStart'), self._show_start_offset),
            (self.tr('Offset\nEnd'), self._show_end_offset),
            (self.tr('Data\nSize'), self._show_size),
            (self.tr('Data'), self._show_data),
        ]

        self._data = []
        if len(self._dat_file.reader.data_parsed) > 1:
            last = self._dat_file.reader.data_parsed[0]
            self._data.append(last)
            # Remove duplicates for easier reading
            # TODO add option this?
            for item in self._dat_file.reader.data_parsed:
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

        return self._sections[index.column()][1](self._data[index.row()])

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if not self.rowCount():
            return None
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self._sections[section][0]
        return None


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

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation != Qt.Horizontal:
            return None
        if role != Qt.DisplayRole:
            return None

        try:
            return self.headers[section]
        except IndexError:
            return None


class DatValueProxyModel(FilterProxyModel):
    def _get_data(self, row, column, parent):
        data = FilterProxyModel._get_data(self, row, column, parent)
        if isinstance(data, DatValue):
            return data.get_value()
        return data

    def _sort_value(self, dat_value):
        v = dat_value
        if QObject.parent(self).option_dereference_pointer.isChecked():
            # DatValue instances now support comprehensions
            v = dat_value.get_value()
        elif dat_value.is_list:
            v = dat_value.value[1]
        elif dat_value.is_pointer:
            v = dat_value.value
        if v is None:
            return -1
        return v

    def lessThan(self, left, right):
        ldata = self.sourceModel().data(left)
        rdata = self.sourceModel().data(right)
        if isinstance(ldata, DatValue):
            ldata = self._sort_value(ldata)
        if isinstance(rdata, DatValue):
            rdata = self._sort_value(rdata)

        try:
            return ldata < rdata
        except TypeError:
            return False
        # TODO debug