import sys
import math
from enum import Enum

ARROWS = ("<", ">", "^", "v")


def err(message) -> None:
    print(message, file=sys.stderr, flush=True)


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Tile(Position):
    def __init__(self, x: int, y: int, tile_type: str):
        super().__init__(x, y)
        self.tile_type = tile_type

    def __repr__(self):
        return "Tile {} @ ({}, {})".format(self.tile_type, self.x, self.y)

    def __eq__(self, other) -> bool:
        assert isinstance(other, Tile)
        return self.x == other.x and self.y == other.y


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = list()
        for j in range(self.height):
            self.grid.append(input())
            err(self.grid[-1])
        err("------------------")

    def get_path_length(self, start_position: Position) -> int:
        start_tile = self.get_tile(start_position)
        current_tile = start_tile
        err("Start = {}".format(current_tile))
        path_length = 1
        while current_tile.tile_type in ARROWS and (path_length == 1 or current_tile != start_tile):
            err(current_tile)
            try:
                current_tile = self.next_tile(current_tile)
            except AssertionError:
                err("Going out of bound")
                return self.height * self.width + 1

            err("next tile = {}".format(current_tile))
            path_length += 1

        if current_tile.tile_type == "T":
            return path_length
        else:
            return self.height * self.width + 1

    def get_tile(self, position: Position) -> Tile:
        return Tile(position.x, position.y, self.grid[position.x][position.y])

    def next_tile(self, tile: Tile):
        assert tile.tile_type in ARROWS
        if tile.tile_type == "^":
            assert tile.x - 1 >= 0
            return self.get_tile(Position(tile.x - 1, tile.y))
        elif tile.tile_type == "v":
            assert tile.x + 1 < self.width
            return self.get_tile(Position(tile.x + 1, tile.y))
        elif tile.tile_type == "<":
            assert tile.y - 1 >= 0
            return self.get_tile(Position(tile.x, tile.y - 1))
        else:
            assert tile.y + 1 < self.height
            return self.get_tile(Position(tile.x, tile.y + 1))


class Game:
    def __init__(self):
        self.width, self.height = [int(i) for i in input().split()]
        err(self.width)
        err(self.height)
        self.start = Position(*[int(i) for i in input().split()])
        err("START POSITION = ({}, {})".format(self.start.x, self.start.y))
        self.n_maps = int(input())
        err(self.n_maps)
        self.list_maps = list()
        for i in range(self.n_maps):
            self.list_maps.append(Grid(self.width, self.height))

    def get_best_map(self):
        best_length_path = self.width * self.height + 1
        best_map_index = -1
        for map_index, current_map in enumerate(self.list_maps):
            path_length = current_map.get_path_length(self.start)
            err("~~~~~~~~~~~~~~~~~")
            if path_length < best_length_path:
                best_length_path = path_length
                best_map_index = map_index

        if best_map_index >= 0:
            return best_map_index
        else:
            return "TRAP"


game = Game()
best_map = game.get_best_map()

print(best_map)
