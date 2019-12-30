"""
Proxy Filter Model

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/ui/shared/proxy_filter_model.py                            |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Proxy model for generic table filtering and related viewing classes.

Agreement
===============================================================================

See PyPoE/LICENSE

TODO
===============================================================================

- Reset filter
- Validate that the filter is working properly for the data; possibly disallow
  wrong filters
- Fix the wierd box appearing on the late page if going back
- Add menu for the generic wizard

"""

# =============================================================================
# Imports
# =============================================================================

# Python
import re
from collections import OrderedDict, defaultdict

# 3rd-party
from PySide2.QtCore import *
from PySide2.QtWidgets import *

# self
from PyPoE.ui.shared.regex_widgets import RegexFlagsBox

# =============================================================================
# Globals
# =============================================================================

__all__ = []

# =============================================================================
# Classes
# =============================================================================

#
# Filters
#

class AbstractFilter:

    NAME = ''

    def __init__(self, value):
        self.value = value

    def get_name(self):
        return self.NAME

    def apply(self, value):
        return True

    def set_defaults(self, qwizardpage):
        pass

    @staticmethod
    def generate_settings(qwizardpage):
        pass

    @staticmethod
    def validate_settings(qwizardpage):
        pass


class RegexFilter(AbstractFilter):

    NAME = QT_TR_NOOP('Regular Expression Filter')

    def __init__(self, value, flags=0):
        self.value = value
        self.flags = flags
        self.regex = re.compile(value, flags)

    def __repr__(self):
        return '%s(value=%s, flags=%s)' % (
            self.__class__.__name__, self.value, self.flags
        )

    def apply(self, value):
        return self.regex.match(str(value)) is not None

    def set_defaults(self, qwizardpage):
        qwizardpage.regex_edit.setText(self.value)
        for flag_info in qwizardpage.regex_flags._regex_flags:
            if flag_info['flag'] & self.flags:
                box = getattr(qwizardpage.regex_flags, flag_info['variable'])
                box.setChecked(True)

    @staticmethod
    def generate_settings(qwizardpage):
        qwizardpage.regex_flags = RegexFlagsBox(parent=qwizardpage)
        qwizardpage.layout.addWidget(qwizardpage.regex_flags)

        qwizardpage.layout.addWidget(QLabel(qwizardpage.tr(
            'Enter a regular expression:'
        )))

        qwizardpage.regex_edit = QLineEdit(parent=qwizardpage)
        qwizardpage.layout.addWidget(qwizardpage.regex_edit)

    @staticmethod
    def validate_settings(qwizardpage):
        regex = qwizardpage.regex_edit.text()
        try:
            obj = RegexFilter(
                value=regex,
                flags=qwizardpage.regex_flags.get_flags()
            )
        except re.error as e:
            QMessageBox.critical(
                qwizardpage,
                qwizardpage.tr('RegEx Error'),
                qwizardpage.tr('Regular Expression error:\n %s') % e.args[0]
            )
            #TODO log error
            return

        return obj


