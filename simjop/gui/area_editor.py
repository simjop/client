from enum import Enum, auto

import wx

from core.painter import Dimension, Painter
from gui.toolbar import ToolBarLogic


class ActionMode(Enum):
    DEFAULT = auto()
    LINE_ENABLED = auto()
    LINE_STARTED = auto()


class AreaEditor(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.buffer = None
        self.toolbar = None
        self.click_mode = ActionMode.DEFAULT

        self._zoom = 3
        self._depth = 32

        self.InitUI()
        self.Centre()

    def InitUI(self):

        self.SetSize((800, 600))
        self.SetTitle("simJOP")

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.buffer = wx.Bitmap(300, 200, depth=self._depth)

        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        file_item = file_menu.Append(wx.ID_EXIT, "Quit", "Quit application")
        menubar.Append(file_menu, "&File")
        self.SetMenuBar(menubar)

        toolbar = self.CreateToolBar()
        bitmap_track = wx.Bitmap("simjop/icons/btn_24_track.svg", wx.BITMAP_TYPE_ANY)
        bitmap_signal = wx.Bitmap("simjop/icons/btn_24_signal.svg", wx.BITMAP_TYPE_ANY)
        line_tool = toolbar.AddCheckTool(wx.ID_ANY, "Line", bitmap_track)
        signal_tool = toolbar.AddCheckTool(wx.ID_ANY, "Signal", bitmap_signal)
        toolbar.Realize()
        self.toolbar = ToolBarLogic(toolbar, ["Line", "Signal"])

        self.Bind(wx.EVT_MENU, self.OnQuit, file_item)
        self.Bind(wx.EVT_TOOL, self.OnLineButton, line_tool)
        self.Bind(wx.EVT_TOOL, self.OnSignalButton, signal_tool)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnCursorEnterWindow)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnCursorLeaveWindow)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftClick)

        statusbar = wx.StatusBar(self)
        statusbar.SetStatusText("Připraveno")
        self.SetStatusBar(statusbar)

        icon = wx.Icon(
            wx.Bitmap("simjop/icons/logo_with_alpha.png", wx.BITMAP_TYPE_ANY)
        )
        self.SetIcon(icon)

    def OnCursorEnterWindow(self, event):
        blank_cursor = wx.Cursor(wx.CURSOR_BLANK)
        self.SetCursor(blank_cursor)

    def OnCursorLeaveWindow(self, event):
        default_cursor = wx.Cursor(wx.CURSOR_DEFAULT)
        self.SetCursor(default_cursor)

    def OnMouseMotion(self, event):

        dc = wx.ClientDC(self)
        dc_w, dc_h = dc.GetSize()

        if self.buffer is None:
            self.buffer = wx.Bitmap(dc_w, dc_h, depth=self._depth)

        bw, bh = self.buffer.GetSize()
        if dc_w != bw or dc_h != bh:
            self.buffer = wx.Bitmap(dc_w, dc_h, depth=self._depth)

        buffered_dc = wx.BufferedDC(dc, buffer=self.buffer, style=wx.BUFFER_CLIENT_AREA)
        self.draw(buffered_dc, event.GetPosition())

    def OnPaint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        self.draw(dc)

    def draw(self, dc, cursor_position=None):
        painter = Painter(dc, self._zoom)
        painter.draw(cursor_position)
        tile = painter.tile
        statusbar = self.GetStatusBar()
        if tile is None:
            statusbar.SetStatusText("[-:-]")
        else:
            statusbar.SetStatusText(f"[{tile[0]}:{tile[1]}]")

    def OnQuit(self, event):
        self.Close()

    def OnLineButton(self, event):
        if self.toolbar.on_button("Line"):
            self.click_mode = ActionMode.LINE_ENABLED
        else:
            self.click_mode = ActionMode.DEFAULT

    def OnSignalButton(self, event):
        self.click_mode = ActionMode.DEFAULT

    def OnLeftClick(self, event):
        dc = wx.ClientDC(self)
        dim = Dimension(dc, self._zoom)
        position = event.GetLogicalPosition(dc)
        tile = dim.xy_to_tile(position)

        match self.click_mode:
            case ActionMode.LINE_ENABLED:
                self.click_mode = ActionMode.LINE_STARTED
            case ActionMode.LINE_STARTED:
                self.click_mode = ActionMode.LINE_ENABLED
            case _:
                pass
