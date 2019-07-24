import wx, mysql.connector

class mainPanel(wx.Panel):
    # Main Panel will include:
        # Admin Panel Option
        # Employee Panel Option
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        title = 'employee-time-tracker'

        self.btnAdminPanel = wx.Button(self, -1, "Admin Login", (360, 290))
        self.btnUserPanel = wx.Button(self, -1, "Employee Panel", (495, 290))

        wx.StaticText(self, -1, 'Employee Time Tracking', (410, 245))

        png = wx.Image('images/logo.png')
        png.Rescale(300, 80)
        logo = wx.Bitmap(png)
        wx.StaticBitmap(self, -1, logo, (340, 140), style=wx.BITMAP_TYPE_PNG)

class adminPanel(wx.Panel):
    # Admin Panel
        # Add / Remove Employees
        # Export Montly Time Reports
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.btn = wx.Button(self, -1, "Back to Main Menu", (350, 150))

class userPanel(wx.Panel):
    # User Panel
        # Employee Selection (enter a four digit PIN) -> sends to Time Record Panel
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.btn = wx.Button(self, -1, "Back to Main Menu", (350, 150))

class recordPanel(wx.Panel):
    # Record Panel
        # Start / Stop Time Clock
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)