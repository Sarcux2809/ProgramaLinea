import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def dda_algorithm_float(x1, y1, x2, y2):
    """
    Versión de DDA que devuelve puntos en float,
    para que la línea se vea suave (sin 'escalones').
    """
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
        points.append((x, y))
        x += x_inc
        y += y_inc
    
    return points

def fill_triangle(ax, points_float):
    """
    Relleno tipo 'scanline' (líneas horizontales).
    Para ello, convertimos los puntos 'float' en enteros
    y los agrupamos por filas (y).
    """
    points_float = sorted(points_float, key=lambda p: p[1])

    edges = []
    for i in range(3):
        x1, y1 = points_float[i]
        x2, y2 = points_float[(i + 1) % 3]
        line_points = dda_algorithm_float(x1, y1, x2, y2)
        edges.extend(line_points)

    edge_dict = {}
    for (xf, yf) in edges:
        x = round(xf)
        y = round(yf)
        if y in edge_dict:
            edge_dict[y].append(x)
        else:
            edge_dict[y] = [x]

    intersections = []
    for y in sorted(edge_dict.keys()):
        x_vals = sorted(edge_dict[y])
        if len(x_vals) > 1:
            x_min, x_max = x_vals[0], x_vals[-1]
            intersections.append((x_min, y, x_max, y))
            ax.plot(range(x_min, x_max + 1), [y]*(x_max - x_min + 1),
                    'r-', markersize=1)
    return intersections

def plot_triangle(canvas, ax, tri_points):
    """
    Dibuja contorno y rellena el triángulo.
    """
    ax.clear()
    
    for i in range(3):
        x1, y1 = tri_points[i]
        x2, y2 = tri_points[(i + 1) % 3]
        line_points = dda_algorithm_float(x1, y1, x2, y2)
        xf = [p[0] for p in line_points]
        yf = [p[1] for p in line_points]
        ax.plot(xf, yf, 'b-', linewidth=2)
    
    intersections = fill_triangle(ax, tri_points)
    
    ax.set_title("Triángulo con DDA", fontsize=14, fontweight='bold')
    ax.set_xlabel("Eje X", fontsize=12)
    ax.set_ylabel("Eje Y", fontsize=12)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True)
    canvas.draw()
    
    return intersections

def calculate_slope(x1, y1, x2, y2):
    if (x2 - x1) != 0:
        return (y2 - y1) / (x2 - x1)
    return None

def update_table(intersections):
    for row in table.get_children():
        table.delete(row)
    for inter in intersections:
        table.insert("", "end", values=(inter[0], inter[1], inter[2], inter[3]))

def run_dda_triangle():
    try:
        xa, ya = int(entry_xa.get()), int(entry_ya.get())
        xb, yb = int(entry_xb.get()), int(entry_yb.get())
        xc, yc = int(entry_xc.get()), int(entry_yc.get())
        
        mAB = calculate_slope(xa, ya, xb, yb)
        mBC = calculate_slope(xb, yb, xc, yc)
        mCA = calculate_slope(xc, yc, xa, ya)
        
        slope_label.config(text=f"Pendiente AB: {mAB}, BC: {mBC}, CA: {mCA}")
        
        intersections = plot_triangle(canvas_plot, ax, [(xa, ya), (xb, yb), (xc, yc)])
        
        update_table(intersections)
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores enteros válidos.")

root = tk.Tk()
root.title("Algoritmo DDA - Triángulo (líneas suaves)")
root.geometry("900x600")
root.config(bg="#f4f4f9")

frame_controls = tk.Frame(root, bg="#f4f4f9")
frame_controls.pack(side=tk.LEFT, padx=30, pady=30, fill=tk.Y)

frame_graph = tk.Frame(root, bg="#f4f4f9")
frame_graph.pack(side=tk.RIGHT, padx=30, pady=30, expand=True, fill=tk.BOTH)

tk.Label(frame_controls, text="Vértices del Triángulo", font=("Arial", 14, "bold"), bg="#f4f4f9").pack(pady=10)

entries = []
labels = ["Xa:", "Ya:", "Xb:", "Yb:", "Xc:", "Yc:"]
for i, lbl in enumerate(labels):
    tk.Label(frame_controls, text=lbl, font=("Arial", 12), bg="#f4f4f9").pack(pady=5)
    entry = tk.Entry(frame_controls, width=8, font=("Arial", 12))
    entry.pack(pady=5)
    entries.append(entry)

entry_xa, entry_ya, entry_xb, entry_yb, entry_xc, entry_yc = entries

tk.Button(frame_controls, text="Generar Triángulo", command=run_dda_triangle,
          font=("Arial", 12), bg="#4CAF50", fg="white", relief="solid", width=20).pack(pady=20)

slope_label = tk.Label(frame_controls, text="Pendientes de las líneas:", font=("Arial", 12), bg="#f4f4f9")
slope_label.pack(pady=10)

table_frame = tk.Frame(frame_controls, bg="#f4f4f9")
table_frame.pack(pady=20)

columns = ("X1", "Y1", "X2", "Y2")
table = ttk.Treeview(table_frame, columns=columns, show="headings", height=5)
table.heading("X1", text="X1", anchor="center")
table.heading("Y1", text="Y1", anchor="center")
table.heading("X2", text="X2", anchor="center")
table.heading("Y2", text="Y2", anchor="center")
table.column("X1", anchor="center", width=80)
table.column("Y1", anchor="center", width=80)
table.column("X2", anchor="center", width=80)
table.column("Y2", anchor="center", width=80)
table.pack()

fig, ax = plt.subplots(figsize=(6, 6))
canvas_plot = FigureCanvasTkAgg(fig, master=frame_graph)
canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)

root.mainloop()
