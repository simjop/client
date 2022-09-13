import wx

from core.painter import Painter


class AreaEditor(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.buffer = None

        self.InitUI()
        self.Centre()

    def InitUI(self):

        self.SetSize((800, 600))
        self.SetTitle("simJOP")

        self._depth = 32

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.buffer = wx.Bitmap(300, 200, depth=self._depth)

        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        file_item = file_menu.Append(wx.ID_EXIT, "Quit", "Quit application")
        menubar.Append(file_menu, "&File")
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnQuit, file_item)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnCursorEnterWindow)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnCursorLeaveWindow)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)

        statusbar = wx.StatusBar(self)
        statusbar.SetStatusText("Připraveno")
        self.SetStatusBar(statusbar)

        icon = wx.Icon(
            wx.Bitmap("simjop/icons/logo_with_alpha.png", wx.BITMAP_TYPE_ANY)
        )
        self.SetIcon(icon)

    def OnCursorEnterWindow(self, e):
        blank_cursor = wx.Cursor(wx.CURSOR_BLANK)
        self.SetCursor(blank_cursor)

    def OnCursorLeaveWindow(self, e):
        default_cursor = wx.Cursor(wx.CURSOR_DEFAULT)
        self.SetCursor(default_cursor)

    def OnMouseMotion(self, e):

        dc = wx.ClientDC(self)
        dc_w, dc_h = dc.GetSize()

        if self.buffer is None:
            self.buffer = wx.Bitmap(dc_w, dc_h, depth=self._depth)

        bw, bh = self.buffer.GetSize()
        if dc_w != bw or dc_h != bh:
            self.buffer = wx.Bitmap(dc_w, dc_h, depth=self._depth)

        buffered_dc = wx.BufferedDC(dc, buffer=self.buffer, style=wx.BUFFER_CLIENT_AREA)
        self.draw(buffered_dc, e.GetPosition())

    def OnPaint(self, e):
        dc = wx.AutoBufferedPaintDC(self)
        self.draw(dc)

    def draw(self, dc, cursor_position=None):
        painter = Painter(dc, zoom=3)
        painter.draw(cursor_position)
        tile = painter.tile
        if tile is None:
            self.StatusBar.SetStatusText("[-:-]")
        else:
            self.StatusBar.SetStatusText(f"[{tile[0]}:{tile[1]}]")

    def OnQuit(self, e):
        self.Close()
