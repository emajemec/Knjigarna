import csv

class Tabela:
    """
    Razred, ki predstavlja tabelo v bazi.

    Polja razreda:
    - ime: ime tabele
    - podatki: datoteka s podatki ali None
    """
    ime = None
    podatki = None

    def __init__(self, conn):
        """
        Konstruktor razreda.
        """
        self.conn = conn

    def ustvari(self):
        """
        Metoda za ustvarjanje tabele.
        Podrazredi morajo povoziti to metodo.
        """
        raise NotImplementedError

    def izbrisi(self):
        """
        Metoda za brisanje tabele.
        """
        self.conn.execute("DROP TABLE IF EXISTS {};".format(self.ime))

    def uvozi(self, encoding="UTF-8", **kwargs):
        """
        Metoda za uvoz podatkov.

        Argumenti:
        - encoding: kodiranje znakov
        - ostali poimenovani argumenti: za metodo dodaj_vrstico
        """
        if self.podatki is None:
            return
        with open(self.podatki, encoding=encoding) as datoteka:
            podatki = csv.reader(datoteka)
            stolpci = self.pretvori(next(podatki), kwargs)
            poizvedba = self.dodajanje(stolpci)
            for vrstica in podatki:
                vrstica = [None if x == "" else x for x in vrstica]
                self.dodaj_vrstico(vrstica, poizvedba, **kwargs)

    def izprazni(self):
        """
        Metodo za praznjenje tabele.
        """
        self.conn.execute("DELETE FROM {};".format(self.ime))

    @staticmethod
    def pretvori(stolpci, kwargs):
        """
        Prilagodi imena stolpcev
        in poskrbi za ustrezne argumente za dodaj_vrstico.

        Privzeto vrne podane stolpce.
        """
        return stolpci

    def dodajanje(self, stolpci=None, stevilo=None):
        """
        Metoda za gradnjo poizvedbe.

        Arugmenti uporabimo enega od njiju):
        - stolpci: seznam stolpcev
        - stevilo: število stolpcev
        """
        if stolpci is None:
            assert stevilo is not None
            st = ""
        else:
            st = " ({})".format(", ".join(stolpci))
            stevilo = len(stolpci)
        return "INSERT INTO {}{} VALUES ({})". \
            format(self.ime, st, ", ".join(["?"] * stevilo))

    def dodaj_vrstico(self, podatki, poizvedba=None, **kwargs):
        """
        Metoda za dodajanje vrstice.

        Argumenti:
        - podatki: seznam s podatki v vrstici
        - poizvedba: poizvedba, ki naj se zažene
        - poljubni poimenovani parametri: privzeto se ignorirajo
        """
        if poizvedba is None:
            poizvedba = self.dodajanje(stevilo=len(podatki))
        cur = self.conn.execute(poizvedba, podatki)
        return cur.lastrowid


class Zanr(Tabela):
    """
    Tabela zalozb.
    """
    ime = "Zanr"

    def ustvari(self):
        """
        Ustvari tabelo zanrov.
        """
        self.conn.execute("""
            CREATE TABLE zanr (
                id INTEGER PRIMARY KEY,
                ime TEXT
            );
        """)

    def dodaj_vrstico(self, podatki, poizvedba=None):
        """
        Dodaj zanr.

        Če zanr že obstaja, vrne obstoječ ID.
        """
        cur = self.conn.execute("""
            SELECT id FROM zanr
            WHERE ime = ?;
        """, podatki)
        r = cur.fetchone()
        if r is None:
            return super().dodaj_vrstico(podatki, poizvedba)
        else:
            id, = r
            return id

