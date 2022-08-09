import sqlite3
from sqlite3 import Error
from anime_database import db_file


class Media():
    def __init__(self, id, name, type_id, type_name):
        self.id = id
        self.name = name
        self.type_id = type_id
        self.type_name = type_name
        self.recommended_count = 0


def get_media_with_type():
    with sqlite3.connect(db_file) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        try:
            cur.execute("""
                SELECT
                    m.id as media_id,
                    m.name as media_name,
                    m.type_id,
                    t.id as media_type_id,
                    t.name as type_name
                FROM media m
                JOIN media_type t
                    ON media_type_id = m.type_id
            """)
            dataset = cur.fetchall()
            all_media = []

            for row in dataset:
                media = Media(id=row['media_id'], name=row['media_name'], type_id=row['media_type_id'], type_name=row['type_name'])
                all_media.append(media.__dict__)

            return all_media
        except Error as e:
            print(e)


def get_media_with_rec_by():
    with sqlite3.connect(db_file) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        try:
            cur.execute("""
                SELECT
                    m.id,
                    m.name as media_name,
                    m.type_id,
                    r.discord_id,
                    r.media_id as rec_by_media_id,
                    mt.id as media_type_id,
                    mt.name as type_name,
                    COUNT(r.media_id) media_id_count
                FROM media m
                LEFT JOIN recommended_by r
                    ON m.id = r.media_id
                LEFT JOIN media_type mt
                    ON mt.id = m.type_id
                GROUP BY media_name;
            """)
            dataset = cur.fetchall()
            all_media = []

            for row in dataset:
                media = Media(id=row['id'], name=row['media_name'], type_id=row['media_type_id'], type_name=row['type_name'])
                media.recommended_count = row['media_id_count']
                all_media.append(media.__dict__)

            return all_media
        except Error as e:
            print(e)


def get_single_media(media_name):
    with sqlite3.connect(db_file) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        media = None
        try:
            cur.execute("""
                SELECT
                    m.id,
                    m.name as media_name,
                    m.type_id,
                    r.discord_id,
                    r.media_id as rec_by_media_id,
                    mt.id as media_type_id,
                    mt.name as type_name,
                    COUNT(r.media_id) media_id_count
                FROM media m
                LEFT JOIN recommended_by r
                    ON m.id = r.media_id
                LEFT JOIN media_type mt
                    ON mt.id = m.type_id
                WHERE media_name = ?
            """, (media_name,))
            data = cur.fetchone()
            if data['id']:
                media = Media(id=data['id'], name=data['media_name'], type_id=data['media_type_id'], type_name=data['type_name'])
                media.recommended_count = data['media_id_count']
                return media.__dict__
            
            return media
        except Error as e:
            print(e)
            

def delete_media(media_id):
    with sqlite3.connect(db_file) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        try:
            cur.execute("""
                DELETE FROM media
                WHERE id = ?
            """, (media_id,))
        except Error as e:
            print(e)


def insert(media=None):
    """
    Insert data into the database
    """
    with sqlite3.connect(db_file) as conn:
        cur = conn.cursor()
        
        try:
            cur.execute('''
                INSERT INTO media (name, type_id)
                VALUES (?, ?)
            ''', (media['name'], media['type_id']))
            conn.commit()
        
        except Error as e:
            print(e)
            
        return get_single_media(media['name'])