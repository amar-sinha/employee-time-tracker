import wx, mysql.connector, time

createdb_query = "CREATE DATABASE IF NOT EXISTS employee_time_tracker;"

users_table_query = """
    CREATE TABLE employee_time_tracker.users (
        pin int(4) NOT NULL,
        f_name varchar(100) NOT NULL,
        l_name varchar(100) NOT NULL,
        role varchar(50) NOT NULL,
        PRIMARY KEY (pin)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1;"""

hours_table_query = """
    CREATE TABLE employee_time_tracker.hours (
        pin int(4) NOT NULL,
        date date NOT NULL,
        start_time time NOT NULL,
        end_time time NOT NULL,
        hours float NOT NULL,
        PRIMARY KEY (pin, date, start_time),
        FOREIGN KEY (pin) REFERENCES employee_time_tracker.users(pin) 
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1;"""

try:
    cnx = mysql.connector.connect(user='root', password='', host='localhost', database='employee_time_tracker')
    cursor = cnx.cursor()

except:
    cnx = mysql.connector.connect(user='root', password='', host='localhost')
    cursor = cnx.cursor()
    cursor.execute(createdb_query)
    cursor.execute(users_table_query)
    cursor.execute(hours_table_query)
    cnx.commit()

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
        # List of Employees (use wx.ListBox or wx.ListCtrl)
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.btn = wx.Button(self, -1, "Back to Main Menu", (410, 375))

        png = wx.Image('images/logo.png')
        png.Rescale(300, 80)
        logo = wx.Bitmap(png)
        wx.StaticBitmap(self, -1, logo, (340, 100), style=wx.BITMAP_TYPE_PNG)

        self.addBtn = wx.Button(self, -1, "Add Employee", (410, 205))
        self.remBtn = wx.Button(self, -1, "Remove Employee", (410, 235))
        self.exportBtn = wx.Button(self, -1, "Export Time Sheets", (410, 265))
    
class addEmpPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.btn = wx.Button(self, -1, "Back to Main Menu", (350, 150))

class empPanel(wx.Panel):
    # Employee Panel
        # Start / Stop Time Clock
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)