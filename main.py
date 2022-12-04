import socket

import wx
import wx.adv
import wx.propgrid

import functions
import i18n
from i18n import translations
import data
import forms

# Read Config
conf = data.NMSLConfig()

lang = translations[conf.config['LANG']]


class NMSLFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=lang.gui.title, pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

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

        self.serverList = wx.TreeCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(150, 300), wx.TR_DEFAULT_STYLE)
        self.serverListRoot = self.serverList.AddRoot(socket.gethostname())
        self.serverListServers = self.serverList.AppendItem(self.serverListRoot, lang.gui.serverlist.servers)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnServerInfo, self.serverList)

        self.serverPropertyGrid = wx.propgrid.PropertyGrid(self, wx.ID_ANY, wx.DefaultPosition,
                                                           wx.Size(310, -1), wx.propgrid.PG_DEFAULT_STYLE)
        self.serverPropertyGridName = self.serverPropertyGrid.Append(wx.propgrid.StringProperty('Name', 'Name'))
        self.serverPropertyGridPath = self.serverPropertyGrid.Append(wx.propgrid.StringProperty('Path', 'Path'))
        self.serverPropertyGridServerside = self.serverPropertyGrid.Append(
            wx.propgrid.StringProperty('Server-side', 'Server-side'))

        self.start = wx.Button(self, wx.ID_ANY, lang.gui.homepage.start_server, wx.DefaultPosition, wx.Size(72, -1), 0)
        self.Bind(wx.EVT_BUTTON, self.OnStart, self.start)

        self.sizer = wx.WrapSizer(wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS)
        self.sub_sizer1 = wx.WrapSizer(wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS)

        self.sub_sizer1.Add(self.serverPropertyGrid, 0, wx.ALL, 5)
        self.sub_sizer1.Add(self.start, 0, wx.ALL, 5)

        self.sizer.Add(self.serverList, 0, wx.ALL, 5)
        self.sizer.Add(self.sub_sizer1, 1, wx.EXPAND, 5)
        # self.sizer.Add(self.serverPropertyGrid, 0, wx.ALL, 5)

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
        new_instance_dialog = forms.NewInstanceDialog(self, lang, conf)
        if new_instance_dialog.ShowModal() == wx.ID_OK:
            print(new_instance_dialog.GetValue())

    @staticmethod
    def OnAbout(event):
        # wx.MessageBox(lang.gui.window.about.content,
        #               lang.gui.window.about.title,
        #               wx.OK | wx.ICON_INFORMATION)
        about_dia = wx.adv.AboutDialogInfo()
        about_dia.SetName('NMSL')
        about_dia.SetVersion(i18n.VERSION)
        about_dia.SetDescription(lang.description)
        about_dia.SetCopyright('(C) 2015 - 2023 CAP')
        about_dia.SetWebSite('https://github.com/woshishabii/NMSL')
        about_dia.AddDeveloper('woshishabii')
        about_dia.AddDeveloper('CreepAmongProjects')
        about_dia.AddArtist('woshishabii')
        about_dia.AddTranslator('woshishabii')
        about_dia.AddDocWriter('woshishabii')
        wx.adv.AboutBox(about_dia)

    def OnStart(self, event):
        functions.start_server(data.ServerConfig(conf.config['SERVERS']
                                                 [self.serverList.GetItemText(self.serverList.GetSelection())]))

    def refreshList(self):
        self.serverList.DeleteChildren(self.serverListServers)
        conf.read_config()
        print(conf.get_servers())
        for _ in conf.get_servers():
            # sc = data.ServerConfig(_)
            # self.serverList.AppendItem(self.serverListServers, sc.config['NAME'])
            self.serverList.AppendItem(self.serverListServers, _)

    def OnServerInfo(self, event):
        # print(self.serverList.GetItemText(self.serverList.GetSelection()))
        _ = self.serverList.GetItemText(self.serverList.GetSelection())
        if _ in conf.config['SERVERS']:
            sc = data.ServerConfig(conf.config['SERVERS'][_])
            self.serverPropertyGridName.SetValue(_)
            self.serverPropertyGridName.Enable(True)
            self.serverPropertyGridPath.SetValue(sc.path)
            self.serverPropertyGridPath.Enable(True)
            self.serverPropertyGridServerside.SetValue(sc.config['SERVERSIDE'])
            self.serverPropertyGridServerside.Enable(True)
            self.start.Enable(True)
        else:
            self.serverPropertyGridName.SetValue('')
            self.serverPropertyGridName.Enable(False)
            self.serverPropertyGridPath.SetValue('')
            self.serverPropertyGridPath.Enable(False)
            self.serverPropertyGridServerside.SetValue('')
            self.serverPropertyGridServerside.Enable(False)
            self.start.Enable(False)


if __name__ == '__main__':
    app = wx.App()
    frm = NMSLFrame(None)
    frm.Show()
    app.MainLoop()
