# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Module containing Basic Qiskit Metal Planar (2D) design for CPW type geometry.

@date: 2019

@author: Zlatko Minev, Thomas McConeky, ... (IBM)
"""

from .design_base import QDesign
from typing import TYPE_CHECKING
from typing import Dict as Dict_
from typing import List, Tuple, Union

__all__ = ['DesignPlanar']


class DesignPlanar(QDesign):
    """Metal class for a planar (2D) design, consisting of a single plane chip.
    Typically assumed to have some CPW geometires.

    Inherits QDesign class.
    """

    def __init__(self, metadata: dict = None, overwrite_enabled: bool = False, enable_renderers: bool = True):
        """Pass metadata to QDesign.

        Args:
            metadata (dict, optional): Pass to QDesign. Defaults to {}.
        """
        super().__init__(metadata=metadata, overwrite_enabled=overwrite_enabled,
                         enable_renderers=enable_renderers)
        self.add_chip_info()

    def add_chip_info(self):
        """TODO How to get the values into self.chip. Will need to set up parser for "self.p" for design base.
        For now, just hard code in something.

        # GDSPY is using numbers based on 1 meter unit.
        # When the gds file is exported, data is converted to "user-selected" units.
        # centered at (0,0) and 5 mm by 5 mm size.
        """
        self._chips['main'] = {}

        self._chips['main']['size'] = {
            'center_x': 0.0, 'center_y': 0.0, 'size_x': 0.005, 'size_y': 0.005}

    def get_x_y_for_chip(self, chip_name: str) -> Tuple[tuple, int]:
        """If the chip_name is in self.chips, along with entry for size information
        then return a tuple=(minx, miny, maxx, maxy). Used for subtraction while exporting design.

        Args:
            chip_name (str): Name of chip that you want the size of.

        Returns:
            Tuple[tuple, int]:
            tuple: The exact placement on rectangle coordinate (minx, miny, maxx, maxy).
            int: 0=all is good, 1=chip_name not in self._chips, 2=size information missing or no good
        """
        x_y_location = tuple()

        if chip_name in self._chips:
            if 'size' in self._chips[chip_name]:
                size = self.chips[chip_name]['size']
                if 'center_x' in size and 'center_y' in size and 'size_x' in size and 'size_y' in size:
                    if (isinstance(size.center_x, int) or isinstance(size.center_x, float)) and \
                       (isinstance(size.center_y, int) or isinstance(size.center_y, float)) and \
                       (isinstance(size.size_x, int) or isinstance(size.size_x, float)) and \
                       (isinstance(size.size_y, int) or isinstance(size.size_y, float)):
                        x_y_location = (
                            size.center_x - (size.size_x / 2.0),
                            size.center_y - (size.size_y / 2.0),
                            size.center_x + (size.size_x / 2.0),
                            size.center_y + (size.size_y / 2.0)
                        )
                        return x_y_location, 0
                    else:
                        self.logger.warning(
                            f'Size information within self.chips[{chip_name}]["size"] is NOT an int or float.')
                        return x_y_location, 2
                else:
                    self.logger.warning(
                        f'center_x or center_y or size_x or size_y NOT in self._chips[{chip_name}]["size"]')
                    return x_y_location, 2
            else:
                self.logger.warning(
                    f'Information for size in NOT in self._chips[{chip_name}] dict. Return "None" in tuple.')
                return x_y_location, 2

        else:
            self.logger.warning(
                f'Chip name "{chip_name}" is not in self._chips dict. Return "None" in tuple.')
            return x_y_location, 1
