import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def dda_algorithm(x1, y1, x2, y2):
    """Genera puntos de una línea entre (x1, y1) y (x2, y2) usando el algoritmo DDA."""
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    
    if steps == 0:
        return [(x1, y1)]
    
    x_inc = dx / steps
    y_inc = dy / steps
    
    x, y = x1, y1
    points = []
    
    for _ in range(int(steps) + 1):
        points.append((round(x), round(y)))
        x += x_inc
        y += y_inc
    
    return points

def fill_triangle(ax, points):
    """Rellena un triángulo usando el algoritmo DDA para determinar los bordes."""
    points = sorted(points, key=lambda p: p[1])  # Ordena por la coordenada y
    
    edges = []
    for i in range(3):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % 3]
        edges.extend(dda_algorithm(x1, y1, x2, y2))
    
    edge_dict = {}
    for x, y in edges:
        if y in edge_dict:
            edge_dict[y].append(x)
        else:
            edge_dict[y] = [x]
    
    # Dibujar líneas de relleno entre los bordes
    intersections = []
    for y in sorted(edge_dict.keys()):
        x_vals = sorted(edge_dict[y])
        if len(x_vals) > 1:
            intersections.append((x_vals[0], y, x_vals[-1], y))  # Puntos de intersección
            ax.plot(range(x_vals[0], x_vals[-1] + 1), [y] * (x_vals[-1] - x_vals[0] + 1), 'r-', markersize=1)
    
    return intersections

def plot_triangle(canvas, ax, points):
    """Dibuja y rellena un triángulo en un gráfico de Matplotlib."""
    ax.clear()
    
    # Dibujar las líneas del triángulo con color fuerte
    for i in range(3):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % 3]
        line_points = dda_algorithm(x1, y1, x2, y2)
        x_vals, y_vals = zip(*line_points)
        ax.plot(x_vals, y_vals, 'b-', linewidth=2)  # Línea azul más gruesa
    
    # Rellenar el triángulo usando las líneas de escaneo
    intersections = fill_triangle(ax, points)
    
    # Mostrar el triángulo con relleno
    ax.set_title("Triángulo con DDA y Relleno")
    ax.set_xlabel("Eje X")
    ax.set_ylabel("Eje Y")
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True)
    canvas.draw()

    return intersections

def calculate_slope(x1, y1, x2, y2):
    """Calcula la pendiente de una línea."""
    if x2 - x1 != 0:
        return (y2 - y1) / (x2 - x1)
    return None

def update_table(intersections):
    """Actualiza la tabla con los puntos de intersección."""
    for row in table.get_children():
        table.delete(row)
    
    for intersection in intersections:
        table.insert("", "end", values=(intersection[0], intersection[1], intersection[2], intersection[3]))

def run_dda_triangle():
    """Obtiene los valores de entrada y genera el triángulo en el gráfico."""
    try:
        xa, ya = int(entry_xa.get()), int(entry_ya.get())
        xb, yb = int(entry_xb.get()), int(entry_yb.get())
        xc, yc = int(entry_xc.get()), int(entry_yc.get())
        
        # Calculando pendientes
        mAB = calculate_slope(xa, ya, xb, yb)
        mBC = calculate_slope(xb, yb, xc, yc)
        mCA = calculate_slope(xc, yc, xa, ya)
        
        # Actualizar la tabla con las pendientes
        slope_label.config(text=f"Pendiente AB: {mAB}, BC: {mBC}, CA: {mCA}")
        
        # Dibujar el triángulo y obtener los puntos de intersección
        intersections = plot_triangle(canvas_plot, ax, [(xa, ya), (xb, yb), (xc, yc)])
        
        # Actualizar la tabla de intersección
        update_table(intersections)
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores enteros válidos.")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Algoritmo DDA - Triángulo")
root.geometry("800x600")

frame_controls = tk.Frame(root)
frame_controls.pack(side=tk.LEFT, padx=20, pady=20)

frame_graph = tk.Frame(root)
frame_graph.pack(side=tk.RIGHT, padx=20, pady=20, expand=True, fill=tk.BOTH)

tk.Label(frame_controls, text="Vértices del Triángulo", font=("Arial", 12, "bold")).pack()

entries = []
labels = ["Xa:", "Ya:", "Xb:", "Yb:", "Xc:", "Yc:"]
for i, label in enumerate(labels):
    tk.Label(frame_controls, text=label).pack()
    entry = tk.Entry(frame_controls, width=5)
    entry.pack()
    entries.append(entry)

entry_xa, entry_ya, entry_xb, entry_yb, entry_xc, entry_yc = entries

tk.Button(frame_controls, text="Generar Triángulo", command=run_dda_triangle).pack(pady=10)

slope_label = tk.Label(frame_controls, text="Pendientes de las líneas:", font=("Arial", 10))
slope_label.pack(pady=10)

# Tabla de puntos de intersección
table_frame = tk.Frame(frame_controls)
table_frame.pack(pady=10)

columns = ("X1", "Y1", "X2", "Y2")
table = ttk.Treeview(table_frame, columns=columns, show="headings")
table.heading("X1", text="X1")
table.heading("Y1", text="Y1")
table.heading("X2", text="X2")
table.heading("Y2", text="Y2")
table.pack()

fig, ax = plt.subplots(figsize=(5, 5))
canvas_plot = FigureCanvasTkAgg(fig, master=frame_graph)
canvas_plot.get_tk_widget().pack()

root.mainloop()
