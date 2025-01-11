# Tiels for the Grid
class Tile:
    def __init__(self, name: str) -> None:
        self.name = name


class BlankTile(Tile):
    def __init__(self, name="Blank") -> None:
        super().__init__(name)


class FoodTile(Tile):
    def __init__(self, name="Food", regrowth_time=10) -> None:
        super().__init__(name)
        self.regrowth_time = regrowth_time
