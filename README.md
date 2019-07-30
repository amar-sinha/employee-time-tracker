# Employee Time Tracker Application
## A MySQL-Python Integrated Implementation

_<h4>A Python program implemented to track employees' time records and export monthly time sheets.</h4>_

### <u>Goal</u>


### <u>Implementation</u>


### <u>Package Installation</u>
Install mysql-connector

    $ pip install mysql-connector-python

Install wxpython

    $ pip install wxPython

### <u>MySQL & Database Specifications</u>
Download the open source MySQL Community Server here: <a href="https://dev.mysql.com/downloads/mysql/">https://dev.mysql.com/downloads/mysql/</a>

To ensure the program executes with no errors, make sure that the MySQL user specifications (user name, password, host, database name) in the Python program are correct. These specifications can be found at the top of the program, and look as such:

    cnx = mysql.connector.connect(user='root', password='pwd', host='localhost', database='db_name')

Furthermore, the database implemented for use with this software consists of two tables, one for storing users and a second for storing daily time report recordings. A visual representation is provided below:

### <u>Program Specifications<u>


