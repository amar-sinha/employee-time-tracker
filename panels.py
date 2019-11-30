from tkinter import *
import tkinter.messagebox, tkinter.filedialog
import time, datetime, calendar
import re, os, psycopg2, subprocess
from tkWindow import tkWindow

PROC = subprocess.Popen('heroku config:get DATABASE_URL -a employee-time-tracker', stdout=subprocess.PIPE, shell=True)
DB_URL = PROC.stdout.read().decode('utf-8').strip() + '?sslmode=require'

try:
    cnx = psycopg2.connect(DB_URL, sslmode='require')
    cursor = cnx.cursor()
except:
    print("Connection to database failed.")

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
                grabUserQuery = "SELECT * FROM users WHERE pin = " + self.pin
                cursor.execute(grabUserQuery)
                user = cursor.fetchone()
                if user is not None:
                    self.main.close()
                    time.sleep(2)
                    if user[3] == "admin":
                        admin = admin_win(cnx, cursor, self.pin, user[1], user[2])
                        admin.admin.run()
                    elif user[3] == "emp":
                        emp = emp_win(cnx, cursor, self.pin, user[1], user[2])
                        emp.emp.run()
                else:
                    tkinter.messagebox.showerror("Error - Employee Time Tracker", "ERROR: Invalid pin entered. Please try again.")
                self.pin = ""
                self.mainLbl.config(text = self.pin)

        elif len(self.pin) < 4:
            # add number to pin
            self.pin += value
            self.mainLbl.config(text = str(self.pin))

