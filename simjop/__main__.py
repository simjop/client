import wx

from gui.area_editor import AreaEditor


def main():

    app = wx.App()
    ex = AreaEditor(None)
    ex.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()


# https://www.linw1995.com/en/blog/Run-Asyncio-Event-Loop-in-another-thread/
# thr = AsyncioEventLoopThread()
# thr.start()
# queue = asyncio.Queue()
#
# try:
#    App(config).mainloop()
# finally:
#    thr.stop()
#
