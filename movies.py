# Erik Safford
# Implementing MySQL Database using Python script, Data read from .csv File
# Spring 2019

import sys
import pymysql
import csv
import json


def query1(username, password):
    conn = pymysql.connect(host='localhost', port=3306, user=username, passwd=password, db='mdb', charset='utf8')
    cur = conn.cursor()

    # Find average budget of all movies, print average budget value
    cur.execute("SELECT ROUND(AVG(budget),2) FROM movies")
    output = cur.fetchone()

    print("1 - Average Budget of All Movies:")
    print(str(output).lstrip('(Decimal(\'').rstrip('\'),)'))
    print()
    cur.close()
    conn.close()


def query2(username, password):
    conn = pymysql.connect(host='localhost', port=3306, user=username, passwd=password, db='mdb', charset='utf8')
    cur = conn.cursor()

    # Find only the movies that were produced in the US, print movie title and production company name
    sqlcmd = "SELECT movies.title, production_companies.company_name FROM mdb.movies \
              NATURAL JOIN movie_companies NATURAL JOIN production_companies \
              NATURAL JOIN movie_countries NATURAL JOIN production_countries \
              WHERE country_id = 'US' ORDER BY movie_id LIMIT 5"

    cur.execute(sqlcmd)
    output = cur.fetchall()

    print("2 - Movies produced in the US:")
    for row in output:
        print(str(row))
    print()

    cur.close()
    conn.close()


def query3(username, password):
    conn = pymysql.connect(host='localhost', port=3306, user=username, passwd=password, db='mdb', charset='utf8')
    cur = conn.cursor()

    # Find the top 5 movies that made the most revenue, print movie title and revenue made
    sqlcmd = "SELECT title, revenue FROM movies \
              ORDER BY revenue DESC LIMIT 5"

    cur.execute(sqlcmd)
    output = cur.fetchall()

    print("3 - Top 5 Movie Revenues:")
    for row in output:
        print(str(row))
    print()

    cur.close()
    conn.close()


def query4(username, password):
    conn = pymysql.connect(host='localhost', port=3306, user=username, passwd=password, db='mdb', charset='utf8')
    cur = conn.cursor()

    # Find movies that have both the genre Science Fiction and Mystery, print movie title and genres
    sqlcmd = "SELECT a.title AS Movie_Title, concat(a.name_genre, ', ', b.name_genre) AS genre FROM \
              ( SELECT movie_id, title, name_genre FROM movies \
                NATURAL JOIN movie_genre NATURAL JOIN genre \
                WHERE name_genre = 'Science Fiction') AS a \
              INNER JOIN \
              ( SELECT movie_id, title, name_genre FROM movies \
                NATURAL JOIN movie_genre NATURAL JOIN genre \
                WHERE name_genre = 'Mystery') as b \
              ON a.movie_id = b.movie_id ORDER BY Movie_Title ASC LIMIT 5"

    cur.execute(sqlcmd)
    output = cur.fetchall()

    print("4 - Movies with Both Science Fiction and Mystery Genres:")
    for row in output:
        print(str(row))
    print()

    cur.close()
    conn.close()


def query5(username, password):
    conn = pymysql.connect(host='localhost', port=3306, user=username, passwd=password, db='mdb', charset='utf8')
    cur = conn.cursor()

    # Find the movies that have a popularity greater then the average popularity, print movie title and popularity
    sqlcmd = "SELECT title, popularity from movies \
              WHERE popularity > (SELECT AVG(popularity) FROM movies) \
              ORDER BY popularity DESC LIMIT 5"

    cur.execute(sqlcmd)
    output = cur.fetchall()

    print("5 - Movies more Popular then Average:")
    for row in output:
        print(str(row))
    print()

    cur.close()
    conn.close()


