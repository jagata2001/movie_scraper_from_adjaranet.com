import os
import sqlite3 as sql

dbfile = "information.db"

if dbfile not in os.listdir():
    conn = sql.connect(dbfile)
    cnx = conn.cursor()
    cnx.execute("""CREATE TABLE actors (

                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                image TEXT,
                actor_id INTEGER,
                name_tag TEXT,
                wp_image TEXT,
                wp_id TEXT,
                inserted INTEGER DEFAULT 0,
                UNIQUE(actor_id)

                )""")

    cnx.execute("""CREATE TABLE directors (

                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                image TEXT,
                director_id INTEGER,
                name_tag TEXT,
                wp_image TEXT,
                wp_id TEXT,
                inserted INTEGER DEFAULT 0,
                UNIQUE(director_id)

                )""")
    cnx.execute("""CREATE TABLE films (

                id INTEGER PRIMARY KEY AUTOINCREMENT,
                film_id INTEGER,
                film_adjaraid INTEGER,
                posted INTEGER DEFAULT 0,
                UNIQUE(film_id,film_adjaraid)

                )""")
    cnx.execute("""CREATE TABLE genres (

                id INTEGER PRIMARY KEY AUTOINCREMENT,
                genre_id INTEGER,
                genre INTEGER,
                wp_id TEXT,
                inserted INTEGER DEFAULT 0,
                UNIQUE(genre_id)

                )""")
    conn.commit()
    conn.close()


class Database:
    def __init__(self,dbfile):
        self.conn = sql.connect(dbfile)

    def insert_films(self,data):
        cnx = self.conn.cursor()
        cnx.executemany("INSERT INTO films (film_id,film_adjaraid) VALUES (?,?) ON CONFLICT DO NOTHING;",data)
        self.conn.commit()
        return cnx.rowcount

    def films_to_parse(self):
        cnx = self.conn.cursor()
        cnx.execute("SELECT * FROM films where posted = 0;")
        data = cnx.fetchall()
        return data

    def get_data(self):
        cnx = self.conn.cursor()
        cnx.execute("SELECT * FROM actors;")
        data = cnx.fetchall()
        print(len(data))

    def insert_actor(self,data):
        cnx = self.conn.cursor()
        cnx.executemany(f"INSERT INTO actors (actor_id,name,image) VALUES (?,?,?) ON CONFLICT DO NOTHING;",data)
        self.conn.commit()
        return cnx.rowcount

    def insert_director(self,data):
        cnx = self.conn.cursor()
        cnx.executemany(f"INSERT INTO directors (director_id,name,image) VALUES (?,?,?) ON CONFLICT DO NOTHING;",data)
        self.conn.commit()
        return cnx.rowcount

    def insert_genres(self,data):
        cnx = self.conn.cursor()
        cnx.executemany(f"INSERT INTO genres (genre_id,genre) VALUES (?,?) ON CONFLICT DO NOTHING;",data)
        self.conn.commit()
        return cnx.rowcount

if __name__ == "__main__":
    conn = sql.connect(dbfile)
    cnx = conn.cursor()
    cnx.execute("SELECT * FROM actors;")
    data = cnx.fetchall()
    print(len(data))


    for each in data:
        print(each)
