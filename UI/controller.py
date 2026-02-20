import flet as ft
import networkx as nx


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self,e):

        min = self._view._txtRangeTrofei.start_value
        max = self._view._txtRangeTrofei.end_value
        # MODO SICURO
        try:
            limite = int(self._view._txtMaxBattaglie.value)
        except ValueError:
            limite = 1000
        grafo = self._model.buildGraph(min,max,limite)
        n_nodi = len(grafo.nodes)
        n_archi= len(grafo.edges)



        self._view._txtNodi.value = n_nodi
        self._view._txtArchi.value= n_archi
        self._view.update_page()

    def handleAnalisi(self, e):
        # 3. Qui stampiamo la CLASSIFICA solo su richiesta
        self._view.txt_result.controls.clear()

        try:
            n_top = int(self._view._ddTopN.value)
        except:
            n_top = 5

        ranking = self._model.get_ranking()

        self._view.txt_result.controls.append(ft.Text(f"🏆 TOP {n_top} CARTE", size=16, weight="bold"))
        for i in range(min(n_top, len(ranking))):
            c = ranking[i]
            self._view.txt_result.controls.append(ft.Text(f"{i + 1}º - {c.card_name} ({c.quantita})"))

        self._view.update_page()

    def handleAdvancedRank(self, e):
        self._view.txt_result.controls.clear()

        if not self._model._graph.nodes:
            self._view.txt_result.controls.append(ft.Text("Crea prima il grafo!", color="red"))
            self._view.update_page()
            return

        # Recuperiamo il limite per il calcolo di N e il top-N per la stampa
        try:
            limite = int(self._view._txtMaxBattaglie.value)
            n_top = int(self._view._ddTopN.value)
        except:
            limite = 1000
            n_top = 10

        migliori_sinergie = self._model.get_top_lift(limite)

        self._view.txt_result.controls.append(
            ft.Text(f"🚀 TOP {n_top} SINERGIE (LIFT ANALYSIS)", weight="bold", size=16, color="orange")
        )

        for i in range(min(n_top, len(migliori_sinergie))):
            u, v, lift, peso = migliori_sinergie[i]
            self._view.txt_result.controls.append(
                ft.Text(f"{u.card_name} + {v.card_name} -> Lift: {lift:.2f} (Insieme in {peso} deck)")
            )

        self._view.update_page()

    def handleConnettivita(self, e):
        if not self._model._graph.nodes:
            self._view.txt_result.controls.append(ft.Text("Errore: Il grafo non esiste!", color="red"))
            self._view.update_page()
            return

        n_comp, dim_max = self._model.get_connettivita_stats()

        self._view._txtNumCompConnesse.value = str(n_comp)
        self._view._txtDimMaxComp.value = str(dim_max)


        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text("📊 ANALISI STRUTTURALE DEL GRAFO", weight="bold", size=16, color="blue")
        )

        if n_comp == 1:
            messaggio = "Il meta è totalmente connesso: ogni carta può potenzialmente raggiungere le altre."
        else:
            messaggio = f"Il meta è frammentato in {n_comp} sottogruppi indipendenti."

        self._view.txt_result.controls.append(ft.Text(messaggio))

        # 5. Refresh della pagina
        self._view.update_page()


    def handleDettagli(self, e):
        pass


    def handleGeneraDeck(self):
        pass

    def riempiTendine(self):
        pass



