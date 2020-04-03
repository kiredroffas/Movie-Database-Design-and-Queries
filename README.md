# Movie Database Design and Queries
* This program was implemented and ran through the MySQL Workbench and PyCharm IDE's.
* Before running: MySQL Workbench and server must be up and running, a database schema must be named 'mdb' in Workbench (python code references 'mdb' as the database).
* In PyCharm run command 'pip install pymysql' to install pymysql, also install csv plugin if necessary to read from csv file.
* To run program: 
    * In PyCharm terminal, enter 'python movies.py username password (optional query #)' where username is the username of your MySQL Workbench server (should be 'root') and password is the password of your MySQL Workbench Server.
    * If no optional query # is entered, all 5 queries will be printed, if a number 1-5 is entered the corresponding query will be printed.
* The create_tables() and insert_tables() functions take around 7 minutes to complete on my computer (due to the large size of the implemented csv dataset), however this will most likely be faster on a newer computer.
* After running create_tables() and insert_tables() once and data is properly inserted into database, it's worthwhile commenting out these functions so the queries run nearly instantly.
* Queries ran on the inserted database are:
    * Average Budget of All Movies, output includes just the average budget value
    * Movies Produced in the US, output includes the movie title and the production company name
    * Top Five Movie Revenues, output includes the movie title and how much revenue it brought in
    * Movies With Both Science Fiction and Mystery Genre, output includes the movie title and genres
    * Movies More Popular Than Average, output includes the movie title and their popularity
# Screenshots
## MySQL Workbench Running With Database Schema 'mdb'
![Alt text](/screenshots/sc1.jpg?raw=true "sc1")
## Login With Root And Password
![Alt text](/screenshots/sc2.jpg?raw=true "sc2")
## Database Empty Initially
![Alt text](/screenshots/sc3.jpg?raw=true "sc3")
## Run Python Script To Create And Insert Tables/Data
![Alt text](/screenshots/sc4.jpg?raw=true "sc4")
## Once Data Is Inserted Into DB, All Queries Will Be Ran
![Alt text](/screenshots/sc5.jpg?raw=true "sc5")
## All CSV Data Is Now Properly Inserted In 2NF
![Alt text](/screenshots/sc6.jpg?raw=true "sc6")
## Comment Out Creation/Insertion Of Tables And Specify Single Query
![Alt text](/screenshots/sc7.jpg?raw=true "sc7")