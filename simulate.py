import numpy as np
import os
from multiprocessing import Pipe
from gui_process import GUIProcess
from circusort.io.probe import load_probe
from circusort.io.template_store import load_template_store
from circusort.io.spikes import load_spikes

_ALL_PIPES_ = ['templates', 'spikes', 'number', 'params', 'data', 'peaks', 'thresholds']

class ORTSimulator(object):
    """Peak displayer"""

    def __init__(self, debug=False, **kwargs):
        """Initialization"""

        self.data_path = 'data'
        self.nb_samples = 1024
        self.dtype = 'float32'
        self.sampling_rate = 20000
        self.probe_path = os.path.join(self.data_path, 'probe.prb')
        self.probe = load_probe(self.probe_path)
        self.nb_channels = self.probe.nb_channels
        self.export_peaks = False
        self.templates = load_template_store(os.path.join(self.data_path, 'templates.h5'), self.probe_path)
        self.spikes = load_spikes(os.path.join(self.data_path, 'spikes.h5'))
        self.all_pipes = {}
        self.debug = debug

        for pipe in _ALL_PIPES_:
            self.all_pipes[pipe] = Pipe()
        
        self._qt_process = GUIProcess(self.all_pipes)

        self._qt_process.start()
        self.number = self.templates[0].creation_time - 10
        self.index = 0
        self.rates = []

        self.all_pipes['params'][1].send({
            'nb_samples': self.nb_samples,
            'sampling_rate': self.sampling_rate, 
            'probe_path' : self.probe_path
        })

        return

    def run(self):

        while True:
            # Here we are increasing the counter

            templates = None

            while self.number == self.templates[self.index].creation_time:
                if templates is None:
                    templates = [self.templates[self.index].to_dict()]
                else:
                    templates += [self.templates[self.index].to_dict()]
                self.index += 1

            t_min = (self.number - 1)*self.nb_samples / self.sampling_rate
            t_max = self.number*self.nb_samples / self.sampling_rate

            # If we want to send real spikes
            spikes = self.spikes.get_spike_data(t_min, t_max, range(self.index))

            # Here we need to generate the fake data
            data = np.random.randn(self.nb_samples, self.nb_channels).astype(np.float32)

            # Here we are generating fake thresholds
            mads = np.std(data, 0)

            if self.export_peaks:
                peaks = {}
                for i in range(self.nb_channels):
                    peaks[i] = np.where(data[i] > mads[i])[0]
            else:
                peaks = None
            
            self.all_pipes['peaks'][1].send(peaks)
            self.all_pipes['data'][1].send(data)
            self.all_pipes['thresholds'][1].send(mads)
            self.all_pipes['number'][1].send(self.number)
            self.all_pipes['templates'][1].send(templates)
            self.all_pipes['spikes'][1].send(spikes)
            self.number += 1
            if self.debug:
                print('Sending packet', self.number, self.index)

if __name__ == "__main__":
    # execute only if run as a script
    simulator = ORTSimulator()
    simulator.run()