class TypedFilter(AbstractFilter):
    operations = OrderedDict((
        ('lt', {
            'name': '<',
            'tooltip': QT_TR_NOOP('less than'),
        }),
        ('le', {
            'name': '<=',
            'tooltip': QT_TR_NOOP('less than or equal to'),
        }),
        ('eq', {
            'name': '==',
            'tooltip': QT_TR_NOOP('equal to'),
        }),
        ('ne', {
            'name': '!=',
            'tooltip': QT_TR_NOOP('not equal to'),
        }),
        ('ge', {
            'name': '>=',
            'tooltip': QT_TR_NOOP('greater than or equal to'),
        }),
        ('gt', {
            'name': '>',
            'tooltip': QT_TR_NOOP('greater than'),
        }),
    ))
    types = OrderedDict((
        (int, {
            'name': QT_TR_NOOP('Integer'),
            'tooltip': QT_TR_NOOP('Any kind of whole number'),
        }),
        (float, {
            'name': QT_TR_NOOP('Float'),
            'tooltip': QT_TR_NOOP('Any kind of floating point number.'),
        }),
        (str, {
            'name': QT_TR_NOOP('String'),
            'tooltip': QT_TR_NOOP('Any kind of string.'),
        }),
    ))

    NAME = QT_TR_NOOP('Simple Operation Filter')

    def __init__(self, value, operation, type):
        if type not in self.types:
            raise TypeError('"%s" is not a valid type.')
        self.type = type

        self.value = self.type(value)

        if operation not in self.operations:
            raise ValueError('"%s" is not a valid operation.' % operation)

        self.operation = operation
        # will raise an exception accordingly
        self._operation_func = getattr(self.type, '__' + operation + '__')

    def __repr__(self):
        return '%s(value=%s, operation=%s, type=%s)' % (
            self.__class__.__name__, self.value, self.operation, self.type
        )

    def apply(self, value):
        try:
            return self._operation_func(self.type(value), self.value)
        except (ValueError, TypeError):
            return False

    def set_defaults(self, qwizardpage):
        qwizardpage.type_box.setCurrentIndex(
            list(self.types.keys()).index(self.type)
        )

        qwizardpage.operation_box.setCurrentIndex(
            list(self.operations.keys()).index(self.operation)
        )

        qwizardpage.value_edit.setText(str(self.value))

    @staticmethod
    def generate_settings(qwizardpage):
        for k in ('type', 'operation'):
            box = QComboBox(parent=qwizardpage)

            for i, info in enumerate(getattr(TypedFilter, k + 's').values()):
                box.addItem(info['name'])
                box.setItemData(i, info['tooltip'], Qt.ToolTipRole)
            qwizardpage.layout.addWidget(box)

            setattr(qwizardpage, '%s_box' % k, box)

        qwizardpage.layout.addWidget(
            QLabel(qwizardpage.tr('Enter value:'), parent=qwizardpage)
        )
        qwizardpage.value_edit = QLineEdit(parent=qwizardpage)
        qwizardpage.layout.addWidget(qwizardpage.value_edit)

    @staticmethod
    def validate_settings(qwizardpage):
        kwargs = {
            'value': qwizardpage.value_edit.text(),
            'operation': list(TypedFilter.operations.keys())[qwizardpage.operation_box.currentIndex()],
            'type': list(TypedFilter.types.keys())[qwizardpage.type_box.currentIndex()],
        }

        try:
            obj = TypedFilter(**kwargs)
        except Exception as e:
            QMessageBox.critical(
                qwizardpage,
                qwizardpage.tr('Error\n'),
                qwizardpage.tr('Error:\n %s') % e.args[0]
            )
            #TODO log error
            return

        return obj


FILTERS = [RegexFilter, TypedFilter]

#
# Filter Wizard & Pages
#


class FilterWizard(QWizard):
    PAGE_COLUMN_SELECTION = 1
    PAGE_FILTER_SELECTION = 2
    PAGE_FILTER_SETTINGS = 3
    PAGE_FILTER_CREATE = 4

    def __init__(self, filter_proxy, *args, **kwargs):
        QWizard.__init__(self, *args, **kwargs)

        self.filter_proxy = filter_proxy

        self.setWindowTitle(self.tr('Modify filters'))
        self.setPage(
            self.PAGE_COLUMN_SELECTION,
            FilterWizardColumnPage(parent=self),
        )
        self.setPage(
            self.PAGE_FILTER_SELECTION,
            FilterWizardFilterSelectionPage(parent=self),
        )
        self.setPage(
            self.PAGE_FILTER_SETTINGS,
            FilterWizardFilterSettingsPage(parent=self),
        )
        self.setPage(
            self.PAGE_FILTER_CREATE,
            FilterWizardCreateFilterPage(parent=self),
        )

        self.currentIdChanged.connect(self._hide_back_button)

    def _hide_back_button(self, id):
        self.button(QWizard.BackButton).setEnabled(False)


class FilterWizardPageShared(QWizardPage):
    def get_filters(self):
        return self.wizard().filter_proxy.filters


class FilterWizardColumnPage(FilterWizardPageShared):
    def __init__(self, *args, **kwargs):
        QWizardPage.__init__(self, *args, **kwargs)
        self.setTitle(self.tr('Select a column'))

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.column_list = QComboBox(parent=self)
        fp = self.parent().filter_proxy
        for column_id in range(0, fp.sourceModel().columnCount()):
            self.column_list.addItem(self.tr('%s: %s (%s filters)') % (
                column_id,
                fp.sourceModel().headerData(column_id, Qt.Horizontal),
                len(fp.filters[column_id]),
            ))
        self.registerField('COLUMN_LIST', self.column_list)
        self.layout.addWidget(self.column_list)


class FilterWizardFilterSelectionPage(FilterWizardPageShared):
    def __init__(self, *args, **kwargs):
        QWizardPage.__init__(self, *args, **kwargs)
        self.setTitle(self.tr('Select a filter'))

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.filter_list = QComboBox(parent=self)
        self.registerField('FILTER_LIST', self.filter_list)
        self.layout.addWidget(self.filter_list)

    def initializePage(self):
        self.filter_list.clear()
        for i, filter in enumerate(self.get_filters()[self.field('COLUMN_LIST')]):
            self.filter_list.addItem(self.tr('%s: %s') % (
                i,
                repr(filter),
            ))
        self.filter_list.addItem(self.tr('Add new filter'))

    def nextId(self):
        filters = self.get_filters()[self.field('COLUMN_LIST')]
        filter_id = self.field('FILTER_LIST')
        if filter_id < len(filters):
            return FilterWizard.PAGE_FILTER_SETTINGS
        else:
            return FilterWizard.PAGE_FILTER_CREATE


