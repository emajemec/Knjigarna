import sqlite3

conn = sqlite3.connect('knjigarna.db')
baza.ustvari_bazo_ce_ne_obstaja()
conn.execute('''
    CREATE TABLE izvod (
    id INTEGER PRIMARY KEY, 
    knjiga INTEGER REFERENCES knjiga(id), 
    založba INTEGER REFERENCES založba(id), 
    št_strani INTEGER, 
    leto INTEGER, 
    cena REAL,
    vezava TEXT REFERENCES vezava(oznaka),
    jezik INTEGER REFERENCES jezik(id)
)''')