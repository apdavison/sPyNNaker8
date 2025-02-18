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

from .all_to_all_connector import AllToAllConnector
from .array_connector import ArrayConnector
from .csa_connector import CSAConnector
from .distance_dependent_probability_connector import (
    DistanceDependentProbabilityConnector)
from .fixed_number_post_connector import FixedNumberPostConnector
from .fixed_number_pre_connector import FixedNumberPreConnector
from .fixed_probability_connector import FixedProbabilityConnector
from .from_file_connector import FromFileConnector
from .from_list_connector import FromListConnector
from .index_based_probability_connector import IndexBasedProbabilityConnector
from .multapse_connector import MultapseConnector as FixedTotalNumberConnector
from .one_to_one_connector import OneToOneConnector
from .small_world_connector import SmallWorldConnector
from .kernel_connector import KernelConnector

__all__ = ["AllToAllConnector", "ArrayConnector", "CSAConnector",
           "DistanceDependentProbabilityConnector", "FixedNumberPostConnector",
           "FixedNumberPreConnector", "FixedProbabilityConnector",
           "FromFileConnector", "FromListConnector",
           "IndexBasedProbabilityConnector", "FixedTotalNumberConnector",
           "OneToOneConnector", "SmallWorldConnector", "KernelConnector"]
