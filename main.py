import wx
import os

from i18n import translations
import data

# Read Config
conf = data.NMSLConfig()

lang = translations[conf.config['LANG']]


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
        new_instance_dialog = NewInstanceDialog(self, lang, conf.get_servers())
        if new_instance_dialog.ShowModal() == wx.ID_OK:
            print(new_instance_dialog.GetValue())

    @staticmethod
    def OnAbout(event):
        wx.MessageBox(lang.gui.window.about.content,
                      lang.gui.window.about.title,
                      wx.OK | wx.ICON_INFORMATION)


class NewInstanceDialog(wx.Dialog):
    def __init__(self, parent, trans, servers):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=trans.gui.window.new_instance.title,
                           pos=wx.DefaultPosition, size=wx.Size(450, 210), style=wx.DEFAULT_DIALOG_STYLE)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.sizer = wx.WrapSizer(wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS)

        self.name = wx.StaticText(self, wx.ID_ANY, trans.gui.window.new_instance.enter_name,
                                  wx.DefaultPosition, wx.Size(100, -1), 0)
        self.name.Wrap(0)

        self.name_textctrl = wx.TextCtrl(self, wx.ID_ANY, trans.gui.window.new_instance.default_name,
                                         wx.DefaultPosition, wx.Size(310, -1), 0)

        self.select_dir_label = wx.StaticText(self, wx.ID_ANY, trans.gui.window.new_instance.opendir_label,
                                              wx.DefaultPosition, wx.Size(100, -1), 0)
        self.select_dir_label.Wrap(-1)

        self.select_dir = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, trans.gui.window.new_instance.opendir_label,
                                           wx.DefaultPosition, wx.Size(310, -1), wx.DIRP_DEFAULT_STYLE)

        self.select_serverside_label = wx.StaticText(self, wx.ID_ANY, trans.gui.window.new_instance.select_serverside,
                                                     wx.DefaultPosition, wx.Size(100, -1), 0)
        self.select_serverside_label.Wrap(-1)

        select_serversideChoices = [u"Vanilla", u"Forge", u"Fabric", u"Spigot", u"Paper"]
        self.select_serverside = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(310, -1),
                                           select_serversideChoices, 0)
        self.select_serverside.SetSelection(0)

        self.select_version_label = wx.StaticText(self, wx.ID_ANY, trans.gui.window.new_instance.select_version,
                                                  wx.DefaultPosition, wx.Size(100, -1), 0)
        self.select_version_label.Wrap(-1)

        select_versionChoices = [u"1.19", u"1.18", u"1.17"]
        self.select_version = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(310, -1), select_versionChoices, 0)
        self.select_version.SetSelection(0)

        self.refresh = wx.Button(self, wx.ID_ANY, trans.gui.window.new_instance.refresh_metadata,
                                 wx.DefaultPosition, wx.Size(205, -1), 0)

        self.go = wx.Button(self, wx.ID_ANY, trans.gui.window.new_instance.start,
                            wx.DefaultPosition, wx.Size(205, -1), 0)

        self.sizer.Add(self.name, 0, wx.ALL, 5)
        self.sizer.Add(self.name_textctrl, 0, wx.ALL, 5)
        self.sizer.Add(self.select_dir_label, 0, wx.ALL, 5)
        self.sizer.Add(self.select_dir, 0, wx.ALL, 5)
        self.sizer.Add(self.select_serverside_label, 0, wx.ALL, 5)
        self.sizer.Add(self.select_serverside, 0, wx.ALL, 5)
        self.sizer.Add(self.select_version_label, 0, wx.ALL, 5)
        self.sizer.Add(self.select_version, 0, wx.ALL, 5)
        self.sizer.Add(self.refresh, 0, wx.ALL, 5)
        self.sizer.Add(self.go, 0, wx.ALL, 5)

        self.SetSizer(self.sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.Bind(wx.EVT_BUTTON, self.OnSubmit, self.go)

        self.trans = trans
        self.servers = servers

    def OnSubmit(self, event):
        if self.name_textctrl.GetValue() in self.servers or self.name_textctrl.GetValue() == '':
            wx.MessageBox(self.trans.gui.window.new_instance.invalid_name,
                          self.trans.gui.window.new_instance.invalid_name_title,
                          wx.ICON_ERROR)
            return
        if not os.path.exists(self.select_dir.GetPath()):
            if wx.MessageBox(self.trans.gui.window.new_instance.dir_not_exist,
                             self.trans.gui.window.new_instance.dir_not_exist_title,
                             wx.YES_NO | wx.ICON_INFORMATION) is not wx.YES:
                return
            else:
                os.makedirs(self.select_dir.GetPath())
        if 'server.nmsl.json' in os.listdir(self.select_dir.GetPath()):
            if not wx.MessageBox(self.trans.gui.window.new_instance.dir_has_file_config,
                                 self.trans.gui.window.new_instance.dir_has_file_title,
                                 wx.YES_NO | wx.ICON_INFORMATION) == wx.YES:
                return
        elif os.listdir(self.select_dir.GetPath()):
            if not wx.MessageBox(self.trans.gui.window.new_instance.dir_has_file,
                                 self.trans.gui.window.new_instance.dir_has_file_title,
                                 wx.YES_NO | wx.ICON_INFORMATION) == wx.YES:
                return
        self.EndModal(wx.ID_OK)

    def GetValue(self):
        return self.name_textctrl.GetValue(), self.select_dir.GetPath(), \
               self.select_serverside.GetSelection(), self.select_version.GetSelection()


if __name__ == '__main__':
    app = wx.App()
    frm = NMSLFrame(None, title=lang.gui.title)
    frm.Show()
    app.MainLoop()
