# 🏃‍♂️ Explicación a Prueba de Balas: Algoritmo de Búsqueda Voraz (`voraz.py`)

Este documento explica **línea por línea** y de forma súper sencilla qué hace exactamente el archivo `algoritmos/voraz.py`.

La **Búsqueda Voraz** (Greedy Best-First Search) es como un conductor desesperado: solo le importa **qué tan cerca parece estar** de su destino (la heurística), y no le importa si ya ha dado muchas vueltas para llegar ahí (el costo del camino).

---

## 1. Importaciones (Trayendo las herramientas)

```python
import time
from nucleo.nodo import Nodo
from nucleo.estructuras import ColaPrioridad
from nucleo.ambiente import Ambiente8Puzzle
from nucleo.metricas import MetricasBusqueda
```
**¿Qué hace esto?**
- `time`: Nos sirve para usar un cronómetro y medir cuántos milisegundos se demora el algoritmo en encontrar la solución.
- `Nodo`: Es la estructura que guarda la "fotografía" de un estado del tablero, quién es su padre (el movimiento anterior), qué jugada lo llevó ahí, y sus costos.
- `ColaPrioridad`: Es la fila VIP. En lugar de sacar al que llegó primero, saca al que tiene la prioridad más alta (el costo `f` más pequeño).
- `Ambiente8Puzzle`: Trae las reglas del juego (saber si ganamos, cuáles son los movimientos válidos).
- `MetricasBusqueda`: Es nuestra libreta de notas para llevar la cuenta de cuántos nodos creamos, cuánto tardamos y cuántos pasos dimos.

---

## 2. Empezando el Algoritmo

```python
def busqueda_voraz(estado_inicial, funcion_heuristica):
    inicio_tiempo = time.perf_counter()
    metricas = MetricasBusqueda()
```
- **Línea 7:** Creamos la función principal. Recibe dos cosas:
  - `estado_inicial`: El tablero desordenado con el que empezamos.
  - `funcion_heuristica`: La fórmula matemática para adivinar "qué tan lejos estamos de ganar" (Manhattan o Piezas Descolocadas).
- **Líneas 8-9:** Prendemos el cronómetro (`inicio_tiempo`) y alistamos la libreta de anotaciones (`metricas`).

---

## 3. Preparando el Nodo Inicial (La Raíz)

```python
    h_0 = funcion_heuristica(estado_inicial)
    nodo_raiz = Nodo(estado_inicial, None, None, 0, h_0)
    nodo_raiz.f = h_0
```
- **Línea 11:** Calculamos la "pista" inicial (`h_0`). Por ejemplo, si usamos piezas descolocadas, miramos el tablero original y decimos "hay 7 piezas mal puestas".
- **Línea 12:** Creamos el primer "Nodo". Como es el inicial, no tiene padre (`None`), no hubo acción para llegar ahí (`None`), el costo de pasos dados es `0`, y su heurística es `h_0`.
- **Línea 13 (¡CRÍTICO!):** `nodo_raiz.f = h_0`. Aquí definimos que **la prioridad de este nodo es ÚNICAMENTE su heurística**. El algoritmo voraz ignora cuántos pasos dio (`g`), solo le importa qué tan cerca parece estar (`h`). 

---

## 4. Configurando la "Fila VIP" y la "Lista Negra"

```python
    frontera = ColaPrioridad()
    frontera.insertar(nodo_raiz)
    metricas.nodos_generados += 1

    visitados = {estado_inicial}
```
- **Línea 15-17:** Creamos la Cola de Prioridad (`frontera`), metemos el nodo inicial ahí, y anotamos en la libreta que hemos generado 1 nodo.
- **Línea 19:** `visitados` es nuestra lista negra (un Set). Si un tablero ya está en esta lista, significa que ya lo vimos y **NO debemos volver a revisarlo** para evitar dar vueltas en círculos infinitamente.

---

