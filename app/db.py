from flask import current_app, g
import sqlite3
from pathlib import Path

def init_db(app):
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(app.config['DATABASE'])
    query = '''\
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
)
'''

    try:
        db.execute(query)
        db.commit()
    finally:
        db.close()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row # allows indexing by field-name
    return g.db

def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
