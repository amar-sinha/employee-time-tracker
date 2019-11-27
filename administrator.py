from tkinter import *
import tkinter.messagebox, time, datetime
from tkWindow import tkWindow

class admin_win():
    def __init__(self, conn, cur, pin, f_name, l_name):
        self.cnx = conn
        self.cursor = cur
        self.admin = tkWindow()
        self.adminTk = self.admin.root
        self.adminTk.title("Admin - Employee Time Tracker")
        self.adminTk.geometry("700x300")
        self.pin = pin

        self.adminLbl = Label(self.adminTk)
        self.adminLbl.grid(row=0, column=1, ipady=5)
        self.adminLbl.config(text = "Administrator: %s, %s" % (l_name, f_name), font=("", 24))

        self.listbox = Listbox(self.adminTk, width=40)
        self.listbox.grid(row=1, column=1, pady=15)

        self.cursor.execute("BEGIN")
        self.loadEmployees()

        self.addEmpBtn = Button(self.adminTk, text="Add Employee", command=lambda cmd=self:self.onAddEmpBtn_Click())
        self.addEmpBtn.grid(row=2, column=0, padx=20, ipadx=10, ipady=5)

        self.rmEmpBtm = Button(self.adminTk, text="Remove Employee")
        self.rmEmpBtm.grid(row=2, column=1, padx=20, ipadx=10, ipady=5)

        self.expDataBtn = Button(self.adminTk, text="Export Timesheet")
        self.expDataBtn.grid(row=2, column=2, padx=20, ipadx=10, ipady=5)

    def onAddEmpBtn_Click(self):
        if len(self.listbox.curselection()) != 0:
            value = self.listbox.get(self.listbox.curselection())
            print(value)
        self.adminTk.geometry("700x500")

        newPinLbl = Label(self.adminTk, text="User PIN:")
        newPinLbl.grid(row=3, column=0, pady=(20,10), sticky="e")
        newPinTxt = Entry(self.adminTk, width=10)
        newPinTxt.grid(row=3, column=1, pady=(20,10), sticky="w")

        newFNameLbl = Label(self.adminTk, text="First Name:")
        newFNameLbl.grid(row=4, column=0, pady=10, sticky="e")
        newFNameTxt = Entry(self.adminTk, width=15)
        newFNameTxt.grid(row=4, column=1, pady=10, sticky="w")

        newLNameLbl = Label(self.adminTk, text="Last Name:")
        newLNameLbl.grid(row=5, column=0, pady=10, sticky="e")
        newLNameTxt = Entry(self.adminTk, width=15)
        newLNameTxt.grid(row=5, column=1, pady=10, sticky="w")

        registerBtn = Button(self.adminTk, text="Register Employee", command=lambda cmd=self:self.onRegisterBtn_Click(newPinTxt.get(), newFNameTxt.get(), newLNameTxt.get()))
        registerBtn.grid(row=6, column=1, pady=10, ipadx=10, ipady=5, sticky="w")

    def onRegisterBtn_Click(self, pin, f_name, l_name):
        if (pin != '' and f_name != '' and l_name != ''):
            regEmpQuery = "INSERT INTO users (pin, f_name, l_name, role) VALUES (%s, '%s', '%s', 'emp')" % (pin, f_name, l_name)
            self.cursor.execute(regEmpQuery)
            self.cnx.commit()
            self.loadEmployees()
            tkinter.messagebox.showinfo("Success - Employee Time Tracker", "Employee %s %s added successfully." % (f_name, l_name))
        else:
            tkinter.messagebox.showerror("Error - Employee Time Tracker", "Error adding employee.")

    def loadEmployees(self):
        self.listbox.delete(0,END)
        getEmpsQuery = "SELECT CONCAT(f_name, ' ', l_name) AS name FROM users WHERE role = 'emp'"
        self.cursor.execute(getEmpsQuery)
        allEmps = self.cursor.fetchall()
        for name in allEmps:
            self.listbox.insert(END, " " + name[0])