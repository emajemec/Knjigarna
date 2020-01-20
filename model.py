import sqlite3
from geslo import sifriraj_geslo, preveri_geslo
import naredi_bazo

conn = sqlite3.connect('knjigarna.db')

def seznam_knjig():
    knjige = []
    sql = 'SELECT naslov, st_strani FROM knjiga'
    for naslov, st_strani in conn.execute(sql):
        knjige.append(naslov)
    return knjige

def stevilo_knjig():
    sql = 'SELECT COUNT(*) FROM knjiga'
    (st_knjig,) = conn.execute(sql).fetchone()
    return st_knjig

class LoginError(Exception):
    """
    Napaka ob napačnem uporabniškem imenu ali geslu.
    """
    pass


class Uporabnik:
    """
    Razred za uporabnika.
    """
    uporabnik = naredi_bazo.Uporabnik()
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