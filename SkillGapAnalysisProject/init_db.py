import sqlite3
from werkzeug.security import generate_password_hash

DB = 'skill_gap.db'

schema = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS resumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    filename TEXT,
    skills TEXT,
    education TEXT,
    experience TEXT
);

CREATE TABLE IF NOT EXISTS company_requirements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_title TEXT,
    skills TEXT
);
'''

conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.executescript(schema)

# Insert demo user if not exists
email = 'admin@example.com'
username = 'admin'
password = 'password123'
hash_pw = generate_password_hash(password)

cur.execute('SELECT * FROM users WHERE email = ?', (email,))
if not cur.fetchone():
    cur.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                (username, email, hash_pw))
    print('Inserted demo user: admin / password123')
else:
    print('Demo user already exists')

conn.commit()
conn.close()
print('Database initialized at', DB)
