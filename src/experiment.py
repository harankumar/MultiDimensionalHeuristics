# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pathfinder import *
from grid import *
from random import random, randint
import time
import matplotlib.pyplot as plt
from multiprocessing import Pool

np.set_printoptions(linewidth=500)

NUM_TRIALS = 10
MAX_DIMENSIONS = 10
MAX_SIZE = 10

HEURISTICS = [
    "canberra",
    "chebyshev",
    "cityblock",
    "cosine",
    "euclidean",
    "hamming",
    "minkowski-0.5n",
    "minkowski-n",
    "null",
    "seuclidean",
    "sqeuclidean"
]

iterations = {}
runtime = {}
error = {}
for heuristic in HEURISTICS:
    iterations[heuristic] = []
    runtime[heuristic] = []
    error[heuristic] = []

total = NUM_TRIALS * (MAX_DIMENSIONS - 1) * len(HEURISTICS)
progress = 0


def run_trial(num_dimensions):
    global total, progress, HEURISTICS, iterations, runtime, error
    # Initialize Grid
    fill = MAX_SIZE ** num_dimensions < 1000
    grid = Grid([randint(3, MAX_SIZE + 1) for i in range(num_dimensions)], fill=fill)
    num_nodes = grid.grid.size
    start = grid.random_coordinate()
    stop = grid.random_coordinate()
    while start == stop:
        stop = grid.random_coordinate()

    path_length = {}
    optimal_path_cost = 1000000000000000000000000000000000
    # run each heuristic, count cells expanded, and physical time it took
    for heuristic in HEURISTICS:
        print "progress: " + str(progress) + "/" + str(total)
        progress += 1
        start_time = time.clock()
        path, num_iterations = find_path(grid, start, stop, heuristic)
        elapsed_time = time.clock() - start_time

        # runtime
        runtime[heuristic].append([])
        runtime[heuristic][-1].append(elapsed_time)

        # optimal path
        error[heuristic].append([])
        path_length[heuristic] = sum([cell.total_cost for cell in path])
        if path_length[heuristic] < optimal_path_cost:
            optimal_path_cost = path_length[heuristic]

        # cells expanded
        iterations[heuristic].append([])
        iterations[heuristic][-1].append(num_iterations)

        grid.reset()

    for heuristic in HEURISTICS:
        error[heuristic][-1].append(100.0 * (path_length[heuristic] / optimal_path_cost) - 100)

if __name__ == "__main__":
    try:
        for dimensions in range(2, MAX_DIMENSIONS + 1):
            for trial in range(0, NUM_TRIALS):
                run_trial(dimensions)

    except MemoryError as me:
        print me

    for heuristic in HEURISTICS:
        for i, trial in enumerate(iterations[heuristic]):
            iterations[heuristic][i] = float(sum(iterations[heuristic][i]) / NUM_TRIALS)
        for i, trial in enumerate(error[heuristic]):
            error[heuristic][i] = float(sum(error[heuristic][i]) / NUM_TRIALS)
        for i, trial in enumerate(runtime[heuristic]):
            runtime[heuristic][i] = float(sum(runtime[heuristic][i]) / NUM_TRIALS)
        print heuristic, error[heuristic], iterations[heuristic], runtime[heuristic]

    plt.rc('lines', linestyle='-')
    plt.rc('font', family='serif', serif='Helvetica Neue')
    plt.rc('figure.subplot', right=0.8)

    fig, axarr = plt.subplots(3, sharex=True)
    dims = np.arange(2, MAX_DIMENSIONS + 1, 1)
    for heuristic in HEURISTICS:
        for i, data in [[0, iterations], [1, error], [2, runtime]]:
            axarr[i].plot(dims, data[heuristic], label=heuristic)

    axarr[0].set_title("Efficiency")
    axarr[1].set_title("Optimality")
    axarr[2].set_title("Runtime")
    fig.text(0.35, 0.04, 'Number of Dimensions')
    fig.text(0.04, 0.77, 'Iterations Used', ha='center', va='center', rotation='vertical')
    fig.text(0.04, 0.50, '% Cost Error', ha='center', va='center', rotation='vertical')
    fig.text(0.04, 0.22, 'Seconds', ha='center', va='center', rotation='vertical')
    axarr[1].legend(bbox_to_anchor=(1.05, 0.55), loc=2, borderaxespad=0.)

    plt.show()
