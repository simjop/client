import wx


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


class Painter:
    def __init__(self, canvas, zoom):
        self._canvas = canvas
        self._dim = Dimension(self._canvas, zoom)
        self._cursor = None

    def _draw_black_background(self):
        self._canvas.SetBrush(wx.Brush("BLACK"))
        self._canvas.SetPen(wx.Pen("BLACK"))
        self._canvas.DrawRectangle(0, 0, self._dim.size[0], self._dim.size[1])

    def _draw_grid(self):
        size = self._dim.size
        offset = self._dim.offset
        tiles = self._dim.tiles
        tile_size = self._dim.tile_size

        self._canvas.SetPen(wx.Pen("LIGHT GREY"))
        self._canvas.DrawLine(offset[0], offset[1], size[0] - 2 * offset[0], offset[1])
        self._canvas.DrawLine(offset[0], offset[1], offset[0], size[1] - 2 * offset[1])

        for i in range(tiles[0]):
            stressed_w = offset[0] + i * tile_size[0]
            self._canvas.DrawLine(stressed_w, offset[1] + 1, stressed_w, offset[1] + 2)
            if (i % 5) == 0:
                self._canvas.DrawLine(
                    stressed_w,
                    offset[1] + 1,
                    stressed_w,
                    offset[1] + int(tile_size[1] / 2),
                )
            if (i % 10) == 0:
                self._canvas.DrawLine(
                    stressed_w,
                    offset[1] + 1,
                    stressed_w,
                    offset[1] + tile_size[1] - 1,
                )

        for i in range(tiles[1]):
            stressed_h = offset[1] + i * tile_size[1]
            self._canvas.DrawLine(offset[0] + 1, stressed_h, offset[0] + 2, stressed_h)
            if (i % 5) == 0:
                self._canvas.DrawLine(
                    offset[0] + 1,
                    stressed_h,
                    offset[0] + int(tile_size[0] / 2),
                    stressed_h,
                )
            if (i % 10) == 0:
                self._canvas.DrawLine(
                    offset[0] + 1,
                    stressed_h,
                    offset[0] + tile_size[0] - 1,
                    stressed_h,
                )

    def _draw_cursor(self):
        offset = self._dim.offset
        tile_size = self._dim.tile_size

        if self._cursor is None:
            return

        x, y = self._dim.tile_to_xy(self._cursor)
        self._canvas.SetPen(wx.Pen("RED"))
        self._canvas.DrawRectangle(x, y, tile_size[0], tile_size[1])

        self._canvas.DrawLine(x, offset[1], x, tile_size[1])
        self._canvas.DrawLine(offset[0], y, tile_size[0], y)

    @property
    def tile(self):
        return self._cursor

    def draw(self, cursor_position=None):

        self._cursor = self._dim.xy_to_tile(cursor_position)

        self._draw_black_background()
        self._draw_grid()
        self._draw_cursor()
