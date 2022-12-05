import wx
import os
import functions
import data
import requests


class NewInstanceDialog(wx.Dialog):
    def __init__(self, parent, trans, conf):
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
        self.servers = conf.get_servers()
        self.conf = conf

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
        self.sc = data.ServerConfig(self.select_dir.GetPath())
        print(self.sc.path)
        self.sc.config['NAME'] = self.name_textctrl.GetValue()
        self.sc.config['SERVERSIDE'] = self.select_serversideChoices[self.select_serverside.GetSelection()]
        self.sc.config['VERSION'] = self.version_list[self.select_version.GetSelection()]
        self.sc.save_config()
        self.conf.add_server(self.sc)
        self.Parent.refreshList()
        functions.install_server(self)
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

    def setupServer(self):
        pass
