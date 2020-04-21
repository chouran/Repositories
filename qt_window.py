from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

#from PyQt5.QtWidgets import*
#from PyQt5.QtCore import*
#from PyQt5.QtGui import*

import sys
from rt_signals import *

class Color(QtWidgets.QWidget):

    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Import Vispy Canvas
        self._canvas = SignalCanvas()
        self._canvas.native.setParent(self)
        signals_widget = self._canvas.native

        #Window Custom
        self.setWindowTitle("Real time signals")

        toolbar = QtWidgets.QToolBar('main toolbar')
        toolbar.setIconSize(QtCore.QSize(32, 32))
        self.addToolBar(toolbar)

        button_action = QtWidgets.QAction(QtGui.QIcon("brain.png"),
                        'button 1', self)                            # Button creation
        button_action.setStatusTip("brain button")                   # Informative text
        button_action.triggered.connect(self.button_click)           # Signal slot connection
        button_action.setCheckable(True)    #1
        button_action.setShortcut(QtGui.QKeySequence("Ctrl+p"))            # Shortcut
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        button_action2 = QtWidgets.QAction(QtGui.QIcon("android.png"), 'button2', self)
        button_action2.setStatusTip("android button")
        button_action2.triggered.connect(self.button_click)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)

        toolbar.addSeparator()
        toolbar.addWidget(QtWidgets.QLabel("Spiking Circus"))
        toolbar.addSeparator()
        toolbar.addWidget(QtWidgets.QCheckBox())
        self.setStatusBar(QtWidgets.QStatusBar(self))

        # Menus => pretty easy to manipulate
        menu = self.menuBar()

        file_menu = menu.addMenu("File")
        file_menu.addAction(button_action)
        file_menu.addSeparator()
        file_menu.addAction(button_action2)

        file_submenu = file_menu.addAction(button_action2)
        menu.addSeparator()
        edit_menu = menu.addMenu("Edit")
        menu.addSeparator()
        options_menu = menu.addMenu("Options")
        menu.addSeparator()
        help_menu = menu.addMenu("Help")

        # Threshold widget
        #widget_seuil = QtWidgets.QDoubleSpinBox()
        #widget_seuil.setMinimum(-1.0)
        #widget_seuil.setMaximum(+1.0)
        #widget_seuil.setSuffix(" mV")
        #widget_seuil.setSingleStep(0.01)
        #widget_seuil.valueChanged.connect(self.th_value)

        widget_th = QtWidgets.QCheckBox()
        widget_th.setText('See Thresholds')
        widget_th.setCheckState(QtCore.Qt.Checked)
        widget_th.stateChanged.connect(self.see_th)

        widget_spikes = QtWidgets.QCheckBox()
        widget_spikes.setText('See Spikes')
        widget_spikes.setCheckState(QtCore.Qt.Checked)
        widget_spikes.stateChanged.connect(self.see_spikes)

        #Scale widgets
        widget_x = QtWidgets.QCheckBox()
        widget_y = QtWidgets.QCheckBox()
        widget_x.setText('x_axis')
        widget_y.setText('y_axis')
        box_button = QtWidgets.QButtonGroup()
        box_button.addButton(widget_x, -1)
        box_button.addButton(widget_y, -1)
        widget_x.setCheckState(QtCore.Qt.Checked)
        #widget_x.stateChanged.connect(self.scale)
        #widget_y.stateChanged.connect(self.scale_y)
        widget_y.setCheckState(QtCore.Qt.Checked)

        # Layout
        layout = QtWidgets.QGridLayout()
        layout.addWidget(widget_th, 0, 0)
        layout.addWidget(widget_spikes, 1, 0)
        layout.addWidget(widget_x, 2, 0)
        layout.addWidget(widget_y, 3, 0)

        layout.addWidget(signals_widget, 0,1)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    # Create the slot associated to the toolbar button
    def button_click(self, s):
        print ("T'as cliqué", s)

    #Connect the spin Box value to the thresholds
    def th_value(self, t):
         #print (" Threshold value = ", t)
         self._canvas.update_threshold(t)

    def see_th(self, t):
        self._canvas.see_thresholds(t)

    def see_spikes(self, s):
        print(s)
        self._canvas.see_spikes(s)

    def scale(self, x):
        print (x)
        self._canvas.update(True,x)


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()