def insert_tables(username, password):
    conn = pymysql.connect(host='localhost', port=3306, user=username, passwd=password, db='mdb', charset='utf8')
    cur = conn.cursor()

    cur.execute("SET FOREIGN_KEY_CHECKS = 0")

    csv_file = csv.DictReader(open("tmdb_5000_movies.csv", encoding='utf8'))

    movie_genre_id = 0
    movie_keyword_id = 0
    movie_companies_id = 0
    movie_country_id = 0
    movie_language_id = 0

    for row in csv_file:  # Read a tuple at a time from the csv file
        # From the tuple...

        # Insert all atomic columns into the 'movies' table
        sqlcmd = "INSERT INTO mdb.movies( movie_id, budget, homepage,\
        original_language, original_title, overview, popularity, release_date, \
        revenue, runtime, status, tagline, title, vote_average, vote_count )\
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        cur.execute(sqlcmd, (row['id'], row['budget'], row['homepage'],
                             row['original_language'], row['original_title'],
                             row['overview'], row['popularity'],
                             row['release_date'], row['revenue'],
                             # If runtime is blank, insert a 0 instead
                             row['runtime'] if row['runtime'] != "" else row['runtime'] == 0,
                             row['status'], row['tagline'],
                             row['title'],
                             row['vote_average'], row['vote_count']))

# ====================================================================================================================

        # Take the multiple attributes in genre column and load string into json_genre as json
        json_genre = json.loads(row['genres'])

        # For the number of genre entries in json
        for i in range(0, len(json_genre)):
            # Insert all genre id's and name's into 'genre' table
            id = json_genre[i]['id']      # Grab id of i'th genre in json
            name = json_genre[i]['name']  # Grab name of i'th genre in json
            sqlcmd = "REPLACE INTO mdb.genre(genre_id, name_genre) VALUES (%s, %s)"  # REPLACE so no duplicate genres
            cur.execute(sqlcmd, (id, name))

            # Insert unique movie_genre_id's (relationship) for each genre a movie has into 'movie_genre' table
            sqlcmd = "INSERT INTO mdb.movie_genre(movie_genre_id, movie_id, genre_id) VALUES (%s, %s, %s)"
            cur.execute(sqlcmd, (movie_genre_id, row['id'], id))
            movie_genre_id += 1

# ====================================================================================================================

        # Take the multiple attributes in keywords column and load string into json_keyword as json
        json_keyword = json.loads(row['keywords'])

        # For the number of keyword entries in json
        for i in range(0, len(json_keyword)):
            # Insert all keyword id's and name's into 'keyword' table
            id = json_keyword[i]['id']    # Grab id of i'th keyword in json
            name = json_keyword[i]['name']  # Grab name of i'th keyword in json
            sqlcmd = "REPLACE INTO mdb.keyword(keyword_id, keyword_name) VALUES (%s, %s)"  # REPLACE so no duplicates
            cur.execute(sqlcmd, (id, name))

            # Insert unique movie_keyword_id's (relationship) for each keyword a movie has into 'movie_keyword' table
            sqlcmd = "INSERT INTO mdb.movie_keyword(movie_keyword_id, movie_id, keyword_id) VALUES (%s, %s, %s)"
            cur.execute(sqlcmd, (movie_keyword_id, row['id'], id))
            movie_keyword_id += 1

# ====================================================================================================================

        # Take the multiple attributes in production_companies column and load string into json_production_company
        json_production_company = json.loads(row['production_companies'])

        # For the number of production companies entries in json
        for i in range(0, len(json_production_company)):
            # Insert all production company id's and name's into 'production_companies' table
            id = json_production_company[i]['id']      # Grab id of i'th production company in json
            name = json_production_company[i]['name']  # Grab name of i'th production company in json
            sqlcmd = "REPLACE INTO mdb.production_companies(company_id, company_name) VALUES (%s, %s)"
            cur.execute(sqlcmd, (id, name))

            # Insert unique movie_companies_id's (relationship) for each company a movie has into 'movie_companies'
            sqlcmd = "INSERT INTO mdb.movie_companies(movie_companies_id, movie_id, company_id) VALUES (%s, %s, %s)"
            cur.execute(sqlcmd, (movie_companies_id, row['id'], id))
            movie_companies_id += 1

