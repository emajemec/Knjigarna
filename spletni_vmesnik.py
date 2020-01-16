import bottle
import model

@bottle.get('/')
def zacetna_stran():
    return bottle.template(
        'zacetna_stran.html',
        knjige=model.seznam_knjig()
    )

bottle.run(reloader=True, debug=True)
