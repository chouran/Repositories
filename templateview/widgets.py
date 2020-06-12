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
        QListWidgetItem, QAbstractItemView, QCheckBox, QTableWidget, QTableWidgetItem

# -----------------------------------------------------------------------------
# Create control widgets
# -----------------------------------------------------------------------------

class ControlWidget:
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

    @staticmethod
    def line_edit(**kwargs):
        """""
        kwargs param
        label : str
        init_value : str
        read_only : bool
        unit : str

        return a dictionnary with the following objects : label, text, unit
        """""
        text_widget = {}
        text_box = QLineEdit()
        if 'label' in kwargs.keys():
            label = QLabel()
            label.setText(kwargs['label'])
            text_widget['label'] = label
        text_box.setText(kwargs['init_value'])
        text_box.setReadOnly(kwargs['read_only'])
        text_box.setAlignment(Qt.AlignRight)
        text_widget['widget'] = text_box
        if 'unit' in kwargs.keys():
            label_unit = QLabel()
            label_unit.setText(kwargs['label_unit'])
            text_widget['label_unit'] = label_unit

        return text_widget

    def grid_layout(self, *args):
        '''
        :param args:
        :return:
        '''

        grid_layout = QGridLayout()


def info_dock(probe_path):
    # Create info widgets.
    info_time_widget = ControlWidget.line_edit(label='Time', init_value='0', read_only=True, label_unit='s')
    info_buffer_widget = ControlWidget.line_edit(label='Buffer', init_value='0', read_only=True, label_unit=None)
    info_probe_widget = ControlWidget.line_edit(label='Probe', init_value="{}".format(probe_path),
                                                read_only=True, label_unit=None)

    info_dock_widget = dock_control('Left', 'Info', info_time_widget, info_buffer_widget, info_probe_widget)
    return info_dock_widget


def dock_canvas(vispy_canvas):
    """ Transform Vispy Canvas into QT Canvas """
    qt_canvas = vispy_canvas.native
    dock_obj = QDockWidget()
    dock_obj.setAllowedAreas(Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)
    dock_obj.setWidget(qt_canvas)
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

    if position == 'Left':
        dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea)
    elif position == 'Right':
        dock_widget.setAllowedAreas(Qt.RightDockWidgetArea)

    for widget_dict in args:
        i = 0  # line_number
        for name, widget_obj in widget_dict.items():
            j = 0  # column number
            grid_layout.addWidget(widget_obj, i, j)
            j += 1
        i += 1
    spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
    grid_layout.addItem(spacer)

    group_box.setLayout(grid_layout)
    dock_widget.setWidget(group_box)
    if title is not None:
        dock_widget.setWindowTitle(title)

    return dock_widget





