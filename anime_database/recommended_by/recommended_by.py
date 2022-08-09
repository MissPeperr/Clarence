import sqlite3
from sqlite3 import Error
from anime_database import db_file

class RecommendedBy():
    def __init__(self, id, discord_id, media_id):
        self.id = id
        self.discord_id = discord_id
        self.media_id = media_id


def get_all():
    with sqlite3.connect(db_file) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        try:
            cur.execute("""
                SELECT
                    id,
                    discord_id,
                    media_id
                FROM recommended_by
            """)
            dataset = cur.fetchall()
            all_rec_by = []

            for row in dataset:
                rec_by = RecommendedBy(row['id'], row['discord_id'], row['media_id'])
                all_rec_by.append(rec_by.__dict__)

            return all_rec_by
        except Error as e:
            print(e)


def check_if_rec_by_exists(discord_id=int, media_id=int):
    with sqlite3.connect(db_file) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        rec_by = None
        try:
            cur.execute("""
                SELECT
                    id,
                    discord_id,
                    media_id
                FROM recommended_by
                WHERE media_id = ?
                AND discord_id = ?
            """, (media_id, discord_id))
            data = cur.fetchone()
            if data:
                rec_by = RecommendedBy(id=['id'], media_id=data['media_id'], discord_id=data['discord_id'])
                return rec_by.__dict__
            
            return rec_by
        except Error as e:
            print(e)


def insert(rec=None):
    """
    Insert data into the database
    """
    with sqlite3.connect(db_file) as conn:
        cur = conn.cursor()
        
        try:
            cur.execute('''
                INSERT INTO recommended_by (discord_id, media_id)
                VALUES (?, ?)
            ''', (rec['discord_id'], rec['media_id']))
            conn.commit()
        except Error as e:
            print(e)
            
        return rec