import wx

from i18n import translations


lang = translations['zh-CN']


class NMSLFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(NMSLFrame, self).__init__(*args, **kw)

        pnl = wx.Panel(self)

        st = wx.StaticText(pnl, label="Hello NMSL!")
        font = wx.Font(32, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'OCR A Extended')
        st.SetFont(font)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(st, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 25))
        pnl.SetSizer(sizer)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText(lang.gui.statusbar.welcome)

    def makeMenuBar(self):
        fileMenu = wx.Menu()
        newInstanceItem = fileMenu.Append(-1, f'{lang.gui.filemenu.new_instance}\tCtrl-N',
                                          lang.gui.statusbar.new_instance)
        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(-1, f'{lang.gui.filemenu.exit}\tCtrl-X',
                                   lang.gui.statusbar.exit)

        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(-1, f'{lang.gui.helpmenu.about}',
                                    lang.gui.statusbar.about)
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, f'{lang.gui.menu.file}(&F)')
        menuBar.Append(helpMenu, f'{lang.gui.menu.help}(&H)')

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnNewInstance, newInstanceItem)
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event):
        self.Close(True)

    def OnNewInstance(self, event):
        wx.MessageBox("Hello again from wxPython")

    def OnAbout(self, event):
        wx.MessageBox(lang.gui.window.about.content,
                      lang.gui.window.about.title,
                      wx.OK | wx.ICON_INFORMATION)


if __name__ == '__main__':
    app = wx.App()
    frm = NMSLFrame(None, title=lang.gui.title)
    frm.Show()
    app.MainLoop()
