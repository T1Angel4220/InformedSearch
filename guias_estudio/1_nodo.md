# Análisis de `nucleo/nodo.py`

Este archivo es la base estructural del árbol de búsqueda. En Inteligencia Artificial, un "estado" (la configuración del tablero) no es lo mismo que un "nodo". Un nodo envuelve al estado y añade metadatos necesarios para que los algoritmos de búsqueda funcionen (como saber de dónde vino y cuánto costó llegar ahí).

## Código línea por línea

```python
class Nodo:
```
Define la clase principal `Nodo`. Un objeto de esta clase representará un punto específico en el árbol de exploración.

```python
    def __init__(self, estado, padre=None, accion=None, costo_g=0, heuristica_h=0):
```
Es el constructor (inicializador) de la clase. Recibe todos los datos necesarios para crear un nodo. 
- `estado`: La tupla que representa el tablero (ej. `(1,2,3,4,5,6,7,8,0)`). Es el único parámetro obligatorio.
- `padre=None`: Apunta al nodo del cual se derivó este nodo. Por defecto es `None` (para el estado inicial o raíz).
- `accion=None`: Qué movimiento se hizo desde el `padre` para llegar a este estado (ej. "Arriba").
- `costo_g=0`: El costo acumulado desde el inicio hasta este nodo.
- `heuristica_h=0`: El valor estimado desde este nodo hasta la meta (calculado por las funciones heurísticas).

```python
        self.estado = estado
        self.padre = padre
        self.accion = accion
        self.costo_g = costo_g
        self.heuristica_h = heuristica_h
```
Estas líneas simplemente toman los parámetros que llegaron en el constructor y los guardan como atributos (`self.xxx`) de la instancia para que puedan ser accedidos después.

```python
        self.f = costo_g + heuristica_h
```
**Concepto Clave:** Aquí se calcula la **función de evaluación $f(n)$**. En la búsqueda informada:
- $g(n)$ es el costo pasado (`costo_g`).
- $h(n)$ es el costo futuro estimado (`heuristica_h`).
- $f(n) = g(n) + h(n)$ es el costo total estimado de la ruta que pasa por este nodo. Este valor es el que usan los algoritmos (especialmente A*) para decidir qué nodo expandir primero.

```python
    def __lt__(self, otro):
```
Este es un **método mágico** o especial de Python (significa *less than*, o "menor que" `<`). Permite enseñar a Python cómo comparar dos objetos de tipo `Nodo`. 

```python
        return self.f < otro.f
```
Le dice a Python: "Un nodo es 'menor' que otro si su valor `f` es más pequeño". 
**¿Por qué es esto importante?** Porque cuando metamos muchos Nodos en nuestra Cola de Prioridad, el algoritmo necesitará saber cuál es el "mejor" (el más pequeño) para sacarlo primero. Sin esta función, Python no sabría cómo ordenar objetos de la clase `Nodo`.
