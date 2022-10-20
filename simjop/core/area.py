from enum import Enum, auto

from core.symbol_constants import SymbolType


class Area:
    def __init__(self):
        self._area = {"lines": []}

    @property
    def tiles(self):
        tiles = []

        for line in self._area["lines"]:
            a_x = line[0][0]
            a_y = line[0][1]
            b_x = line[1][0]
            b_y = line[1][1]

            if a_x == b_x and a_y == b_y:  # orientation .
                tiles.append({"tile": line[0], "type": SymbolType.LINE_1})
            elif a_x == b_x and a_y < b_y:  # orientation |
                for i in range(b_y - a_y + 1):
                    tiles.append({"tile": (a_x, a_y + i), "type": SymbolType.LINE_3})
            elif a_x == b_x and a_y > b_y:  # orientation |
                for i in range(a_y - b_y + 1):
                    tiles.append({"tile": (a_x, a_y - i), "type": SymbolType.LINE_3})
            elif a_y == b_y:  # orientation -
                for i in range(b_x - a_x + 1):
                    tiles.append({"tile": (a_x + i, a_y), "type": SymbolType.LINE_1})
            elif a_x < b_x and a_y > b_y:  # orientation /
                step_x = b_x - a_x
                step_y = a_y - b_y
                for i in range(step_x + step_y + 1):
                    if i % 2:
                        tiles.append(
                            {
                                "tile": (a_x + int(i / 2), a_y - int(i / 2) - 1),
                                "type": SymbolType.LINE_2a,
                            }
                        )
                    else:
                        tiles.append(
                            {
                                "tile": (a_x + int(i / 2), a_y - int(i / 2)),
                                "type": SymbolType.LINE_2b,
                            }
                        )
            elif a_x < b_x and a_y < b_y:  # orientation \
                step_x = b_x - a_x
                step_y = b_y - a_y
                for i in range(step_x + step_y + 1):
                    if i % 2:
                        tiles.append(
                            {
                                "tile": (a_x + int(i / 2), a_y + int(i / 2) + 1),
                                "type": SymbolType.LINE_4a,
                            }
                        )
                    else:
                        tiles.append(
                            {
                                "tile": (a_x + int(i / 2), a_y + int(i / 2)),
                                "type": SymbolType.LINE_4b,
                            }
                        )

            else:
                print("Unknow coordinates")  # TODO

        return tiles

    def add_line(self, begin_tile, end_tile):
        if begin_tile[0] <= end_tile[0]:
            self._area["lines"].append([begin_tile, end_tile])
        else:
            self._area["lines"].append([end_tile, begin_tile])
        print(self._area)