## 5. El Bucle Principal (Pensando y Jugando)

```python
    while not frontera.esta_vacia():
        nodo_actual = frontera.extraer_minimo()
        metricas.nodos_evaluados += 1
```
- **Línea 21:** El código se va a repetir **mientras haya nodos en la fila VIP**. Si la fila se vacía y no ganamos, significa que es imposible resolverlo.
- **Línea 22:** Aquí ocurre la magia. `extraer_minimo()` busca en la frontera el nodo que tenga el valor `f` más bajito (el que parece estar más cerca de ganar) y lo saca para analizarlo.
- **Línea 23:** Anotamos en la libreta que evaluamos un nodo más.

---

## 6. ¿Ganamos?

```python
        if Ambiente8Puzzle.es_meta(nodo_actual.estado):
            fin_tiempo = time.perf_counter()
            metricas.tiempo_ejecucion_ms = (fin_tiempo - inicio_tiempo) * 1000.0
            metricas.reconstruir_ruta(nodo_actual)
            return metricas
```
- **Línea 25:** Pregunta al ambiente: "¿Este tablero es el objetivo (1,2,3,4,5,6,7,8,0)?".
- **Líneas 26-29:** Si ganamos, apagamos el cronómetro, calculamos los milisegundos transcurridos, ordenamos a las `metricas` que reconstruyan el camino (yendo de padre en padre desde el nodo final hasta el inicial) y devolvemos las notas finales para que se muestren en pantalla.

---

## 7. Si no ganamos, buscar las siguientes jugadas

```python
        for accion, nuevo_estado in Ambiente8Puzzle.obtener_sucesores(nodo_actual.estado):
            if nuevo_estado not in visitados:
                visitados.add(nuevo_estado)
                h = funcion_heuristica(nuevo_estado)
                hijo = Nodo(nuevo_estado, nodo_actual, accion, nodo_actual.costo_g + 1, h)
                hijo.f = h
                frontera.insertar(hijo)
                metricas.nodos_generados += 1
```
- **Línea 31:** Si no hemos ganado, pedimos los posibles movimientos legales (`obtener_sucesores`). Por cada movimiento posible (ej. "Mover Arriba"), nos da la acción y cómo quedaría el tablero (`nuevo_estado`).
- **Línea 32:** Preguntamos: "¿Ya revisamos este tablero alguna vez en el pasado?". Si no lo hemos revisado, entramos.
- **Línea 33:** Lo metemos a la lista negra (`visitados`) para no volver a pasar por aquí.
- **Línea 34:** Le calculamos su heurística (`h`). "Si muevo esta pieza, ¿ahora cuántas me faltan?".
- **Línea 35:** Creamos el nodo "hijo". Sabemos de dónde vino (`nodo_actual`), qué acción tomamos (`accion`), y su cantidad de pasos dados sube en 1 (`costo_g + 1`).
- **Línea 36 (¡MAGIA VORAZ!):** `hijo.f = h`. Igual que antes, sobrescribimos su costo total (`f`). Ignoramos los pasos dados (`g`) y decimos "tu valor total es solo tu heurística `h`".
- **Líneas 37-38:** Lo metemos a la Fila VIP (`frontera`) para que el programa decida más tarde si es buena idea explorarlo, y anotamos en la libreta que generamos otro nodo.

---

## 8. ¿Qué pasa si no hay solución?

```python
    fin_tiempo = time.perf_counter()
    metricas.tiempo_ejecucion_ms = (fin_tiempo - inicio_tiempo) * 1000.0
    return metricas
```
- **Líneas 40-42:** Si el bucle `while` termina y nunca entró al `if` de ganar (la fila VIP se vació sin hallar la respuesta), el código llega acá. Apaga el cronómetro, anota el tiempo, y devuelve las métricas. Como no se llamó a `reconstruir_ruta`, las métricas dirán "Fracaso" y no habrá ruta que dibujar.
