
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
        edges = DAO.getAllEdges(min, max)
        for edge in edges:
            self._graph.add_edge(self._idMap[edge.card_a], self._idMap[edge.card_b], weight=edge.peso)

        return self._graph

    def get_ranking(self):
        # Restituisce i nodi (oggetti Card) ordinati per quantita
        return sorted(self._graph.nodes, key=lambda x: x.quantita, reverse=True)

    def get_top_lift(self, limite):
        N = limite * 2

        sinergie = []
        for u, v, d in self._graph.edges(data=True):
            peso = d['weight']
            # u e v sono oggetti Card, usiamo il loro attributo frequenza
            lift = (peso * N) / (u.quantita * v.quantita)
            sinergie.append((u, v, lift, peso))

        # Ordiniamo per Lift decrescente
        sinergie.sort(key=lambda x: x[2], reverse=True)
        return sinergie

    def get_connettivita_stats(self):
        """Analizza quante isole (componenti) ci sono e quanto è grande la principale."""
        # Trova tutti i gruppi di nodi isolati
        componenti = list(nx.connected_components(self._graph))

        numero_componenti = len(componenti)

        # Calcoliamo la dimensione della componente più grande
        if componenti:
            dim_max = len(max(componenti, key=len))
        else:
            dim_max = 0

        return numero_componenti, dim_max