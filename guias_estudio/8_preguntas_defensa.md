# 🎓 Guía de Preguntas Técnicas y Fundamentos Teóricos

Este documento contiene un banco exhaustivo de preguntas técnicas sobre Inteligencia Artificial y Algoritmos de Búsqueda Informada aplicados al 8-Puzzle, con sus justificaciones matemáticas y correspondencia en la implementación.

---

### 1. "A ver, muéstrame exactamente en qué línea de código A* se diferencia de Búsqueda Voraz."
**Respuesta ideal:** 
"La diferencia principal está en la función de evaluación $f(n)$. En el archivo `a_estrella.py` (líneas 31 y 36), calculamos `nuevo_g = nodo_actual.costo_g + 1` y al crear el hijo pasamos ese costo. El nodo internamente suma $f = g + h$. 
En cambio, si vamos a `voraz.py` (línea 36), después de crear el hijo, sobrescribimos explícitamente su valor con `hijo.f = h`. Esto hace que la Cola de Prioridad en Voraz ignore por completo el costo pasado $g$ y se vuelva 'ciega' al esfuerzo acumulado."

### 2. "¿Por qué A* usa un Diccionario (`dict`) para los nodos visitados y Voraz usa un Conjunto (`set`)?"
**Respuesta ideal:**
"En Búsqueda Voraz no nos importa el costo, solo queremos llegar rápido. Así que si ya pasamos por un estado, lo guardamos en un `set` (línea 19 de `voraz.py`) y si lo volvemos a ver, lo ignoramos.
Pero A* busca la ruta **óptima**. Es posible que lleguemos a un estado por un camino largo, y más tarde encontremos un atajo hacia ese mismo estado. Por eso usamos un `dict` (línea 18 de `a_estrella.py`) que mapea `Estado -> Costo G`. Si volvemos a ver un estado, pero el nuevo costo `nuevo_g` es **menor** que el que teníamos guardado, actualizamos el diccionario y volvemos a meter el nodo a la frontera (reapertura de nodos)."

### 3. "¿Cómo demuestras que tus heurísticas son Admisibles? ¿Qué pasa si no lo fueran?"
**Respuesta ideal:**
"Una heurística es admisible si **nunca sobreestima** el costo real para llegar a la meta. 
En mi código, en `ambiente.py`:
- $h_1$ (Piezas Descolocadas) es admisible porque cada pieza fuera de lugar requerirá, como absoluto mínimo, 1 movimiento para arreglarse.
- $h_2$ (Manhattan) es admisible porque calcula los movimientos rectos necesarios si las piezas pudieran 'atravesarse' unas a otras. Es el camino mínimo teórico ideal.
Si una heurística no fuera admisible (sobreestimara), A* perdería su garantía matemática de optimalidad, y podría devolvernos rutas más largas."

### 4. "¿Por qué Manhattan ($h_2$) explora menos nodos que Piezas Descolocadas ($h_1$)? Demuéstralo."
**Respuesta ideal:**
"Porque la heurística Manhattan **domina** a la de Piezas Descolocadas. Matemáticamente, para cualquier estado $n$, se cumple que $h_2(n) \geq h_1(n)$. Al dar un valor más cercano al costo real (es más 'informada'), Manhattan poda muchísimas más ramas del árbol de búsqueda que $h_1$. En nuestras métricas, vemos que A* con $h_1$ genera miles de nodos, mientras que con $h_2$ genera apenas unos cientos."

### 5. "Veo que implementaste tu propia `ColaPrioridad` con una lista. ¿Cuál es su complejidad al extraer el mínimo y por qué no usaste `heapq`?"
**Respuesta ideal:**
"Implementé la cola desde cero en `estructuras.py` por requerimiento académico, para demostrar el control sobre la estructura subyacente. Al usar una lista desordenada, la inserción es rápida $O(1)$, pero mi método `extraer_minimo()` hace una búsqueda lineal mediante un ciclo `for` (línea 15), por lo que tiene una complejidad de $O(n)$ en el peor de los casos. 
En un entorno de producción o para un puzzle más grande (como el 15-Puzzle), lo correcto sería usar un montículo binario (`heapq`), lo cual reduciría la extracción a $O(\log n)$."

### 6. "¿Cómo sabe tu programa que el puzzle generado aleatoriamente se puede resolver? Porque si no, se quedaría en un bucle infinito."
**Respuesta ideal:**
"Lo prevengo en `ambiente.py` usando el teorema de la **Paridad de Inversiones**. En el método `es_resoluble`, saco todas las piezas (ignorando el cero) y cuento cuántas veces un número mayor está antes que un número menor en la lectura lineal. El puzzle de $3\times3$ es matemáticamente resoluble **solo si** ese número de inversiones es **par**. El generador de estados aleatorios (`generar_estado_aleatorio`) rechaza cualquier tablero que sea impar antes de siquiera pasárselo a la interfaz."

### 7. "Una vez que A* llega a la meta, ¿dónde y cómo saca la lista de movimientos ('Arriba', 'Abajo', etc.)?"
**Respuesta ideal:**
"Ningún algoritmo guarda la lista completa de acciones por cada nodo, porque colapsaría la memoria RAM (el árbol crece exponencialmente). 
En su lugar, cada `Nodo` guarda un puntero a su `padre` y la `accion` que lo generó.
Cuando llegamos a la meta, se llama a `reconstruir_ruta` en `metricas.py` (línea 12). Este método usa un ciclo `while` para viajar hacia atrás por los punteros `actual.padre` hasta llegar a la raíz. Como esto nos da la ruta al revés (de Meta a Inicio), aplicamos `.reverse()` a las listas al final para tener la secuencia correcta de movimientos."
