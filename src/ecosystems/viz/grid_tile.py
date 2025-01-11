# Viz tools for grid & tiles
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import numpy as np

from ecosystems.generation.grid import Grid
from ecosystems.generation.tile import BlankTile, FoodTile


def plot_grid(grid: Grid, tile_colors={
    FoodTile: "green",
    BlankTile: "white",
}):
    # This is meant to plot the grid on the background
    fig, ax = plt.subplots(1, 1)
    for i in range(len(grid.x) - 1):
        for j in range(len(grid.y) - 1):
            rectangle_data = ((grid.x[i], grid.y[j]), grid.dx, grid.dy)
            if isinstance(grid.tile_data[(i, j)], FoodTile):
                ax.add_patch(Rectangle(*rectangle_data,
                             color=tile_colors[FoodTile]))
            else:  # blank tile
                ax.add_patch(Rectangle(*rectangle_data,
                             color=tile_colors[BlankTile]))

    ax.vlines(grid.x, np.min(grid.y), np.max(grid.y), colors='k')
    ax.hlines(grid.y, np.min(grid.x), np.max(grid.x), colors='k')

    return fig, ax
