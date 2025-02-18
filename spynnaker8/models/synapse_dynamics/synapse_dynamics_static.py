# Copyright (c) 2017-2019 The University of Manchester
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pyNN.standardmodels.synapses import StaticSynapse as PyNNStaticSynapse
from spinn_front_end_common.utilities import globals_variables
from spynnaker.pyNN.models.neuron.synapse_dynamics import (
    SynapseDynamicsStatic as
    _BaseClass)


class SynapseDynamicsStatic(_BaseClass):
    __slots__ = [
        "__delay",
        "__weight"]

    def __init__(
            self, weight=PyNNStaticSynapse.default_parameters['weight'],
            delay=None):
        super(SynapseDynamicsStatic, self).__init__()
        self.__weight = weight

        if delay is None:
            delay = globals_variables.get_simulator().min_delay
        self.__delay = delay

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, new_value):
        self.__weight = new_value

    @property
    def delay(self):
        return self.__delay

    @delay.setter
    def delay(self, new_value):
        self.__delay = new_value
