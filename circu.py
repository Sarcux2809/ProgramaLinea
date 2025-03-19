import math
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import List, Tuple, Set


def midpoint_circle_algorithm(xc: int, yc: int, r: int) -> List[Tuple[int, int]]:
    """
    Calcula los puntos de una circunferencia utilizando el algoritmo del punto medio.

    Este algoritmo inicia en (0, r) y, usando el parámetro de decisión 'p',
    determina en cada iteración el siguiente punto. Se aprovecha la simetría
    de 8 octantes para reflejar cada punto calculado en todas las direcciones.

    Fórmulas utilizadas:
        - Ecuación del círculo: (x - xc)² + (y - yc)² = r²
        - Valor de decisión inicial: p0 = 1 - r
        - Si p < 0: pₖ₊₁ = pₖ + 2x + 3
        - Si p ≥ 0: pₖ₊₁ = pₖ + 2x - 2y + 5 (y se reduce y en 1)

    Args:
        xc (int): Coordenada X del centro.
        yc (int): Coordenada Y del centro.
        r (int): Radio del círculo.

    Returns:
        List[Tuple[int, int]]: Lista de puntos (x, y) de la circunferencia.
    """
    x = 0
    y = r
    p = 1 - r  # Valor de decisión inicial
    points: Set[Tuple[int, int]] = set()

    while x <= y:
        # Agrega los 8 puntos de simetría
        points.update({
            (xc + x, yc + y),
            (xc - x, yc + y),
            (xc + x, yc - y),
            (xc - x, yc - y),
            (xc + y, yc + x),
            (xc - y, yc + x),
            (xc + y, yc - x),
            (xc - y, yc - x)
        })
        if p < 0:
            p += 2 * x + 3
        else:
            p += 2 * x - 2 * y + 5
            y -= 1
        x += 1

    return sorted(list(points), key=lambda pt: (pt[0], pt[1]))


def fill_circle(ax: plt.Axes, xc: int, yc: int, r: int, color: str = 'orange') -> None:
    """
    Rellena el círculo utilizando la técnica de 'scanline'.

    Para cada valor de y entre (yc - r) y (yc + r), se calcula la extensión horizontal
    (x_start, x_end) mediante la ecuación del círculo:
        dx = sqrt(r² - (y - yc)²)
    y se dibuja una línea horizontal entre (xc - dx) y (xc + dx).

    Args:
        ax (plt.Axes): Objeto de ejes de matplotlib.
        xc (int): Coordenada X del centro.
        yc (int): Coordenada Y del centro.
        r (int): Radio del círculo.
        color (str, optional): Color del relleno. Por defecto es 'orange'.
    """
    for y in range(yc - r, yc + r + 1):
        try:
            dx = int(round(math.sqrt(r * r - (y - yc) ** 2)))
        except ValueError:
            continue
        x_start = xc - dx
        x_end = xc + dx
        ax.hlines(y, x_start, x_end, colors=color, linewidth=1)


def plot_circle(canvas: tk.Frame, points: List[Tuple[int, int]], xc: int, yc: int, r: int, fill: bool) -> None:
    """
    Grafica la circunferencia (y opcionalmente su relleno) en un canvas de Tkinter.

    Args:
        canvas (tk.Frame): Frame de Tkinter donde se mostrará la gráfica.
        points (List[Tuple[int, int]]): Puntos calculados de la circunferencia.
        xc (int): Coordenada X del centro.
        yc (int): Coordenada Y del centro.
        r (int): Radio del círculo.
        fill (bool): Indica si se debe rellenar el círculo.
    """
    fig, ax = plt.subplots(figsize=(6, 6))
    # Extrae las coordenadas para graficar
    x_vals = [pt[0] for pt in points]
    y_vals = [pt[1] for pt in points]
    ax.scatter(x_vals, y_vals, color='blue', label='Circunferencia', s=10)
    # Marca el centro
    ax.scatter([xc], [yc], color='green', s=100, marker='x', label='Centro')

    if fill:
        fill_circle(ax, xc, yc, r)

    ax.set_title("Círculo generado (Algoritmo de Punto Medio)")
    ax.set_xlabel("Eje X")
    ax.set_ylabel("Eje Y")
    ax.grid(True)
    ax.set_aspect('equal', adjustable='box')

    margin = r * 0.2 if r > 0 else 10
    ax.set_xlim(xc - r - margin, xc + r + margin)
    ax.set_ylim(yc - r - margin, yc + r + margin)
    ax.legend()

    # Limpia el canvas y muestra la nueva gráfica
    for widget in canvas.winfo_children():
        widget.destroy()
    canvas_plot = FigureCanvasTkAgg(fig, master=canvas)
    canvas_plot.draw()
    canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def is_valid_int(value: str) -> bool:
    """
    Valida si la cadena puede convertirse a entero.

    Args:
        value (str): Cadena a validar.

    Returns:
        bool: True si es entero, False en caso contrario.
    """
    try:
        int(value)
        return True
    except ValueError:
        return False


