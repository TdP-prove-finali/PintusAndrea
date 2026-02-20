import flet as ft


class View:
    def __init__(self, page: ft.Page):
        self._page = page
        self._page.title = "Analisi Avanzata Clash Royale"
        self._page.theme_mode = ft.ThemeMode.DARK
        self._page.bgcolor = "#0b0e14"
        self._page.window_width = 1300
        self._page.window_height = 900

        self._controller = None


        self._txtRangeTrofei = ft.RangeSlider(
            min=0,
            max=9000,
            start_value=4000,
            end_value=8000,
            divisions=18,
            label="{value}",  # Usa 'label' invece di 'label_format'
            inactive_color="white24"
        )
        self._txtMaxBattaglie = ft.TextField(label="Max Battaglie", value="1000", border_color="cyan", width=150)

        # Statistiche Grafo
        self._txtNodi = ft.Text("0", size=25, weight="bold", color="cyan")
        self._txtArchi = ft.Text("0", size=25, weight="bold", color="cyan")

        # --- 2. Analisi Connettività e Classifiche ---
        self._ddTopN = ft.Dropdown(
            label="Visualizza Top-N",
            options=[ft.dropdown.Option(str(i)) for i in [5, 10, 20]],
            value="10", width=120
        )
        self._txtNumCompConnesse = ft.Text("0", size=25, weight="bold", color="orange")
        self._txtDimMaxComp = ft.Text("0", size=25, weight="bold", color="orange")

        # --- 3. Generazione Guidata Deck (Ricorsione) ---
        self._ddSeedCard = ft.Dropdown(label="Carta Seed", border_color="orange", expand=True)
        self._sliderProfondita = ft.Slider(min=1, max=8, value=8, divisions=7, label="Profondità: {value}")
        self._sliderSogliaPeso = ft.Slider(min=0, max=1, value=0.5, divisions=10, label="Soglia Peso: {value}")
        self._txtTopCandidati = ft.TextField(label="Top-N per passo", value="3", width=120)

        # Area Risultati (ListView per i deck generati e le classifiche)
        self.txt_result = ft.ListView(expand=True, spacing=10, padding=10, auto_scroll=False)

    def load_interface(self):
        # Header
        header = ft.Container(
            content=ft.Row([
                ft.Icon(ft.icons.QUERY_STATS, color="cyan", size=35),
                ft.Text("CLASH ROYALE DECK ANALYZER", size=28, weight="bold", font_family="Verdana"),
            ]),
            margin=ft.margin.only(bottom=20)
        )

        # Sidebar: Input e Controlli
        sidebar = ft.Container(
            width=380,
            bgcolor="#1a1f26",
            border_radius=15,
            padding=20,
            content=ft.Column([
                ft.Text("1. ESTRAZIONE E GRAFO", weight="bold", color="cyan"),
                ft.Text("Range Trofei:", size=12),
                self._txtRangeTrofei,
                self._txtMaxBattaglie,
                ft.ElevatedButton("Costruisci Grafo", icon=ft.icons.GITE_OUTLINED,
                                  on_click=self._controller.handleCreaGrafo, width=380, bgcolor="cyan", color="black"),

                ft.Divider(height=20, color="white10"),

                ft.Text("2. ANALISI E CLASSIFICHE", weight="bold", color="cyan"),
                ft.Row([self._ddTopN,
                        ft.ElevatedButton("Ranking/Centralità", on_click=self._controller.handleAnalisi, expand=True)]),
                ft.Row([
                    ft.TextButton("Confidenza/Lift", icon=ft.icons.ANALYTICS,
                                  on_click=self._controller.handleAdvancedRank),
                    ft.TextButton("Connettività", icon=ft.icons.HUB, on_click=self._controller.handleConnettivita),
                ]),

                ft.Divider(height=20, color="white10"),

                ft.Text("3. GENERAZIONE DECK (RICORSIONE)", weight="bold", color="orange"),
                self._ddSeedCard,
                ft.Text("Parametri Algoritmo:", size=12),
                self._sliderProfondita,
                self._sliderSogliaPeso,
                self._txtTopCandidati,
                ft.ElevatedButton("Genera Deck Candidati", icon=ft.icons.PLAY_FOR_WORK,
                                  on_click=self._controller.handleGeneraDeck, width=380, bgcolor="orange",
                                  color="black"),
            ], spacing=10, scroll=ft.ScrollMode.ADAPTIVE)
        )

        # Griglia Statistiche Superiori
        stats_row = ft.Row([
            self._create_card("NODI", self._txtNodi),
            self._create_card("ARCHI", self._txtArchi),
            self._create_card("COMP. CONNESSE", self._txtNumCompConnesse),
            self._create_card("MAX COMP.", self._txtDimMaxComp),
        ], spacing=10)

        # Pannello Risultati
        results_panel = ft.Container(
            expand=True,
            bgcolor="#1a1f26",
            border_radius=15,
            padding=15,
            content=ft.Column([
                ft.Row([
                    ft.Text("OUTPUT ANALISI E DECK SUGGERITI", weight="bold"),
                    ft.IconButton(ft.icons.DELETE_SWEEP, on_click=lambda _: self.txt_result.controls.clear())
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(color="white10"),
                self.txt_result
            ])
        )

        # Layout finale
        self._page.add(
            header,
            ft.Row([
                sidebar,
                ft.Column([stats_row, results_panel], expand=True)
            ], expand=True)
        )

        self._controller.riempiTendine()
        self._page.update()

    def _create_card(self, label, value_obj):
        return ft.Container(
            expand=1,
            bgcolor="#1a1f26",
            padding=10,
            border_radius=12,
            border=ft.border.all(1, "white10"),
            content=ft.Column([
                ft.Text(label, size=10, color="white54", weight="bold"),
                value_obj
            ], horizontal_alignment="center", spacing=2)
        )

    def set_controller(self, controller):
        self._controller = controller

    def update_page(self):
        self._page.update()