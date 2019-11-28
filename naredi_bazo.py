import sqlite3

conn = sqlite3.connect('knjigarna.db')

with open('knjigarna.sql') as f:
    sql_ukazi = f.read()
conn.executescript(sql_ukazi)