# ====================================================================================================================

        # Take the multiple attributes in production_countries column and load string into json_production_country
        json_production_country = json.loads(row['production_countries'])

        # For the number of production countries entries in json
        for i in range(0, len(json_production_country)):
            # Insert all production country id's and name's into 'production_countries' table
            id = json_production_country[i]['iso_3166_1']  # Grab id of i'th production country iso in json
            name = json_production_country[i]['name']  # Grab name of i'th production country in json
            sqlcmd = "REPLACE INTO mdb.production_countries(country_id, country_name) VALUES (%s, %s)"
            cur.execute(sqlcmd, (id, name))

            # Insert unique movie_country_id's (relationship) for each country a movie has into 'movie_countries'
            sqlcmd = "INSERT INTO mdb.movie_countries(movie_country_id, movie_id, country_id) VALUES (%s, %s, %s)"
            cur.execute(sqlcmd, (movie_country_id, row['id'], id))
            movie_country_id += 1

# ====================================================================================================================

        # Take the multiple attributes in spoken_languages column and load string into json_spoken_language
        json_spoken_language = json.loads(row['spoken_languages'])

        # For the number of spoken language entries in json
        for i in range(0, len(json_spoken_language)):
            # Insert all spoken language id's and name's into 'spoken_languages' table
            id = json_spoken_language[i]['iso_639_1']  # Grab id of i'th spoken language iso in json
            name = json_spoken_language[i]['name']  # Grab name of i'th spoken language in json
            sqlcmd = "REPLACE INTO mdb.spoken_languages(language_id, language_name) VALUES (%s, %s)"
            cur.execute(sqlcmd, (id, name))

            # Insert unique movie_lang_id's (relationship) for each language a movie has into 'movie_languages'
            sqlcmd = "INSERT INTO mdb.movie_languages(movie_lang_id, movie_id, language_id) VALUES (%s, %s, %s)"
            cur.execute(sqlcmd, (movie_language_id, row['id'], id))
            movie_language_id += 1

# =====================================================================================================================

    conn.commit()
    cur.execute("SET FOREIGN_KEY_CHECKS = 1")
    cur.close()
    conn.close()


