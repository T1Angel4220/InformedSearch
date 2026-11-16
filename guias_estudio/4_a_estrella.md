# Análisis de `algoritmos/a_estrella.py`

Este archivo contiene la implementación del **Algoritmo A* (A-Star)**, uno de los algoritmos de búsqueda más famosos en Inteligencia Artificial por sus propiedades matemáticas de completitud y optimalidad.

## Concepto Teórico

A* es una evolución del algoritmo de Dijkstra. Mientras Dijkstra explora en todas direcciones buscando el camino más corto (basado solo en $g(n)$), A* usa una brújula (la heurística $h(n)$) para enfocar su búsqueda hacia la meta.
La función que dirige A* es $f(n) = g(n) + h(n)$. 

Para que A* sea óptimo, su heurística debe ser **admisible** (nunca debe ser pesimista/nunca debe sobreestimar el costo real).

## Código línea por línea

```python
import time
from nucleo.nodo import Nodo
from nucleo.estructuras import ColaPrioridad
from nucleo.ambiente import Ambiente8Puzzle
from nucleo.metricas import MetricasBusqueda
```
Importamos todas las piezas que construimos en la capa `nucleo` y el módulo `time` para medir milisegundos.

```python
def busqueda_a_estrella(estado_inicial, funcion_heuristica):
```
Es la función principal. Recibe el tablero de inicio y, muy importante, **recibe la función heurística como parámetro** (`funcion_heuristica`). Esto es programación funcional; le pasamos la "receta" de cómo calcular $h$ para que el algoritmo sea genérico.

```python
    inicio_tiempo = time.perf_counter()
    metricas = MetricasBusqueda()
```
Arrancamos el cronómetro de alta precisión y preparamos el objeto donde guardaremos los resultados (nodos generados, etc.).

```python
    h_0 = funcion_heuristica(estado_inicial)
    nodo_raiz = Nodo(estado_inicial, None, None, 0, h_0)
```
Creamos el nodo "semilla". Llamamos a la heurística con el estado inicial. Al crear el `Nodo`, su `padre` es `None`, su `accion` es `None`, y su `costo_g` (pasado) es 0 porque apenas estamos empezando.

```python
    frontera = ColaPrioridad()
    frontera.insertar(nodo_raiz)
    metricas.nodos_generados += 1
```
Inicializamos la frontera (la lista de nodos por explorar) e insertamos nuestra semilla. Contamos que hemos "generado" (creado en memoria) 1 nodo.

```python
    visitados = {estado_inicial: 0}
```
**Concepto Clave:** Este diccionario guarda qué estados hemos visto y **cuánto nos costó llegar ahí**. En búsquedas en grafos (no en árboles), puedes llegar al mismo estado por múltiples caminos. Guardar esto evita ciclos infinitos. Se mapea la tupla del estado a su `costo_g`.

```python
    while not frontera.esta_vacia():
```
El bucle principal. Se repite mientras haya nodos por explorar.

```python
        nodo_actual = frontera.extraer_minimo()
        metricas.nodos_evaluados += 1
```
Sacamos el "mejor" nodo de la frontera (el de menor $f(n)$). "Evaluar" o "Expandir" significa sacarlo de la frontera para ver a sus hijos.

```python
        if Ambiente8Puzzle.es_meta(nodo_actual.estado):
            fin_tiempo = time.perf_counter()
            metricas.tiempo_ejecucion_ms = (fin_tiempo - inicio_tiempo) * 1000.0
            metricas.reconstruir_ruta(nodo_actual)
            return metricas
```
Si el estado de este nodo es el objetivo, ¡hemos ganado! Paramos el tiempo, usamos `reconstruir_ruta()` (que viajará por los `nodo.padre` hacia atrás hasta la raíz para sacar la lista de acciones) y retornamos las métricas.

```python
        for accion, nuevo_estado in Ambiente8Puzzle.obtener_sucesores(nodo_actual.estado):
```
Si no es la meta, le pedimos al `Ambiente` que nos diga a dónde podemos movernos desde aquí.

```python
            nuevo_g = nodo_actual.costo_g + 1
```
Calculamos el costo para llegar al hijo. Como en el 8-Puzzle cada movimiento cuesta 1, el $g$ del hijo es simplemente el $g$ del padre + 1.

```python
            if nuevo_estado not in visitados or nuevo_g < visitados[nuevo_estado]:
```
**El corazón de A* (Reapertura de nodos):**
Decidimos si este hijo vale la pena. Solo lo agregamos a la frontera sí:
1. Nunca habíamos visto este tablero antes (`not in visitados`).
2. O lo habíamos visto, pero el camino que acabamos de encontrar es **más barato** (`nuevo_g < visitados[nuevo_estado]`). Esto garantiza la optimalidad.

```python
                visitados[nuevo_estado] = nuevo_g
                h = funcion_heuristica(nuevo_estado)
                hijo = Nodo(nuevo_estado, nodo_actual, accion, nuevo_g, h)
                frontera.insertar(hijo)
                metricas.nodos_generados += 1
```
Si vale la pena, actualizamos el diccionario de visitados con el nuevo mejor costo. Calculamos su heurística, creamos el `Nodo` envolviendo todos estos datos, lo metemos a la `frontera` y contamos que generamos un nodo más.

```python
    fin_tiempo = time.perf_counter()
    metricas.tiempo_ejecucion_ms = (fin_tiempo - inicio_tiempo) * 1000.0
    return metricas
```
Si el bucle `while` termina sin encontrar la meta (la frontera se vació), significa que no hay solución. Calculamos el tiempo y retornamos las métricas vacías.
