import tkinter as tk
from tkinter import ttk, messagebox

from nucleo.ambiente import Ambiente8Puzzle
from algoritmos.voraz import busqueda_voraz
from algoritmos.a_estrella import busqueda_a_estrella

class AplicacionPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("Agente de Búsqueda Informada - 8 Puzzle")
        self.root.geometry("1050x700")
        self.root.configure(bg="#1e1e2e")

        self.estado_actual = Ambiente8Puzzle.generar_estado_aleatorio()
        self.ruta_estados = [self.estado_actual]
        self.ruta_acciones = []
        self.indice_animacion = 0
        self.animando = False

        self._configurar_estilos()
        self._crear_interfaz()
        self._actualizar_tablero(self.estado_actual)

    def _configurar_estilos(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.style.configure("TNotebook", background="#1e1e2e", borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#313244", foreground="#cdd6f4", padding=[12, 6], font=("Segoe UI", 10, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", "#45475a")], foreground=[("selected", "#89b4fa")])

        self.style.configure("TLabelframe", background="#1e1e2e", foreground="#cdd6f4", borderwidth=1, relief="solid")
        self.style.configure("TLabelframe.Label", background="#1e1e2e", foreground="#89b4fa", font=("Segoe UI", 11, "bold"))

        self.style.configure("TLabel", background="#1e1e2e", foreground="#cdd6f4", font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#cdd6f4")
        self.style.configure("Metric.TLabel", font=("Segoe UI", 10, "bold"), foreground="#a6e3a1")

        self.style.configure("TButton", background="#45475a", foreground="#cdd6f4", font=("Segoe UI", 10, "bold"), borderwidth=0, padding=6)
        self.style.map("TButton", background=[("active", "#585b70")])

        self.style.configure("Primary.TButton", background="#89b4fa", foreground="#11111b", font=("Segoe UI", 10, "bold"), padding=8)
        self.style.map("Primary.TButton", background=[("active", "#b4befe")])

        self.style.configure("Treeview", background="#313244", foreground="#cdd6f4", fieldbackground="#313244", rowheight=28, font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", background="#45475a", foreground="#89b4fa", font=("Segoe UI", 10, "bold"))

    def _crear_interfaz(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        tab_agente = ttk.Frame(notebook)
        tab_comparativa = ttk.Frame(notebook)

        notebook.add(tab_agente, text="Agente & Tablero 3x3")
        notebook.add(tab_comparativa, text="Matriz Comparativa de Métricas")

        self._crear_pestana_agente(tab_agente)
        self._crear_pestana_comparativa(tab_comparativa)

    def _crear_pestana_agente(self, parent):
        frame_izq = ttk.Frame(parent)
        frame_izq.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        frame_der = ttk.Frame(parent)
        frame_der.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        lbl_titulo = ttk.Label(frame_izq, text="Estado del Tablero 3x3", style="Header.TLabel")
        lbl_titulo.pack(pady=(0, 10))

        self.frame_grid = tk.Frame(frame_izq, bg="#181825", bd=4, relief="ridge")
        self.frame_grid.pack(pady=10)

        self.botones_tablero = []
        for i in range(9):
            row = i // 3
            col = i % 3
            btn = tk.Button(
                self.frame_grid,
                text="",
                font=("Segoe UI", 24, "bold"),
                width=5,
                height=2,
                bd=2,
                relief="raised",
                bg="#313244",
                fg="#cdd6f4",
                activebackground="#45475a",
                activeforeground="#cdd6f4"
            )
            btn.grid(row=row, column=col, padx=4, pady=4)
            self.botones_tablero.append(btn)

        frame_anim = ttk.LabelFrame(frame_izq, text="Control de Animación de Ruta")
        frame_anim.pack(fill="x", pady=10)

        btn_prev = ttk.Button(frame_anim, text="Anterior", command=self._paso_anterior)
        btn_prev.pack(side="left", padx=5, pady=5)

        self.btn_play = ttk.Button(frame_anim, text="Reproducir", command=self._toggle_animacion)
        self.btn_play.pack(side="left", padx=5, pady=5)

        btn_next = ttk.Button(frame_anim, text="Siguiente", command=self._paso_siguiente)
        btn_next.pack(side="left", padx=5, pady=5)

        btn_reset = ttk.Button(frame_anim, text="Reiniciar", command=self._reiniciar_animacion)
        btn_reset.pack(side="left", padx=5, pady=5)

        self.lbl_paso_actual = ttk.Label(frame_anim, text="Paso: 0 / 0", style="Metric.TLabel")
        self.lbl_paso_actual.pack(side="right", padx=10)

        frame_config = ttk.LabelFrame(frame_der, text="Configuración del Agente")
        frame_config.pack(fill="x", pady=(0, 10))

        btn_aleatorio = ttk.Button(frame_config, text="Generar Estado Aleatorio Resoluble", command=self._generar_aleatorio)
        btn_aleatorio.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_config, text="Algoritmo de Búsqueda:").pack(anchor="w", padx=10, pady=(5, 2))
        self.combo_algoritmo = ttk.Combobox(frame_config, values=["Algoritmo A*", "Búsqueda Voraz"], state="readonly")
        self.combo_algoritmo.current(0)
        self.combo_algoritmo.pack(fill="x", padx=10, pady=2)

        ttk.Label(frame_config, text="Función Heurística:").pack(anchor="w", padx=10, pady=(5, 2))
        self.combo_heuristica = ttk.Combobox(frame_config, values=["Distancia Manhattan (h2)", "Piezas Descolocadas (h1)"], state="readonly")
        self.combo_heuristica.current(0)
        self.combo_heuristica.pack(fill="x", padx=10, pady=2)

        btn_ejecutar = ttk.Button(frame_config, text="Resolver 8-Puzzle", style="Primary.TButton", command=self._ejecutar_busqueda)
        btn_ejecutar.pack(fill="x", padx=10, pady=10)

        frame_metricas = ttk.LabelFrame(frame_der, text="Métricas de Ejecución")
        frame_metricas.pack(fill="x", pady=10)

        self.lbl_generados = ttk.Label(frame_metricas, text="Nodos Generados: -")
        self.lbl_generados.pack(anchor="w", padx=10, pady=2)

        self.lbl_evaluados = ttk.Label(frame_metricas, text="Nodos Evaluados: -")
        self.lbl_evaluados.pack(anchor="w", padx=10, pady=2)

        self.lbl_tiempo = ttk.Label(frame_metricas, text="Tiempo de Ejecución: - ms")
        self.lbl_tiempo.pack(anchor="w", padx=10, pady=2)

        self.lbl_costo = ttk.Label(frame_metricas, text="Costo de Camino g(n): -")
        self.lbl_costo.pack(anchor="w", padx=10, pady=2)

        self.lbl_pasos = ttk.Label(frame_metricas, text="Pasos de Solución: -")
        self.lbl_pasos.pack(anchor="w", padx=10, pady=2)

        frame_ruta = ttk.LabelFrame(frame_der, text="Secuencia de Movimientos de la Ruta")
        frame_ruta.pack(fill="both", expand=True, pady=10)

        self.txt_ruta = tk.Text(frame_ruta, height=6, bg="#313244", fg="#cdd6f4", font=("Consolas", 10), bd=0)
        self.txt_ruta.pack(fill="both", expand=True, padx=5, pady=5)

    def _crear_pestana_comparativa(self, parent):
        frame_top = ttk.Frame(parent)
        frame_top.pack(fill="x", padx=10, pady=10)

        btn_comparar = ttk.Button(frame_top, text="Ejecutar Comparativa Completa de Métricas", style="Primary.TButton", command=self._ejecutar_comparativa)
        btn_comparar.pack(side="left")

        lbl_info = ttk.Label(frame_top, text="Evalúa las 4 combinaciones posibles en el estado inicial actual")
        lbl_info.pack(side="left", padx=15)

        columnas = ("algoritmo", "heuristica", "generados", "evaluados", "tiempo", "costo", "pasos")
        self.tabla_comparativa = ttk.Treeview(parent, columns=columnas, show="headings", height=10)

        self.tabla_comparativa.heading("algoritmo", text="Algoritmo")
        self.tabla_comparativa.heading("heuristica", text="Heurística")
        self.tabla_comparativa.heading("generados", text="Nodos Generados")
        self.tabla_comparativa.heading("evaluados", text="Nodos Evaluados")
        self.tabla_comparativa.heading("tiempo", text="Tiempo (ms)")
        self.tabla_comparativa.heading("costo", text="Costo g(n)")
        self.tabla_comparativa.heading("pasos", text="Pasos")

        self.tabla_comparativa.column("algoritmo", width=140, anchor="center")
        self.tabla_comparativa.column("heuristica", width=180, anchor="center")
        self.tabla_comparativa.column("generados", width=130, anchor="center")
        self.tabla_comparativa.column("evaluados", width=130, anchor="center")
        self.tabla_comparativa.column("tiempo", width=120, anchor="center")
        self.tabla_comparativa.column("costo", width=100, anchor="center")
        self.tabla_comparativa.column("pasos", width=100, anchor="center")

        self.tabla_comparativa.pack(fill="both", expand=True, padx=10, pady=10)

        lbl_explicacion = ttk.Label(
            parent,
            text="Nota Teórica: A* con Distancia Manhattan garantiza optimalidad (menor costo g(n)) expandiendo el menor número de nodos debido al carácter admisible y dominante de h2.",
            font=("Segoe UI", 9, "italic"),
            foreground="#89b4fa"
        )
        lbl_explicacion.pack(pady=5)

    def _actualizar_tablero(self, estado):
        for i, val in enumerate(estado):
            btn = self.botones_tablero[i]
            if val == 0:
                btn.config(text="", bg="#181825", state="disabled")
            else:
                btn.config(text=str(val), bg="#89b4fa" if val % 2 == 0 else "#b4befe", fg="#11111b", state="normal")

    def _generar_aleatorio(self):
        self.animando = False
        self.estado_actual = Ambiente8Puzzle.generar_estado_aleatorio()
        self.ruta_estados = [self.estado_actual]
        self.ruta_acciones = []
        self.indice_animacion = 0
        self._actualizar_tablero(self.estado_actual)
        self.lbl_paso_actual.config(text="Paso: 0 / 0")
        self.txt_ruta.delete("1.0", tk.END)

    def _obtener_heuristica_seleccionada(self):
        if "Manhattan" in self.combo_heuristica.get():
            return Ambiente8Puzzle.distancia_manhattan
        return Ambiente8Puzzle.piezas_descolocadas

    def _ejecutar_busqueda(self):
        func_h = self._obtener_heuristica_seleccionada()
        nombre_alg = self.combo_algoritmo.get()

        if nombre_alg == "Algoritmo A*":
            res = busqueda_a_estrella(self.estado_actual, func_h)
        else:
            res = busqueda_voraz(self.estado_actual, func_h)

        if not res.exito:
            messagebox.showerror("Error", "No se encontró solución para este estado.")
            return

        self.ruta_estados = res.ruta_estados
        self.ruta_acciones = res.ruta_acciones
        self.indice_animacion = 0

        self.lbl_generados.config(text=f"Nodos Generados: {res.nodos_generados}")
        self.lbl_evaluados.config(text=f"Nodos Evaluados: {res.nodos_evaluados}")
        self.lbl_tiempo.config(text=f"Tiempo de Ejecución: {res.tiempo_ejecucion_ms:.2f} ms")
        self.lbl_costo.config(text=f"Costo de Camino g(n): {res.costo_camino}")
        self.lbl_pasos.config(text=f"Pasos de Solución: {res.longitud_solucion}")
        self.lbl_paso_actual.config(text=f"Paso: 0 / {len(self.ruta_acciones)}")

        self.txt_ruta.delete("1.0", tk.END)
        self.txt_ruta.insert(tk.END, "Ruta de Solución Recomendada:\n")
        self.txt_ruta.insert(tk.END, " -> ".join(["Inicio"] + res.ruta_acciones))

        self._actualizar_tablero(self.ruta_estados[0])

    def _paso_siguiente(self):
        if self.indice_animacion < len(self.ruta_estados) - 1:
            self.indice_animacion += 1
            self._actualizar_tablero(self.ruta_estados[self.indice_animacion])
            self.lbl_paso_actual.config(text=f"Paso: {self.indice_animacion} / {len(self.ruta_acciones)}")

    def _paso_anterior(self):
        if self.indice_animacion > 0:
            self.indice_animacion -= 1
            self._actualizar_tablero(self.ruta_estados[self.indice_animacion])
            self.lbl_paso_actual.config(text=f"Paso: {self.indice_animacion} / {len(self.ruta_acciones)}")

    def _reiniciar_animacion(self):
        self.animando = False
        self.btn_play.config(text="Reproducir")
        self.indice_animacion = 0
        if self.ruta_estados:
            self._actualizar_tablero(self.ruta_estados[0])
            self.lbl_paso_actual.config(text=f"Paso: 0 / {len(self.ruta_acciones)}")

    def _toggle_animacion(self):
        if self.animando:
            self.animando = False
            self.btn_play.config(text="Reproducir")
        else:
            if len(self.ruta_estados) <= 1:
                return
            self.animando = True
            self.btn_play.config(text="Pausar")
            self._bucle_animacion()

    def _bucle_animacion(self):
        if not self.animando:
            return
        if self.indice_animacion < len(self.ruta_estados) - 1:
            self._paso_siguiente()
            self.root.after(400, self._bucle_animacion)
        else:
            self.animando = False
            self.btn_play.config(text="Reproducir")

    def _ejecutar_comparativa(self):
        for item in self.tabla_comparativa.get_children():
            self.tabla_comparativa.delete(item)

        combinaciones = [
            ("Algoritmo A*", "Distancia Manhattan (h2)", busqueda_a_estrella, Ambiente8Puzzle.distancia_manhattan),
            ("Algoritmo A*", "Piezas Descolocadas (h1)", busqueda_a_estrella, Ambiente8Puzzle.piezas_descolocadas),
            ("Búsqueda Voraz", "Distancia Manhattan (h2)", busqueda_voraz, Ambiente8Puzzle.distancia_manhattan),
            ("Búsqueda Voraz", "Piezas Descolocadas (h1)", busqueda_voraz, Ambiente8Puzzle.piezas_descolocadas),
        ]

        for alg_nom, heur_nom, func_alg, func_h in combinaciones:
            res = func_alg(self.estado_actual, func_h)
            self.tabla_comparativa.insert(
                "",
                "end",
                values=(
                    alg_nom,
                    heur_nom,
                    res.nodos_generados,
                    res.nodos_evaluados,
                    f"{res.tiempo_ejecucion_ms:.2f}",
                    res.costo_camino,
                    res.longitud_solucion
                )
            )
