# 🧠 Preguntas Frecuentes y Fundamentos Técnicos - Búsquedas Informadas

Este documento resume las preguntas técnicas fundamentales sobre la implementación del **8-Puzzle**, explicadas de forma didáctica, clara y con la referencia exacta al código fuente.

---

## 1. 🧩 ¿Dónde y cómo se genera el tablero inicial y su solvabilidad?

**Pregunta técnica:** "¿Cómo se genera el tablero inicial y cómo se garantiza matemáticamente que tenga solución?"

**Respuesta conceptual:** 
El tablero se genera creando una lista de números del 0 al 8 (donde el 0 representa la casilla vacía) y desordenándolos de forma pseudoaleatoria. Posteriormente, el estado pasa por una validación analítica de paridad de inversiones. En un tablero de 3×3, una configuración es resoluble si y solo si la cantidad de inversiones es un número par. Si resulta impar, el generador descarta la configuración y produce una nueva hasta obtener un estado válido solvable.

**Referencia en el código:**
- **Archivo:** `nucleo/ambiente.py`
- **Función:** `generar_estado_aleatorio()` (ciclo de generación y verificación).
- **Validación matemática:** `es_resoluble(estado)` (cálculo de inversiones).

---

## 2. 🎨 ¿Cómo se representa y actualiza el tablero en la interfaz gráfica?

**Pregunta técnica:** "¿Qué arquitectura y componentes gráficos se emplean para visualizar el tablero y su animación?"

**Respuesta conceptual:** 
La interfaz gráfica está construida sobre `tkinter` y `ttk`. El tablero de 3×3 se compone de una cuadrícula de 9 botones (`tk.Button`) estilizados. Durante la animación de la solución encontrada, el motor gráfico recorre secuencialmente la lista de estados generados por el algoritmo, actualizando en cada intervalo de tiempo el texto, posición y color de las fichas (mostrando la casilla vacía cuando el valor es 0).

**Referencia en el código:**
- **Archivo:** `visualizador/aplicacion.py`
- **Construcción visual:** `_crear_pestana_agente()` (instanciación de widgets).
- **Actualización dinámica:** `_actualizar_tablero(estado)` y el despachador de animación `_paso_animacion()`.

---

## 3. 🔍 ¿Cuál es la diferencia fundamental entre el Algoritmo A* y la Búsqueda Voraz?

**Pregunta técnica:** "¿Por qué A* garantiza la solución óptima mientras que Búsqueda Voraz no lo hace?"

**Respuesta conceptual:** 
- **Algoritmo A*:** Evalúa los nodos mediante la función de evaluación integral $f(n) = g(n) + h(n)$, balanceando el costo acumulado desde el origen $g(n)$ con la estimación heurística a la meta $h(n)$. Al utilizar una heurística admisible y consistente, garantiza encontrar el camino de menor costo (óptimo).
- **Búsqueda Voraz (Greedy Best-First):** Utiliza únicamente la función heurística $f(n) = h(n)$. Es miope respecto al camino recorrido; prioriza únicamente la proximidad aparente al objetivo, lo que puede derivar en soluciones subóptimas o mayor exploración en mínimos locales.

**Referencia en el código:**
- **A*:** `algoritmos/a_estrella.py` (cálculo acumulativo de `nuevo_g = nodo_actual.costo_g + 1` y evaluación de costos).
- **Voraz:** `algoritmos/voraz.py` (asignación directa de prioridad `hijo.f = h`, omitiendo el costo acumulado $g$).

---

## 4. 📏 Heurísticas: Distancia Manhattan vs. Piezas Descolocadas

**Pregunta técnica:** "¿Cómo se calculan ambas heurísticas y cuál presenta mayor dominancia?"

**Respuesta conceptual:** 
- **Piezas Descolocadas ($h_1$):** Cuenta la cantidad de fichas que no ocupan su posición final en el estado objetivo.
- **Distancia Manhattan ($h_2$):** Calcula la suma de las distancias horizontales y verticales (norma $L_1$) requeridas para que cada ficha alcance su coordenada meta:
  $$\sum |x_i - x_{meta}| + |y_i - y_{meta}|$$
- **Dominancia:** Para cualquier estado $n$, se cumple que $h_2(n) \ge h_1(n)$ y ambas son admisibles (nunca sobreestiman el costo real). En consecuencia, Manhattan domina a Piezas Descolocadas, permitiendo que A* pode una cantidad sustancialmente mayor de nodos del árbol de búsqueda.

**Referencia en el código:**
- **Archivo:** `nucleo/ambiente.py`
- **Funciones:** `piezas_descolocadas(estado)` y `distancia_manhattan(estado)`.

---

## 5. 🗂️ Estructura de Datos de la Frontera (Lista de Abiertos)

**Pregunta técnica:** "¿Por qué se utiliza una Cola de Prioridad en lugar de una lista o pila estándar?"

**Respuesta conceptual:** 
Tanto A* como Voraz requieren expandir en cada iteración el nodo más prometedor según su función de evaluación $f(n)$. Una lista FIFO (cola) daría búsqueda en anchura, y LIFO (pila) daría búsqueda en profundidad. La `ColaPrioridad` garantiza la extracción eficiente del nodo con el menor valor de $f(n)$ (`extraer_minimo()`).

**Referencia en el código:**
- **Archivo:** `nucleo/estructuras.py`
- **Clase:** `ColaPrioridad`, implementando inserción y extracción lineal por costo mínimo.

---

## 6. 🔄 Control de Movimientos Válidos y Transición de Estados

**Pregunta técnica:** "¿Cómo valida el entorno los movimientos legales para evitar desbordamiento del tablero?"

**Respuesta conceptual:** 
El espacio vacío (0) se ubica en el arreglo unidimensional mediante su índice, determinando sus coordenadas matriciales $(fila, columna)$ con `idx // 3` y `idx % 3`. Se validan las cotas de la grilla de $3\times3$ ($fila \in [0, 2]$, $columna \in [0, 2]$) antes de generar cualquier permutación sucesora, asegurando que solo se generen estados alcanzables válidos.

**Referencia en el código:**
- **Archivo:** `nucleo/ambiente.py`
- **Función:** `obtener_sucesores()`.
