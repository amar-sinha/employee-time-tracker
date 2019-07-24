import wx, mysql.connector, panels

class Program(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, 'employee-time-tracker')

        sizer = wx.BoxSizer()
        self.SetSizer(sizer)

        self.panel_one = panels.mainPanel(self)
        self.panel_two = panels.adminPanel(self)
        self.panel_three = panels.userPanel(self)

        sizer.Add(self.panel_one, 1, wx.EXPAND)

        self.panel_one.btnAdminPanel.Bind(wx.EVT_BUTTON, self.show_panel_two)
        sizer.Add(self.panel_two, 1, wx.EXPAND)
        self.panel_two.btn.Bind(wx.EVT_BUTTON, self.show_panel_one)
        self.panel_two.Hide()

        self.panel_one.btnUserPanel.Bind(wx.EVT_BUTTON, self.show_panel_three)
        sizer.Add(self.panel_three, 1, wx.EXPAND)
        self.panel_three.btn.Bind(wx.EVT_BUTTON, self.show_panel_one)
        self.panel_three.Hide()

        self.SetSize((960, 540))
        self.Centre()
    
    def show_panel_one(self, event):
        self.panel_one.Show()
        self.panel_two.Hide()
        self.panel_three.Hide()
        self.Layout()
    
    def show_panel_two(self, event):
        self.panel_two.Show()
        self.panel_one.Hide()
        self.Layout()

    def show_panel_three(self, event):
        self.panel_three.Show()
        self.panel_one.Hide()
        self.Layout()