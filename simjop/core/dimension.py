class Dimension:
    def __init__(self, canvas, zoom):
        self._width, self._height = canvas.GetSize()
        self._tile_w = 4 * zoom
        self._tile_h = 6 * zoom
        self._offset_w = int((self._width % self._tile_w) / 2)
        self._offset_h = int((self._height % self._tile_h) / 2)
        self._tile_count_w = int(self._width / self._tile_w)
        self._tile_count_h = int(self._height / self._tile_h)

    @property
    def size(self):
        return self._width, self._height

    @property
    def tiles(self):
        return self._tile_count_w, self._tile_count_h

    @property
    def tile_size(self):
        return self._tile_w, self._tile_h

    @property
    def offset(self):
        return self._offset_w, self._offset_h

    def xy_to_tile(self, position):
        if position is None:
            return None
        normalized_x = max(position[0], self._offset_w)
        normalized_x = min(position[0], self._width - self._offset_w - self._tile_w)
        normalized_y = max(position[1], self._offset_h)
        normalized_y = min(position[1], self._height - self._offset_h - self._tile_h)
        return int(normalized_x / self._tile_w), int(normalized_y / self._tile_h)

    def tile_to_xy(self, tile):
        return (
            tile[0] * self._tile_w + self._offset_w,
            tile[1] * self._tile_h + self._offset_h,
        )
