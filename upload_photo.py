import sqlite3
import sys
from pathlib import Path

DB_PATH = 'photos.db'
TABLE_SCHEMA = '''
CREATE TABLE IF NOT EXISTS photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    data BLOB NOT NULL
)
'''

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(TABLE_SCHEMA)
    conn.commit()
    return conn

def insert_photo(conn, file_path: str):
    path = Path(file_path)
    with path.open('rb') as f:
        data = f.read()
    conn.execute('INSERT INTO photos (filename, data) VALUES (?, ?)', (path.name, data))
    conn.commit()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python upload_photo.py <image-path>')
        sys.exit(1)
    conn = init_db()
    insert_photo(conn, sys.argv[1])
    print(f'Uploaded {sys.argv[1]} to {DB_PATH}')
