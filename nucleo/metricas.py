class MetricasBusqueda:
    def __init__(self):
        self.nodos_generados = 0
        self.nodos_evaluados = 0
        self.tiempo_ejecucion_ms = 0.0
        self.costo_camino = 0
        self.longitud_solucion = 0
        self.ruta_acciones = []
        self.ruta_estados = []
        self.exito = False

    def reconstruir_ruta(self, nodo_final):
        acciones = []
        estados = []
        actual = nodo_final
        while actual is not None:
            estados.append(actual.estado)
            if actual.accion is not None:
                acciones.append(actual.accion)
            actual = actual.padre
        estados.reverse()
        acciones.reverse()
        self.ruta_estados = estados
        self.ruta_acciones = acciones
        self.longitud_solucion = len(acciones)
        self.costo_camino = nodo_final.costo_g
        self.exito = True
