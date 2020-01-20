import sqlite3
from geslo import sifriraj_geslo


conn = sqlite3.connect('knjigarna.db')

with open('knjigarna.sql', encoding='utf-8') as f:
    sql_ukazi = f.read()
conn.executescript(sql_ukazi)



with open('podatki.sql', encoding='utf-8') as f:
    sql_ukazi = f.read()
with conn:
    for sql_ukaz in sql_ukazi.splitlines():
        conn.execute(sql_ukaz)

class Uporabnik():
    """
    Tabela za uporabnike.
    """
    ime = "uporabnik"
    podatki = "podatki/uporabnik.csv"

    def ustvari(self):
        """
        Ustvari tabelo uporabnik.
        """
        self.conn.execute("""
            CREATE TABLE uporabnik (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                ime       TEXT NOT NULL UNIQUE,
                zgostitev TEXT NOT NULL,
                sol       TEXT NOT NULL
            )
        """)

    @staticmethod
    def pretvori(stolpci, kwargs):
        """
        Zapomni si indeksa stolpcev za zgostitev in sol.
        """
        kwargs["zgostitev"] = stolpci.index("zgostitev")
        kwargs["sol"] = stolpci.index("sol")
        return stolpci

    def dodaj_vrstico(self, podatki, poizvedba=None, zgostitev=None, sol=None):
        """
        Dodaj uporabnika.

        Če sol ni podana, zašifrira podano geslo.
        """
        if sol is not None and zgostitev is not None and podatki[sol] is None:
            podatki[zgostitev], podatki[sol] = sifriraj_geslo(podatki[zgostitev])
        return super().dodaj_vrstico(podatki, poizvedba)

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