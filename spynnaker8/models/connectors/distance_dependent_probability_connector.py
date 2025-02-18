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

from pyNN.connectors import (
    DistanceDependentProbabilityConnector as
    PyNNDistanceDependentProbabilityConnector)
from spynnaker.pyNN.models.neural_projections.connectors import (
    DistanceDependentProbabilityConnector as
    CommonDistanceDependentProbabilityConnector)


class DistanceDependentProbabilityConnector(
        CommonDistanceDependentProbabilityConnector,
        PyNNDistanceDependentProbabilityConnector):
    """ Make connections using a distribution which varies with distance.
    """
    __slots__ = []

    def __init__(
            self, d_expression, allow_self_connections=True,  safe=True,
            verbose=False, n_connections=None, rng=None, callback=None):
        """

        :param `string` d_expression: \
            the right-hand side of a valid python expression for\
            probability, involving 'd', e.g. "exp(-abs(d))", or "d<3",\
            that can be parsed by eval(), that computes the distance\
            dependent distribution
        :param `bool` allow_self_connections: \
            if the connector is used to connect a\
            Population to itself, this flag determines whether a neuron is\
            allowed to connect to itself, or only to other neurons in the\
            Population.
        :param `int` n_connections: \
            The number of efferent synaptic connections per neuron.
        :param safe: if True, check that weights and delays have valid\
            values. If False, this check is skipped.
        """
        # pylint: disable=too-many-arguments
        CommonDistanceDependentProbabilityConnector.__init__(
            self, d_expression=d_expression,
            allow_self_connections=allow_self_connections,
            safe=safe, verbose=verbose, n_connections=n_connections)
        PyNNDistanceDependentProbabilityConnector.__init__(
            self, d_expression=d_expression,
            allow_self_connections=allow_self_connections, rng=rng, safe=safe,
            callback=callback)