class admin_win():
    def __init__(self, conn, cur, pin, f_name, l_name):
        self.cnx = conn
        self.cursor = cur
        self.admin = tkWindow()
        self.adminTk = self.admin.root
        self.adminTk.title("Admin - Employee Time Tracker")
        self.adminTk.geometry("725x300")
        self.pin = pin

        self.adminLbl = Label(self.adminTk)
        self.adminLbl.grid(row=0, column=1, ipady=5)
        self.adminLbl.config(text = "Administrator: %s, %s" % (l_name, f_name), font=("", 24))

        self.listbox = Listbox(self.adminTk, width=40)
        # scrollbar = Scrollbar(self.listbox, orient=VERTICAL)
        # self.listbox.config(yscrollcommand=scrollbar.set)
        # scrollbar.config(command=self.listbox.yview)
        self.listbox.grid(row=1, column=1, pady=15)

        self.cursor.execute("BEGIN")
        self.loadEmployees()

        self.addEmpBtn = Button(self.adminTk, text="Add/Edit Employee", command=lambda cmd=self:self.onAddEmpBtn_Click())
        self.addEmpBtn.grid(row=2, column=0, padx=20, ipadx=10, ipady=5)

        self.rmEmpBtm = Button(self.adminTk, text="Remove Employee", command=lambda cmd=self:self.onRemEmpBtn_Click())
        self.rmEmpBtm.grid(row=2, column=1, padx=20, ipadx=10, ipady=5, sticky="w")

        self.expDataBtn = Button(self.adminTk, text="Export Timesheet", command=lambda cmd=self:self.onExpDataBtn_Click())
        self.expDataBtn.grid(row=2, column=1, padx=20, ipadx=10, ipady=5, sticky="e")

        self.backBtn = Button(self.adminTk, text="Return to Log In", command=lambda cmd=self:self.onBackBtn_Click())
        self.backBtn.grid(row=2, column=2, padx=20, ipadx=10, ipady=5)

    def onBackBtn_Click(self):
        self.admin.close()
        m = main_win()
        m.main.run()

    def onExpDataBtn_Click(self):
        self.adminTk.geometry("725x475")

        # export by month, year options
        monthLbl = Label(self.adminTk, text="Month:")
        monthLbl.grid(row=3, column=1, pady=(10,0))
        monthDict = { "January" : "01", "February" : "02", "March" : "03", "April" : "04", "May" : "05", "June" : "06", "July" : "07", "August" : "08", "September" : "09", "October" : "10", "November" : "11", "December" : "12"}
        months= list(monthDict.keys())
        curMonth = StringVar(self.adminTk)
        curMonth.set(months[0])
        monthMenu = OptionMenu(self.adminTk, curMonth, *months)
        monthMenu.config(width=10)
        monthMenu.grid(row=4, column=1)

        yearLbl = Label(self.adminTk, text="Year:")
        yearLbl.grid(row=5, column=1, pady=(10,0))
        yearTxt = Entry(self.adminTk, width=10)
        yearTxt.grid(row=6, column=1)
        year = StringVar()
        year.set(datetime.datetime.today().year)
        yearTxt.config(text=year)

        # export buttons
        expSelectedBtn = Button(self.adminTk, text="Export For Selected", command=lambda cmd=self:onExpSelectedBtn_Click())
        expSelectedBtn.grid(row=7, column=0, ipadx=10, ipady=5, pady=(10,0))
        expAllBtn = Button(self.adminTk, text="Export for All", command=lambda cmd=self:onExpAllBtn_Click())
        expAllBtn.grid(row=7, column=1, padx=20, ipadx=10, ipady=5, pady=(10,0), sticky="w")
        expYearReportBtn = Button(self.adminTk, text="Export Yearly Report", command=lambda cmd=self:onExpYearReportBtn_Click())
        expYearReportBtn.grid(row=7, column=1, padx=20, ipadx=10, ipady=5, pady=(10,0), sticky="e")
        cancelBtn = Button(self.adminTk, text="Cancel", command=lambda cmd=self:onCancelBtn_Click())
        cancelBtn.grid(row=7, column=2, ipadx=10, ipady=5, pady=(10,0))

        def onCancelBtn_Click():
            elements = [monthLbl, monthMenu, yearLbl, yearTxt, expSelectedBtn, expAllBtn, expYearReportBtn, cancelBtn]
            for element in elements:
                element.grid_remove()
            self.adminTk.geometry("725x300")

        def onExpSelectedBtn_Click():
            if len(self.listbox.curselection()) != 0:
                value = self.listbox.get(self.listbox.curselection()).strip().split()
                curPin = re.sub(r'[^\w]', '', value[0])
                filePath = tkinter.filedialog.askdirectory()
                filePath += '/emp_hours.csv'

                month = monthDict[curMonth.get()]
                year = yearTxt.get()
                finalDate = calendar.monthrange(int(year), int(month))[1]
                dateRange = "'%s-%s-01 00:00:00' AND '%s-%s-%s 23:59:59'" % (year, month, year, month, finalDate)

                exportQuery = "COPY (SELECT hours.pin, users.f_name, users.l_name, hours.start_time, hours.end_time, hours.hours FROM hours JOIN users ON hours.pin = users.pin WHERE users.pin = %s AND start_time BETWEEN %s ORDER BY hours.start_time DESC) TO STDOUT DELIMITER ',' CSV HEADER" % (curPin, dateRange)
                with open(filePath, "w") as file:
                    self.cursor.copy_expert(exportQuery, file)
            else:
                tkinter.messagebox.showerror("Error - Employee Time Tracker", "No employee selected to generate report for.")

        def onExpAllBtn_Click():
            filePath = tkinter.filedialog.askdirectory()
            filePath += '/all_emp_hours.csv'

            month = monthDict[curMonth.get()]
            year = yearTxt.get()
            finalDate = calendar.monthrange(int(year), int(month))[1]
            dateRange = "'%s-%s-01 00:00:00' AND '%s-%s-%s 23:59:59'" % (year, month, year, month, finalDate)

            exportQuery = "COPY (SELECT users.f_name, users.l_name, sum(hours.hours) FROM hours JOIN users ON hours.pin = users.pin WHERE start_time BETWEEN %s GROUP BY users.pin) TO STDOUT DELIMITER ',' CSV HEADER" % dateRange
            with open(filePath, "w") as file:
                self.cursor.copy_expert(exportQuery, file)
        
        def onExpYearReportBtn_Click():
            curYear = str(datetime.datetime.today().year)
            nextYear = str(int(curYear)+1)
            
            filePath = tkinter.filedialog.askdirectory()
            filePath += '/%s_%s_report_emp_hours.csv' % (curYear, nextYear[2:])

            yearReportQuery = "COPY ("

            newRowQuery = """SELECT f_name, l_name, 
                COALESCE((select sum(hours) from hours where pin = %s and start_time BETWEEN'%s-09-01 00:00:00' AND '%s-09-30 23:59:59'), 0) as sept, 
                COALESCE((select sum(hours) from hours where pin = %s and start_time BETWEEN'%s-10-01 00:00:00' AND '%s-10-31 23:59:59'), 0) as oct, 
                COALESCE((select sum(hours) from hours where pin = %s and start_time BETWEEN'%s-11-01 00:00:00' AND '%s-11-30 23:59:59'), 0) as nov, 
                COALESCE((select sum(hours) from hours where pin = %s and start_time BETWEEN'%s-12-01 00:00:00' AND '%s-12-31 23:59:59'), 0) as dec,
                COALESCE((select sum(hours) from hours where pin = %s and start_time BETWEEN'%s-01-01 00:00:00' AND '%s-01-31 23:59:59'), 0) as jan, 
                COALESCE((select sum(hours) from hours where pin = %s and start_time BETWEEN'%s-02-01 00:00:00' AND '%s-02-28 23:59:59'), 0) as feb, 
                COALESCE((select sum(hours) from hours where pin = %s and start_time BETWEEN'%s-03-01 00:00:00' AND '%s-03-31 23:59:59'), 0) as mar, 
                COALESCE((select sum(hours) from hours where pin = %s and start_time BETWEEN'%s-04-01 00:00:00' AND '%s-04-30 23:59:59'), 0) as apr, 
                COALESCE((select sum(hours) from hours where pin = %s and start_time BETWEEN'%s-05-01 00:00:00' AND '%s-05-31 23:59:59'), 0) as may, 
                COALESCE((select sum(hours) from hours where pin = %s and start_time BETWEEN'%s-06-01 00:00:00' AND '%s-06-30 23:59:59'), 0) as june, 
                COALESCE((select sum(hours) from hours where pin = %s and start_time BETWEEN'%s-07-01 00:00:00' AND '%s-07-31 23:59:59'), 0) as july, 
                COALESCE((select sum(hours) from hours where pin = %s and start_time BETWEEN'%s-08-01 00:00:00' AND '%s-08-31 23:59:59'), 0) as aug from users where pin = %s"""

            employees = self.listbox.get(0,END)
            pins = []
            for emp in employees:
                value = emp.strip().split()
                pin = re.sub(r'[^\w]', '', value[0])
                pins.append(pin)
            
            for pin in pins:
                yearReportQuery += newRowQuery % (pin, curYear, curYear, pin, curYear, curYear, pin, curYear, curYear, pin, curYear, curYear, pin, nextYear, nextYear, pin, nextYear, nextYear, pin, nextYear, nextYear, pin, nextYear, nextYear, pin, nextYear, nextYear, pin, nextYear, nextYear, pin, nextYear, nextYear, pin, nextYear, nextYear, pin)
                if pins.index(pin) != len(pins)-1:
                    yearReportQuery += " UNION ALL "
                elif pins.index(pin) == len(pins)-1:
                    yearReportQuery += ") TO STDOUT DELIMITER ',' CSV HEADER"
            
            with open(filePath, "w") as file:
                self.cursor.copy_expert(yearReportQuery, file)

    def onAddEmpBtn_Click(self):
        def newPinTxt_LostFocus(newPinTxt):
            if self.adminTk.focus_get != newPinTxt:
                if len(newPinTxt.get()) > 4:
                    newPinTxt.delete(4,END)

        def loadExistingEmp(regEditBtn, newPinTxt, newFNameTxt, newLNameTxt):
            if len(self.listbox.curselection()) != 0:
                regEditBtn.config(text="Register/Update Employee", command=lambda cmd=self:onRegEditBtn_Click(newPinTxt, newFNameTxt, newLNameTxt, 1))
                value = self.listbox.get(self.listbox.curselection()).strip().split()
                self.curPin = re.sub(r'[^\w]', '', value[0])
                self.curFName = value[1]
                self.curLName = value[2]

                newPinTxt.insert(0, self.curPin)
                newFNameTxt.insert(0, self.curFName)
                newLNameTxt.insert(0, self.curLName)
            else:
                regEditBtn.config(text="Register/Update Employee", command=lambda cmd=self:onRegEditBtn_Click(newPinTxt, newFNameTxt, newLNameTxt, 0))

        def onCancelBtn_Click(elements):
            for element in elements:
                element.grid_remove()
            self.adminTk.geometry("725x300")

        def onRegEditBtn_Click(newPinTxt, newFNameTxt, newLNameTxt, upd_flag):
            pin, f_name, l_name = newPinTxt.get(), newFNameTxt.get(), newLNameTxt.get()
            if upd_flag == 0: # adding a new user
                if (pin != '' and f_name != '' and l_name != ''):
                    try:
                        regEmpQuery = "INSERT INTO users (pin, f_name, l_name, role) VALUES (%s, '%s', '%s', 'emp')" % (pin, f_name, l_name)
                        self.cursor.execute(regEmpQuery)
                        self.cnx.commit()
                        self.loadEmployees()
                        tkinter.messagebox.showinfo("Success - Employee Time Tracker", "Employee %s %s added successfully." % (f_name, l_name))
                        newPinTxt.delete(0,END)
                        newFNameTxt.delete(0,END)
                        newLNameTxt.delete(0,END)
                    except (Exception, psycopg2.Error) as error:
                        if (self.cnx):
                            tkinter.messagebox.showerror("Error - Employee Time Tracker", "User with this PIN already exists. Please provide a new PIN.")
                else:
                    tkinter.messagebox.showerror("Error - Employee Time Tracker", "Error adding employee.")

            elif upd_flag == 1: # load user for update/edit
                updtFields = ""
                if (newPinTxt.get() != self.curPin):
                    updtFields += "pin = %s" % newPinTxt.get() if updtFields == "" else " AND pin = %s" % newPinTxt.get()

                if (newFNameTxt.get() != self.curFName):
                    updtFields += "f_name = '%s'" % newFNameTxt.get() if updtFields == "" else " AND f_name = '%s'" % newFNameTxt.get()

                if (newLNameTxt.get() != self.curLName):
                    updtFields += "l_name = '%s'" % newLNameTxt.get() if updtFields == "" else " AND l_name = '%s'" % newLNameTxt.get()

                updtCond = "WHERE pin = %s" % self.curPin
                updtUserQuery = "UPDATE users SET %s %s" % (updtFields, updtCond)
                if updtFields != "":
                    try:
                        self.cursor.execute(updtUserQuery)
                        self.cnx.commit()
                        self.loadEmployees()
                        tkinter.messagebox.showinfo("Success - Employee Time Tracker", "Employee updated successfully.")
                        newPinTxt.delete(0,END)
                        newFNameTxt.delete(0,END)
                        newLNameTxt.delete(0,END)
                    except (Exception, psycopg2.Error) as error:
                        if (self.cnx):
                            print(error)
                else:
                    tkinter.messagebox.showinfo("Message - Employee Time Tracker", "Nothing to update.")

        self.adminTk.geometry("725x500")

        newPinLbl = Label(self.adminTk, text="User PIN:")
        newPinLbl.grid(row=3, column=0, pady=(20,10), sticky="e")
        newPinTxt = Entry(self.adminTk, width=10)
        newPinTxt.grid(row=3, column=1, pady=(20,10), sticky="w")
        newPinTxt.bind("<FocusOut>", newPinTxt_LostFocus(newPinTxt))

        newFNameLbl = Label(self.adminTk, text="First Name:")
        newFNameLbl.grid(row=4, column=0, pady=10, sticky="e")
        newFNameTxt = Entry(self.adminTk, width=15)
        newFNameTxt.grid(row=4, column=1, pady=10, sticky="w")

        newLNameLbl = Label(self.adminTk, text="Last Name:")
        newLNameLbl.grid(row=5, column=0, pady=10, sticky="e")
        newLNameTxt = Entry(self.adminTk, width=15)
        newLNameTxt.grid(row=5, column=1, pady=10, sticky="w")

        regEditBtn = Button(self.adminTk)
        regEditBtn.grid(row=6, column=1, pady=10, ipadx=10, ipady=5, sticky="w")
        loadExistingEmp(regEditBtn, newPinTxt, newFNameTxt, newLNameTxt)

        cancelBtn = Button(self.adminTk, text="Cancel")
        cancelBtn.grid(row=6, column=0, pady=10, ipadx=10, ipady=5, sticky="e")

        elements = [newPinLbl, newPinTxt, newFNameLbl, newFNameTxt, newLNameLbl, newLNameTxt, cancelBtn, regEditBtn]

        cancelBtn.config(command=lambda cmd=self:onCancelBtn_Click(elements))

    def onRemEmpBtn_Click(self):
        if len(self.listbox.curselection()) != 0:
            value = self.listbox.get(self.listbox.curselection()).strip().split()
            remPin = re.sub(r'[^\w]', '', value[0])
            remFName = value[1]
            remLName = value[2]
            confirm = tkinter.messagebox.askyesno("Remove Employee - Employee Time Tracker", "Are you sure you want to remove employee %s %s? Deleting employee will delete all associated time records as well." % (remFName, remLName))
            
            if confirm == TRUE:
                try:
                    remEmpQuery = "DELETE FROM users WHERE pin = %s AND f_name = '%s' AND l_name = '%s'" % (remPin, remFName, remLName)
                    remEmpHoursQuery = "DELETE FROM hours WHERE pin = %s" % remPin
                    self.cursor.execute(remEmpHoursQuery)
                    self.cursor.execute(remEmpQuery)
                    self.cnx.commit()
                    self.loadEmployees()
                    tkinter.messagebox.showinfo("Success - Employee Time Tracker", "Employee %s %s removed successfully." % (remFName, remLName))
                except (Exception, psycopg2.Error) as error:
                    if (self.cnx):
                        tkinter.messagebox.showerror("Error - Employee Time Tracker", "Error removing employee. Please try again.")
        else:
            tkinter.messagebox.showerror("Error - Employee Time Tracker", "No employee selected for removal.")

    def loadEmployees(self):
        self.listbox.delete(0,END)
        getEmpsQuery = "SELECT CONCAT(' ', pin, ': ', f_name, ' ', l_name) AS emp FROM users WHERE role = 'emp' ORDER BY f_name ASC"
        self.cursor.execute(getEmpsQuery)
        allEmps = self.cursor.fetchall()
        for emp in allEmps:
            self.listbox.insert(END, emp[0])

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
        else:
            self.start_time, self.end_time = -1, -1

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
        elif (lastEntry is None):
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

        self.emp.close()
        m = main_win()
        m.main.run()

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

        self.emp.close()
        m = main_win()
        m.main.run()

    def addClockInOutBtns(self, in_out):
        if (in_out == "in"):
            self.clockInBtn.grid(row=1, column=0, columnspan=1, pady=20, ipadx=10, ipady=5)
            self.clockInBtn.configure(command=lambda cmd=self:self.onClockInBtn_Click())
        elif (in_out == "out"):
            self.clockOutBtn.grid(row=1, column=1, columnspan=1, pady=20, ipadx=10, ipady=5)
            self.clockOutBtn.configure(command=lambda cmd=self.start_time:self.onClockOutBtn_Click(self.start_time))