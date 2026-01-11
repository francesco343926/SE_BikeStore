from UI.view import View
from model.model import Model
import flet as ft
import datetime

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def set_dates(self):
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        categoria =self._view.dd_category.value
        giornoS = self._view.dp1.value
        giornoF=self._view.dp2.value
        self._model.creagrafo(categoria, giornoS, giornoF)
        ###
        nodi =len(self._model.G.nodes)
        archi = len(self._model.G.edges)
        ###
        self._view.txt_risultato.clean()
        self._view.txt_risultato.controls.append(ft.Text(f" Numero nodi {nodi} numero archi {archi}"))
        nodi = list(self._model.G.nodes())
        for n in nodi:
            self._view.dd_prodotto_iniziale.options.append(ft.dropdown.Option(text=n.name, key=n.id))
            self._view.dd_prodotto_finale.options.append(ft.dropdown.Option(text=n.name, key= n.id))
        self._view.page.update()



    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        fiveprod= self._model.getbestprod() #list di tup
        self._view.txt_risultato.controls.append(ft.Text(f"i cinque prodotti piu venduti sono:"))
        for p in fiveprod:
            self._view.txt_risultato.controls.append(ft.Text(f" {p[0]} con score {p[1]}"))
        self._view.page.update()




    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        if not self._view.txt_lunghezza_cammino.value.isdigit():
            self._view.show_alert("inserire valore valido")
        lung= int(self._view.txt_lunghezza_cammino.value)
        partenza = self._view.dd_prodotto_iniziale.value
        arrivo= self._view.dd_prodotto_finale.value
        path= self._model.calcolabestpath(partenza, arrivo , lung)
        score = self._model.scorebestpath
        self._view.txt_risultato.clean()
        for p in path:
            self._view.txt_risultato.controls.append(ft.Text(f"{p.name}"))
        self._view.txt_risultato.controls.append(ft.Text(f"Score : {score}"))
        self._view.page.update()

    def populate_dd(self):
        categorie = self._model.getCategorie()
        for categoria in categorie:
            self._view.dd_category.options.append(ft.dropdown.Option(text=categoria))
        self._view.page.update()

