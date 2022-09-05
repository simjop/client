import wx


def normalize(x, minv, maxv, step):
    x = max(x, minv)
    x = min(x, maxv - step)
    return x


class Painter:
    def __init__(self, canvas, zoom):
        self._tile_w = 4 * zoom
        self._tile_h = 6 * zoom
        self._canvas = canvas
        self._canvas_w, self._canvas_h = self._canvas.GetSize()
        self._offset_w = int((self._canvas_w % self._tile_w) / 2)
        self._offset_h = int((self._canvas_h % self._tile_h) / 2)
        self._tile_count_w = int(self._canvas_w / self._tile_w)
        self._tile_count_h = int(self._canvas_h / self._tile_h)
        self._cursor = None

    def _draw_black_background(self):
        self._canvas.SetBrush(wx.Brush("BLACK"))
        self._canvas.SetPen(wx.Pen("BLACK"))
        self._canvas.DrawRectangle(0, 0, self._canvas_w, self._canvas_h)

    def _draw_grid(self):

        self._canvas.SetPen(wx.Pen("LIGHT GREY"))

        self._canvas.DrawLine(
            self._offset_w,
            self._offset_h,
            self._canvas_w - 2 * self._offset_w,
            self._offset_h,
        )
        self._canvas.DrawLine(
            self._offset_w,
            self._offset_h,
            self._offset_w,
            self._canvas_h - 2 * self._offset_h,
        )

        for i in range(self._tile_count_w):
            stressed_w = self._offset_w + i * self._tile_w
            self._canvas.DrawLine(
                stressed_w, self._offset_h + 1, stressed_w, self._offset_h + 2
            )
            if (i % 5) == 0:
                self._canvas.DrawLine(
                    stressed_w,
                    self._offset_h + 1,
                    stressed_w,
                    self._offset_h + int(self._tile_h / 2),
                )
            if (i % 10) == 0:
                self._canvas.DrawLine(
                    stressed_w,
                    self._offset_h + 1,
                    stressed_w,
                    self._offset_h + self._tile_h - 1,
                )

        for i in range(self._tile_count_h):
            stressed_h = self._offset_h + i * self._tile_h
            self._canvas.DrawLine(
                self._offset_w + 1, stressed_h, self._offset_w + 2, stressed_h
            )
            if (i % 5) == 0:
                self._canvas.DrawLine(
                    self._offset_w + 1,
                    stressed_h,
                    self._offset_w + int(self._tile_w / 2),
                    stressed_h,
                )
            if (i % 10) == 0:
                self._canvas.DrawLine(
                    self._offset_w + 1,
                    stressed_h,
                    self._offset_w + self._tile_w - 1,
                    stressed_h,
                )

    def _draw_cursor(self):

        if self._cursor is None:
            return

        cx = normalize(
            self._cursor[0],
            self._offset_w,
            self._canvas_w - self._offset_w,
            self._tile_w,
        )
        cy = normalize(
            self._cursor[1],
            self._offset_h,
            self._canvas_h - self._offset_h,
            self._tile_h,
        )

        x = self._offset_w + cx - int(cx % self._tile_w)
        y = self._offset_h + cy - int(cy % self._tile_h)
        self._canvas.SetPen(wx.Pen("RED"))
        self._canvas.DrawRectangle(x, y, self._tile_w, self._tile_h)

        self._canvas.DrawLine(x, self._offset_h, x, self._tile_h)
        self._canvas.DrawLine(self._offset_w, y, self._tile_w, y)

    @property
    def tile(self):
        if self._cursor is None:
            return None

        cx = normalize(
            self._cursor[0],
            self._offset_w,
            self._canvas_w - self._offset_w,
            self._tile_w,
        )
        cy = normalize(
            self._cursor[1],
            self._offset_h,
            self._canvas_h - self._offset_h,
            self._tile_h,
        )

        return int(cx / self._tile_w), int(cy / self._tile_h)

    def draw(self, cursor_position=None):

        self._cursor = cursor_position

        self._draw_black_background()
        self._draw_grid()
        self._draw_cursor()
