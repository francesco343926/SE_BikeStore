import networkx as nx
import copy
from database.dao import DAO

class Model:
    def __init__(self):
        self.mapCategorie= dict()
        self.mapProdotti= dict()
        self.listaVendite = dict()
        self.G= nx.DiGraph()
        self.scorebestpath= 0
        self.bestpath= []

    def get_date_range(self):
        return DAO.get_date_range()

    def getCategorie(self):
        self.mapCategorie= DAO.getCategorie()
        return [c for c in self.mapCategorie.values()]

    def creagrafo(self, cat, dat1, dat2):
        #fai una mappa di prodotti objects e vendite objects con 2 estraz diverse
        for id in self.mapCategorie:
            if self.mapCategorie[id] == cat:
                cat= id
                break
        self.mapProdotti= DAO.getProdotti(cat)
        self.listaVendite= DAO.getVendite(dat1, dat2)
        for v in self.listaVendite:
            if v.product_id in self.mapProdotti:
                self.mapProdotti[v.product_id].num_vendite += 1

        self.G.clear()
        for p_id in self.mapProdotti:
            for p2_id in self.mapProdotti:
                if p_id != p2_id:
                    p1= self.mapProdotti[p_id]
                    p2 = self.mapProdotti[p2_id]
                    nv1= self.mapProdotti[p_id].num_vendite
                    nv2 = self.mapProdotti[p2_id].num_vendite
                    if nv1 == nv2:
                        self.G.add_edge(p1, p2, weight= nv1)
                        self.G.add_edge(p2, p1, weight=nv2)
                    if nv1> nv2:
                        self.G.add_edge(p1, p2, weight=nv1)
                    else:
                        self.G.add_edge(p2, p1, weight=nv1)


    def getbestprod(self):
        for p in self.mapProdotti.values():
            all_neigh = self.G.edges(p, data=True)

            for e in all_neigh:
                p.score += e[2]["weight"]
                e[1].score -= e[2]["weight"]

        l = sorted(list(self.mapProdotti.values()), key= lambda x: x.score, reverse=True)
        tuple= [ (p.name , p.score) for p in l]
        return tuple[:5]

    def calcolabestpath(self, part, arriv, l):
        part = self.mapProdotti[int(part)]
        arriv = self.mapProdotti[int(arriv)]
        parziale = [part]
        pesocorr= 0
        self.ricorsione(parziale, arriv, pesocorr, l)
        return self.bestpath

    def ricorsione(self, parziale, arriv, pesocorr, l):
        if len(parziale)== l and parziale[-1]== arriv:
            if pesocorr> self.scorebestpath:
                self.bestpath= copy.deepcopy(parziale)
                self.scorebestpath = pesocorr
            return

        if len(parziale)> l:
            return

        for arco in self.G.edges(parziale[-1], data=True):
            lista = list(self.G.edges(parziale[-1], data=True))
            pass
            if arco[1] not in parziale:
                parziale.append(arco[1])
                pesocorr += arco[2]['weight']
                self.ricorsione(parziale, arriv, pesocorr, l)
                parziale.pop()
                pesocorr -= arco[2]['weight']

        '''path= nx.dijkstra_path(self.G, parziale[0], arriv, weight= 'weight')
        pass'''



    def pesotot(self, lista):
        pass


