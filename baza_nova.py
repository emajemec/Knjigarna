import csv

def pobrisi_tabele(conn):
    """
    Pobriše tabele iz baze.
    """
    conn.execute("DROP TABLE IF EXISTS izvod;")
    conn.execute("DROP TABLE IF EXISTS knjiga;")
    conn.execute("DROP TABLE IF EXISTS je_ocenil;")
    conn.execute("DROP TABLE IF EXISTS zanr;")
    conn.execute("DROP TABLE IF EXISTS uporabnik;")
    conn.execute("DROP TABLE IF EXISTS zalozba;")
    conn.execute("DROP TABLE IF EXISTS vezava;")
    conn.execute("DROP TABLE IF EXISTS jezik;")
    conn.execute("DROP TABLE IF EXISTS pripada;")
    conn.execute("DROP TABLE IF EXISTS oseba;")


def ustvari_tabele(conn):
    """
    Ustvari tabele v bazi.
    """
    conn.execute("""
        CREATE TABLE izdaja (
            id INTEGER PRIMARY KEY, 
            knjiga INTEGER REFERENCES knjiga(id), 
            zalozba INTEGER REFERENCES zalozba(id), 
            st_strani INTEGER, 
            leto INTEGER, 
            cena REAL,
            vezava CHARACTER CHECK (vezava IN ('T', 'M', 'S')),
            jezik INTEGER REFERENCES jezik(id)
        );
    """)
    conn.execute("""
        CREATE TABLE je_ocenil (
            id_knjige INTEGER REFERENCES knjiga(id),
            ocena INTEGER,
            komentar TEXT,
            cas DATE,
            uporabnik INTEGER REFERENCES uporabnik(id) 
        );
    """)
    conn.execute("""
        CREATE TABLE jezik (
            id INTEGER,
            jezik TEXT
        );
    """)
    conn.execute("""
        CREATE TABLE vezava (
            id  INTEGER PRIMARY KEY,
            ime TEXT
        );
    """)
    conn.execute("""
        CREATE TABLE knjiga (
            id INTEGER PRIMARY KEY,
            naslov TEXT,
            zanr INTEGER REFERENCES zanr(id),
            opis TEXT
        );
    """)
    conn.execute("""
        CREATE TABLE oseba (
            id INTEGER PRIMARY KEY,
            ime TEXT,
            zivljenjepis TEXT
        );
    """)
    conn.execute("""
        CREATE TABLE pripada (
            knjiga INTEGER REFERENCES izvod(id),
            oseba INTEGER REFERENCES oseba(id),
            tip CHARACTER CHECK (tip IN ('O', 'P'))
        );
    """)
    conn.execute("""
        CREATE TABLE uporabnik (
            id INTEGER,
            ime TEXT,
            email TEXT 
        );
    """)
    conn.execute("""
        CREATE TABLE zalozba (
            id INTEGER,
            ime TEXT
        );
    """)
    conn.execute("""
        CREATE TABLE zanr (
            id INTEGER PRIMARY KEY,
            ime TEXT
        );
    """)


def uvozi_izvod(conn):
    """
    Uvozi podatke o izvodih.
    """
    conn.execute("DELETE FROM izvod;")
    conn.execute("DELETE FROM knjiga;")
    conn.execute("DELETE FROM zalozba;")
    conn.execute("DELETE FROM vezava;")
    conn.execute("DELETE FROM jezika;")
    conn.execute("DELETE FROM pripada;")
    with open('podatki/books.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO izvod VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            conn.execute(poizvedba, vrstica)

def uvozi_knjiga(conn):
    """
    Uvozi podatke o knjigah.
    """
    conn.execute("DELETE FROM knjiga;")
    conn.execute("DELETE FROM zanr;")
    conn.execute("DELETE FROM izvod;")
    conn.execute("DELETE FROM je_ocenil;")
    with open('podatki/books.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO knjiga VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            conn.execute(poizvedba, vrstica)

def uvozi_zanr (conn):
    """
    Uvozi podatke o žanrih.
    """
    conn.execute("DELETE FROM zanr;")
    conn.execute("DELETE FROM knjiga;")
    with open('podatki/zanr.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO zanr VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            conn.execute(poizvedba, vrstica)

def uvozi_je_ocenil(conn):
    """
    Uvozi podatke o ocenah.
    """
    conn.execute("DELETE FROM je_ocenil;")
    conn.execute("DELETE FROM knjiga;")
    conn.execute("DELETE FROM uporabnik;")
    with open('podatki/je_ocenil.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO je_ocenil VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            conn.execute(poizvedba, vrstica)

def uvozi_uporabnik(conn):
    """
    Uvozi podatke o uporabnikih.
    """
    conn.execute("DELETE FROM je_ocenil;")
    conn.execute("DELETE FROM uporabnik;")
    with open('podatki/uporabnik.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO uporabnik VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            conn.execute(poizvedba, vrstica)

def uvozi_zalozba(conn):
    """
    Uvozi podatke o zalozbah.
    """
    conn.execute("DELETE FROM izvod;")
    conn.execute("DELETE FROM zalozba;")
    with open('podatki/zalozba.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO zalozba VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            conn.execute(poizvedba, vrstica)

def uvozi_vezava(conn):
    """
    Uvozi podatke o vezavah.
    """
    conn.execute("DELETE FROM izvod;")
    conn.execute("DELETE FROM vezava;")
    with open('podatki/vezava.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO vezava VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            conn.execute(poizvedba, vrstica)

def uvozi_jezik(conn):
    """
    Uvozi podatke o jezikih.
    """
    conn.execute("DELETE FROM izvod;")
    conn.execute("DELETE FROM jezik;")
    with open('podatki/jezik.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO jezik VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            conn.execute(poizvedba, vrstica)

def uvozi_pripada(conn):
    """
    Uvozi podatke o osebah, ki pripadajo dolocenemu izvodu.
    """
    conn.execute("DELETE FROM izvod;")
    conn.execute("DELETE FROM oseba;")
    conn.execute("DELETE FROM pripada;")
    with open('podatki/pripada.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO pripada VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            conn.execute(poizvedba, vrstica)

def uvozi_oseba(conn):
    """
    Uvozi podatke o osebah.
    """
    conn.execute("DELETE FROM oseba;")
    conn.execute("DELETE FROM pripada;")
    with open('podatki/oseba.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO oseba VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            conn.execute(poizvedba, vrstica)

def ustvari_bazo(conn):
    """
    Opravi celoten postopek postavitve baze.
    """
    pobrisi_tabele(conn)
    ustvari_tabele(conn)
    uvozi_izvod(conn)
    uvozi_knjiga(conn)
    uvozi_zanr(conn)
    uvozi_je_ocenil(conn)
    uvozi_uporabnik(conn)
    uvozi_zalozba(conn)
    uvozi_vezava(conn)
    uvozi_jezik(conn)
    uvozi_pripada(conn)
    uvozi_oseba(conn)

def ustvari_bazo_ce_ne_obstaja(conn):
    """
    Ustvari bazo, če ta še ne obstaja.
    """
    with conn:
        conn = conn.execute("SELECT COUNT(*) FROM sqlite_master")
        if conn.fetchone() == (0, ):
            ustvari_bazo(conn)