import sqlite3
from flask import g

DATABASE = 'skill_gap.db'

# Get DB connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # So we can access columns by name
    return db

# Execute a query and fetch results
def query_db(query, args=(), one=False):
    cur = get_db().cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# Close DB connection when app context ends
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
