from tkinter import *
import tkinter.messagebox, tkinter.filedialog
import re, time, datetime, psycopg2
from tkWindow import tkWindow

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
        self.rmEmpBtm.grid(row=2, column=1, padx=20, ipadx=10, ipady=5)

        self.expDataBtn = Button(self.adminTk, text="Export Timesheet", command=lambda cmd=self:self.onExpDataBtn_Click())
        self.expDataBtn.grid(row=2, column=2, padx=20, ipadx=10, ipady=5)

    def onExpDataBtn_Click(self):
        if len(self.listbox.curselection()) != 0:
            value = self.listbox.get(self.listbox.curselection()).strip().split()
            curPin = re.sub(r'[^\w]', '', value[0])
        filePath = tkinter.filedialog.askdirectory()
        filePath += '/emp_hours.csv'
        print(filePath)
        exportQuery = "COPY (SELECT hours.pin, users.f_name, users.l_name, hours.start_time, hours.end_time, hours.hours FROM hours JOIN users ON hours.pin = users.pin WHERE users.pin = %s) TO STDOUT DELIMITER ',' CSV HEADER" % curPin
        with open(filePath, "w") as file:
            self.cursor.copy_expert(exportQuery, file)

    def onAddEmpBtn_Click(self):
        self.adminTk.geometry("725x500")

        self.newPinLbl = Label(self.adminTk, text="User PIN:")
        self.newPinLbl.grid(row=3, column=0, pady=(20,10), sticky="e")
        self.newPinTxt = Entry(self.adminTk, width=10)
        self.newPinTxt.grid(row=3, column=1, pady=(20,10), sticky="w")
        self.newPinTxt.bind("<FocusOut>", self.newPinTxt_LostFocus)

        self.newFNameLbl = Label(self.adminTk, text="First Name:")
        self.newFNameLbl.grid(row=4, column=0, pady=10, sticky="e")
        self.newFNameTxt = Entry(self.adminTk, width=15)
        self.newFNameTxt.grid(row=4, column=1, pady=10, sticky="w")

        self.newLNameLbl = Label(self.adminTk, text="Last Name:")
        self.newLNameLbl.grid(row=5, column=0, pady=10, sticky="e")
        self.newLNameTxt = Entry(self.adminTk, width=15)
        self.newLNameTxt.grid(row=5, column=1, pady=10, sticky="w")

        if len(self.listbox.curselection()) != 0:
            self.loadExistingEmp()
            self.regEditBtn = Button(self.adminTk, text="Register/Update Employee", command=lambda cmd=self:self.onRegEditBtn_Click(self.newPinTxt.get(), self.newFNameTxt.get(), self.newLNameTxt.get(), 1))
        else:
            self.regEditBtn = Button(self.adminTk, text="Register/Update Employee", command=lambda cmd=self:self.onRegEditBtn_Click(self.newPinTxt.get(), self.newFNameTxt.get(), self.newLNameTxt.get(), 0))

        self.regEditBtn.grid(row=6, column=1, pady=10, ipadx=10, ipady=5, sticky="w")

        self.cancelBtn = Button(self.adminTk, text="Cancel", command=lambda cmd=self:self.onCancelBtn_Click())
        self.cancelBtn.grid(row=6, column=0, pady=10, ipadx=10, ipady=5, sticky="e")

    def onCancelBtn_Click(self):
        toRemove = [self.newPinLbl, self.newPinTxt, self.newFNameLbl, self.newFNameTxt, self.newLNameLbl, self.newLNameTxt, self.cancelBtn, self.regEditBtn]
        for element in toRemove:
            element.grid_remove()
        self.adminTk.geometry("725x300")

    def loadExistingEmp(self):
            value = self.listbox.get(self.listbox.curselection()).strip().split()
            self.curPin = re.sub(r'[^\w]', '', value[0])
            self.curFName = value[1]
            self.curLName = value[2]

            self.newPinTxt.insert(0, self.curPin)
            self.newFNameTxt.insert(0, self.curFName)
            self.newLNameTxt.insert(0, self.curLName)

    def onRegEditBtn_Click(self, pin, f_name, l_name, upd_flag):
        if upd_flag == 0: # adding a new user
            if (pin != '' and f_name != '' and l_name != ''):
                try:
                    regEmpQuery = "INSERT INTO users (pin, f_name, l_name, role) VALUES (%s, '%s', '%s', 'emp')" % (pin, f_name, l_name)
                    self.cursor.execute(regEmpQuery)
                    self.cnx.commit()
                    self.loadEmployees()
                    tkinter.messagebox.showinfo("Success - Employee Time Tracker", "Employee %s %s added successfully." % (f_name, l_name))
                    self.newPinTxt.delete(0,END)
                    self.newFNameTxt.delete(0,END)
                    self.newLNameTxt.delete(0,END)
                except (Exception, psycopg2.Error) as error:
                    if (self.cnx):
                        tkinter.messagebox.showerror("Error - Employee Time Tracker", "User with this PIN already exists. Please provide a new PIN.")
            else:
                tkinter.messagebox.showerror("Error - Employee Time Tracker", "Error adding employee.")

        elif upd_flag == 1: # load user for update/edit
            updtFields = ""
            if (self.newPinTxt.get() != self.curPin):
                updtFields += "pin = %s" % self.newPinTxt.get() if updtFields == "" else " AND pin = %s" % self.newPinTxt.get()

            if (self.newFNameTxt.get() != self.curFName):
                updtFields += "f_name = '%s'" % self.newFNameTxt.get() if updtFields == "" else " AND f_name = '%s'" % self.newFNameTxt.get()

            if (self.newLNameTxt.get() != self.curLName):
                updtFields += "l_name = '%s'" % self.newLNameTxt.get() if updtFields == "" else " AND l_name = '%s'" % self.newLNameTxt.get()

            updtCond = "WHERE pin = %s" % self.curPin
            updtUserQuery = "UPDATE users SET %s %s" % (updtFields, updtCond)
            if updtFields == "":
                try:
                    self.cursor.execute(updtUserQuery)
                    self.cnx.commit()
                    self.loadEmployees()
                    tkinter.messagebox.showinfo("Success - Employee Time Tracker", "Employee updated successfully.")
                    self.newPinTxt.delete(0,END)
                    self.newFNameTxt.delete(0,END)
                    self.newLNameTxt.delete(0,END)
                except (Exception, psycopg2.Error) as error:
                    if (self.cnx):
                        print(error)
            else:
                tkinter.messagebox.showinfo("Message - Employee Time Tracker", "Nothing to update.")

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
    
    def newPinTxt_LostFocus(self, event):
        if self.adminTk.focus_get != self.newPinTxt:
            if len(self.newPinTxt.get()) > 4:
                self.newPinTxt.delete(4,END)