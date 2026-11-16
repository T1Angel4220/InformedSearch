# Análisis de `nucleo/metricas.py`

Este archivo define la clase `MetricasBusqueda`, que es como la "caja negra" o el sistema de telemetría de nuestros algoritmos. Se encarga de recolectar toda la información de rendimiento para luego poder imprimirla y compararla en la tabla del informe.

## Código línea por línea

```python
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
```
Inicializa todas las métricas en 0 o vacío. 
- **Nodos generados:** Cuántos Nodos creamos en memoria (mide consumo de RAM).
- **Nodos evaluados (expandidos):** A cuántos nodos les aplicamos la función sucesor (mide esfuerzo de CPU).

```python
    def reconstruir_ruta(self, nodo_final):
```
Este método es vital. Los algoritmos no guardan todo el camino en la memoria principal (sería muy ineficiente). Solo guardan punteros hacia atrás (`nodo.padre`). Cuando el algoritmo llega al `nodo_final` (la meta), llama a este método para ir "retrocediendo" hasta encontrar el inicio y descubrir cuál fue la ruta.

```python
        acciones = []
        estados = []
        actual = nodo_final
        while actual is not None:
            estados.append(actual.estado)
            if actual.accion is not None:
                acciones.append(actual.accion)
            actual = actual.padre
```
Empieza en el final. Mientras el nodo `actual` no sea `None` (recordemos que el `padre` de la raíz era `None`), extrae qué acción se tomó para llegar ahí y cuál es el estado de ese nodo. Luego, salta hacia atrás haciendo `actual = actual.padre`.
Como saltamos de la Meta hacia el Inicio, las listas quedarán guardadas al revés (de fin a principio).

```python
        estados.reverse()
        acciones.reverse()
```
Soluciona el problema de inversión. Ahora las listas están de Principio a Fin.

```python
        self.ruta_estados = estados
        self.ruta_acciones = acciones
        self.longitud_solucion = len(acciones)
        self.costo_camino = nodo_final.costo_g
        self.exito = True
```
Finalmente, empaqueta los resultados en los atributos de la clase y marca `exito = True` para avisar a la interfaz gráfica que encontramos la solución óptima.
