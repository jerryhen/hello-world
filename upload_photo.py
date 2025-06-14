import sqlite3
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

DB_PATH = 'photos.db'
NORMAL_DIR = Path('normal')
ABNORMAL_DIR = Path('abnormal')

SCHEMA = '''
CREATE TABLE IF NOT EXISTS photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    label TEXT NOT NULL,
    data BLOB NOT NULL
)
'''

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(SCHEMA)
    conn.commit()
    return conn

def save_photo(conn, file_path: Path, label: str):
    with file_path.open('rb') as f:
        data = f.read()
    conn.execute(
        'INSERT INTO photos (filename, label, data) VALUES (?, ?, ?)',
        (file_path.name, label, data)
    )
    conn.commit()
    dest_dir = NORMAL_DIR if label == 'normal' else ABNORMAL_DIR
    dest_dir.mkdir(exist_ok=True)
    shutil.copy(file_path, dest_dir / file_path.name)

def main():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title='Select an image')
    if not file_path:
        return
    response = messagebox.askquestion(
        'Classification',
        'Is the selected image a NORMAL mucosa?'
    )
    label = 'normal' if response == 'yes' else 'abnormal'
    conn = init_db()
    save_photo(conn, Path(file_path), label)
    messagebox.showinfo('Success', f'Saved {file_path} as {label}')

if __name__ == '__main__':
    main()
