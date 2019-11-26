from tkinter import *
import time, datetime
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
        lastEntryQuery = "SELECT start_time, end_time from hours WHERE pin = %s ORDER BY start_time DESC LIMIT 1 FOR UPDATE" % self.pin
        self.cursor.execute(lastEntryQuery)
        lastEntry = self.cursor.fetchone()
        if lastEntry is not None:
            self.start_time, self.end_time = lastEntry[0], lastEntry[1]

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
                self.clockOutBtn.configure(command=lambda cmd=self.start_time:self.onClockOutBtn_Click(self.start_time))
                self.clockInBtn.grid_remove()

                self.clockInLbl.grid(row=1, column=0, columnspan=1, pady=20, ipadx=10, ipady=5)
                self.clockInLbl.config(text = "Clock In Time: " + str(self.start_time))
            else:
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
        self.cursor.execute(insertRowQuery)
        self.cnx.commit()

    def onClockOutBtn_Click(self, then):
        now = datetime.datetime.now()
        self.end_time = now.strftime("%Y-%m-%d %H:%M:%S")

        self.clockOutBtn.grid_remove()
        self.clockInLbl.grid_remove()
        self.addClockInOutBtns("in")

        updtCond = "WHERE pin = %s AND start_time = '%s'" % (self.pin, str(self.start_time))
        updateEndTimeQuery = "UPDATE hours SET end_time = '%s' %s" % (self.end_time, updtCond)
        self.cursor.execute(updateEndTimeQuery)
        updateDurationQuery = "UPDATE hours SET duration = end_time - start_time %s" % updtCond
        self.cursor.execute(updateDurationQuery)
        updateHoursQuery = "UPDATE hours SET hours = round(extract(epoch from duration)/3600) %s" % updtCond
        self.cursor.execute(updateHoursQuery)
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