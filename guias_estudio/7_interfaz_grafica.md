# Análisis de Interfaz Gráfica (`main.py` y `aplicacion.py`)

Estos dos archivos se encargan exclusivamente de la Interfaz Gráfica de Usuario (GUI) utilizando la librería estándar de Python `tkinter`. 
Siguen el patrón de diseño "Controlador de Vista" (MVC simplificado), donde estos archivos son la **Vista/Controlador** y no saben cómo resolver el puzzle, solo llaman a la capa **Núcleo** y **Algoritmos** (el Modelo) para que lo hagan.

## 1. `main.py` (El Punto de Entrada)

```python
import tkinter as tk
from visualizador.aplicacion import AplicacionPuzzle

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionPuzzle(root)
    root.mainloop()
```
Es el archivo más simple de todos. 
1. `tk.Tk()` crea la ventana principal del sistema operativo (con sus botones de cerrar, minimizar).
2. Se instancia `AplicacionPuzzle(root)`, inyectándole esa ventana principal. Esto se conoce como Inyección de Dependencias.
3. `root.mainloop()` entra en un bucle infinito que escucha eventos del usuario (clics, movimientos del ratón) hasta que se cierra el programa.

## 2. `visualizador/aplicacion.py` (El Dashboard)

Aunque el código es largo, conceptualmente se divide en responsabilidades muy claras:

### Construcción de la Interfaz
Utiliza el concepto de *Notebook* (pestañas) para separar la simulación de la comparativa.
- **Widgets:** Todo lo que ves en la pantalla (botones, etiquetas, dropdowns) son objetos instanciados de clases como `ttk.Button`, `ttk.Label`, `ttk.Combobox`.
- **Canvas / Tablero:** El tablero 3x3 no son simples botones, normalmente se dibuja sobre un `Canvas` o un Grid (cuadrícula) para poder actualizar visualmente las fichas cuando se mueven.

### Enlace de Eventos (Binding)
Cuando el usuario presiona "Resolver 8-Puzzle", el botón tiene asignado un comando o "callback" (ej. `command=self.resolver_puzzle`). Ese método se ejecuta en el momento del clic.

### El Flujo de Resolución (Método `resolver_puzzle` u homólogo)
1. Lee qué algoritmo y qué heurística seleccionó el usuario en los comboboxes.
2. Lee el `estado_actual` que se haya generado aleatoriamente.
3. Llama a la función correspondiente de la capa inferior (ej. `busqueda_a_estrella(estado, h_manhattan)`).
4. El algoritmo de la capa inferior hace todo el trabajo matemático (que ya vimos en `4_a_estrella.md`) y devuelve un objeto `MetricasBusqueda`.
5. La GUI lee los resultados (tiempos, costos, arrays de posiciones) de ese objeto.

### Sistema de Animación (Método `animar_ruta`)
Aquí ocurre algo clave en las interfaces gráficas modernas. Si intentamos mover las piezas dentro de un bucle `for` o `while` tradicional, la pantalla se congela hasta que el bucle termina, y luego vemos la ficha mágicamente en la meta.
Para evitar esto, `tkinter` usa el método `root.after(milisegundos, funcion)`.
- El algoritmo devuelve la `ruta_estados` (ej. una lista de 17 tableros).
- El sistema de animación carga el primer tablero.
- Usa `.after(500, self.siguiente_paso)` para decirle a Python: "Dentro de 500 milisegundos, pausa el bucle principal un microsegundo, dibuja el tablero 2, y continúa".
Esto crea la ilusión de movimiento cuadro por cuadro.

### Tabla de Comparativas
Simplemente itera las 4 posibles combinaciones (Voraz+h1, Voraz+h2, A*+h1, A*+h2), las ejecuta todas de golpe (en silencio, sin animar el tablero) y usa un widget tipo `Treeview` de `ttk` para inyectar los resultados en columnas, permitiendo la comparación directa que pusimos en el reporte.
