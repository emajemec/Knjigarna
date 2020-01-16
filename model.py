import sqlite3

conn = sqlite3.connect('knjigarna.db')

def seznam_knjig():
    knjige = []
    sql = 'SELECT naslov, št_strani FROM knjiga'
    for naslov, st_strani in conn.execute(sql):
        knjige.append(naslov)
    return knjige