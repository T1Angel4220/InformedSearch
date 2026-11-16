# Análisis de `algoritmos/voraz.py`

Este archivo contiene la implementación del algoritmo **Búsqueda Voraz (Greedy Best-First Search)**.

## Concepto Teórico

La Búsqueda Voraz es como una persona en un laberinto tratando de llegar al centro guiándose solo por su vista. Siempre toma el camino que *parece* acercarle más rápido al objetivo, sin importarle cuánto ha caminado ya.
Matemáticamente, su función de evaluación es $f(n) = h(n)$. Ignora completamente $g(n)$.
Por esto, **no es óptimo** y se puede equivocar si la heurística lo engaña llevándolo por un camino largo.

## Diferencias Clave con A* (Línea por línea)

La estructura es casi idéntica a `a_estrella.py`, pero con dos diferencias fundamentales en la lógica:

```python
    h_0 = funcion_heuristica(estado_inicial)
    nodo_raiz = Nodo(estado_inicial, None, None, 0, h_0)
    nodo_raiz.f = h_0
```
**Diferencia 1:** Por defecto, la clase `Nodo` calcula `f = g + h`. Aquí, en Voraz, sobrescribimos explícitamente `nodo_raiz.f = h_0` (o sea, `f = h`). Obligamos a la Cola de Prioridad a ordenar los nodos solo fijándose en quién tiene la heurística más pequeña.

```python
    visitados = {estado_inicial}
```
**Diferencia 2:** En A*, usábamos un *diccionario* porque nos importaba recordar *cuánto nos costó* llegar a un estado para ver si luego encontrábamos un camino más barato. En Voraz, solo usamos un *conjunto (`set`)*. Si ya visitamos un estado, simplemente no volvemos a pasar por ahí. No nos importa si ahora es más barato o más caro, solo queremos avanzar hacia la meta sin retroceder o pensar en costos.

```python
        for accion, nuevo_estado in Ambiente8Puzzle.obtener_sucesores(nodo_actual.estado):
            if nuevo_estado not in visitados:
                visitados.add(nuevo_estado)
```
Como solo usamos un `set`, la condición para expandir un hijo es muy simple: "¿Ya lo vi antes? Si no, lo agrego a visitados y lo pongo en la frontera".
No hay lógica de "reapertura de nodos" ni de comparación de costos.

```python
                h = funcion_heuristica(nuevo_estado)
                hijo = Nodo(nuevo_estado, nodo_actual, accion, nodo_actual.costo_g + 1, h)
                hijo.f = h
                frontera.insertar(hijo)
```
Al crear el hijo, volvemos a aplicar la Diferencia 1: sobrescribimos `hijo.f = h` para asegurar que el algoritmo se mantenga miope y voraz, fijándose solo en $h$.

## Conclusión
Voraz es un algoritmo "ansioso". Es más simple que A* y a veces puede encontrar una solución muy rápido (explorando menos nodos), pero frecuentemente encuentra caminos mucho más largos y sub-óptimos porque no planifica considerando el esfuerzo acumulado.
