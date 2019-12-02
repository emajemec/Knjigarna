import csv

class Tabela:
    '''Razred. ki predstavlja tabelo v bazi.
    Polja razreda:
    - ime: ime tabele
    - podatki: datoteka s podatki ali None
    id: stolpec z lastnostjo AUTOINCREMENT ali None
    '''
    ime = None
    podatki = None
    id = None

    def __init__(self, conn):
        '''Konstruktor razreda'''
        self.conn = conn

    def ustvari(self):
        raise NotImplementedError

    def izbrisi(self):
        '''Metoda za izbrisanje tabele'''
        self.conn.execute("DROP TABLE IF EXISTS {};".format(self.ime))

    def uvozi(self, encoding="UTF-8", **kwargs):
        '''Metoda za uvoz podatkov

        Argumenti:
        -encoding: kodiranje znakov
        - ostali poimenovali elementi: za metodo dodaj_vrstico
        '''
        if self.podatki is None:
            return
        with open(self.podatki, encoding=encoding) as datoteka:
            podatki = csv.reader(datoteka) 
            '''za branje datoteke'''
            stolpci = self.pretvori(next(podatki), kwargs)
            poizvedba = self.dodajanje(stolpci)
            for vrstica in podatki:
                vrstica = [None if x == "" else x for x in vrstica]
                self.dodaj_vrstico(vrstica, poizvedba, **kwargs)

    def izprazni(self):
        '''Metoda za praznjenje tabele. (brisanje podatkov iz tabele)'''
        self.conn.execute("DELETE FROM {};".format(self.ime))

    @staticmethod
    def pretvori(stolpci, kwargs):
        '''Prilagodi imena stolpcev in poskrbi za ustrezne argumente 
        za dodaj_vrstico
        Privzeto vrne podane stolpce'''
        return stolpci

    def dodajanje(self, stolpci=None, stevilo=None):
        '''Metoda za gradnjo poizvedbe
        Argumenti: uporabimo enega od njiju
        -stolpci: seznam stolpcev
        -stevilo: št stolpcev
        '''
        if stolpci is None:
            assert stevilo is not None
            st = ""
        else:
            st = "({})".format(", ".join(stolpci))
            stevilo = len(stolpci)
        return "INSERT INTO {}{} VALUES ({})". \
            format(self.ime, st, ", ".join(["?"] * stevilo))

    def dodaj_vrstico(self, podatki, poizvedba=None, **kwargs):
        '''Metoda za dodajanje vrstice.
        Argumenti:
        -podatki: seznam s podatki v vrstici
        -poizvedba: poizvedba, ki naj se zažene
        -poljubni poimenovani parametri: privzeto se ignorirajo
        '''
        if poizvedba is None:
            poizvedba = self.dodajanje(stevilo=len(podatki))
        cur = self.conn.execute(poizvedba, podatki) 
        '''metoda execute'''
        if self.id is not None:
            return cur.lastrowid


class Zanr(Tabela):
    '''Tabela za žanre'''
    ime = "zanr"
    id = "id"

    def ustvari(self):
        '''Ustvari tabelo žanr'''
        self.conn.execute("""
            CREATE TABLE zanr (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                naziv TEXT
            );
        """)

    def dodaj_vrstico(self, podatki, poizvedba=None):
        '''Dodaj žanr.
        Če žanr že obstaja, vrne obstoječ ID'''
        cur = self.conn.execute("""
            SELECT id FROM zanr
            WHERE naziv = ?;
        """, podatki)
        r = cur.fetchone() 
        '''vrne eno vrstico'''
        if r is None:
            return super().dodaj_vrstico(podatki, poizvedba)
        else:
            id, = r 
            '''poberemo en podatek'''
            return id


class Oznaka(Tabela):
    ime = "oznaka"

    def ustvari(self):
        self.conn.execute("""
            CREATE TABLE oznaka (
                kratica TEXT PRIMARY KEY
            );
        """)

    def dodaj_vrstico(self, podatki, poizvedba=None):
        cur = self.conn.execute("""
            SELECT kratica FROM oznaka
            WHERE kratica = ?;
        """, podatki)
        r = cur.fetchone()
        if r is None:
            super().dodaj_vrstico(podatki, poizvedba)


class Film(Tabela):
    '''Tabela za filme'''
    ime = "film"
    podatki = "podatki/film.csv"

    def __init__(self, conn, oznaka):
        '''Konstruktor tabele filmov.
        Argumenti:
        -conn: povezava na bazo
        -oznaka: tabela za oznake
        '''
        super().__init__(conn)
        self.oznaka = oznaka

    def ustvari(self):
        '''Ustvari tabelo film'''
        self.conn.execute("""
            CREATE TABLE film (
                id        INTEGER PRIMARY KEY,
                naslov    TEXT,
                dolzina   INTEGER,
                leto      INTEGER,
                ocena     REAL,
                metascore INTEGER,
                glasovi   INTEGER,
                zasluzek  INTEGER,
                oznaka    TEXT    REFERENCES oznaka (kratica),
                opis      TEXT
            );
        """)

    def uvozi(self, encoding="UTF-8"):
        '''Uvozi podatke o filmih in pripadajoče oznake'''
        insert = self.oznaka.dodajanje(stevilo=1)
        super().uvozi(encoding=encoding, insert=insert)

    @staticmethod
    def pretvori(stolpci, kwargs):
        '''zapomni si indeks stolpca z oznako'''
        kwargs["oznaka"] = stolpci.index("oznaka")
        return stolpci

    def dodaj_vrstico(self, podatki, poizvedba=None, insert=None, oznaka=None):
        '''dodaj film in pripadajočo oznako
        Argumenti:
        -podatki: seznam s podatki o filmu
        -poizvedba: poizvedba za dodajanje filma
        -insert: poizvedba za dodajanje oznake
        -oznaka: indeks stolpca z oznako'''
        assert oznaka is not None
        if insert is None: 
            '''ce oznaka obstaja, jo dodamo'''
            insert = self.oznaka.dodajanje(1)
        if podatki[oznaka] is not None:
            self.oznaka.dodaj_vrstico([podatki[oznaka]], insert)
        super().dodaj_vrstico(podatki, poizvedba)


