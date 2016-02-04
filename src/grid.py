# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import numpy as np
from random import randint, random


class Grid:
    def __init__(self, dimensions, fill):
        self.dimensions = dimensions
        self.num_dimensions = len(dimensions)
        self.grid = np.ndarray(dimensions, dtype=object)
        self.shape = self.grid.shape
        self.filled = fill
        if fill:
            self.fill()

    def get_cell(self, coordinates):
        coordinates = tuple(coordinates)
        if not self.filled and not isinstance(self.grid[coordinates], Cell):
            self.grid[coordinates] = Cell(self, coordinates)
        return self.grid[tuple(coordinates)]

    def fill(self):
        iterator = np.nditer(self.grid,
                             flags=['refs_ok', 'multi_index'],
                             op_flags=['readwrite'])
        for cell in iterator:
            cell[...] = Cell(self, iterator.multi_index)

    def random_coordinate(self):
        return self.get_cell([randint(0, x - 1) for x in self.dimensions])

    def reset(self):
        # print "resetting"
        iterator = np.nditer(self.grid,
                             flags=['refs_ok', 'multi_index'],
                             op_flags=['readwrite'])
        for cell in iterator:
            # new_cell = Cell(self, iterator.multi_index)
            if not self.filled and (cell is None or str(cell) == "None"):
                pass
            else:
                self.grid[tuple(iterator.multi_index)].reset()
            #     new_cell.cost = float(str(cell))
            # cell[...] = new_cell
            # print cell
            # print cell[...]
            # print cell[...].coordinates


class Cell:
    def __init__(self, grid, coordinates):
        self.grid = grid
        self.coordinates = coordinates

        self.cost = 2 * random()
        self.visited_from_start = False
        self.visited_from_goal = False
        self.closed = False

        self.previous = None
        self.successor = None

        self.cost_to = 100000000.0
        self.cost_from = 100000000.0
        self.predicted_cost_from = 100000000.0
        self.predicted_cost_to = 100000000.0
        self.total_cost = 200000000.0

    def __str__(self):
        return str(self.cost)

    def __eq__(self, other):
        return self.coordinates == other.coordinates

    def __lt__(self, other):
        return self.total_cost < other.total_cost

    def get_neighbors(self):
        dims = self.grid.num_dimensions

        offsets = np.take(np.r_[-1, 0, 1], np.indices((3,) * dims).reshape(dims, -1).T)
        offsets = offsets[np.any(offsets, 1)]

        neighbours = self.coordinates + offsets
        valid = np.all((neighbours < np.array(self.grid.shape)) & (neighbours >= 0), axis=1)
        neighbours = neighbours[valid]

        return [self.grid.get_cell(coordinates) for coordinates in neighbours]

    def reset(self):
        self.visited_from_start = False
        self.visited_from_goal = False
        self.closed = False

        self.previous = None
        self.successor = None

        self.cost_to = 100000000.0
        self.cost_from = 100000000.0
        self.predicted_cost_from = 100000000.0
        self.predicted_cost_to = 100000000.0
        self.total_cost = 200000000.0