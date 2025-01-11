# 2D Grid class for simulations
import numpy as np
from typing import Dict, Tuple

from ecosystems.generation.tile import BlankTile, Tile


class Grid:
    def __init__(self, num_x: int, num_y: int,
                 x_start=0., x_end=100., y_start=0., y_end=100.) -> None:
        # Coordinates
        self.x = np.linspace(x_start, x_end, num=num_x)
        self.y = np.linspace(y_start, y_end, num=num_y)

        # spacing
        self.dx = self.x[1] - self.x[0]
        self.dy = self.y[1] - self.y[0]

        self.coords = np.array(np.meshgrid(
            self.x, self.y, indexing='ij')).transpose(1, 2, 0)

        # Initialize empty array of tiles
        # Note the "minus 1" because we have cell centers vs edges
        self.tile_data = {}
        for i in range(num_x - 1):
            for j in range(num_y - 1):
                self.tile_data[(i, j)] = BlankTile("Blank")

    def init_tiles(self, tiles: Dict):
        # Set up tiles: 'tiles' dictionary should be a ndarray: Tile map
        for coord, tile in tiles.items():
            self.tile_data[coord] = tile

# Maybe these could be optimized but it's good enough for now
    def nearest_coord_idxs(self, position: np.ndarray) -> np.ndarray:
        # Find the indices of the nearest coordinate to the position
        i = np.abs(self.x - position[0]).argmin()
        j = np.abs(self.y - position[1]).argmin()
        return np.array([i, j])

    def nearest_coord(self, position: np.ndarray) -> np.ndarray:
        # Find nearest coordinate to position
        return self.coords[self.nearest_coord_idxs(position)]
