This program was implemented and ran through the MySQL Workbench and PyCharm IDE's.

Before running: MySQL Workbench and server must be up and running, a database schema 
must be named 'mdb' in Workbench (python code references 'mdb' as the database).
				
In PyCharm run command 'pip install pymysql' to install pymysql, also install csv 
plugin if necessary to read from csv file.
				
To run program: 

In PyCharm terminal, enter 'python movies.py username password <optional query #>' 
where username is the username of your MySQL Workbench server (should be 'root') 
and password is the password of your MySQL Workbench Server.

If no optional query # is entered, all 5 queries will be printed, if a number 1-5 
is entered the corresponding query will be printed.

The create_tables() and insert_tables() functions take around 7 minutes to complete 
on my computer, however this will most likely be faster on a newer computer.

After running create_tables() and insert_tables() once and data is properly inserted 
into database, it's worthwhile commenting out these functions so the queries run 
nearly instantly.

