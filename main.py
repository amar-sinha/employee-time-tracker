from tkinter import *
import mysql.connector

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


def code(value):
    # inform function to use external/global variable
    global pin

    if value == '*':
        # remove last number from `pin`
        pin = pin[:-1]
        e.config(text = str(pin))

    elif len(pin) <= 4:
        if value == '#':
            # check pin
            grabUserQuery = "SELECT * FROM employee_time_tracker.users WHERE pin = " + str(pin)
            cursor.execute(grabUserQuery)
            user = cursor.fetchone()
            if user is not None:
                printstr = ""
                for val in user:
                    printstr += str(val) + " "
                print(printstr)
                # main_window.quit()
            else:
                err_msg()
            pin = ""
            e.config(text=str(pin))

        else:
            # add number to pin
            pin += value
            e.config(text = str(pin))

def err_msg():
    error = Tk()

    error.resizable(0, 0) # prevent window resizing

    windowWidth = error.winfo_reqwidth()
    windowHeight = error.winfo_reqheight()

    # get horizontal and vertical screen sizes
    positionHorizontal = int(main_window.winfo_screenwidth()/2 - windowWidth/2)
    positionVertical = int(main_window.winfo_screenheight()/2 - windowHeight/2)

    # position window in center of the screen
    main_window.geometry("+{}+{}".format(positionHorizontal, positionVertical))

    error.title("Error - Employee Time Tracker")

    e = Label(error)
    e.config(text="ERROR: Invalid pin entered. Please try again.")
    e.grid(row=0, column=0, columnspan=3, ipady=5)
    b = Button(error, text="Close", command=lambda val=error:error.destroy())
    b.grid(row=1, column=0, ipadx=20, ipady=5)

if __name__ == "__main__":
    main_window = Tk()

    main_window.resizable(0, 0) # prevent window resizing

    windowWidth = main_window.winfo_reqwidth()
    windowHeight = main_window.winfo_reqheight()

    # get horizontal and vertical screen sizes
    positionHorizontal = int(main_window.winfo_screenwidth()/2 - windowWidth/2)
    positionVertical = int(main_window.winfo_screenheight()/2 - windowHeight/2)

    # position window in center of the screen
    main_window.geometry("+{}+{}".format(positionHorizontal, positionVertical))

    main_window.title("Employee Time Tracker")

    # set the keypad layout
    keys = [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9'],
        ['*', '0', '#'],
    ]

    # create global variable for pin
    pin = ''

    # place to display pin
    e = Label(main_window)
    e.grid(row=0, column=0, columnspan=3, ipady=5)

    # create buttons using keypad layout
    for y, row in enumerate(keys, 1):
        for x, key in enumerate(row):
            b = Button(main_window, text=key, command=lambda val=key:code(val))
            b.grid(row=y, column=x, ipadx=20, ipady=5)

    main_window.mainloop()