"""
Handlers for viewing GGG files

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/ui/shared/file/handler.py                                  |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Contains file-type views and handler for various file types.

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os
import io
import struct
from tempfile import TemporaryDirectory

# 3rd Party
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtOpenGL import *
from PySide2.QtWidgets import *
try:
    from OpenGL import GL
except ImportError:
    GL = None

# self
from PyPoE.poe.file.dat import DatFile, DatValue
import PyPoE.poe.file.file_system as file_system
from PyPoE.ui.shared.proxy_filter_model import FilterMenu
from PyPoE.ui.shared.table_context_menus import TableContextReadOnlyMenu
from PyPoE.ui.shared.file.model import (
    DatTableModel, DatDataModel, DatValueProxyModel
)

# =============================================================================
# Globals
# =============================================================================

__all__ = [
    'DatDataHandler',
    'DDSDataHandler',
    'FileDataHandler',
    'ImageDataHandler',
    'TextDataHandler',
]

# =============================================================================
# Globals
# =============================================================================


class FileDataHandler:
    def _verify_data(self, file_data):
        if isinstance(file_data, bytes):
            d = io.BytesIO()
            d.write(file_data)
        elif isinstance(file_data, io.BytesIO):
            d = file_data
        else:
            raise TypeError('file data must be bytes or io.BytesIO')

    def get_widget(self, file_data, file_name, *args, **kwargs):
        raise NotImplementedError


class DatStyle(QStyledItemDelegate):
    CELL_ALIGNMENT = Qt.AlignVCenter | Qt.AlignLeft

    def __init__(self, *args, data_style=False, **kwargs):
        QStyledItemDelegate.__init__(self, *args, **kwargs)
        self.data_style = data_style

    def _sort_value(self, dat_value):
        if self.parent().option_dereference_pointer.isChecked():
            if dat_value.is_list:
                return self._show_value(dat_value)
            elif dat_value.is_pointer:
                return dat_value.child.value
        if dat_value.is_list:
            return dat_value.value[1]
        return dat_value.value

    def _show_value(self, outstr, dat_value, format='{0}'):
        if self.data_style or \
                self.parent().option_dereference_pointer.isChecked():
            if dat_value.is_pointer:
                self._show_value(outstr, dat_value.child)
                if self.parent().option_show_pointer.isChecked():
                    outstr.append("@")
                    outstr.append(str(dat_value.value))
            elif dat_value.is_list:
                outstr.append('[')
                for v in dat_value.children:
                    self._show_value(outstr, v)
                    outstr.append(', ')
                # Remove extra comma
                if dat_value.children:
                    outstr.pop(-1)
                outstr.append(']')
                if self.parent().option_show_pointer.isChecked():
                    outstr.append("@")
                    outstr.append(str(dat_value.value[1]))
            else:
                outstr.append(format.format(dat_value.value))
        elif dat_value.is_pointer:
            outstr.append("@")
            outstr.append(str(dat_value.value))
        elif dat_value.is_list:
            outstr.append("["),
            outstr.append(str(dat_value.value[0]))
            outstr.append(", @")
            outstr.append(str(dat_value.value[1]))
            outstr.append(']')
        else:
            outstr.append(format.format(dat_value.value))

    def _get_text(self, data):
        if isinstance(data, DatValue):
            outstr = []
            self._show_value(outstr, data, data.specification.display_type)
            text = ''.join(outstr)
        else:
            text = str(data)

        return text

    def paint(self, painter=QPainter(), option=QStyleOptionViewItem(),
              index=QModelIndex()):
        painter.save()

        QStyledItemDelegate.paint(self, painter, option, QModelIndex())

        text = self._get_text(index.data())
        rect = option.rect.adjusted(4, 0, -4, 0)

        painter.drawText(rect, self.CELL_ALIGNMENT, text)

        # Doesnt work
        #style = QApplication.style()
        #rect = style.subElementRect(QStyle.SE_ItemViewItemText, option)
        #QApplication.style().drawControl(QStyle.CE_ItemViewItem, option, painter, widget)
            #index.data = lambda *args: self._show_value(data)
            #self._dat_file.table_columns[c-1]['display_type']
        #QStyledItemDelegate.paint(self, painter, option, index)

        painter.restore()

    def sizeHint(self, option=QStyleOptionViewItem(), index=QModelIndex()):
        fm = QFontMetrics(option.font)
        text = self._get_text(index.data())
        size = fm.boundingRect(option.rect, self.CELL_ALIGNMENT, text).size()
        return size+QSize(4,0)


class DatTableViewContextMenu(TableContextReadOnlyMenu):
    def _handle_data(self, data):
        return self.parent().itemDelegate()._get_text(data)


class DatFrame(QFrame):
    def __init__(self, dat_file=None, parent=None, *args, **kwargs):
        self._dat_file = dat_file

        QFrame.__init__(self, parent=parent)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        #
        # Information Stuff
        #
        self.frame_info = QGroupBox(self.tr('File Overview', parent=self))
        self.layout.addWidget(self.frame_info)

        self.frame_info_layout = QGridLayout()
        self.frame_info_layout.setColumnStretch(5, 1)
        self.frame_info.setLayout(self.frame_info_layout)

        self.row_label = QLabel(
            self.tr('Rows:'),
            parent=self.frame_info
        )
        self.frame_info_layout.addWidget(self.row_label, 0, 0)

        self.row_value = QLabel(
            str(dat_file.reader.table_rows),
            parent=self.frame_info
        )
        self.frame_info_layout.addWidget(self.row_value, 0, 1)

        self.length_label = QLabel(
            self.tr('Record Length:'),
            parent=self.frame_info
        )
        self.frame_info_layout.addWidget(self.length_label, 0, 2)

        self.length_value = QLabel(
            str(dat_file.reader.table_record_length),
            parent=self.frame_info,
        )
        self.frame_info_layout.addWidget(self.length_value, 0, 3)

        self.data_length_label = QLabel(
            self.tr('Data Length:'),
            parent=self.frame_info,
        )
        self.frame_info_layout.addWidget(self.data_length_label, 0, 4)

        self.data_length_value = QLabel(
            str(dat_file.reader.file_length-dat_file.reader.data_offset),
            parent=self.frame_info,
        )
        self.frame_info_layout.addWidget(self.data_length_value, 0, 5)

        #
        # Options
        #
        self.option_group_box = QGroupBox(self.tr('Options', parent=self))
        self.layout.addWidget(self.option_group_box)

        self.option_group_box_layout = QHBoxLayout()
        self.option_group_box.setLayout(self.option_group_box_layout)

        self.option_dereference_pointer = QCheckBox(
            self.tr('Dereference Pointer'),
            parent=self.option_group_box
        )
        self.option_dereference_pointer.setChecked(True)
        self.option_dereference_pointer.stateChanged.connect(
            self._on_option_deref_change
        )
        self.option_group_box_layout.addWidget(self.option_dereference_pointer)

        self.option_show_pointer = QCheckBox(
            self.tr('Always Show Pointer'), parent=self.option_group_box
        )
        self.option_show_pointer.setChecked(False)
        self.option_show_pointer.stateChanged.connect(self._refresh)
        self.option_group_box_layout.addWidget(self.option_show_pointer)

        #
        # Data Tables
        #

        self.table_main = QTableView(parent=self)
        self.table_main_context = DatTableViewContextMenu(
            parent=self.table_main
        )
        self.table_main_model = DatTableModel(dat_file)
        self.table_main_proxy_model = DatValueProxyModel(parent=self)
        self.table_main_proxy_model.setSourceModel(self.table_main_model)
        self.table_main.setModel(self.table_main_proxy_model)
        self.table_main.setSortingEnabled(True)
        self.table_main.setItemDelegate(DatStyle(self))
        head = self.table_main.horizontalHeader()
        head.setSectionResizeMode(QHeaderView.Interactive)
        #head.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.layout.addWidget(self.table_main)

        self.table_main_filter_menu = FilterMenu(
            self.table_main.horizontalHeader(),
            proxy_model=self.table_main_proxy_model,
        )

        self.table_data = QTableView(parent=self)
        self.table_data_context = DatTableViewContextMenu(
            parent=self.table_data
        )
        self.table_data_model = DatDataModel(dat_file)
        self.table_data_proxy_model = DatValueProxyModel(self)
        self.table_data_proxy_model.setSourceModel(self.table_data_model)
        self.table_data.setModel(self.table_data_proxy_model)
        self.table_data.setSortingEnabled(True)
        self.table_data.setItemDelegate(DatStyle(self, data_style=True))
        head = self.table_data.horizontalHeader()
        head.setSectionResizeMode(QHeaderView.Interactive)
        self.layout.addWidget(self.table_data)

        self.table_data_filter_menu = FilterMenu(
            self.table_data.horizontalHeader(),
            proxy_model=self.table_data_proxy_model,
        )

        self._refresh()

    def _on_option_deref_change(self, state):
        # State = 2 if checked, State = 0 if unchecked
        self.option_show_pointer.setEnabled(bool(state))
        self._refresh()

    def _refresh(self, *args):
        self.table_main.resizeColumnsToContents()
        self.table_data.resizeColumnsToContents()
        self.table_data_model.dataChanged.emit(0, 0)
        self.table_main_model.dataChanged.emit(0, 0)


class DatDataHandler(FileDataHandler):
    def __init__(self, x64=False):
        self.x64 = x64

    def get_widget(self, file_data, file_name='', parent=None, *args, **kwargs):
        dat_file = DatFile(file_name)
        # We want dat values here
        dat_file.read(file_data, use_dat_value=True, x64=self.x64)

        frame = DatFrame(dat_file=dat_file, parent=parent)

        return frame


class DDSDataHandler(FileDataHandler):
    """

    DDS Format:
    see: https://msdn.microsoft.com/en-us/library/bb943982.aspx

    """

    class DDSException(Exception):
        pass

    @staticmethod
    def dds_file_to_qimage(path):
        q = QGLWidget()
        q.makeCurrent()
        texture = q.bindTexture(path)
        if not texture:
            return

        GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
        w = GL.glGetTexLevelParameteriv(
            GL.GL_TEXTURE_2D, 0, GL.GL_TEXTURE_WIDTH
        )
        h = GL.glGetTexLevelParameteriv(
            GL.GL_TEXTURE_2D, 0, GL.GL_TEXTURE_HEIGHT
        )

        if w == 0 or h == 0:
            return

        pbuffer = QGLPixelBuffer(w, h, q.format(), q)
        if not pbuffer.makeCurrent():
            return

        pbuffer.drawTexture(QRectF(-1, -1, 2, 2), texture)
        return pbuffer.toImage()

    @staticmethod
    def get_image(file_data):
        """
        based on http://www.qtcentre.org/threads/29933-How-to-display-DDS-images

        TODO Fix warnings

        :param file_data:
        :return:
        """
        file_bytes = file_data.read()
        try:
            file_data = io.BytesIO(file_system.extract_dds(file_bytes))
        except NotImplementedError as e:
            raise DDSDataHandler.DDSException(*e.args)
        except ValueError as e:
            raise DDSDataHandler.DDSException(
                'This file is a reference to "%s"' %
                file_bytes[1:].decode('utf-8')
            )

        with TemporaryDirectory() as tmp_dir:
            tmp_file_path = os.path.join(tmp_dir, 'file.dds')
            with open(tmp_file_path, 'b+w') as tmp_file:
                tmp_file.write(file_data.read(20))
                # ddsHeader->dwLinearSize fix ... fuck you QT
                tmp_file.write(struct.pack('<I', 1))
                file_data.seek(24)
                # Write all data entries until
                # DDS_HEADER.DDS_PIXELFORMAT.dwFourCC
                tmp_file.write(file_data.read(15*4))
                dxt_type = file_data.read(4).decode('ascii')
                # Fix for displaying those. They have alpha precomputed, but it
                # should be a non issue, rather want to have them shown
                if dxt_type == 'DXT2':
                    dxt_type = 'DXT3'
                elif dxt_type == 'DXT4':
                    dxt_type = 'DXT5'
                tmp_file.write(dxt_type.encode('ascii'))
                tmp_file.write(file_data.read())
            return DDSDataHandler.dds_file_to_qimage(tmp_file_path)

    def get_widget(self, file_data, file_name, *args, **kwargs):
        label = QLabel(*args, **kwargs)
        # PyOpenGL not installed
        if GL is None:
            label.setText(label.tr('Install PyOpenGL to view DDS files.'))

        try:
            img = DDSDataHandler.get_image(file_data)
        except DDSDataHandler.DDSException as e:
            label.setText(label.tr(e.args[0]))
        else:
            if img is None:
                label.setText(label.tr('Unsupported DDS Format'))
            else:
                label.setPixmap(QPixmap.fromImage(img))

        scroll = QScrollArea()
        scroll.setWidget(label)
        scroll.setFrameStyle(QFrame.NoFrame)

        return scroll


class ImageDataHandler(FileDataHandler):
    extensions = ['.bmp', '.gif' '.jpg', '.png', '.pbm', '.pgm', '.ppm',
                  '.tiff', '.xbm', '.xpm']

    def get_widget(self, file_data, file_name, *args, **kwargs):
        self._verify_data(file_data)

        q = QByteArray.fromRawData(file_data.read())

        img = QImage.fromData(q)
        label = QLabel(*args, **kwargs)
        label.setPixmap(QPixmap.fromImage(img))

        scroll = QScrollArea()
        scroll.setWidget(label)
        scroll.setFrameStyle(QFrame.NoFrame)

        return scroll


class TextDataHandler(FileDataHandler):
    def __init__(self, encoding='utf-16_le'):
        self.encoding = encoding

    def get_widget(self, file_data, file_name, *args, **kwargs):
        self._verify_data(file_data)
        widget = QTextEdit(*args, **kwargs)
        widget.setReadOnly(True)
        widget.setText(file_data.read().decode(self.encoding))

        return widget

        # TODO ?
        #file_data.close()
