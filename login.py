from tkinter import *
import tkinter.messagebox, time, datetime
import os, psycopg2, subprocess
from employee import emp_win
from administrator import admin_win
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