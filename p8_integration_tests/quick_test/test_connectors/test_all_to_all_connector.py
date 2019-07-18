import spynnaker8 as sim
from p8_integration_tests.base_test_case import BaseTestCase


class TestAllToAllConnector(BaseTestCase):

    def check_weights(self, projection, sources, destinations):
        weights = projection.get(["weight"], "list")
        s_d_set = set((s, d) for s, d, _ in weights)
        self.assertEqual(len(weights), sources * destinations)
        self.assertEqual(len(s_d_set), sources * destinations)

    def check_other_connect(self, sources, destinations):
        sim.setup(1.0)
        pop1 = sim.Population(sources, sim.IF_curr_exp(), label="pop1")
        pop2 = sim.Population(destinations, sim.IF_curr_exp(), label="pop2")
        synapse_type = sim.StaticSynapse(weight=5, delay=1)
        projection = sim.Projection(
            pop1, pop2, sim.AllToAllConnector(), synapse_type=synapse_type)
        sim.run(1)
        self.check_weights(projection, sources, destinations)
        sim.end()

    def same(self):
        self.check_other_connect(5, 5)

    def test_same(self):
        self.runsafe(self.same)

    def less_sources(self):
        self.check_other_connect(5, 10)

    def test_less_sources(self):
        self.runsafe(self.less_sources)

    def less_destinations(self):
        self.check_other_connect(10, 5)

    def test_less_destinations(self):
        self.runsafe(self.less_destinations)

    def many(self):
        self.check_other_connect(500, 500)

    def test_many(self):
        self.runsafe(self.many)

    def get_before_run(self):
        sim.setup(1.0)
        pop1 = sim.Population(3, sim.IF_curr_exp(), label="pop1")
        pop2 = sim.Population(3, sim.IF_curr_exp(), label="pop2")
        synapse_type = sim.StaticSynapse(weight=5, delay=1)
        projection = sim.Projection(
            pop1, pop2, sim.AllToAllConnector(),
            synapse_type=synapse_type)
        weights = projection.get(["weight"], "list")
        sim.run(0)
        length = len(weights)
        self.assertEqual(9, length)
        sim.end()

    def test_get_before_run(self):
        self.runsafe(self.get_before_run)

    def using_static_synapse_singles(self):
        sim.setup(timestep=1.0)
        input = sim.Population(2, sim.SpikeSourceArray([0]), label="input")
        pop = sim.Population(2, sim.IF_curr_exp(), label="pop")
        conn = sim.Projection(input, pop, sim.AllToAllConnector(),
                              sim.StaticSynapse(weight=0.7, delay=3))
        sim.run(1)
        weights = conn.get(['weight', 'delay'], 'list')
        sim.end()
        target = [(0, 0, 0.7, 3), (0, 1, 3, 33), (1, 0, 0.4, 12),
                  (1, 1, 0.5, 21)]
        for i in range(2):
            for j in range(2):
                self.assertAlmostEqual(weights[i][j], target[i][j], places=3)

    def test_using_static_synapse_singles(self):
        self.runsafe(self.using_static_synapse_singles)
