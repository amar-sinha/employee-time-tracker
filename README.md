# Employee Time Tracker Application
## A PostgreSQL-Python Integrated Implementation

_<h4>A Python program implemented to track employees' time records and export time report records.</h4>_

### <u>Goal</u>
To develop an employee time tracking software to apply knowledge of integrated PostgreSQL database transactions. The program will store and record timesheet data and users (admins and employees). The database has two tables to store the data, as described in the _PostgreSQL & Database Specifications_ section below.

### <u>Implementation</u>
The employee time tracking software is implemented with a Python program and PostgreSQL database integration. The database is remotely hosted on the Heroku Cloud Platform. The program utilizes the psycopg2 Python package to provide the communication between Python and PostgreSQL. The Python program provides a graphical user-interface (GUI) implemented using the tkinter GUI toolkit package.

### <u>Package Installation</u>
Install tkinter

    $ pip install tkinter

Install Heroku (macOs)

    $ brew tap heroku/brew && brew install heroku

### <u>PostgreSQL & Database Specifications</u>
Create an app on the Heroku Cloud Platform service (<a href="https://www.heroku.com/">https://www.heroku.com/</a>). Configure the app with the Heroku Postgres add-on (<a href="https://elements.heroku.com/addons/heroku-postgresql">https://elements.heroku.com/addons/heroku-postgresql</a>) attached as the app's database.

To ensure the program executes with no errors, make sure that the PostgreSQL database specifications in the Python program are correct. These specifications can be found at the top of the program, and look as such:

    PROC = subprocess.Popen('heroku config:get DATABASE_URL -a project-name-here', stdout=subprocess.PIPE, shell=True)
    DB_URL = PROC.stdout.read().decode('utf-8').strip() + '?sslmode=require'

Since the database URL is dynamic and can change regularly, the use of the suprocess.Popen method call allows the program to grab the most current database URL to ensure proper connection to the database.

Furthermore, the database implemented for use with this software consists of two tables, one for storing users and a second for storing daily time report recordings. A visual representation is provided below:

<img src="https://github.com/amar-sinha/employee-time-tracker/blob/master/images/db_structure.png?raw=true" alt="db_structure" width="500"/>

### <u>Program Specifications</u>
* _Main Panel_ - 

* _Admin Panel_ - 

* _Add/Remove Employee Panels_ - 

* _Employee Panel_ -

