import wx, mysql.connector

class mainPanel(wx.Panel):
    # Main Panel will include:
        # Keypad for PIN entry
        # On Enter Press: will check with DB and send user to Admin or Employee Panel

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        title = 'employee-time-tracker'

        png = wx.Image('images/logo.png')
        png.Rescale(300, 80)
        logo = wx.Bitmap(png)
        wx.StaticBitmap(self, -1, logo, (340, 100), style=wx.BITMAP_TYPE_PNG)

        wx.StaticText(self, -1, 'Employee Time Tracking', (410, 205))

        self.pin = wx.TextCtrl(self, pos=(440, 250), size=(90, 24))

        self.btnOne = wx.Button(self, -1, "1", (440, 280), size=(30,30))
        self.btnTwo = wx.Button(self, -1, "2", (470, 280), size=(30, 30))
        self.btnThree = wx.Button(self, -1, "3", (500, 280), size=(30, 30))        
        self.btnFour = wx.Button(self, -1, "4", (440, 310), size=(30, 30))
        self.btnFive = wx.Button(self, -1, "5", (470, 310), size=(30, 30))
        self.btnSix = wx.Button(self, -1, "6", (500, 310), size=(30, 30))
        self.btnSeven = wx.Button(self, -1, "7", (440, 340), size=(30, 30))
        self.btnEight = wx.Button(self, -1, "8", (470, 340), size=(30, 30))
        self.btnNine = wx.Button(self, -1, "9", (500, 340), size=(30, 30))
        self.btnZero = wx.Button(self, -1, "0", (470, 370), size=(30, 30))

        self.btnEnter = wx.Button(self, -1, "Enter", (445, 410))

class adminPanel(wx.Panel):
    # Admin Panel
        # Add / Remove Employees
        # Export Montly Time Reports
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.btn = wx.Button(self, -1, "Back to Main Menu", (350, 150))

class empPanel(wx.Panel):
    # Employee Panel
        # Start / Stop Time Clock
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)