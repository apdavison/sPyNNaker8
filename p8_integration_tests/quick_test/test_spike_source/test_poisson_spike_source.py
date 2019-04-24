from __future__ import division
from p8_integration_tests.base_test_case import BaseTestCase
import spynnaker8 as sim


class MyTestCase(BaseTestCase):

    def check_spikes(self, input, expected):
        neo = input.get_data("spikes")
        spikes = neo.segments[0].spiketrains
        count = 0
        for a_spikes in spikes:
            count += len(a_spikes)
        self.assertAlmostEqual(expected, count/len(spikes), delta=expected/10,
                               msg="Errror on {}".format(input.label))

    def recording_poisson_spikes(self, run_zero):
        sim.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
        n_neurons = 200  # number of neurons in each population
        sim.set_number_of_neurons_per_core(sim.IF_curr_exp, n_neurons / 2)

        cell_params_lif = {'cm': 0.25,
                           'i_offset': 0.0,
                           'tau_m': 20.0,
                           'tau_refrac': 2.0,
                           'tau_syn_E': 5.0,
                           'tau_syn_I': 5.0,
                           'v_reset': -70.0,
                           'v_rest': -65.0,
                           'v_thresh': -50.0
                           }

        pop_1 = sim.Population(
            n_neurons, sim.IF_curr_exp, cell_params_lif, label='pop_1')
        input = sim.Population(
            n_neurons, sim.SpikeSourcePoisson, {}, label='inputSpikes_1')

        sim.Projection(input, pop_1, sim.OneToOneConnector())

        input.record("spikes")

        if run_zero:
            sim.run(0)
        sim.run(5000)
        self.check_spikes(input, 5)

        sim.end()

    def recording_poisson_spikes_no_zero(self):
        self.recording_poisson_spikes(False)

    def test_recording_poisson_spikes_no_zero(self):
        self.runsafe(self.recording_poisson_spikes_no_zero)

    def recording_poisson_spikes_with_zero(self):
        self.recording_poisson_spikes(True)

    def test_recording_poisson_spikes_with_zero(self):
        self.runsafe(self.recording_poisson_spikes_with_zero)

    def recording_poisson_spikes_big(self):
        sim.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
        n_neurons = 2560  # number of neurons in each population
        sim.set_number_of_neurons_per_core(sim.IF_curr_exp, n_neurons / 2)

        cell_params_lif = {'cm': 0.25,
                           'i_offset': 0.0,
                           'tau_m': 20.0,
                           'tau_refrac': 2.0,
                           'tau_syn_E': 5.0,
                           'tau_syn_I': 5.0,
                           'v_reset': -70.0,
                           'v_rest': -65.0,
                           'v_thresh': -50.0
                           }

        pop_1 = sim.Population(
            n_neurons, sim.IF_curr_exp, cell_params_lif, label='pop_1')
        input = sim.Population(
            n_neurons, sim.SpikeSourcePoisson, {}, label='inputSpikes_1')

        sim.Projection(input, pop_1, sim.OneToOneConnector())

        input.record("spikes")

        sim.run(5000)
        self.check_spikes(input, 5)

        sim.end()

    def test_recording_poisson_spikes_big(self):
        self.runsafe(self.recording_poisson_spikes_big)

    def recording_poisson_spikes_rate_0(self):
        sim.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
        n_neurons = 256  # number of neurons in each population
        sim.set_number_of_neurons_per_core(sim.IF_curr_exp, n_neurons / 2)

        cell_params_lif = {'cm': 0.25,
                           'i_offset': 0.0,
                           'tau_m': 20.0,
                           'tau_refrac': 2.0,
                           'tau_syn_E': 5.0,
                           'tau_syn_I': 5.0,
                           'v_reset': -70.0,
                           'v_rest': -65.0,
                           'v_thresh': -50.0
                           }

        pop_1 = sim.Population(
            n_neurons, sim.IF_curr_exp, cell_params_lif, label='pop_1')
        input = sim.Population(
            n_neurons, sim.SpikeSourcePoisson, {'rate': 0}, label='input')

        sim.Projection(input, pop_1, sim.OneToOneConnector())

        input.record("spikes")

        sim.run(5000)
        self.check_spikes(input, 0)

        sim.end()

    def test_recording_poisson_spikes_rate_0(self):
        self.runsafe(self.recording_poisson_spikes_rate_0)

    def check_rates(self, rates, seconds):
        n_neurons = 100
        sim.setup(timestep=1.0)
        inputs = {}
        for rate in rates:
            params = {"rate": rate}
            input = sim.Population(
                n_neurons, sim.SpikeSourcePoisson, params,
                label='inputSpikes_{}'.format(rate))
            input.record("spikes")
            inputs[rate] = input
        sim.run(seconds * 1000)
        for rate in rates:
            self.check_spikes(inputs[rate], rate*seconds)
        sim.end()

    def recording_poisson_spikes_rate_fast(self):
        self.check_rates(
            [10.24, 20.48, 40.96, 81.92, 163.84, 327.68, 655.36, 1310.72], 10)

    def test_recording_poisson_spikes_rate_fast(self):
        self.runsafe(self.recording_poisson_spikes_rate_fast)

    def recording_poisson_spikes_rate_slow(self):
        try:
            self.check_rates(
                [0, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32,
                 0.64, 1.28, 2.56, 5.12],
                100)
        except AssertionError:
            sim.end()
            self.known_issue(
                "https://github.com/SpiNNakerManchester/sPyNNaker/issues/629")

    def test_recording_poisson_spikes_rate_slow(self):
        self.runsafe(self.recording_poisson_spikes_rate_slow)