class Zalozba(Tabela):
    """
    Tabela zalozb.
    """
    ime = "Zalozba"

    def ustvari(self):
        """
        Ustvari tabelo zalozb.
        """
        self.conn.execute("""
            CREATE TABLE zalozba (
                id INTEGER PRIMARY KEY,
                ime TEXT
            );
        """)

    def dodaj_vrstico(self, podatki, poizvedba=None):
        """
        Dodaj zalozbo.

        Če zalozba že obstaja, vrne obstoječ ID.
        """
        cur = self.conn.execute("""
            SELECT id FROM zalozba
            WHERE ime = ?;
        """, podatki)
        r = cur.fetchone()
        if r is None:
            return super().dodaj_vrstico(podatki, poizvedba)
        else:
            id, = r
            return id

class Jezik(Tabela):
    """
    Tabela jezikov.
    """
    ime = "Jezik"

    def ustvari(self):
        """
        Ustvari tabelo jezikov.
        """
        self.conn.execute("""
            CREATE TABLE jezik (
                id INTEGER PRIMARY KEY,
                ime TEXT
            );
        """)

    def dodaj_vrstico(self, podatki, poizvedba=None):
        """
        Dodaj jezik.

        Če jezik že obstaja, vrne obstoječ ID.
        """
        cur = self.conn.execute("""
            SELECT id FROM jezik
            WHERE ime = ?;
        """, podatki)
        r = cur.fetchone()
        if r is None:
            return super().dodaj_vrstico(podatki, poizvedba)
        else:
            id, = r
            return id

'SPREMENI!!!!!!!!!'
class Oznaka(Tabela):
    """
    Tabela za oznake.
    """
    ime = "oznaka"

    def ustvari(self):
        """
        Ustvari tabelo oznaka.
        """
        self.conn.execute("""
            CREATE TABLE oznaka (
                kratica TEXT PRIMARY KEY
            );
        """)

    def dodaj_vrstico(self, podatki, poizvedba=None):
        """
        Dodaj oznako.

        Če oznaka že obstaja, je ne dodamo še enkrat.
        """
        cur = self.conn.execute("""
            SELECT kratica FROM oznaka
            WHERE kratica = ?;
        """, podatki)
        r = cur.fetchone()
        if r is None:
            return super().dodaj_vrstico(podatki, poizvedba)

'SPREMENI!!!!!!!!!'
class Film(Tabela):
    """
    Tabela za filme.
    """
    ime = "film"
    podatki = "podatki/film.csv"

    def __init__(self, conn, oznaka):
        """
        Konstruktor tabele filmov.

        Argumenti:
        - conn: povezava na bazo
        - oznaka: tabela za oznake
        """
        super().__init__(conn)
        self.oznaka = oznaka

    def ustvari(self):
        """
        Ustavari tabelo film.
        """
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
        """
        Uvozi podatke o filmih in pripadajoče oznake.
        """
        insert = self.oznaka.dodajanje(stevilo=1)
        super().uvozi(encoding=encoding, insert=insert)

    @staticmethod
    def pretvori(stolpci, kwargs):
        """
        Zapomni si indeks stolpca z oznako.
        """
        kwargs["oznaka"] = stolpci.index("oznaka")
        return stolpci

    def dodaj_vrstico(self, podatki, poizvedba=None, insert=None, oznaka=None):
        """
        Dodaj film in pripadajočo oznako.

        Argumenti:
        - podatki: seznam s podatki o filmu
        - poizvedba: poizvedba za dodajanje filma
        - insert: poizvedba za dodajanje oznake
        - oznaka: indeks stolpca z oznako
        """
        if oznaka is not None:
            if insert is None:
                insert = self.oznaka.dodajanje(1)
            if podatki[oznaka] is not None:
                self.oznaka.dodaj_vrstico([podatki[oznaka]], insert)
        return super().dodaj_vrstico(podatki, poizvedba)

'SPREMENI!!!!!!!!!'
class Oseba(Tabela):
    """
    Tabela za osebe.
    """
    ime = "oseba"
    podatki = "podatki/oseba.csv"

    def ustvari(self):
        """
        Ustvari tabelo oseba.
        """
        self.conn.execute("""
            CREATE TABLE oseba (
                id  INTEGER PRIMARY KEY,
                ime TEXT
            );
        """)

