import socket

import wx
import os
import requests

from i18n import translations
import data
import functions

# Read Config
conf = data.NMSLConfig()

lang = translations[conf.config['LANG']]


class NMSLFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=lang.gui.title, pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        self.statusBar = self.CreateStatusBar(1, wx.STB_SIZEGRIP)
        self.menuBar = wx.MenuBar(0)
        self.fileMenu = wx.Menu()
        self.newInstanceItem = wx.MenuItem(self.fileMenu, wx.ID_ANY, f'{lang.gui.filemenu.new_instance}\tCtrl-N',
                                           lang.gui.statusbar.new_instance, wx.ITEM_NORMAL)
        self.exitItem = wx.MenuItem(self.fileMenu, wx.ID_ANY, f'{lang.gui.filemenu.exit}\tCtrl-X',
                                    lang.gui.statusbar.exit, wx.ITEM_NORMAL)
        self.fileMenu.Append(self.newInstanceItem)
        self.fileMenu.AppendSeparator()
        self.fileMenu.Append(self.exitItem)
        self.menuBar.Append(self.fileMenu, f'{lang.gui.menu.file}(&F)')
        self.helpMenu = wx.Menu()
        self.aboutItem = wx.MenuItem(self.helpMenu, wx.ID_ANY, lang.gui.helpmenu.about,
                                     lang.gui.statusbar.about, wx.ITEM_NORMAL)
        self.helpMenu.Append(self.aboutItem)
        self.menuBar.Append(self.helpMenu, f'{lang.gui.menu.help}(&H)')
        self.SetMenuBar(self.menuBar)
        self.Bind(wx.EVT_MENU, self.OnNewInstance, self.newInstanceItem)
        self.Bind(wx.EVT_MENU, self.OnExit, self.exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, self.aboutItem)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.serverList = wx.TreeCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(150, 300), wx.TR_DEFAULT_STYLE)
        self.serverListRoot = self.serverList.AddRoot(socket.gethostname())
        self.serverListServers = self.serverList.AppendItem(self.serverListRoot, lang.gui.serverlist.servers)
        # print(self.serverList.GetItemText(self.serverList.GetSelection()))
        self.sizer.Add(self.serverList, 0, wx.ALL, 5)
        # self.Bind(wx.EVT_TREE_KEY_DOWN, self.OnRefreshList, self.serverList)

        self.SetSizer(self.sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # create a menu bar
        # self.makeMenuBar()

        # and a status bar
        # self.CreateStatusBar()
        self.SetStatusText(lang.gui.statusbar.welcome)
        self.refreshList()

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

    def refreshList(self):
        self.serverList.DeleteChildren(self.serverListServers)
        conf.read_config()
        print(conf.get_servers())
        for _ in conf.get_servers():
            sc = data.ServerConfig(_)
            self.serverList.AppendItem(self.serverListServers, sc.config['NAME'])


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

        self.select_serversideChoices = [u"Vanilla", u"Forge", u"Fabric", u"Spigot", u"Paper"]
        self.select_serverside = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(310, -1),
                                           self.select_serversideChoices, 0)
        self.select_serverside.SetSelection(0)

        self.select_version_label = wx.StaticText(self, wx.ID_ANY, trans.gui.window.new_instance.select_version,
                                                  wx.DefaultPosition, wx.Size(100, -1), 0)
        self.select_version_label.Wrap(-1)

        self.version_list = functions.get_serverside_version_list(self.select_serversideChoices
                                                                  [self.select_serverside.GetSelection()])
        self.select_version = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(310, -1),
                                        self.version_list, 0)
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

        self.Bind(wx.EVT_CHOICE, self.OnChoice)
        self.Bind(wx.EVT_BUTTON, self.OnSubmit, self.go)
        self.Bind(wx.EVT_BUTTON, self.OnRefresh, self.refresh)

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
        conf.add_server(self.select_dir.GetPath())
        self.sc = data.ServerConfig(self.select_dir.GetPath())
        self.sc.config['NAME'] = self.name_textctrl.GetValue()
        self.sc.config['SERVERSIDE'] = self.select_serversideChoices[self.select_serverside.GetSelection()]
        self.sc.config['VERSION'] = self.version_list[self.select_version.GetSelection()]
        self.sc.save_config()
        self.Parent.refreshList()
        self.DownloadServer()
        self.EndModal(wx.ID_OK)

    def OnRefresh(self, event=None):
        self.select_version.Clear()
        self.version_list = functions.get_serverside_version_list(
            self.select_serversideChoices[self.select_serverside.GetSelection()]
        )
        self.select_version.AppendItems(self.version_list)
        self.select_version.SetSelection(0)

    def OnChoice(self, event):
        if event.GetEventObject() == self.select_serverside:
            self.OnRefresh()

    def GetValue(self):
        return self.name_textctrl.GetValue(), self.select_dir.GetPath(), \
               self.select_serverside.GetSelection(), self.select_version.GetSelection()

    def DownloadServer(self):
        l = functions.get_link(
            self.select_serversideChoices[self.select_serverside.GetSelection()],
            self.version_list[self.select_version.GetSelection()]
        )
        head = requests.head(l)
        fs = head.headers.get('Content-Length')
        if fs is not None:
            fs = int(fs)
        r = requests.get(l, stream=True)
        cs = 1024
        self.progress_dia = wx.ProgressDialog(lang.gui.window.new_instance.down_progress_title,
                                              lang.gui.window.new_instance.down_progress,
                                              maximum=fs,
                                              style=wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_ESTIMATED_TIME)
        dl = 0
        os.mkdir(f'{self.sc.path}/server')
        with open(f'{self.sc.path}/server/server.jar', 'wb') as f:
            for c in r.iter_content(chunk_size=cs):
                f.write(c)
                dl += cs
                self.progress_dia.Update(dl)


if __name__ == '__main__':
    app = wx.App()
    frm = NMSLFrame(None)
    frm.Show()
    app.MainLoop()
