# Análisis de `nucleo/estructuras.py`

Este archivo contiene la implementación de la estructura de datos que controla qué nodos se deben explorar a continuación: la **Cola de Prioridad** (también conocida como "Frontera" en los algoritmos de búsqueda).

## Concepto Teórico

En una búsqueda como BFS (Anchura), se usa una cola FIFO (primero en entrar, primero en salir). En DFS (Profundidad), se usa una Pila LIFO. 
En **Búsqueda Informada (Voraz o A*)**, necesitamos una **Cola de Prioridad**. Esto significa que los nodos no salen en el orden en que entraron, sino **basado en quién tiene el menor valor de $f(n)$**.

Para evitar usar librerías externas que hacen esto automáticamente (como `heapq`), aquí se implementa "desde cero" usando una lista estándar y un algoritmo de búsqueda lineal.

## Código línea por línea

```python
class ColaPrioridad:
    def __init__(self):
        self.elementos = []
```
Define la clase y su constructor. Inicializa `self.elementos` como una lista vacía `[]`. Esta lista actuará como el contenedor de todos los nodos descubiertos que aún no han sido explorados.

```python
    def esta_vacia(self):
        return len(self.elementos) == 0
```
Un método auxiliar simple. Devuelve `True` si la longitud de la lista es 0 (no hay nodos por explorar). Esto es vital porque el algoritmo principal se detiene (da error de "no hay solución") si la frontera se queda vacía.

```python
    def insertar(self, nodo):
        self.elementos.append(nodo)
```
Agrega un nuevo nodo al final de la lista. En este diseño, la lista se mantiene desordenada. Es en el momento de *extraer* cuando buscamos el mejor. (En estructuras avanzadas como los *Heaps Binarios*, la lista se ordena al insertar).

```python
    def extraer_minimo(self):
        if self.esta_vacia():
            return None
```
Es el método más importante. Intenta sacar el nodo con menor costo. Si la lista está vacía, devuelve `None` para evitar un error.

```python
        indice_minimo = 0
```
Asume temporalmente que el primer nodo de la lista (índice 0) es el que tiene el menor costo $f$.

```python
        for i in range(1, len(self.elementos)):
```
Inicia un bucle `for` que va desde el segundo elemento (índice 1) hasta el final de la lista. Esta es una **búsqueda lineal**. Su complejidad es $O(n)$, lo que significa que a medida que la lista crece, se vuelve más lento buscar el mínimo.

```python
            if self.elementos[i].f < self.elementos[indice_minimo].f:
                indice_minimo = i
```
Aquí está la magia. Compara el valor $f$ del nodo en la posición actual `i` (`self.elementos[i].f`) con el valor $f$ del nodo que creíamos era el mínimo (`self.elementos[indice_minimo].f`). 
Si encuentra uno más pequeño, actualiza `indice_minimo` con la nueva posición ganadora.

```python
        return self.elementos.pop(indice_minimo)
```
Una vez que el bucle termina, `indice_minimo` tiene la posición real del nodo con menor costo. `pop()` hace dos cosas al mismo tiempo: 
1. Elimina ese nodo de la lista.
2. Lo devuelve para que el algoritmo principal lo use.

```python
    def obtener_tamano(self):
        return len(self.elementos)
```
Simplemente devuelve cuántos elementos hay actualmente en la frontera. Útil para llevar estadísticas (métricas) o depurar.
