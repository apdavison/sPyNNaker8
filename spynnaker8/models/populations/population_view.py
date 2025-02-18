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

import logging
import numpy
from six import integer_types
from pyNN import descriptions
from pyNN.random import NumpyRNG
from spinn_utilities.ranged.abstract_sized import AbstractSized
from .idmixin import IDMixin
from .population_base import PopulationBase

logger = logging.getLogger(__name__)


class PopulationView(PopulationBase):
    """ A view of a subset of neurons within a :py:class:`Population`.

    In most ways, Populations and PopulationViews have the same behaviour,\
    i.e., they can be recorded, connected with Projections, etc. \
    It should be noted that any changes to neurons in a PopulationView\
    will be reflected in the parent Population and vice versa.

    It is possible to have views of views.

    .. note::
        Selector to Id is actually handled by :py:class:`AbstractSized`.
    """
    __slots__ = [
        "__annotations",
        "__indexes",
        "__label",
        "__mask",
        "__parent",
        "__population"]

    def __init__(self, parent, selector, label=None):
        """
        :param selector: a slice or numpy mask array.\
            The mask array should either be a boolean array (ideally) of the\
            same size as the parent,\
            or an integer array containing cell indices,\
            i.e. if `p.size == 5` then:

            ::

                PopulationView(p, array([False, False, True, False, True]))
                PopulationView(p, array([2, 4]))
                PopulationView(p, slice(2, 5, 2))

            will all create the same view.
        """
        self.__parent = parent
        sized = AbstractSized(parent.size)
        ids = sized.selector_to_ids(selector, warn=True)

        if isinstance(parent, PopulationView):
            self.__population = parent.grandparent
            self.__indexes = parent.index_in_grandparent(ids)
        else:
            self.__population = parent
            self.__indexes = ids
        self.__mask = selector
        self.__label = label
        self.__annotations = dict()

    @property
    def size(self):
        """ The total number of neurons in the Population.
        """
        return len(self.__indexes)

    @property
    def label(self):
        """ A label for the Population.
        """
        return self.__label

    @property
    def celltype(self):
        """ The type of neurons making up the Population.
        """
        return self.__population.celltype

    @property
    def initial_values(self):
        """ A dict containing the initial values of the state variables.
        """
        return self.__population.get_initial_values(selector=self.__indexes)

    @property
    def parent(self):
        """ A reference to the parent Population (that this is a view of).
        """
        return self.__parent

    @property
    def mask(self):
        """  The selector mask that was used to create this view.
        """
        return self.__mask

    @property
    def all_cells(self):
        """ An array containing the cell IDs of all neurons in the\
            Population (all MPI nodes). """
        return [IDMixin(self.__population, idx) for idx in self.__indexes]

    @property
    def _indexes(self):
        return tuple(self.__indexes)

    def __getitem__(self, index):
        """ Return either a single cell (ID object) from the Population,\
            if index is an integer, or a subset of the cells\
            (PopulationView object), if index is a slice or array.

        Note that __getitem__ is called when using[] access, e.g. p =\
            Population(...) p[2] is equivalent to p.__getitem__(2).p[3:6] is\
            equivalent to p.__getitem__(slice(3, 6))
        """
        if isinstance(index, integer_types):
            return IDMixin(self.__population, index)
        return PopulationView(self, index, label=self.label+"_" + str(index))

    def __iter__(self):
        """ Iterator over cell IDs (on the local node).
        """
        for idx in self.__indexes:
            yield IDMixin(self, idx)

    def __len__(self):
        """ Return the total number of cells in the population (all nodes).
        """
        return len(self.__indexes)

    def all(self):
        """ Iterator over cell IDs (on all MPI nodes).
        """
        for idx in self.__indexes:
            yield IDMixin(self, idx)

    def can_record(self, variable):
        """ Determine whether variable can be recorded from this population.
        """
        return self.__population.can_record(variable)

    @property
    def conductance_based(self):
        """ Indicates whether the post-synaptic response is modelled as a\
            change in conductance or a change in current.
        """
        return self.__population.conductance_based

    def describe(self, template='populationview_default.txt',
                 engine='default'):
        """ Returns a human-readable description of the population view.

        The output may be customized by specifying a different template\
        together with an associated template engine (see pyNN.descriptions).

        If template is None, then a dictionary containing the template\
        context will be returned.
        """
        context = {"label": self.label,
                   "parent": self.parent.label,
                   "mask": self.mask,
                   "size": self.size}
        context.update(self.__annotations)
        return descriptions.render(engine, template, context)

    def find_units(self, variable):
        """
        .. warning::
            NO PyNN description of this method.
        """
        return self.__population.find_units(variable)

    def get(self, parameter_names, gather=False, simplify=True):
        """ Get the values of the given parameters for every local cell in\
            the population, or, if gather=True,\
            for all cells in the population.

        Values will be expressed in the standard PyNN units (i.e. millivolts,\
        nanoamps, milliseconds, microsiemens, nanofarads, event per second).
        """
        if simplify is not True:
            logger.warning("The simplify value is ignored if not set to true")

        return self.__population.get_by_selector(
            self.__indexes, parameter_names)

    def get_data(self, variables='all', gather=True, clear=False):
        """ Return a Neo Block containing the data(spikes, state variables)\
            recorded from the Population.

        :param variables: Either a single variable name or a list of variable\
            names. Variables must have been previously recorded, otherwise an\
            Exception will be raised.
        :param gather: For parallel simulators, if gather is True, all data\
            will be gathered to all nodes and the Neo Block will contain data\
            from all nodes. \
            Otherwise, the Neo Block will contain only data from the cells\
            simulated on the local node.

            .. note::
                SpiNNaker always gathers.

        :param clear: If True, recorded data will be deleted from the\
            Population.
        """
        if not gather:
            logger.warning("SpiNNaker only supports gather=True. We will run "
                           "as if gather was set to True.")
        return self.__population.get_data_by_indexes(
            variables, self.__indexes, clear=clear)

    def get_spike_counts(self, gather=True):
        """ Returns a dict containing the number of spikes for each neuron.

        The dict keys are neuron IDs, not indices.
        """
        logger.info("get_spike_counts is inefficient as it just counts the "
                    "results of get_datas('spikes')")
        neo = self.get_data("spikes")
        spiketrains = neo.segments[len(neo.segments) - 1].spiketrains
        return {
            idx: len(spiketrains[i])
            for i, idx in enumerate(self.__indexes)}

    @property
    def grandparent(self):
        """ Returns the parent Population at the root of the tree (since the\
            immediate parent may itself be a PopulationView).

        The name "grandparent" is of course a little misleading, as it could\
        be just the parent, or the great, great, great, ..., grandparent.
        """
        return self.__population

    def id_to_index(self, id):  # @ReservedAssignment
        """ Given the ID(s) of cell(s) in the PopulationView, return its /\
            their index / indices(order in the PopulationView).

        assert pv.id_to_index(pv[3]) == 3
        """
        if isinstance(id, integer_types):
            return self.__indexes.index(id)
        return [self.__indexes.index(idx) for idx in id]

    def index_in_grandparent(self, indices):
        """ Given an array of indices, return the indices in the parent\
            population at the root of the tree.
        """
        return [self.__indexes[index] for index in indices]

    def initialize(self, **initial_values):
        """ Set initial values of state variables, e.g. the membrane\
        potential.  Values passed to initialize() may be:

        * single numeric values (all neurons set to the same value), or
        * RandomDistribution objects, or
        * lists / arrays of numbers of the same size as the population\
          mapping functions, where a mapping function accepts a single\
          argument(the cell index) and returns a single number.

        Values should be expressed in the standard PyNN units(\
        i.e. millivolts, nanoamps, milliseconds, microsiemens, nanofarads,\
        event per second).

        Examples::

            p.initialize(v=-70.0)
            p.initialize(v=rand_distr, gsyn_exc=0.0)
            p.initialize(v=lambda i: -65 + i / 10.0)
        """
        for variable, value in initial_values.items():
            self.__population.set_initial_value(
                variable, value, self.__indexes)

    def record(self, variables, to_file=None, sampling_interval=None):
        """ Record the specified variable or variables for all cells in the\
            Population or view.

        :param varables: either a single variable name or a list of variable\
            names. For a given celltype class, celltype.recordable contains a\
            list of variables that can be recorded for that celltype.
        :param to_file: \
            If specified, should be a Neo IO instance and write_data()\
            will be automatically called when end() is called.
        :param sampling_interval: \
            should be a value in milliseconds, and an integer\
            multiple of the simulation timestep.
        """
        self.__population._record_with_indexes(
            variables, to_file, sampling_interval, self.__indexes)

    def sample(self, n, rng=None):
        """ Randomly sample `n` cells from the Population, and return a\
            PopulationView object.
        """
        if not rng:
            rng = NumpyRNG()
        indices = rng.permutation(
            numpy.arange(len(self), dtype=numpy.int))[0:n]
        return PopulationView(
            self, indices,
            label="Random sample size {} from {}".format(n, self.label))

    def set(self, **parameters):
        """ Set one or more parameters for every cell in the population.\
            Values passed to `set()` may be:

        * single values,
        * RandomDistribution objects, or
        * lists / arrays of values of the same size as the population\
          mapping functions, where a mapping function accepts a single\
          argument (the cell index) and returns a single value.

        Here, a "single value" may be either a single number or a list /\
        array of numbers (e.g. for spike times).

        Values should be expressed in the standard PyNN units\
            (i.e. millivolts, nanoamps, milliseconds, microsiemens,\
            nanofarads, event per second).

        Examples::

            p.set(tau_m=20.0, v_rest=-65).
            p.set(spike_times=[0.3, 0.7, 0.9, 1.4])
            p.set(cm=rand_distr, tau_m=lambda i: 10 + i / 10.0)
        """
        for (parameter, value) in parameters.items():
            self.__population.set_by_selector(
                selector=self.__indexes, parameter=parameter, value=value)

    def write_data(self, io, variables='all', gather=True, clear=False,
                   annotations=None):
        """ Write recorded data to file, using one of the file formats\
            supported by Neo.

        :param io: a Neo IO instance
        :param variables: either a single variable name or a list of variable\
            names. These must have been previously recorded, otherwise an\
            Exception will be raised.
        :param gather: For parallel simulators, if this is True, all data will\
            be gathered to the master node and a single output file created\
            there. Otherwise, a file will be written on each node,\
            containing only data from the cells simulated on that node.
        :param clear: If this is True, recorded data will be deleted from the\
            Population.
        :param annotations: should be a dict containing simple data types such\
            as numbers and strings. The contents will be written into the\
            output data file as metadata.
        """
