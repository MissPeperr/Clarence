import sqlite3
from sqlite3 import Error
from anime_database import db_file

class MediaType():
    def __init__(self, id, name):
        self.id = id
        self.name = name


def get_all():
    with sqlite3.connect(db_file) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        try:
            cur.execute("""
                SELECT
                    id,
                    name
                FROM media_type
            """)
            dataset = cur.fetchall()
            all_types = []

            for row in dataset:
                media_type = MediaType(row['id'], row['name'])
                all_types.append(media_type.__dict__)

            return all_types
        except Error as e:
            print(e)


def insert(media_type=None):
    """
    Insert data into the database
    """
    with sqlite3.connect(db_file) as conn:
        cur = conn.cursor()
        
        try:
            cur.execute('''
                INSERT INTO media_type (id, name)
                VALUES (?)
            ''', (media_type['name']))
            conn.commit()
        except Error as e:
            print(e)
            
        return media_type