'SPREMENI!!!!!!!!!'
class Vloga(Tabela):
    """
    Tabela za vloge.
    """
    ime = "vloga"
    podatki = "podatki/vloga.csv"

    def ustvari(self):
        """
        Ustvari tabelo vloga.
        """
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

'ŠE MALO ZA SPREMENIT!!!!!!!!'
class Pripada(Tabela):
    """
    Tabela za relacijo pripadnosti knjige osebi.
    """
    ime = "pripada"
    podatki = "podatki/books.csv"

    def __init__(self, conn, Oseba):
        """
        Konstruktor tabele pripadnosti osebam.

        Argumenti:
        - conn: povezava na bazo
        - Zalozba: tabela za osebe
        """
        super().__init__(conn)
        self.Oseba = Oseba

    def ustvari(self):
        """
        Ustvari tabelo pripada.
        """
        self.conn.execute("""
            CREATE TABLE pripada (
                knjiga INTEGER REFERENCES izvod(id),
                oseba INTEGER REFERENCES oseba(id),
                tip CHARACTER CHECK (tip IN ('O', 'P'))
            );
        """)

    def uvozi(self, encoding="UTF-8"):
        """
        Uvozi pripadnosti oseb in pripadajočih knjig.
        """
        insert = self.Oseba.dodajanje(["ime"])
        super().uvozi(encoding=encoding, insert=insert)

    @staticmethod
    def pretvori(stolpci, kwargs):
        """
        Spremeni ime stolpca z zalozbaom
        in si zapomni njegov indeks.
        """
        naziv = kwargs["ime"] = stolpci.index("ime")
        stolpci[naziv] = "Oseba"
        return stolpci

    def dodaj_vrstico(self, podatki, poizvedba=None, insert=None, naziv=None):
        """
        Dodaj pripadnost filma in pripadajoči zalozba.

        Argumenti:
        - podatki: seznam s podatki o pripadnosti
        - poizvedba: poizvedba za dodajanje pripadnosti
        - insert: poizvedba za dodajanje zalozbaa
        - oznaka: indeks stolpca z zalozbaom
        """
        assert naziv is not None
        if insert is None:
            insert = self.Oseba.dodajanje(["ime"])
        podatki[naziv] = self.Oseba.dodaj_vrstico([podatki[naziv]], insert)
        return super().dodaj_vrstico(podatki, poizvedba)


def ustvari_tabele(tabele):
    """
    Ustvari podane tabele.
    """
    for t in tabele:
        t.ustvari()


def izbrisi_tabele(tabele):
    """
    Izbriši podane tabele.
    """
    for t in tabele:
        t.izbrisi()


def uvozi_podatke(tabele):
    """
    Uvozi podatke v podane tabele.
    """
    for t in tabele:
        t.uvozi()


def izprazni_tabele(tabele):
    """
    Izprazni podane tabele.
    """
    for t in tabele:
        t.izprazni()


def ustvari_bazo(conn):
    """
    Izvede ustvarjanje baze.
    """
    tabele = pripravi_tabele(conn)
    izbrisi_tabele(tabele)
    ustvari_tabele(tabele)
    uvozi_podatke(tabele)


def pripravi_tabele(conn):
    """
    Pripravi objekte za tabele.
    """
    Zalozba = Zalozba(conn)
    oznaka = Oznaka(conn)
    film = Film(conn, oznaka)
    oseba = Oseba(conn)
    vloga = Vloga(conn)
    pripada = Pripada(conn, Zalozba)
    return [Zalozba, oznaka, film, oseba, vloga, pripada]


def ustvari_bazo_ce_ne_obstaja(conn):
    """
    Ustvari bazo, če ta še ne obstaja.
    """
    with conn:
        cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
        if cur.fetchone() == (0, ):
            ustvari_bazo(conn)