import numpy as np
from multiprocessing import Pipe
from gui_process import GUIProcess
from circusort.io.probe import load_probe
from circusort.io.template_store import load_template_store
from circusort.io.spikes import load_spikes

_ALL_PIPES_ = ['templates', 'spikes', 'number', 'params']
_ALL_PIPES_NO_PARAMS_ = ['templates', 'spikes', 'number']

class ORTSimulator(object):
    """Peak displayer"""

    def __init__(self, **kwargs):
        """Initialization"""

        self.nb_samples = 1024
        self.dtype = 'float32'
        self.sampling_rate = 20000
        self.probe_path = 'data/probe.prb'
        self.probe = load_probe(self.probe_path)
        self.nb_channels = self.probe.nb_channels
        self.export_peaks = True
        self.templates = load_template_store('data/templates.h5', self.probe_path)
        self.spikes = load_spikes('data/spikes.h5')
        self.all_pipes = {}

        for pipe in _ALL_PIPES_:
            self.all_pipes[pipe] = Pipe()
        
        self._qt_process = GUIProcess(self.all_pipes, probe_path=self.probe_path)

        self._qt_process.start()
        self.number = self.templates[0].creation_time - 10
        self.index = 0
        self.rates = []

        self.all_pipes['params'][1].send({
            'nb_samples': self.nb_samples,
            'sampling_rate': self.sampling_rate
        })

        return

    def run(self):

        while True:
            # Here we are increasing the counter

            templates = None
            print('test', self.number)
            while self.number == self.templates[self.index].creation_time:
                if templates is None:
                    templates = [self.templates[self.index].to_dict()]
                else:
                    templates += [self.templates[self.index].to_dict()]
                self.index += 1
                self.rates += [5 + 20*np.random.rand()]

            t_min = (self.number - 1)*self.nb_samples / self.sampling_rate
            t_max = self.number*self.nb_samples / self.sampling_rate

            # If we want to send real spikes
            spikes = self.spikes.get_spike_data(t_min, t_max, range(self.index))

            ## Otherwise we generate fake data
            # spike_times = [np.zeros(0, dtype=np.float32)]
            # amplitudes = [np.zeros(0, dtype=np.float32)]
            # templates = [np.zeros(0, dtype=np.int32)]
            

            # for ii in range(self.index):
            #     nb_spikes = int((t_max - t_min)*self.rates[ii])
            #     spike_times += [(t_min + t_max*np.random.rand(nb_spikes)).astype(np.float32)]
            #     amplitudes += [np.random.randn(nb_spikes).astype(np.float32)]
            #     templates += [ii*np.ones(nb_spikes, dtype=np.int32)]

            # spikes = {'spike_times' : np.concatenate(spike_times),
            #           'amplitudes' : np.concatenate(amplitudes),
            #           'templates' : np.concatenate(templates)}

            self.all_pipes['number'][1].send(self.number)
            self.all_pipes['templates'][1].send(templates)
            self.all_pipes['spikes'][1].send(spikes)
            self.number += 1

if __name__ == "__main__":
    # execute only if run as a script
    simulator = ORTSimulator()
    simulator.run()
