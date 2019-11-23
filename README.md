# Employee Time Tracker Application
## A MySQL-Python Integrated Implementation

_<h4>A Python program implemented to track employees' time records and export monthly time sheets.</h4>_

### <u>Goal</u>
To develop an employee time tracking software to apply knowledge of integrated MySQL database transactions. The program will store and record timesheet data and users (admins and employees). The database has two tables to store the data, as described in the _MySQL & Database Specifications_ section below.

### <u>Implementation</u>


### <u>Package Installation</u>
Install mysql-connector

    $ pip install mysql-connector-python

### <u>MySQL & Database Specifications</u>
Download the open source MySQL Community Server here: <a href="https://dev.mysql.com/downloads/mysql/">https://dev.mysql.com/downloads/mysql/</a>

To ensure the program executes with no errors, make sure that the MySQL user specifications (user name, password, host, database name) in the Python program are correct. These specifications can be found at the top of the program, and look as such:

    cnx = mysql.connector.connect(user='root', password='pwd', host='localhost', database='db_name')

Furthermore, the database implemented for use with this software consists of two tables, one for storing users and a second for storing daily time report recordings. A visual representation is provided below:

<img src="https://github.com/amar-sinha/employee-time-tracker/blob/master/images/db_structure.png?raw=true" alt="db_structure" width="500"/>

### <u>Program Specifications</u>
* _Main Panel_ - 

* _Admin Panel_ - 

* _Add/Remove Employee Panels_ - 

* _Employee Panel_ -

