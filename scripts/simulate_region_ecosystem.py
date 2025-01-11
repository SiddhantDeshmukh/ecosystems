# Simple single-region ecosystem
from ecosystems.generation.grid import Grid
from ecosystems.generation.tile import FoodTile
from ecosystems.viz.grid_tile import plot_grid

import matplotlib.pyplot as plt
import numpy as np
import random

SEED = 420
np.random.seed(SEED)


def main():
    grid = Grid(10, 20, y_end=200)
    # Randomize food tiles
    tiles = {}
    for i in range(len(grid.x)):
        for j in range(len(grid.y)):
            if random.random() <= 0.1:
                tiles[(i, j)] = FoodTile("Food", np.random.randint(5, 15))

    grid.init_tiles(tiles)

    # Init creatures

    # Add simple AI

    # Monitor populations

    fig, ax = plot_grid(grid)

    plt.show()


if __name__ == "__main__":
    main()
