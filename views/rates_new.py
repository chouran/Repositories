import numpy as np

from vispy import app, gloo
from vispy.util import keys

from circusort.io.probe import load_probe
from circusort.io.template import load_template_from_dict

from utils.widgets import Controler
from views.canvas import ViewCanvas
from views.programs import SingleLinePlot, LinesPlot
from circusort.obj.cells import Cells
from circusort.obj.cell import Cell
from circusort.obj.train import Train
from circusort.obj.amplitude import Amplitude


class RateCanvas(ViewCanvas):

    requires = ['spikes', 'time']

    name = "Rates"

    def __init__(self, probe_path=None, params=None):
        ViewCanvas.__init__(self, title="Rate view")

        self.probe = load_probe(probe_path)
        self.add_single_box()
        self.cells = Cells({})
        self.time_window = 50
        self.time_window_from_start = True
        self.programs['rates'] = SingleLinePlot()
        self.controler = RateControler(self)
        self.selection = np.zeros(self.programs['rates'].nb_data, dtype=np.int32)

    @property
    def nb_templates(self):
        return len(self.cells)

    def zoom(self, zoom_value):
        self.programs['rates'].set_zoom_y_axis(zoom_value)
        self.update()
        return

    def _highlight_selection(self, selection):
        self.selection = np.zeros(self.programs['rates'].nb_data, dtype=np.int32)
        for i in selection:
            self.selection[i] = 1
        return

    def _set_value(self, key, value):

        if key == "full":
            self.time_window_from_start = value
        elif key == "range":
            self.time_window = int((value[0] // value[1]))

    def _on_reception(self, data):
        
        spikes = data['spikes'] if 'spikes' in data else None
        self.time = data['time'] if 'time' in data else None
        old_size = self.nb_templates

        if spikes is not None:

            is_known = np.in1d(np.unique(spikes['templates']), self.cells.ids)
            not_kwown = is_known[is_known == False]

            for i in range(len(not_kwown)):
                template = None
                new_cell = Cell(template, Train([], t_min=0), Amplitude([], [], t_min=0))
                self.cells.append(new_cell)

            self.cells.add_spikes(spikes['spike_times'], spikes['amplitudes'], spikes['templates'])    
            self.cells.set_t_max(self.time)

            if self.nb_templates > 0:          
                rates = self.cells.rate(self.controler.bin_size)
                colors = self.get_colors(self.nb_templates)
            
                if not self.time_window_from_start:
                    rates = rates[:, -self.time_window:]

                self.programs['rates'].set_data(rates, colors)
                #print(self.nb_templates, self.selection)
                #self._highlight_selection(self.selection)
                #self.programs['rates'].set_selection(self.selection)

        return


class RateControler(Controler):

    def __init__(self, canvas, bin_size=0.1):
        '''
        Control widgets:
        '''

        Controler.__init__(self, canvas)
        self.bin_size = bin_size
        
        self.dsb_bin_size = self.double_spin_box(label='Bin Size', unit='seconds', min_value=0.01,
                                                 max_value=100, step=0.1, init_value=self.bin_size)

        self.dsb_zoom = self.double_spin_box(label='Zoom', min_value=1, max_value=50, step=0.1,
                                             init_value=1)
        self.dsb_time_window = self.double_spin_box(label='Time window', unit='seconds',
                                                    min_value=1, max_value=50, step=0.1,
                                                    init_value=1)
        self.cb_tw = self.checkbox(label='Time window from start', init_state=True)


        self.add_widget(self.dsb_bin_size, self._on_binsize_changed)
        self.add_widget(self.dsb_zoom, self._on_zoomrates_changed)
        self.add_widget(self.dsb_time_window, self._on_time_window_changed)
        self.add_widget(self.cb_tw, self._time_window_rate_full)

    def _on_binsize_changed(self, bin_size):
        self.bin_size = self.dsb_bin_size['widget'].value()
        return

    def _on_zoomrates_changed(self):
        zoom_value = self.dsb_zoom['widget'].value()
        self.canvas.zoom_rates(zoom_value)
        return

    def _time_window_rate_full(self):
        value = self.cb_tw['widget'].isChecked()
        self.canvas.set_value({"full" : value})
        return

    def _on_time_window_changed(self):
        tw_value = self.dsb_time_window['widget'].value()
        self.canvas.set_value({"range" : (tw_value, self.bin_size)})
        return