def create_tables(username, password):
    conn = pymysql.connect(host='localhost', port=3306, user=username, passwd=password, db='mdb', charset='utf8')
    cur = conn.cursor()

    # Drop tables if they already exist
    cur.execute("DROP TABLE IF EXISTS mdb.movie_genre")
    cur.execute("DROP TABLE IF EXISTS mdb.genre")
    cur.execute("DROP TABLE IF EXISTS mdb.movie_keyword")
    cur.execute("DROP TABLE IF EXISTS mdb.keyword")
    cur.execute("DROP TABLE IF EXISTS mdb.movie_companies")
    cur.execute("DROP TABLE IF EXISTS mdb.production_companies")
    cur.execute("DROP TABLE IF EXISTS mdb.movie_countries")
    cur.execute("DROP TABLE IF EXISTS mdb.production_countries")
    cur.execute("DROP TABLE IF EXISTS mdb.movie_languages")
    cur.execute("DROP TABLE IF EXISTS mdb.spoken_languages")
    cur.execute("DROP TABLE IF EXISTS mdb.movies")

    # Create 'movies' table
    cur.execute("CREATE TABLE mdb.movies("
                "movie_id INT,"
                "budget INT,"
                "homepage VARCHAR(1000),"
                "original_language VARCHAR(100),"
                "original_title VARCHAR(100),"
                "overview VARCHAR(2000),"
                "popularity FLOAT,"
                "release_date VARCHAR(100),"
                "revenue BIGINT,"
                "runtime INT,"
                "status VARCHAR(100),"
                "tagline VARCHAR(2000),"
                "title VARCHAR(100),"
                "vote_average FLOAT,"
                "vote_count INT,"
                "PRIMARY KEY(movie_id)"
                ")"
                )

    # Create 'genre' table
    cur.execute("CREATE TABLE mdb.genre("
                "genre_id INT,"
                "name_genre VARCHAR(100),"
                "PRIMARY KEY(genre_id)"
                ")"
                )

    # Create 'movie_genre' table
    cur.execute("CREATE TABLE mdb.movie_genre("
                "movie_genre_id INT,"
                "movie_id INT,"
                "genre_id INT,"
                "PRIMARY KEY(movie_genre_id),"
                "FOREIGN KEY(movie_id) REFERENCES mdb.movies(movie_id),"
                "FOREIGN KEY(genre_id) REFERENCES mdb.genre(genre_id)"
                ")"
                )

    # Create 'keyword' table
    cur.execute("CREATE TABLE mdb.keyword("
                "keyword_id INT,"
                "keyword_name VARCHAR(100),"
                "PRIMARY KEY(keyword_id)"
                ")"
                )

    # Create 'movie_keyword' table
    cur.execute("CREATE TABLE mdb.movie_keyword("
                "movie_keyword_id INT,"
                "movie_id INT,"
                "keyword_id INT,"
                "PRIMARY KEY(movie_keyword_id),"
                "FOREIGN KEY(movie_id) REFERENCES mdb.movies(movie_id),"
                "FOREIGN KEY(keyword_id) REFERENCES mdb.keyword(keyword_id)"
                ")"
                )

    # Create 'production_companies' table
    cur.execute("CREATE TABLE mdb.production_companies("
                "company_id INT,"
                "company_name VARCHAR(100),"
                "PRIMARY KEY(company_id)"
                ")"
                )

    # Create 'movie_companies' table
    cur.execute("CREATE TABLE mdb.movie_companies("
                "movie_companies_id INT,"
                "movie_id INT,"
                "company_id INT,"
                "PRIMARY KEY(movie_companies_id),"
                "FOREIGN KEY(movie_id) REFERENCES mdb.movies(movie_id),"
                "FOREIGN KEY(company_id) REFERENCES mdb.production_companies(company_id)"
                ")"
                )

    # Create 'production_countries' table
    cur.execute("CREATE TABLE mdb.production_countries("
                "country_id VARCHAR(10),"
                "country_name VARCHAR(100),"
                "PRIMARY KEY(country_id)"
                ")"
                )

    # Create 'movie_countries' table
    cur.execute("CREATE TABLE mdb.movie_countries("
                "movie_country_id INT,"
                "movie_id INT,"
                "country_id VARCHAR(10),"
                "PRIMARY KEY(movie_country_id),"
                "FOREIGN KEY(movie_id) REFERENCES mdb.movies(movie_id),"
                "FOREIGN KEY(country_id) REFERENCES mdb.production_countries(country_id)"
                ")"
                )

    # Create 'spoken_languages' table
    cur.execute("CREATE TABLE mdb.spoken_languages("
                "language_id VARCHAR(10),"
                "language_name VARCHAR(100),"
                "PRIMARY KEY(language_id)"
                ")"
                )

    # Create 'movie_languages' table
    cur.execute("CREATE TABLE mdb.movie_languages("
                "movie_lang_id INT,"
                "movie_id INT,"
                "language_id VARCHAR(10),"
                "PRIMARY KEY(movie_lang_id),"
                "FOREIGN KEY(movie_id) REFERENCES mdb.movies(movie_id),"
                "FOREIGN KEY(language_id) REFERENCES mdb.spoken_languages(language_id)"
                ")"
                )

    # conn.commit()  # Runs faster without this commit
    cur.close()
    conn.close()


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Incorrect command line formatting, should be: python movies.py username password <optional query 1-5>")
        sys.exit()

    username = sys.argv[1]
    password = sys.argv[2]

    create_tables(username, password)
    insert_tables(username, password)

    print("Database username: " + username)
    print("Database password: " + password)
    print("Database schema should be 'mdb'")
    print()

    if len(sys.argv) == 3:
        query1(username, password)
        query2(username, password)
        query3(username, password)
        query4(username, password)
        query5(username, password)
    elif len(sys.argv) == 4:
        if sys.argv[3] == '1':
            query1(username, password)
        elif sys.argv[3] == '2':
            query2(username, password)
        elif sys.argv[3] == '3':
            query3(username, password)
        elif sys.argv[3] == '4':
            query4(username, password)
        elif sys.argv[3] == '5':
            query5(username, password)


main()
