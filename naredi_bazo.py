import sqlite3

conn = sqlite3.connect('knjigarna.db')

with open('knjigarna.sql', encoding='utf-8') as f:
    sql_ukazi = f.read()
conn.executescript(sql_ukazi)


with open('data.sql', encoding='utf-8') as f:
    sql_ukazi = f.read()
conn.executescript(sql_ukazi)