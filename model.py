
from pomozne_funkcije import Seznam
import baza
import sqlite3
from geslo import sifriraj_geslo, preveri_geslo

conn = sqlite3.connect('knjigarna.db')
baza.ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')

uporabnik = baza.pripravi_tabele(conn)

class LoginError(Exception):
    """
    Napaka ob napačnem uporabniškem imenu ali geslu.
    """
    pass

class Uporabnik:
    """
    Razred za uporabnika.
    """

    insert = uporabnik.dodajanje(["ime", "zgostitev", "sol"])

    def __init__(self, ime, id=None):
        """
        Konstruktor uporabnika.
        """
        self.id = id
        self.ime = ime

    def __str__(self):
        """
        Znakovna predstavitev uporabnika.

        Vrne uporabniško ime.
        """
        return self.ime

    @staticmethod
    def prijava(ime, geslo):
        """
        Preveri, ali sta uporabniško ime geslo pravilna.
        """
        sql = """
            SELECT id, zgostitev, sol FROM uporabnik
            WHERE ime = ?
        """
        try:
            id, zgostitev, sol = conn.execute(sql, [ime]).fetchone()
            if preveri_geslo(geslo, zgostitev, sol):
                return Uporabnik(ime, id)
        except TypeError:
            pass
        raise LoginError(ime)

    def dodaj_v_bazo(self, geslo):
        """
        V bazo doda uporabnika s podanim geslom.
        """
        assert self.id is None
        zgostitev, sol = sifriraj_geslo(geslo)
        with conn:
            self.id = uporabnik.dodaj_vrstico(
                [self.ime, zgostitev, sol],
                self.insert
            )
class Avtorji:
    def __init__(self, ime, priimek, id = None):
        """Konstruktor avtorjev"""
        self.ime = ime
        self.priimek = priimek

    def __str__(self):
        """ Znakovna predstavitev avtorja, njegov ime in priimek. """
        return self.ime + " " + self.priimek


class Knjiga:

    def __init__(self, naslov, id=None):
        """
        Konstruktor knjig.
        """
        self.id = id
        self.naslov = naslov

    def __str__(self):
        """
        Znakovna predstavitev knjige.

        Vrne naslov knjige.
        """
        return self.naslov

    
    @staticmethod
    def po_crkah(crka):
        
        '''Vrne knjige na isto črko. '''
        sql = """SELECT naslov
                FROM knjiga
                WHERE naslov LIKE ? """
        for naslov in conn.execute(sql, [crka + '%']):
            yield Knjiga(naslov = naslov)
            

    @staticmethod
    def tab_crk():
        "Vrne niz zacetnic knjig"
        tab = []
        sql = """SELECT SUBSTR(naslov, 1, 1) 
                FROM knjiga
                GROUP BY SUBSTR(naslov, 1, 1);"""
        for crka in conn.execute(sql):
            tab.append(crka[0])
        return tab

    @staticmethod
    def stevilo_knjig():
        sql = 'SELECT COUNT(*) FROM knjiga'
        (st_knjig,) = conn.execute(sql).fetchone()
        return st_knjig

    @staticmethod
    def seznam_knjig():
        knjige = []
        sql = 'SELECT naslov, st_strani FROM knjiga'
        for naslov, st_strani in conn.execute(sql):
            knjige.append(naslov)
        return knjige

    @staticmethod
    def poisci_knjigo(niz):
        sql = 'SELECT naslov FROM knjiga WHERE naslov LIKE ?'
        for naslov in conn.execute(sql, ['%' + niz + '%']):
            yield Knjiga(naslov = naslov)

