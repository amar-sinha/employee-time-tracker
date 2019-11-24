from tkinter import *
import tkinter.messagebox
import mysql.connector, time, datetime

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
        end_time time,
        hours float,
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


class tkWindow():
    def __init__(self):
        self.root = Tk()
        
        windowWidth = self.root.winfo_reqwidth()
        windowHeight = self.root.winfo_reqheight()
        
         # get horizontal and vertical screen sizes
        positionHorizontal = int(self.root.winfo_screenwidth()/2 - windowWidth/2)
        positionVertical = int(self.root.winfo_screenheight()/2 - windowHeight/2)
        
        # position window in center of the screen
        self.root.geometry("+{}+{}".format(positionHorizontal, positionVertical))
        self.root.resizable(0, 0) # prevent window resizing

    def run(self):
        self.root.mainloop()

    def quit(self):
        self.root.quit()

    def close(self):
        self.root.destroy()

class emp_win():
    def __init__(self, pin, f_name, l_name):
        self.emp = tkWindow()
        self.empTk = self.emp.root
        self.empTk.title("Employees - Employee Time Tracker")

        lastEntryQuery = "SELECT start_time, end_time from employee_time_tracker.hours WHERE pin = %s ORDER BY pin DESC, date DESC, start_time DESC" % pin
        print(pin)
        cursor.execute(lastEntryQuery)
        lastEntry = cursor.fetchone()
        print(lastEntry)

        # set clock in and out buttons
        self.empLbl = Label(self.empTk, width=30)
        self.empLbl.grid(row=0, column=0, columnspan=2, ipady=5)
        self.empLbl.config(text = "Employee: %s, %s" % (l_name, f_name), font=("",24))

        self.clockInBtn = Button(self.empTk, text="Clock In")
        self.clockInBtn.grid(row=1, column=0, columnspan=1, pady=20, ipadx=10, ipady=5)

        self.clockOutBtn = Button(self.empTk, text="Clock Out")
        self.clockOutBtn.grid(row=1, column=1, columnspan=1, pady=20, ipadx=10, ipady=5)

        if (lastEntry is not None):
            if (lastEntry[0] is None):
                print('ok')
                self.clockOutBtn.grid_remove()
            elif (lastEntry[1] is None):
                test = self.convertSQLDateTimeToTimestamp(lastEntry[0])
                self.clockOutBtn.configure(command=lambda val=test:self.onClockOutBtn_Click(test))
                self.clockInBtn.grid_remove()
                
                self.clockInLbl = Label(self.empTk)
                self.clockInLbl.grid(row=1, column=0, columnspan=1, pady=20, ipadx=10, ipady=5)
                self.clockInLbl.config(text = "Clock In Time: " + str(test))

    def onClockOutBtn_Click(self, then):
        now = datetime.datetime.now().time()
        print("Current Time =", now)
        
        then_delta = datetime.timedelta(hours=then.hour, minutes=then.minute, seconds=then.second)
        now_delta = datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
        diff_delta_sec = now_delta - then_delta
        diff_delta_hrs = diff_delta_sec.total_seconds()/3600
        
        print(self.roundTime(diff_delta_hrs))

    def convertSQLDateTimeToTimestamp(self, value):
        return (datetime.datetime.min + value).time()

    def roundTime(self, value):
        return round(value * 2) / 2


class main_win():
    def __init__(self):
        self.main = tkWindow()
        self.mainTk = self.main.root
        self.mainTk.title("Employee Time Tracker")
        self.pin = ""
        self.keys = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ['DELETE', '0', 'SUBMIT'],
        ]

        # label to display pin
        self.mainLbl = Label(self.mainTk)
        self.mainLbl.grid(row=0, column=0, columnspan=3, ipady=5)
        self.mainLbl.config(font=("",24))

        # create buttons using keypad layout
        for y, row in enumerate(self.keys, 1):
            for x, key in enumerate(row):
                b = Button(self.mainTk, text=key, command=lambda val=key:self.check_code(val), width = 10, height = 3)
                b.grid(row=y, column=x, ipadx=20, ipady=5)

    def check_code(self, value):
        if value == 'DELETE':
            # remove last number from pin
            self.pin = self.pin[:-1]
            self.mainLbl.config(text = self.pin)
        
        elif value == 'SUBMIT':
                # check pin
                grabUserQuery = "SELECT * FROM employee_time_tracker.users WHERE pin = " + self.pin
                cursor.execute(grabUserQuery)
                user = cursor.fetchone()
                print(user)
                if user is not None:
                    self.main.close()
                    time.sleep(2)
                    if user[3] == "admin":
                        print(user)
                    elif user[3] == "emp":
                        emp = emp_win(self.pin, user[1], user[2])
                        emp.emp.run()
                else:
                    tkinter.messagebox.showinfo("Error - Employee Time Tracker", "ERROR: Invalid pin entered. Please try again.")
                self.pin = ""
                self.mainLbl.config(text = self.pin)

        elif len(self.pin) < 4:
            # add number to pin
            self.pin += value
            self.mainLbl.config(text = str(self.pin))

if __name__ == "__main__":
    m = main_win()
    m.main.run()