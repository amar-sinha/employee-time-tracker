import wx, mysql.connector

class Program(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, 'employee-time-tracker')

        sizer = wx.BoxSizer()
        self.SetSizer(sizer)

        self.Centre()