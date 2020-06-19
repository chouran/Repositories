# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

try:
    # Python 2 compatibility.
    from PyQt4.QtCore import Qt
    from PyQt4.QtGui import QMainWindow, QLabel, QDoubleSpinBox, QSpacerItem, \
        QSizePolicy, QGroupBox, QGridLayout, QLineEdit, QDockWidget, QListWidget, \
        QListWidgetItem, QAbstractItemView, QCheckBox, QTableWidget, QTableWidgetItem
except ImportError:  # i.e. ModuleNotFoundError
    # Python 3 compatibility.
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QMainWindow, QLabel, QDoubleSpinBox, QSpacerItem, \
        QSizePolicy, QGroupBox, QGridLayout, QLineEdit, QDockWidget, QListWidget, \
        QListWidgetItem, QAbstractItemView, QCheckBox, QTableWidget, QTableWidgetItem, QTreeWidget
    from PyQt5 import QtGui, QtCore


# -----------------------------------------------------------------------------
# Create control widgets
# -----------------------------------------------------------------------------

class CustomWidget:
    def __init__(self):
        self.x = 3

    def double_spin_box(self, **kwargs):

        """""
        kwargs parameters 
        label : str
        unit : str
        min value : float
        max value : float
        step : float
        init_value : float
        
        return a dictionnary with the following objects : label, double spin box, unit_label
        """""

        dsb_widget = {}
        dsb = QDoubleSpinBox()
        dsb.setMaximumWidth(100)
        if 'label' in kwargs.keys():
            label_dsb = QLabel()
            label_dsb.setText(kwargs['label'])
            dsb_widget['label'] = label_dsb
        if 'min_value' in kwargs.keys():
            dsb.setMinimum(kwargs['min_value'])
        if 'max_value' in kwargs.keys():
            dsb.setMaximum(kwargs['max_value'])
        if 'step' in kwargs.keys():
            dsb.setSingleStep(kwargs['step'])
        if 'init_value' in kwargs.keys():
            dsb.setValue(kwargs['init_value'])

        dsb_widget['widget'] = dsb

        if 'unit' in kwargs.keys():
            label_unit = QLabel()
            label_unit.setText(kwargs['unit'])
            dsb_widget['unit'] = label_unit

        return dsb_widget

    def checkbox(self, **kwargs):

        """""
        kwargs param
        label : str
        init_state : bool
        
        return a dictionnary with the following objects : label, checkbox
        """""

        cb_widget = {}
        cb = QCheckBox()

        if 'label' in kwargs.keys():
            label_cb = QLabel()
            label_cb.setText(kwargs['label'])
            cb_widget['label'] = label_cb
        if 'init_state' in kwargs.keys():
            cb.setChecked(kwargs['init_state'])
        cb_widget['widget'] = cb

        return cb_widget

    def line_edit(self, **kwargs):
        """""
        kwargs param
        label : str
        init_value : str
        read_only : bool
        unit : str

        return a dictionnary with the following objects : label, text, unit
        """""
        text_widget = {}
        self.text_box = QLineEdit()
        self.text_box.setMaximumWidth(300)
        if 'label' in kwargs.keys():
            self.label = QLabel()
            self.label.setText(kwargs['label'])
            text_widget['label'] = self.label
        self.text_box.setText(kwargs['init_value'])
        self.text_box.setReadOnly(kwargs['read_only'])
        self.text_box.setAlignment(Qt.AlignRight)
        text_widget['widget'] = self.text_box
        if 'unit' in kwargs.keys():
            self.label_unit = QLabel()
            self.label_unit.setText(kwargs['label_unit'])
            text_widget['label_unit'] = self.label_unit

        return text_widget


class TreeWidget(QTreeWidget):
    def sizeHint(self):
        return QtCore.QSize(100, 50)


def dock_canvas(vispy_canvas, title=None):
    """ Transform Vispy Canvas into QT Canvas """
    qt_canvas = vispy_canvas.native
    dock_obj = QDockWidget()
    dock_obj.setWidget(qt_canvas)
    if title is not None:
        dock_obj.setWindowTitle(title)
    return dock_obj


def dock_control(title=None, position=None, *args):
    """"
    title : str
    position : str ('Left', ' Right', 'Top', 'Bottom')
    args : dict of widgets
    return a grid layout object with the widgets correctly  positioned
    """

    grid_layout = QGridLayout()
    group_box = QGroupBox()
    dock_widget = QDockWidget()

    resize = TreeWidget()

    i = 0  # line_number
    for widget_dict in args:
        j = 0  # column_number
        for name, widget_obj in widget_dict.items():
            grid_layout.addWidget(widget_obj, i, j)
            j += 1
        i += 1
    spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
    grid_layout.addItem(spacer)
    grid_layout.setSizeConstraint(50)

    group_box.setLayout(grid_layout)
    dock_widget.setWidget(group_box)
    if title is not None:
        dock_widget.setWindowTitle(title)

    # TODO Resize dock or individual widget?
    # dock_widget.setWidget(resize)

    return dock_widget


def dock_pos(position):
    if position == 'left':
        return Qt.LeftDockWidgetArea
    elif position == 'right':
        return Qt.RightDockWidgetArea
    elif position == 'bottom':
        return Qt.BottomDockWidgetArea
    elif position == 'top':
        return Qt.TopDockWidgetArea