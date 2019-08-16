from spynnaker.pyNN.models.neuron.plasticity.stdp.weight_dependence \
    import WeightDependenceERBPad as _BaseClass


class WeightDependenceERBPad(_BaseClass):
    # noinspection PyPep8Naming
    def __init__(self, w_min=0.0, w_max=1.0, reg_rate=0.0):
        super(WeightDependenceERBPad, self).__init__(
            w_min=w_min, w_max=w_max, reg_rate=reg_rate)
