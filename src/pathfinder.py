# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from Queue import PriorityQueue
from scipy.spatial.distance import *
from grid import Grid


def find_path(grid, start_cell, stop_cell, heuristic):
    def distance(p1, p2, name=heuristic, dimensions=grid.num_dimensions):
        p1 = p1.coordinates
        p2 = p2.coordinates
        if name == 'null':
            return 0.0
        elif name == 'minkowski-n':
            return pdist([p1, p2],
                         'minkowski',
                         p=dimensions)
        elif name == 'minkowski-0.5n':
            return pdist([p1, p2],
                         'minkowski',
                         p=dimensions/2)
        else:
            return pdist([p1, p2], name)

    open_cells = PriorityQueue()
    start_cell.known_cost = start_cell.cost
    open_cells.put(start_cell)

    num_iterations = 0

    while not open_cells.empty():
        current_cell = open_cells.get()
        num_iterations += 1

        if current_cell == stop_cell:
            path = []
            while current_cell.previous is not None:
                path.append(current_cell)
                current_cell = current_cell.previous
            path.append(current_cell)
            path.reverse()
            return path, num_iterations

        current_cell.closed = True

        neighbors = current_cell.get_neighbors()

        for neighbor in neighbors:
            if neighbor.closed:
                continue

            known_cost = current_cell.known_cost + neighbor.cost
            visited = neighbor.visited
            if (not visited) or known_cost < neighbor.known_cost:
                neighbor.visited = True
                neighbor.previous = current_cell
                if neighbor.predicted_cost == 100000000.0:
                    neighbor.predicted_cost = distance(neighbor, stop_cell)
                neighbor.known_cost = known_cost
                neighbor.total_cost = neighbor.known_cost + neighbor.predicted_cost

                if visited:
                    open_cells.queue.remove(neighbor)
                open_cells.put(neighbor)
