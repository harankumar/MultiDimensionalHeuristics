# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from Queue import PriorityQueue
from scipy.spatial.distance import *
from grid import Grid


def find_path(grid, start_cell, goal_cell, heuristic):
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
                         p=dimensions / 2)
        else:
            return pdist([p1, p2], name)

    print "started pathfinding"

    start_frontier = PriorityQueue()
    start_cell.cost_to = start_cell.cost
    start_frontier.put(start_cell)

    goal_frontier = PriorityQueue()
    goal_cell.cost_from = goal_cell.cost
    goal_frontier.put(goal_cell)
    num_iterations = 0

    while not start_frontier.empty() and not goal_frontier.empty():
        num_iterations += 1
        current_start_cell = start_frontier.get()
        current_goal_cell = goal_frontier.get()
        print(str(current_start_cell) + " " + str(current_goal_cell))

        if current_start_cell == current_goal_cell:
            path = []
            while current_start_cell.previous is not None:
                path.append(current_start_cell)
                current_start_cell = current_start_cell.previous
            path.append(current_start_cell)
            path.reverse()
            path.append(current_goal_cell)
            while current_goal_cell.successor is not None:
                path.append(current_goal_cell)
                current_goal_cell = current_goal_cell.successor
            return path, num_iterations

        if current_start_cell.visited_from_goal:
            print "1"
            path = []
            current = current_start_cell
            while not current == goal_cell:
                current.successor.previous = current
                current = current.successor
            current = goal_cell
            while current.previous is not None:
                path.append(current)
                current = current.previous
            path.append(current)
            path.reverse()
            return path, num_iterations

        if current_goal_cell.visited_from_start:
            print "2"
            path = []
            current = current_goal_cell
            while current.previous is not None:
                path.append(current)
                current = current.previous
            path.append(current)
            path.reverse()
            current = current_goal_cell
            while not current == goal_cell:
                path.append(current.successor)
                current = current.successor
            return path, num_iterations

        current_start_cell.closed = True

        # add to start frontier
        neighbors = current_start_cell.get_neighbors()

        for neighbor in neighbors:
            if neighbor.closed:
                continue

            cost_to = current_start_cell.cost_to + neighbor.cost
            visited = neighbor.visited_from_start
            if (not visited) or cost_to < neighbor.cost_to:
                neighbor.visited_from_start = True
                neighbor.previous = current_start_cell
                if neighbor.predicted_cost_from == 100000000.0:
                    neighbor.predicted_cost_from = distance(neighbor, goal_cell)
                neighbor.cost_to = cost_to
                neighbor.predicted_cost_to = cost_to
                neighbor.total_cost = neighbor.cost_to + neighbor.predicted_cost_from

                if visited:
                    start_frontier.queue.remove(neighbor)
                start_frontier.put(neighbor)

        # add to goal frontier
        neighbors = current_goal_cell.get_neighbors()

        for neighbor in neighbors:
            if neighbor.closed:
                continue

            cost_from = current_goal_cell.cost_from + neighbor.cost
            visited = neighbor.visited_from_goal
            if (not visited) or cost_from < neighbor.cost_from:
                neighbor.visited_from_goal = True
                neighbor.successor = current_goal_cell
                if neighbor.predicted_cost_to == 100000000.0:
                    neighbor.predicted_cost_to = distance(neighbor, start_cell)
                neighbor.cost_from = cost_from
                neighbor.predicted_cost_from = cost_from
                neighbor.total_cost = neighbor.cost_from + neighbor.predicted_cost_to

                if visited:
                    goal_frontier.queue.remove(neighbor)
                goal_frontier.put(neighbor)


# np.set_printoptions(linewidth=500)
# g = Grid([5, 5], fill=True)
# print g.grid
# print g.get_cell([0,0])
# print g.get_cell([4,4])
# path, iter = find_path(g, g.get_cell([0, 0]), g.get_cell([4, 4]), heuristic='null')
# print [str(i) for i in path]
# print iter
