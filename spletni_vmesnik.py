import bottle
import model
import random
from sqlite3 import IntegrityError
import json

NASTAVITVE = 'nastavitve.json'

try:
    with open(NASTAVITVE) as f:
        nastavitve = json.load(f)
        SKRIVNOST = nastavitve['skrivnost']
except FileNotFoundError:
    SKRIVNOST = "".join(chr(random.randrange(32, 128)) for _ in range(32))
    with open(NASTAVITVE, "w") as f:
        json.dump({'skrivnost': SKRIVNOST}, f)


def zahtevaj_prijavo():
    if bottle.request.get_cookie('uporabnik', secret=SKRIVNOST) != 'admin':
        bottle.abort(401, 'Nimate pravice za urejanje!')


def zahtevaj_odjavo():
    if bottle.request.get_cookie('uporabnik', secret=SKRIVNOST):
        bottle.redirect('/')


@bottle.get('/prijava/')
def prijava():
    zahtevaj_odjavo()
    return bottle.template(
        'prijava.html',
        napaka=None, ime=""
    )


@bottle.post('/prijava/')
def prijava_post():
    zahtevaj_odjavo()
    ime = bottle.request.forms['uporabnisko_ime']
    geslo = bottle.request.forms['geslo']
    try:
        uporabnik = Uporabnik.prijava(ime, geslo)
        bottle.response.set_cookie('uporabnik', ime, path='/', secret=SKRIVNOST)
        bottle.response.set_cookie('uid', uporabnik.id, path='/', secret=SKRIVNOST)
        bottle.redirect('/')
    except LoginError:
        return bottle.template(
            'prijava.html',
            napaka='Uporabniško ime in geslo se ne ujemata!',
            ime=ime
        )


@bottle.get('/vpis/')
def vpis():
    zahtevaj_odjavo()
    return bottle.template(
        'vpis.html',
        napaka=None, ime=""
    )


@bottle.post('/vpis/')
def vpis_post():
    zahtevaj_odjavo()
    ime = bottle.request.forms['uporabnisko_ime']
    geslo1 = bottle.request.forms['geslo1']
    geslo2 = bottle.request.forms['geslo2']
    if geslo1 != geslo2:
        return bottle.template(
            'vpis.html',
            napaka='Gesli se ne ujemata!',
            ime=ime
        )
    try:
        uporabnik = Uporabnik(ime)
        uporabnik.dodaj_v_bazo(geslo1)
        bottle.response.set_cookie('uporabnik', ime, path='/', secret=SKRIVNOST)
        bottle.response.set_cookie('uid', uporabnik.id, path='/', secret=SKRIVNOST)
        bottle.redirect('/')
    except IntegrityError:
        return bottle.template(
            'vpis.html',
            napaka='Uporabniško ime že obstaja!',
            ime=ime
        )


@bottle.get('/odjava/')
def odjava():
    bottle.response.delete_cookie('uporabnik', path='/')
    bottle.redirect('/')


@bottle.get('/')
def zacetna_stran():
    st_knjig = model.stevilo_knjig()
    return bottle.template(
        'zacetna_stran.html',
        knjige=model.seznam_knjig(),
        st_knjig=st_knjig
    )

bottle.run(reloader=True, debug=True)

