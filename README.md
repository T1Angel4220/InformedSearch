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
9. [Documentación Técnica Detallada](#-documentación-técnica-detallada)
10. [Créditos y Autores](#-créditos-y-autores)

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

* **$g(n)$**: Costo acumulado exacto del camino desde el estado raíz hasta el nodo actual (costo unitario por movimiento, $g(hijo) = g(padre) + 1$).
* **$h(n)$**: Costo heurístico estimado desde el nodo actual hasta la meta.

**Propiedades teóricas:**
* **Optimalidad y Completitud**: Garantizadas siempre que la función heurística $h(n)$ sea **admisible** (nunca sobreestima el costo real) y **consistente** (cumple la desigualdad triangular $h(n) \le c(n, a, n') + h(n')$).
* **Control de Ciclos y Reapertura**: Implementa un registro de estados visitados mediante una tabla hash (`dict`) que almacena la relación `Estado -> Costo G`. Si un estado ya conocido es alcanzado a través de un camino más corto ($g_{nuevo} < g_{previo}$), el costo se actualiza y el nodo se reinserta en la frontera.

### 2. Búsqueda Voraz / Primero el Mejor (Greedy Best-First Search)
La Búsqueda Voraz selecciona el siguiente nodo a expandir basándose exclusivamente en su cercanía aparente a la meta:

$$f(n) = h(n)$$

* **Comportamiento**: Ignora por completo el costo del camino ya recorrido ($g(n)$).
* **Ventajas**: Puede converger con rapidez extrema en problemas simples o con heurísticas altamente informadas.
* **Desventajas**: **No garantiza optimalidad**; puede quedar atrapado en ramas profundas no óptimas o mínimos locales antes de alcanzar la solución. Utiliza un conjunto cerrado (`set`) para poda de estados ya explorados.

---

## 📐 Funciones Heurísticas

### 1. Piezas Descolocadas ($h_1$ - Misplaced Tiles)
Cuenta la cantidad de fichas numéricas ($f_i \neq 0$) que no se encuentran en su posición objetivo final:

$$h_1(s) = \sum_{i=1}^{8} \mathbb{I}(s[i] \neq s_{meta}[i] \land s[i] \neq 0)$$

* **Admisibilidad**: Sí. Cada pieza mal ubicada requerirá al menos 1 movimiento para llegar a su celda destino.

### 2. Distancia Manhattan ($h_2$ - Taxicab Distance)
Calcula la suma de los desplazamientos absolutos ortogonales (horizontales y verticales en norma $L_1$) requeridos por cada ficha para alcanzar su coordenada meta:

$$h_2(s) = \sum_{i=1}^{8} \left( |fila_{actual}(i) - fila_{meta}(i)| + |col_{actual}(i) - col_{meta}(i)| \right)$$

* **Admisibilidad y Consistencia**: Sí. Asume un escenario ideal relajado donde las fichas pueden deslizarse libremente sin colisionar entre sí.
* **Teorema de Dominancia**: Para cualquier estado $n$:

$$h_2(n) \ge h_1(n)$$

Al ser $h_2$ una heurística más ajustada al costo real, **domina** a $h_1$, lo que matemáticamente asegura que $A^*$ con $h_2$ podará un espacio de búsqueda igual o mayor que con $h_1$, reduciendo drásticamente el número de nodos expandidos y el uso de memoria.

---

## 🔒 Control Matemático de Solvabilidad

No todas las configuraciones aleatorias del 8-Puzzle son alcanzables. En una cuadrícula de dimensión impar ($N=3$), un estado inicial es resoluble si y solo si la **paridad de inversiones** es par:

$$\text{Inversiones} = \sum_{i < j} [A[i] > A[j]] \quad (\forall A[i], A[j] \neq 0)$$

* **Inversión**: Se produce cuando una ficha con un número mayor precede linealmente a una ficha con un número menor en la lectura fila por fila del tablero.
* **Mecanismo**: El módulo `nucleo/ambiente.py` implementa `es_resoluble(estado)`. Cualquier tablero generado aleatoriamente con inversiones impares es automáticamente descartado y regenerado, asegurando que el agente nunca ingrese en bucles infinitos por estados matemáticamente insolubles.

---

## 🏛️ Arquitectura del Proyecto

El proyecto está diseñado bajo principios de arquitectura modular limpia, desacoplando la capa de lógica matemática, la capa algorítmica y la capa de presentación visual. No depende de paquetes externos de terceros, utilizando exclusivamente la biblioteca estándar de Python:

```text
InformedSearch/
├── main.py                          # Punto de entrada principal para iniciar la GUI
├── README.md                        # Documentación técnica completa del repositorio
├── .gitignore                       # Filtro integral de archivos de sistema, entorno y caché
│
├── nucleo/                          # Capa de dominio y estructuras base
│   ├── nodo.py                      # Abstracción Nodo: estado, padre, acción, g(n), h(n), f(n)
│   ├── estructuras.py               # ColaPrioridad propia (implementación de lista con extracción mínima)
│   ├── ambiente.py                  # Reglas del 8-Puzzle, sucesores legales, paridad e heurísticas
│   └── metricas.py                  # Objeto MetricasBusqueda y algoritmo de reconstrucción de ruta
│
├── algoritmos/                      # Capa de estrategias de búsqueda heurística
│   ├── a_estrella.py                # Algoritmo A* con reapertura de nodos
│   └── voraz.py                     # Algoritmo Búsqueda Voraz (Greedy Best-First)
│
├── visualizador/                    # Capa de presentación gráfica
│   └── aplicacion.py                # Dashboard Tkinter/TTK: cuadrícula 3x3, animación y comparativas
│
└── guias_estudio/                   # Documentación técnica complementaria y análisis
    ├── 1_nodo.md                    # Análisis detallado de nucleo/nodo.py
    ├── 2_estructuras.md             # Análisis de la Cola de Prioridad
    ├── 3_ambiente.md                # Lógica del entorno y operadores de movimiento
    ├── 4_a_estrella.md              # Desglose matemático y operacional de A*
    ├── 5_voraz.md                   # Desglose operacional de Búsqueda Voraz
    ├── 6_metricas.md                # Reconstrucción de la trayectoria óptima
    ├── 7_interfaz_grafica.md        # Arquitectura de eventos y renderizado Tkinter
    ├── 8_preguntas_defensa.md       # Banco de preguntas teóricas y defensa conceptual
    ├── explicacion_voraz.md         # Fundamentos y análisis de Búsqueda Voraz
    └── preguntas_profesor.md        # Preguntas técnicas frecuentes y respuestas de diseño
```

---

## 🖥️ Interfaz Gráfica y Funcionalidades

La aplicación cuenta con una interfaz gráfica moderna con paleta de colores estilo *Catppuccin Mocha*, estructurada en dos pestañas principales:

### Pestaña 1: Agente & Tablero 3x3
* **Visualización del Tablero**: Renderizado dinámico de la cuadrícula de fichas con identificación del espacio vacío.
* **Generador de Estados**: Botón para producir aleatoriamente estados iniciales garantizados como solubles.
* **Selectores**: Configuración en tiempo de ejecución del algoritmo ($A^*$ o Voraz) y la heurística ($h_1$ o $h_2$).
* **Panel de Métricas en Vivo**: Muestra en tiempo real:
  * Nodos Generados.
  * Nodos Evaluados (Expandidos).
  * Tiempo de Ejecución en milisegundos (`perf_counter`).
  * Costo acumulado del camino $g(n)$.
  * Cantidad de pasos en la solución.
* **Control de Animación**: Reproducción automática, pausa, avance paso a paso y reinicio del recorrido de fichas hacia la meta.
* **Secuencia de Movimientos**: Registro textual de la secuencia de acciones (`Arriba`, `Abajo`, `Izquierda`, `Derecha`).

### Pestaña 2: Matriz Comparativa de Métricas
* **Benchmarking Multivariable**: Ejecuta en un solo clic las 4 combinaciones posibles sobre el mismo estado inicial:
  1. $A^*$ + Distancia Manhattan ($h_2$)
  2. $A^*$ + Piezas Descolocadas ($h_1$)
  3. Búsqueda Voraz + Distancia Manhattan ($h_2$)
  4. Búsqueda Voraz + Piezas Descolocadas ($h_1$)
* **Tabla Treeview**: Visualización tabular unificada para contrastar directamente la eficiencia y la longitud del camino de cada método.

---

## 📊 Matriz Comparativa de Rendimiento

A continuación se ilustra un ejemplo de los resultados empíricos típicos generados por la aplicación ante un estado inicial de profundidad media ($d = 14$):

| Algoritmo | Heurística | Nodos Generados | Nodos Evaluados | Tiempo (ms) | Costo $g(n)$ | Pasos | Garantía Óptima |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **A\*** | **Manhattan ($h_2$)** | 185 | 82 | 4.8 ms | 14 | 14 | ✅ Sí |
| **A\*** | **Piezas Descolocadas ($h_1$)** | 1,420 | 690 | 45.2 ms | 14 | 14 | ✅ Sí |
| **Búsqueda Voraz** | **Manhattan ($h_2$)** | 48 | 21 | 1.9 ms | 18 | 18 | ❌ No (Subóptima) |
| **Búsqueda Voraz** | **Piezas Descolocadas ($h_1$)** | 412 | 185 | 16.4 ms | 32 | 32 | ❌ No (Subóptima) |

> **Conclusiones clave del análisis:**
> 1. $A^*$ con Manhattan es el estándar de referencia: encuentra la ruta estrictamente óptima evaluando una fracción de los nodos que requiere Piezas Descolocadas.
> 2. Búsqueda Voraz suele ser más veloz en tiempo de CPU al evaluar menos nodos, pero sus soluciones suelen tener caminos significativamente más largos (subóptimos).

---

## 🚀 Instalación y Ejecución

### Prerrequisitos
* **Python 3.8 o superior** (probado y optimizado en Python 3.10+).
* No se requieren librerías externas (`pip install` no es necesario), ya que todo se apoya en módulos nativos de Python (`tkinter`, `time`, `random`).

### Clonación y Puesta en Marcha

```bash
# 1. Clonar el repositorio
git clone https://github.com/T1Angel4220/InformedSearch.git

# 2. Ingresar al directorio del proyecto
cd InformedSearch

# 3. Ejecutar la aplicación
python main.py
```

---

## 📚 Documentación Técnica Detallada

En la carpeta [`guias_estudio/`](./guias_estudio/) se encuentra disponible un análisis exhaustivo del código y su fundamentación:
* [`1_nodo.md`](./guias_estudio/1_nodo.md): Explicación del envoltorio de estado y método `__lt__`.
* [`2_estructuras.md`](./guias_estudio/2_estructuras.md): Arquitectura de la `ColaPrioridad` y análisis de complejidad $O(n)$.
* [`3_ambiente.md`](./guias_estudio/3_ambiente.md): Modelado del espacio de estados y funciones heurísticas.
* [`4_a_estrella.md`](./guias_estudio/4_a_estrella.md): Implementación algorítmica de $A^*$ y gestión de frontera.
* [`5_voraz.md`](./guias_estudio/5_voraz.md): Funcionamiento de Greedy Best-First Search.
* [`6_metricas.md`](./guias_estudio/6_metricas.md): Reconstrucción inversa de la ruta por punteros de precedencia.
* [`7_interfaz_grafica.md`](./guias_estudio/7_interfaz_grafica.md): Arquitectura del frontend interactivo con Tkinter.
* [`8_preguntas_defensa.md`](./guias_estudio/8_preguntas_defensa.md): Banco de preguntas teóricas avanzadas para defensa del proyecto.
* [`preguntas_profesor.md`](./guias_estudio/preguntas_profesor.md): Fundamentos técnicos y guía de preguntas frecuentes.

---

## 👥 Créditos y Autores

Proyecto académico y de portafolio profesional desarrollado por:

* **Angel Israel Ayuquina Chimborazo** - [GitHub](https://github.com/T1Angel4220)
* **Sebastian Alejandro Ortiz Bustos**

**Institución:** Universidad Técnica de Ambato (UTA)  
**Facultad:** Facultad de Ingeniería en Sistemas, Electrónica e Industrial (FISEI)  
**Carrera:** Ingeniería de Software  
**Área:** Inteligencia Artificial  
