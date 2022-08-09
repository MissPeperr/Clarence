""" 
File to interact with the anime.db with 
\n Run 'python anime.py' to create the db
"""
import sqlite3
from sqlite3 import Error
from db_config import db_file


def create_table(conn: sqlite3.Connection, create_table_sql: str):
    """ Create a table from the create_table_sql statement
    \nArgs:
        conn (Connection): Connection object
        create_table_sql (str): a CREATE TABLE statement
    """
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    # make the table sql
    media_type_sql =    '''CREATE TABLE IF NOT EXISTS media_type (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                name text NOT NULL
                            );'''
    media_sql =         '''CREATE TABLE IF NOT EXISTS media (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                name text NOT NULL,
                                type_id integer NOT NULL,
                                FOREIGN KEY (type_id) REFERENCES media_type (id)
                            );'''
    recommended_by_sql = '''CREATE TABLE IF NOT EXISTS recommended_by (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                discord_id text NOT NULL,
                                media_id integer NOT NULL,
                                FOREIGN KEY (media_id) REFERENCES media_type (id)
                            );'''
    # create the db connection                        
    with sqlite3.connect(db_file) as conn:
    
        # create tables
        if conn is not None:
            create_table(conn, media_type_sql)
            create_table(conn, media_sql)
            create_table(conn, recommended_by_sql)
            
            c = conn.cursor()
            c.execute('''INSERT INTO media_type (name) VALUES('Test Type')''')
            c.execute('''INSERT INTO media_type (name) VALUES('Anime')''')
            c.execute('''INSERT INTO media_type (name) VALUES('Manga')''')
            c.execute('''INSERT INTO media (name, type_id) VALUES('Test Anime', 1)''')
            c.execute('''INSERT INTO media (name, type_id) VALUES('Test Manga', 1)''')
            c.execute('''INSERT INTO recommended_by (discord_id, media_id) VALUES(125464834379743232, 1)''')
        else:
            print("Error! Cannot create the database connection.")

        conn.commit()

if __name__ == '__main__':
    main()