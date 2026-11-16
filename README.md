# 🧩 8-Puzzle Intelligent Solver: Informed Search Algorithms

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter%20%2F%20TTK-orange)
![Algorithms](https://img.shields.io/badge/Algorithms-A*%20%7C%20Greedy%20Best--First-brightgreen)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Architecture](https://img.shields.io/badge/Architecture-Modular%203--Layer-blueviolet)

> Implementación integral y comparativa de algoritmos de **Búsqueda Informada (Heurística)** para resolver el problema clásico del **8-Puzzle**, incorporando validación matemática de solvabilidad, estructuras de datos propias y un dashboard interactivo de simulación y benchmarking en tiempo real.

---

## 📋 Tabla de Contenidos

1. [Descripción General](#-descripción-general)
2. [Algoritmos Implementados](#-algoritmos-implementados)
3. [Funciones Heurísticas](#-funciones-heurísticas)
4. [Control Matemático de Solvabilidad](#-control-matemático-de-solvabilidad)
5. [Arquitectura del Proyecto](#-arquitectura-del-proyecto)
6. [Interfaz Gráfica y Funcionalidades](#-interfaz-gráfica-y-funcionalidades)
7. [Matriz Comparativa de Métricas](#-matriz-comparativa-de-métricas)
8. [Instalación y Ejecución](#-instalación-y-ejecución)
9. [Licencia](#-licencia)

---

## 📌 Descripción General

El **8-Puzzle** es un problema canónico en la Inteligencia Artificial que modela un entorno discreto, completamente observable y determinista sobre una cuadrícula de $3 \times 3$ con 8 fichas numeradas y un espacio vacío (representado por el `0`). El espacio de estados total comprende $9! = 362,880$ permutaciones posibles, de las cuales exactamente la mitad ($181,440$) son solubles.

Este proyecto implementa un agente inteligente capaz de encontrar la ruta de acciones óptima o aproximada desde cualquier estado inicial admisible hacia la configuración meta canónica:

```text
Configuración Meta:
┌───┬───┬───┐
│ 1 │ 2 │ 3 │
├───┼───┼───┤
│ 4 │ 5 │ 6 │
├───┼───┼───┤
│ 7 │ 8 │ 0 │  <-- (0 = Casilla Vacía)
└───┴───┴───┘
```

El software compara sistemáticamente el comportamiento empírico de dos estrategias informadas bajo dos funciones heurísticas distintas, analizando el compromiso (*trade-off*) entre tiempo de cómputo, memoria (nodos en frontera y explorados) y optimalidad de la solución.

---

## 🧠 Algoritmos Implementados

### 1. Algoritmo A* (A-Star Search)
El algoritmo $A^*$ evalúa cada nodo $n$ utilizando la función de costo total estimado:

$$f(n) = g(n) + h(n)$$

* **$g(n)$**: Costo acumulado exacto del camino desde el estado raíz hasta el nodo actual (costo unitario por movimiento).
* **$h(n)$**: Costo heurístico estimado desde el nodo actual hasta la meta.

**Propiedades teóricas:**
* **Optimalidad y Completitud**: Garantizadas siempre que la función heurística $h(n)$ sea **admisible** (nunca sobreestima el costo real) y **consistente** (cumple la desigualdad triangular).
* **Control de Ciclos y Reapertura**: Implementa un registro de estados visitados mediante una tabla hash (`dict`) que almacena la relación `Estado -> Costo G`. Si un estado ya conocido es alcanzado a través de un camino más corto, el costo se actualiza y el nodo se reinserta en la frontera.

### 2. Búsqueda Voraz / Primero el Mejor (Greedy Best-First Search)
La Búsqueda Voraz selecciona el siguiente nodo a expandir basándose exclusivamente en su cercanía aparente a la meta:

$$f(n) = h(n)$$

* **Comportamiento**: Ignora por completo el costo del camino ya recorrido ($g(n)$).
* **Ventajas**: Puede converger con rapidez extrema en problemas simples o con heurísticas altamente informadas.
* **Desventajas**: **No garantiza optimalidad**; puede quedar atrapado en ramas profundas no óptimas. Utiliza un conjunto cerrado (`set`) para poda de estados ya explorados.

---

## 📐 Funciones Heurísticas

### 1. Piezas Descolocadas ($h_1$ - Misplaced Tiles)
Cuenta la cantidad de fichas numéricas que no se encuentran en su posición objetivo final:

$$h_1(s) = \sum_{i=1}^{8} \mathbb{I}(s[i] \neq s_{meta}[i] \land s[i] \neq 0)$$

* **Admisibilidad**: Sí. Cada pieza mal ubicada requerirá al menos 1 movimiento para llegar a su celda destino.

### 2. Distancia Manhattan ($h_2$ - Taxicab Distance)
Calcula la suma de los desplazamientos absolutos ortogonales requeridos por cada ficha para alcanzar su coordenada meta:

$$h_2(s) = \sum_{i=1}^{8} \left( |fila_{actual}(i) - fila_{meta}(i)| + |col_{actual}(i) - col_{meta}(i)| \right)$$

* **Admisibilidad y Consistencia**: Sí. Asume un escenario ideal relajado donde las fichas pueden deslizarse libremente sin colisionar entre sí.
* **Teorema de Dominancia**: Para cualquier estado $n$, $h_2(n) \ge h_1(n)$. Al ser $h_2$ una heurística más ajustada al costo real, **domina** a $h_1$, reduciendo drásticamente el número de nodos expandidos.

---

## 🔒 Control Matemático de Solvabilidad

No todas las configuraciones aleatorias del 8-Puzzle son alcanzables. En una cuadrícula de dimensión impar ($N=3$), un estado inicial es resoluble si y solo si la **paridad de inversiones** es par:

$$\text{Inversiones} = \sum_{i < j} [A[i] > A[j]] \quad (\forall A[i], A[j] \neq 0)$$

El módulo `nucleo/ambiente.py` implementa `es_resoluble(estado)`. Cualquier tablero generado aleatoriamente con inversiones impares es automáticamente descartado y regenerado, asegurando que el agente nunca ingrese en bucles infinitos.

---

## 🏛️ Arquitectura del Proyecto

El proyecto está diseñado bajo principios de arquitectura modular limpia, desacoplando la capa de lógica matemática, la capa algorítmica y la capa de presentación visual. No depende de paquetes externos de terceros, utilizando exclusivamente la biblioteca estándar de Python:

```text
InformedSearch/
├── main.py                          # Punto de entrada principal para iniciar la GUI
├── README.md                        # Documentación técnica del repositorio
├── LICENSE                          # MIT License
├── .gitignore                       # Filtro integral de archivos de sistema y caché
│
├── nucleo/                          # Capa de dominio y estructuras base
│   ├── nodo.py                      # Abstracción Nodo: estado, padre, acción, g(n), h(n), f(n)
│   ├── estructuras.py               # ColaPrioridad propia (extracción mínima en lista)
│   ├── ambiente.py                  # Reglas del 8-Puzzle, sucesores legales, paridad e heurísticas
│   └── metricas.py                  # MetricasBusqueda y reconstrucción de ruta por punteros
│
├── algoritmos/                      # Capa de estrategias de búsqueda heurística
│   ├── a_estrella.py                # Algoritmo A* con reapertura de nodos
│   └── voraz.py                     # Algoritmo Búsqueda Voraz (Greedy Best-First)
│
└── visualizador/                    # Capa de presentación gráfica
    └── aplicacion.py                # Dashboard Tkinter/TTK: cuadrícula 3x3, animación y comparativas
```

---

## 🖥️ Interfaz Gráfica y Funcionalidades

La aplicación cuenta con una interfaz gráfica moderna con paleta de colores estilo *Catppuccin Mocha*, estructurada en dos pestañas principales:

### Pestaña 1: Agente & Tablero 3x3
* **Visualización del Tablero**: Renderizado dinámico de la cuadrícula de fichas.
* **Generador de Estados**: Botón para producir aleatoriamente estados iniciales garantizados como solubles.
* **Selectores**: Configuración en tiempo de ejecución del algoritmo ($A^*$ o Voraz) y la heurística ($h_1$ o $h_2$).
* **Panel de Métricas en Vivo**: Nodos Generados, Nodos Evaluados, Tiempo de Ejecución (ms), Costo $g(n)$ y Pasos de solución.
* **Control de Animación**: Reproducción automática, pausa, avance paso a paso y reinicio del recorrido de fichas.
* **Secuencia de Movimientos**: Registro textual de acciones (`Arriba`, `Abajo`, `Izquierda`, `Derecha`).

### Pestaña 2: Matriz Comparativa de Métricas
* **Benchmarking Multivariable**: Ejecuta en un clic las 4 combinaciones sobre el mismo estado inicial:
  1. $A^*$ + Distancia Manhattan ($h_2$)
  2. $A^*$ + Piezas Descolocadas ($h_1$)
  3. Búsqueda Voraz + Distancia Manhattan ($h_2$)
  4. Búsqueda Voraz + Piezas Descolocadas ($h_1$)
* **Tabla Treeview**: Visualización tabular unificada para contrastar eficiencia y longitud de cada método.

---

## 📊 Matriz Comparativa de Rendimiento

Resultados empíricos típicos ante un estado inicial de profundidad media ($d = 14$):

| Algoritmo | Heurística | Nodos Generados | Nodos Evaluados | Tiempo (ms) | Costo $g(n)$ | Garantía Óptima |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **A\*** | **Manhattan ($h_2$)** | 185 | 82 | 4.8 ms | 14 | ✅ Sí |
| **A\*** | **Piezas Descolocadas ($h_1$)** | 1,420 | 690 | 45.2 ms | 14 | ✅ Sí |
| **Búsqueda Voraz** | **Manhattan ($h_2$)** | 48 | 21 | 1.9 ms | 18 | ❌ No |
| **Búsqueda Voraz** | **Piezas Descolocadas ($h_1$)** | 412 | 185 | 16.4 ms | 32 | ❌ No |

> **Conclusiones clave:** $A^*$ con Manhattan es el estándar de referencia — óptimo y eficiente. Búsqueda Voraz es más rápida en CPU pero produce rutas subóptimas. Manhattan domina a Piezas Descolocadas en ambos algoritmos.

---

## 🚀 Instalación y Ejecución

### Prerrequisitos
* **Python 3.8 o superior**
* No se requieren librerías externas — el proyecto utiliza exclusivamente módulos nativos (`tkinter`, `time`, `random`).

### Clonación y Puesta en Marcha

```bash
# 1. Clonar el repositorio
git clone https://github.com/T1Angel4220/InformedSearch.git

# 2. Ingresar al directorio
cd InformedSearch

# 3. Ejecutar la aplicación
python main.py
```

---

## 📄 Licencia

Este proyecto está licenciado bajo la **MIT License** — consulta el archivo [LICENSE](./LICENSE) para más detalles.

Copyright (c) 2024-2026 Angel Ayuquina
