import time
from nucleo.nodo import Nodo
from nucleo.estructuras import ColaPrioridad
from nucleo.ambiente import Ambiente8Puzzle
from nucleo.metricas import MetricasBusqueda

def busqueda_a_estrella(estado_inicial, funcion_heuristica):
    inicio_tiempo = time.perf_counter()
    metricas = MetricasBusqueda()

    h_0 = funcion_heuristica(estado_inicial)
    nodo_raiz = Nodo(estado_inicial, None, None, 0, h_0)

    frontera = ColaPrioridad()
    frontera.insertar(nodo_raiz)
    metricas.nodos_generados += 1

    visitados = {estado_inicial: 0}

    while not frontera.esta_vacia():
        nodo_actual = frontera.extraer_minimo()
        metricas.nodos_evaluados += 1

        if Ambiente8Puzzle.es_meta(nodo_actual.estado):
            fin_tiempo = time.perf_counter()
            metricas.tiempo_ejecucion_ms = (fin_tiempo - inicio_tiempo) * 1000.0
            metricas.reconstruir_ruta(nodo_actual)
            return metricas

        for accion, nuevo_estado in Ambiente8Puzzle.obtener_sucesores(nodo_actual.estado):
            nuevo_g = nodo_actual.costo_g + 1

            if nuevo_estado not in visitados or nuevo_g < visitados[nuevo_estado]:
                visitados[nuevo_estado] = nuevo_g
                h = funcion_heuristica(nuevo_estado)
                hijo = Nodo(nuevo_estado, nodo_actual, accion, nuevo_g, h)
                frontera.insertar(hijo)
                metricas.nodos_generados += 1

    fin_tiempo = time.perf_counter()
    metricas.tiempo_ejecucion_ms = (fin_tiempo - inicio_tiempo) * 1000.0
    return metricas
