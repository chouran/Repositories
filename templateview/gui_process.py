import sys

from multiprocessing import Process
try:
    from PyQt4.QtGui import QApplication  # Python 2 compatibility.
except ImportError:  # i.e. ModuleNotFoundError
    from PyQt5.QtWidgets import QApplication  # Python 3 compatibility.

from template_window import TemplateWindow

class GUIProcess(Process):

    def __init__(self, params_pipe, number_pipe, templates_pipe, spikes_pipe, probe_path=None):

        Process.__init__(self)

        self._params_pipe = params_pipe
        self._number_pipe = number_pipe
        self._templates_pipe = templates_pipe
        self._spikes_pipe = spikes_pipe
        self._probe_path = probe_path

    def run(self):

        app = QApplication(sys.argv)
        screen_resolution = app.desktop().screenGeometry()
        window = TemplateWindow(self._params_pipe, self._number_pipe, self._templates_pipe, self._spikes_pipe,
                        probe_path=self._probe_path, screen_resolution=screen_resolution)
        window.show()
        app.exec_()

        return
