import wx


class Painter:
    def __init__(self, canvas, dimension, cursor_tile=None):
        self._canvas = canvas
        self._dim = dimension
        self._cursor = cursor_tile

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

    def draw(self):
        self._draw_black_background()
        self._draw_grid()
        self._draw_cursor()
