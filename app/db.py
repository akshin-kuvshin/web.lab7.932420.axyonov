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

# create
def add_product(name, price, stock):
    db = get_db()
    query = 'INSERT INTO products (name, price, stock) VALUES (?, ?, ?)'
    params = (name, price, stock)

    cursor = db.execute(query, params)
    db.commit()

    return cursor.lastrowid # id of added record

# retrieve
def get_products(min_price=None, max_price=None):
    db = get_db()
    query = 'SELECT id, name, price, stock FROM products'
    params = []

    if min_price is not None and max_price is not None:
        query += ' WHERE price BETWEEN ? AND ?'
        params.extend((min_price, max_price))
    elif min_price is not None:
        query += ' WHERE price >= ?'
        params.append(min_price)
    elif max_price is not None:
        query += ' WHERE price <= ?'
        params.append(max_price)

    rows = db.execute(query, params).fetchall()
    return [dict(row) for row in rows]

# update
def update_product_stock(id, stock):
    db = get_db()
    query = 'UPDATE products SET stock = ? WHERE id = ?'
    params = (stock, id)

    cursor = db.execute(query, params)
    db.commit()

    return cursor.rowcount == 1 # exactly 1 record was modified (> 1 is impossible, btw)

# delete
def delete_product(id):
    db = get_db()
    query = 'DELETE FROM products WHERE id = ?'
    params = (id,)

    cursor = db.execute(query, params)
    db.commit()

    return cursor.rowcount == 1 # exactly 1 record was deleted (again, > 1 is impossible because of id)

# create + retrieve + update + delete = CRUD!