class CircleApp:
    """
    Aplicación gráfica para generar y visualizar círculos utilizando el algoritmo de punto medio.

    Además de graficar la circunferencia y su posible relleno, se muestra una tabla
    explicativa que indica, para cada punto calculado, una breve descripción y se
    incluye un área con las fórmulas utilizadas.
    """
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Algoritmo de Círculo - Punto Medio")
        self.root.geometry("1100x750")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        self.create_widgets()

    def create_widgets(self) -> None:
        """
        Crea y organiza los widgets de la interfaz.
        """
        # Panel izquierdo: Controles, tabla y explicación
        self.frame_left = tk.Frame(self.root, bg="#f0f0f0")
        self.frame_left.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)

        # Panel derecho: Gráfica
        self.frame_right = tk.Frame(self.root, bg="#ffffff")
        self.frame_right.pack(side=tk.RIGHT, padx=20, pady=20, expand=True, fill=tk.BOTH)

        # Encabezado
        tk.Label(self.frame_left, text="Parámetros del Círculo", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

        # Entradas de datos
        self.entry_frame = tk.Frame(self.frame_left, bg="#f0f0f0")
        self.entry_frame.pack(pady=10)

        tk.Label(self.entry_frame, text="Centro X:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_xc = tk.Entry(self.entry_frame, font=("Arial", 12), width=5)
        self.entry_xc.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.entry_frame, text="Centro Y:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_yc = tk.Entry(self.entry_frame, font=("Arial", 12), width=5)
        self.entry_yc.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.entry_frame, text="Radio:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.entry_r = tk.Entry(self.entry_frame, font=("Arial", 12), width=5)
        self.entry_r.grid(row=2, column=1, padx=5, pady=5)

        # Checkbox para opción de rellenar
        self.fill_var = tk.BooleanVar()
        self.fill_check = tk.Checkbutton(self.frame_left, text="Rellenar Círculo", variable=self.fill_var, font=("Arial", 12), bg="#f0f0f0")
        self.fill_check.pack(pady=10)

        # Botones
        tk.Button(self.frame_left, text="Generar Círculo", command=self.run_circle, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=5)
        tk.Button(self.frame_left, text="Limpiar", command=self.clear_entries, font=("Arial", 12), bg="#f44336", fg="white").pack(pady=5)

        # Tabla explicativa de puntos (usando Treeview)
        tk.Label(self.frame_left, text="Tabla de Puntos y Explicación", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
        self.tree = ttk.Treeview(self.frame_left, columns=("punto", "descripcion"), show="headings", height=8)
        self.tree.heading("punto", text="Punto")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.column("punto", width=100, anchor="center")
        self.tree.column("descripcion", width=250, anchor="w")
        self.tree.pack(pady=5)

        # Área de explicación del algoritmo con fórmulas
        formulas_text = (
            "Fórmulas Utilizadas:\n"
            "• Ecuación del Círculo: (x - xc)² + (y - yc)² = r²\n"
            "• Valor inicial: p₀ = 1 - r\n"
            "• Si p < 0: pₖ₊₁ = pₖ + 2x + 3\n"
            "• Si p ≥ 0: pₖ₊₁ = pₖ + 2x - 2y + 5\n"
            "• Para relleno: dx = sqrt(r² - (y - yc)²)"
        )
        tk.Label(self.frame_left, text=formulas_text, font=("Arial", 10), bg="#f0f0f0", justify="left", wraplength=350).pack(pady=10)

        # Canvas para la gráfica en el panel derecho
        self.graph_canvas = tk.Frame(self.frame_right, bg="#ffffff")
        self.graph_canvas.pack(expand=True, fill=tk.BOTH)
        tk.Label(self.frame_right, text="Plano de Coordenadas", font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=10)

    def run_circle(self) -> None:
        """
        Valida las entradas, calcula la circunferencia, actualiza la gráfica y la tabla explicativa.
        """
        xc_val = self.entry_xc.get().strip()
        yc_val = self.entry_yc.get().strip()
        r_val = self.entry_r.get().strip()

        if not (is_valid_int(xc_val) and is_valid_int(yc_val) and is_valid_int(r_val)):
            messagebox.showerror("Error", "Ingrese valores enteros válidos.")
            return

        xc = int(xc_val)
        yc = int(yc_val)
        r = int(r_val)
        if r < 0:
            messagebox.showerror("Error", "El radio debe ser un número positivo.")
            return

        points = midpoint_circle_algorithm(xc, yc, r)
        fill_option = self.fill_var.get()

        # Actualiza la tabla de puntos y explicación
        for item in self.tree.get_children():
            self.tree.delete(item)
        for pt in points:
            punto_str = f"({pt[0]}, {pt[1]})"
            descripcion = "Calculado por simetría (Punto Medio)"
            self.tree.insert("", tk.END, values=(punto_str, descripcion))

        # Grafica el círculo
        plot_circle(self.graph_canvas, points, xc, yc, r, fill_option)

    def clear_entries(self) -> None:
        """
        Limpia las entradas, la tabla y la gráfica.
        """
        self.entry_xc.delete(0, tk.END)
        self.entry_yc.delete(0, tk.END)
        self.entry_r.delete(0, tk.END)
        for item in self.tree.get_children():
            self.tree.delete(item)
        for widget in self.graph_canvas.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = CircleApp(root)
    root.mainloop()