class FilterWizardFilterSettingsPage(FilterWizardPageShared):
    def __init__(self, *args, **kwargs):
        QWizardPage.__init__(self, *args, **kwargs)
        self.setTitle(self.tr('Modify filter settings'))
        self.setFinalPage(True)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def _get_filter(self):
        return self.get_filters()[self.field('COLUMN_LIST')][self.field('FILTER_LIST')]

    def nextId(self):
        return -1

    def cleanupPage(self):

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def initializePage(self):
        filter = self._get_filter()
        filter.generate_settings(self)
        if not isinstance(filter, type):
            filter.set_defaults(self)

    def validatePage(self):
        filter = self._get_filter()

        obj = filter.validate_settings(self)
        if obj is None:
            return False

        filter_list = self.get_filters()[self.field('COLUMN_LIST')]
        # Replace the filter (will be class or old object)
        filter_list[-1] = obj

        self.wizard().filter_proxy.invalidateFilter()

        return True


class FilterWizardCreateFilterPage(FilterWizardPageShared):
    def __init__(self, *args, **kwargs):
        QWizardPage.__init__(self, *args, **kwargs)
        self.setTitle(self.tr('Create a new filter'))

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.filter_type_list = QComboBox(parent=self)
        for filter_cls in FILTERS:
            self.filter_type_list.addItem(filter_cls.NAME)

        self.layout.addWidget(self.filter_type_list)

    def cleanupPage(self):
        try:
            self.get_filters()[self.field('COLUMN_LIST')].pop(-1)
        except IndexError:
            pass

    def validatePage(self):
        self.get_filters()[self.field('COLUMN_LIST')].append(
            FILTERS[self.filter_type_list.currentIndex()]
        )

        return True

    def nextId(self):
        return FilterWizard.PAGE_FILTER_SETTINGS


#
# Misc
#


class FilterMenu(QMenu):
    def __init__(self, *args, proxy_model=None, **kwargs):
        QMenu.__init__(self, *args, **kwargs)

        header = self.parent()
        header.setContextMenuPolicy(Qt.CustomContextMenu)
        header.customContextMenuRequested.connect(self.popup)

        if not isinstance(proxy_model, FilterProxyModel):
            raise TypeError("proxy_model has invalid type %s" % type(proxy_model))
        self.proxy_model = proxy_model

        self.action_add_filter = self.addAction(
            self.tr("Add/Change filter"),
            self.add_filter,
        )
        self.action_reset_filter = self.addAction(
            self.tr("Reset filter"),
            self.reset_filter,
        )
        self.addSeparator()
        self.action_reset_all_filters = self.addAction(
            self.tr("Reset all filters"),
            self.reset_all_filters,
        )

        self.point = None

    def add_filter(self, *args, **kwargs):
        index = self.parent().logicalIndexAt(self.point)
        wizard = FilterWizard(
            filter_proxy=self.proxy_model,
            parent=self,
        )
        wizard.setField('COLUMN_LIST', index)
        wizard.setStartId(FilterWizard.PAGE_FILTER_SELECTION)
        wizard.show()

    def reset_filter(self, *args, **kwargs):
        index = self.parent().logicalIndexAt(self.point)
        self.proxy_model.filters[index] = []
        self.proxy_model.invalidateFilter()

    def reset_all_filters(self, *args, **kwargs):
        self.proxy_model.reset_all_filters()
        self.proxy_model.invalidateFilter()

    def popup(self, point, *args, **kwargs):
        self.point = point
        QMenu.popup(self, self.parent().mapToGlobal(point))


class FilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent, *args, **kwargs):
        QSortFilterProxyModel.__init__(self, *args, parent=parent, **kwargs)

        self.reset_all_filters()

    def reset_all_filters(self):
        """
        Resets all filters
        """
        self.filters = defaultdict(lambda: [])

    def add_filter(self, row, filter):
        if row not in self.filters:
            self.filters[row] = [filter, ]
        else:
            self.filters[row].append(filter)

    def _get_data(self, row, column, parent):

        # Should probably not use data()
        return self.sourceModel().index(row, column, parent).data()

    def filterAcceptsRow(self, source_row, source_parent):
        accepted = True
        for column, filters in self.filters.items():
            data = self._get_data(source_row, column, source_parent)
            for filter in filters:
                accepted = accepted and filter.apply(data)
                if not accepted:
                    return False

        return accepted

# =============================================================================
# Functions
# =============================================================================
