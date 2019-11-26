from tkinter import *
import tkinter.messagebox, time, datetime
from tkWindow import tkWindow

class emp_win():
    def __init__(self, conn, cur, pin, f_name, l_name):
        self.cnx = conn
        self.cursor = cur
        self.emp = tkWindow()
        self.empTk = self.emp.root
        self.empTk.title("Employees - Employee Time Tracker")
        self.pin = pin

        self.cursor.execute("BEGIN")
        lastEntryQuery = "SELECT * from hours WHERE pin = %s ORDER BY start_time DESC LIMIT 1 FOR UPDATE" % self.pin
        self.cursor.execute(lastEntryQuery)
        lastEntry = self.cursor.fetchone()
        if lastEntry is not None:
            self.start_time, self.end_time, self.hours = lastEntry[1], lastEntry[2], lastEntry[3]

        # set clock in and out buttons
        self.empLbl = Label(self.empTk, width=30)
        self.empLbl.grid(row=0, column=0, columnspan=2, ipady=5)
        self.empLbl.config(text = "Employee: %s, %s" % (l_name, f_name), font=("",24))

        self.clockInBtn = Button(self.empTk, text="Clock In")
        self.clockOutBtn = Button(self.empTk, text="Clock Out")
        self.clockInLbl = Label(self.empTk)

        self.addClockInOutBtns("in")
        self.addClockInOutBtns("out")

        if (lastEntry is not None):
            if (self.end_time is None):
                print('ko')
                self.clockOutBtn.configure(command=lambda cmd=self.start_time:self.onClockOutBtn_Click(self.start_time))
                self.clockInBtn.grid_remove()

                self.clockInLbl.grid(row=1, column=0, columnspan=1, pady=20, ipadx=10, ipady=5)
                self.clockInLbl.config(text = "Clock In Time: " + str(self.start_time))
            else:
                print('ok')
                self.clockInBtn.configure(command=lambda cmd=self:self.onClockInBtn_Click())
                self.clockOutBtn.grid_remove()

    def onClockInBtn_Click(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.start_time = datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S")

        self.clockInBtn.grid_remove()
        self.clockInLbl.grid(row=1, column=0, columnspan=1, pady=20, ipadx=10, ipady=5)
        self.clockInLbl.config(text = "Clock In Time: " + now)
        self.addClockInOutBtns("out")

        insertRowQuery = "INSERT INTO hours (pin, start_time) VALUES (%s, '%s')" % (self.pin, now)
        print(insertRowQuery)
        self.cursor.execute(insertRowQuery)
        self.cnx.commit()

    def onClockOutBtn_Click(self, then):
        now = datetime.datetime.now()
        self.end_time = now.strftime("%Y-%m-%d %H:%M:%S")

        diff_delta_sec = now - self.start_time
        diff_delta_hrs = diff_delta_sec.total_seconds() / 3600
        self.hours = str(int(self.roundTime(diff_delta_hrs)))

        self.clockOutBtn.grid_remove()
        self.clockInLbl.grid_remove()
        self.addClockInOutBtns("in")

        updateRowQuery = "UPDATE hours SET end_time = '%s', hours = %s WHERE pin = %s AND start_time = '%s'" % (self.end_time, self.hours, self.pin, str(self.start_time))
        print(updateRowQuery)
        self.cursor.execute(updateRowQuery)
        self.cnx.commit()

    def addClockInOutBtns(self, in_out):
        if (in_out == "in"):
            self.clockInBtn.grid(row=1, column=0, columnspan=1, pady=20, ipadx=10, ipady=5)
            self.clockInBtn.configure(command=lambda cmd=self:self.onClockInBtn_Click())
        elif (in_out == "out"):
            self.clockOutBtn.grid(row=1, column=1, columnspan=1, pady=20, ipadx=10, ipady=5)
            self.clockOutBtn.configure(command=lambda cmd=self.start_time:self.onClockOutBtn_Click(self.start_time))

    def roundTime(self, value):
        return round(value * 2) / 2