import sqlite3
from pathlib import Path

def get_messages_between_dates(input_dir, date1, date2):

    def get(input_db_path, date1, date2):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
    
        query = '''
        SELECT id, type, date, edit_date, content, reply_to, user_id, media_id
        FROM messages
        WHERE date BETWEEN ? AND ?
        '''
        cursor.execute(query, (date1, date2))
        rows = cursor.fetchall()
        keys = ['id', 'type', 'date', 'edit_date', 'content', 'reply_to', 'user_id', 'media_id']
        messages = [dict(zip(keys, row)) for row in rows]
    
        conn.close()
    
        return messages

    twitter_msgs = get(input_dir / "twitter.sqlite", date1, date2)
    telegram_msgs = get(input_dir / "telegram.sqlite", date1, date2)

    return twitter_msgs + telegram_msgs