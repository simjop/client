class LineHelper:
    def __init__(self, area, begin_tile):
        self._area = area
        self._begin_tile = begin_tile

    def clue(self, end_tile):
        match = False
        for tile in self._area.tiles:
            if self._begin_tile == tile:
                match = True

    def finish(self, end_tile):
        self._area.add_line(self._begin_tile, end_tile)
