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

from spinn_front_end_common.utilities.exceptions import ConfigurationException


class Spynnaker8Exception(Exception):
    """ Superclass of all exceptions from the pynn module
    """


class MemReadException(Spynnaker8Exception):
    """ Raised when the pynn front end fails to read a certain memory region
    """
    pass


class FilterableException(Spynnaker8Exception):
    """ Raised when it is not possible to determine if an edge should be\
        filtered
    """
    pass


class SynapticConfigurationException(ConfigurationException):
    """ Raised when the synaptic manager fails for some reason
    """
    pass


class SynapticBlockGenerationException(ConfigurationException):
    """ Raised when the synaptic manager fails to generate a synaptic block
    """
    pass


class SynapticBlockReadException(ConfigurationException):
    """ Raised when the synaptic manager fails to read a synaptic block or\
        convert it into readable values
    """
    pass


class SynapticMaxIncomingAtomsSupportException(ConfigurationException):
    """ Raised when a synaptic sublist exceeds the max atoms possible to be\
        supported
    """
    pass


class DelayExtensionException(ConfigurationException):
    """ Raised when a delay extension vertex fails
    """
    pass


class InvalidParameterType(Spynnaker8Exception):
    """ Raised when a parameter is not recognised
    """
    pass