class Oseba(Tabela):
    '''tabela za osebe'''
    ime = "oseba"
    podatki = "podatki/oseba.csv"

    def ustvari(self):
        '''ustvari tabelo tabela'''
        self.conn.execute("""
            CREATE TABLE oseba (
                id  INTEGER PRIMARY KEY,
                ime TEXT
            );
        """)


class Vloga(Tabela):
    '''tabela za vloge'''
    ime = "vloga"
    podatki = "podatki/vloga.csv"

    def ustvari(self):
        '''ustvari tabelo vloga'''
        self.conn.execute("""
            CREATE TABLE vloga (
                film  INTEGER   REFERENCES film (id),
                oseba INTEGER   REFERENCES oseba (id),
                tip   CHARACTER CHECK (tip IN ('I',
                                'R') ),
                mesto INTEGER,
                PRIMARY KEY (
                    film,
                    oseba,
                    tip
                )
            );
        """)


class Pripada(Tabela):
    '''tabela za relacijo pripadnosti filma žanru'''
    ime = "pripada"
    podatki = "podatki/zanr.csv"

    def __init__(self, conn, zanr):
        '''konstruktor tabele pripadnosti žanru
        Argumenti:
        -conn: povezava na bazo
        -zanr: tabela za žanre'''
        super().__init__(conn)
        self.zanr = zanr

    def ustvari(self):
        '''ustvarimo tabelo žanrov'''
        self.conn.execute("""
            CREATE TABLE pripada (
                film INTEGER REFERENCES film (id),
                zanr INTEGER REFERENCES zanr (id),
                PRIMARY KEY (
                    film,
                    zanr
                )
            );
        """)

    def uvozi(self, encoding="UTF-8"):
        '''uvozi pripadnosti filmov in pripadajoče žanre'''
        insert = self.zanr.dodajanje(["naziv"])
        super().uvozi(encoding=encoding, insert=insert)

    @staticmethod
    def pretvori(stolpci, kwargs):
        '''spremeni ime stolpca z žanrom in si zapomni njegov indeks'''
        naziv = kwargs["naziv"] = stolpci.index("naziv")
        stolpci[naziv] = "zanr"
        return stolpci

    def dodaj_vrstico(self, podatki, poizvedba=None, insert=None, naziv=None):
        '''dodaj pripadnost filma in pripadajoči žanr
        Argumenti:
        -podatki: seznam s podatki o pripadnosti
        -poizvedba: poizvedba za dodajanje pripadnosti
        -insert: poizvedba za dodajanje žanra
        -oznaka: indeks stolpca z žanrom'''

        assert naziv is not None
        if insert is None:
            insert = self.zanr.dodajanje(["naziv"])
        podatki[naziv] = self.zanr.dodaj_vrstico([podatki[naziv]], insert)
        super().dodaj_vrstico(podatki, poizvedba)


def ustvari_tabele(tabele):
    '''ustvari podane tabele'''
    for t in tabele:
        t.ustvari()


def izbrisi_tabele(tabele):
    '''izbriše podane tabele'''
    for t in tabele:
        t.izbrisi()


def uvozi_podatke(tabele):
    '''uvozi podatke podane tabele'''
    for t in tabele:
        t.uvozi()


def izprazni_tabele(tabele):
    '''izprazni podane tabele'''
    for t in tabele:
        t.izprazni()


def ustvari_bazo(conn):
    '''izvede ustvarjene tabele'''
    tabele = pripravi_tabele(conn)
    izbrisi_tabele(tabele)
    ustvari_tabele(tabele)
    uvozi_podatke(tabele)


def pripravi_tabele(conn):
    '''pripravi objekte za tabele'''
    zanr = Zanr(conn)
    oznaka = Oznaka(conn)
    film = Film(conn, oznaka)
    oseba = Oseba(conn)
    vloga = Vloga(conn)
    pripada = Pripada(conn, zanr)
    return [zanr, oznaka, film, oseba, vloga, pripada]


def ustvari_bazo_ce_ne_obstaja(conn):
    '''ustvari bazo, če ta še ne obstaja'''
    with conn: 
        '''vse naj bo v eni transakciji'''
        cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
        if cur.fetchone() == (0, ):
            ustvari_bazo(conn)