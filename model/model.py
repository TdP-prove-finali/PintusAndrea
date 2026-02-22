import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}

    def buildGraph(self,min,max,limite):
        self._graph.clear()
        self._graph.add_nodes_from(DAO.getAllNodes(min,max,limite))
        self._idMap = {c.card_name: c for c in self._graph.nodes}
        edges = DAO.getAllEdges(min, max,limite)

        for edge in edges:
            self._graph.add_edge(self._idMap[edge.card_a], self._idMap[edge.card_b], weight=edge.peso)

        return self._graph

    def get_ranking(self):
        return sorted(self._graph.nodes, key=lambda x: x.quantita, reverse=True)

    def get_top_lift(self, limite):
        N = limite * 2

        sinergie = []
        for u, v, d in self._graph.edges(data=True):
            peso = d['weight']
            lift = (peso * N) / (u.quantita * v.quantita)
            sinergie.append((u, v, lift, peso))

        sinergie.sort(key=lambda x: x[2], reverse=True)
        return sinergie

    def get_connettivita_stats(self):
        componenti = list(nx.connected_components(self._graph))

        numero_componenti = len(componenti)

        if componenti:
            dim_max = len(max(componenti, key=len))
        else:
            dim_max = 0

        return numero_componenti, dim_max

    def get_candidati_deck(self, seed_card, profondita, soglia_lift, top_n):
        self._candidati = []
        parziale = [seed_card]
        N = 1000 * 2
        self._ricorsione_lift_al_volo(parziale, profondita, soglia_lift, top_n, N)

        self._candidati.sort(key=lambda x: x[1], reverse=True)

        risultati_unici = []
        for mazzo, score in self._candidati:
            set_attuale = set(mazzo)
            troppo_simile = False
            for gia_preso, s in risultati_unici:

                if len(set_attuale.intersection(set(gia_preso))) > (profondita - 3):
                    troppo_simile = True
                    break

            if not troppo_simile:
                risultati_unici.append((mazzo, score))

            if len(risultati_unici) == 5:
                break

        return risultati_unici

    def _ricorsione_lift_al_volo(self, parziale, profondita, soglia_lift, top_n, N):

        if len(parziale) == profondita:
            punteggio = self._calcola_sinergia_lift_manuale(parziale, N)
            self._candidati.append((list(parziale), punteggio))
            return

        ultima = parziale[-1]
        vicini_validi = []

        for vicino in self._graph.neighbors(ultima):
            if vicino not in parziale:

                peso = self._graph[ultima][vicino]['weight']

                lift_calcolato = (peso * N) / (ultima.quantita * vicino.quantita)

                if lift_calcolato >= soglia_lift:
                    vicini_validi.append((vicino, lift_calcolato))

        vicini_validi.sort(key=lambda x: x[1], reverse=True)

        for vicino, lift in vicini_validi[:top_n]:
            parziale.append(vicino)
            self._ricorsione_lift_al_volo(parziale, profondita, soglia_lift, top_n, N)
            parziale.pop()

    def _calcola_sinergia_lift_manuale(self, deck, N):
        sinergia_tot = 0
        for i in range(len(deck)):
            for j in range(i + 1, len(deck)):
                if self._graph.has_edge(deck[i], deck[j]):
                    peso = self._graph[deck[i]][deck[j]]['weight']
                    lift = (peso * N) / (deck[i].quantita * deck[j].quantita)
                    sinergia_tot += lift
        return round(sinergia_tot, 2)