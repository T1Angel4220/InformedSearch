# Análisis de `nucleo/ambiente.py`

Este archivo contiene la lógica de negocio pura del problema del 8-Puzzle. En IA, esto se conoce como el **Entorno** (Environment) o el **Modelo de Transición**. Define qué es el juego, cuáles son las reglas, cómo se mueve y cómo se calculan los costos.

## Concepto Teórico

Separar el ambiente del algoritmo es una buena práctica (Arquitectura Limpia). El algoritmo (A* o Voraz) no necesita saber si está jugando al 8-Puzzle, ajedrez o buscando una ruta en un mapa. Solo necesita pedirle al ambiente: "¿Es esta la meta?", "¿Cuáles son los hijos de este nodo?", "¿Cuál es el valor heurístico?".

## Código línea por línea

```python
import random

class Ambiente8Puzzle:
    ESTADO_OBJETIVO = (1, 2, 3, 4, 5, 6, 7, 8, 0)
```
Importa `random` para mezclar el tablero inicial. Se define `ESTADO_OBJETIVO` como una constante de clase (tupla). `0` representa el espacio vacío.

```python
    @staticmethod
    def es_resoluble(estado):
```
`@staticmethod` significa que no necesitamos instanciar la clase (`Ambiente8Puzzle()`) para usar este método. Lo usamos directamente `Ambiente8Puzzle.es_resoluble(...)`.

```python
        inversiones = 0
        lista_fichas = [f for f in estado if f != 0]
        for i in range(len(lista_fichas)):
            for j in range(i + 1, len(lista_fichas)):
                if lista_fichas[i] > lista_fichas[j]:
                    inversiones += 1
        return inversiones % 2 == 0
```
**Concepto Clave (Paridad de Inversiones):** No todos los tableros del 8-Puzzle tienen solución. Si desarmas físicamente el rompecabezas y lo armas al azar, tienes 50% de probabilidad de que sea imposible de resolver. 
Para saber si es posible matemáticamente, extraemos todas las piezas (ignorando el `0`). Luego contamos las "inversiones" (cuántas veces un número mayor aparece antes que un número menor). Si el número de inversiones es **par** (`inversiones % 2 == 0`), el puzzle tiene solución. Si es impar, es imposible.

```python
    @staticmethod
    def generar_estado_aleatorio():
        fichas = list(range(9))
        while True:
            random.shuffle(fichas)
            estado = tuple(fichas)
            if estado != Ambiente8Puzzle.ESTADO_OBJETIVO and Ambiente8Puzzle.es_resoluble(estado):
                return estado
```
Crea una lista de 0 a 8. Entra en un bucle infinito donde la desordena al azar (`shuffle`). Si el tablero desordenado NO es ya la meta, y SÍ es resoluble (verificando la paridad), devuelve el tablero. Si no, vuelve a intentarlo.

```python
    @staticmethod
    def es_meta(estado):
        return estado == Ambiente8Puzzle.ESTADO_OBJETIVO
```
Función booleana sencilla que los algoritmos llaman para saber si ya ganaron.

```python
    @staticmethod
    def obtener_sucesores(estado):
        sucesores = []
        idx = estado.index(0)
        fila = idx // 3
        col = idx % 3
```
Aquí generamos el árbol. Primero, encuentra dónde está el vacío `0` (`idx`). Luego calcula su fila (`// 3` división entera) y columna (`% 3` módulo). Como es un arreglo 1D (tupla de 9 elementos), estas matemáticas lo mapean a un grid imaginario de 3x3.

```python
        movimientos = []
        if fila > 0: movimientos.append(("Arriba", idx - 3))
        if fila < 2: movimientos.append(("Abajo", idx + 3))
        if col > 0: movimientos.append(("Izquierda", idx - 1))
        if col < 2: movimientos.append(("Derecha", idx + 1))
```
El vacío solo se puede mover Arriba si no está en la fila 0 superior (`fila > 0`). Si se mueve Arriba, en el arreglo unidimensional eso equivale a restar 3 a su índice. Hace lo mismo para todas las direcciones, controlando no salirse de los bordes.

```python
        for accion, nuevo_idx in movimientos:
            nuevo_estado = list(estado)
            nuevo_estado[idx], nuevo_estado[nuevo_idx] = nuevo_estado[nuevo_idx], nuevo_estado[idx]
            sucesores.append((accion, tuple(nuevo_estado)))
        return sucesores
```
Ejecuta los movimientos. Como las tuplas son inmutables, la convierte a lista, intercambia (swap) el vacío con la pieza correspondiente, y lo vuelve a convertir a tupla para devolverlo junto con la acción (ej. `("Arriba", (1,2...))`).

```python
    @staticmethod
    def piezas_descolocadas(estado):
        descolocadas = 0
        for i in range(9):
            if estado[i] != 0 and estado[i] != Ambiente8Puzzle.ESTADO_OBJETIVO[i]:
                descolocadas += 1
        return descolocadas
```
**Heurística 1 ($h_1$):** Compara el estado actual con la meta. Si la pieza en el índice `i` no es 0 (ignoramos el vacío) y no coincide con la pieza en la meta en ese mismo índice `i`, suma 1 al contador de descolocadas.

```python
    @staticmethod
    def distancia_manhattan(estado):
        distancia = 0
        for idx, valor in enumerate(estado):
            if valor != 0:
                fila_actual = idx // 3
                col_actual = idx % 3
                idx_meta = valor - 1
                fila_meta = idx_meta // 3
                col_meta = idx_meta % 3
                distancia += abs(fila_actual - fila_meta) + abs(col_actual - col_meta)
        return distancia
```
**Heurística 2 ($h_2$):** Es mucho mejor ("domina" a $h_1$). Por cada pieza (que no sea el 0), calcula en qué fila/columna está. Luego calcula en qué fila/columna *debería* estar (`idx_meta = valor - 1`, ej. la pieza 1 va en el índice 0). Finalmente suma la distancia en "bloques de ciudad" (valor absoluto de la diferencia en X más la diferencia en Y).
