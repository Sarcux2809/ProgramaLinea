import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def dda_algorithm(x1, y1, x2, y2):
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
    points = sorted(points, key=lambda p: p[1])
    
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
    
    intersections = []
    for y in sorted(edge_dict.keys()):
        x_vals = sorted(edge_dict[y])
        if len(x_vals) > 1:
            intersections.append((x_vals[0], y, x_vals[-1], y))
            ax.plot(range(x_vals[0], x_vals[-1] + 1), [y] * (x_vals[-1] - x_vals[0] + 1), 'r-', markersize=1)
    
    return intersections

def plot_triangle(canvas, ax, points):
    ax.clear()
    
    for i in range(3):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % 3]
        line_points = dda_algorithm(x1, y1, x2, y2)
        x_vals, y_vals = zip(*line_points)
        ax.plot(x_vals, y_vals, 'b-', linewidth=2)
    
    intersections = fill_triangle(ax, points)
    
    ax.set_title("Triángulo con DDA y Relleno", fontsize=14, fontweight='bold')
    ax.set_xlabel("Eje X", fontsize=12)
    ax.set_ylabel("Eje Y", fontsize=12)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True)
    canvas.draw()

    return intersections

def calculate_slope(x1, y1, x2, y2):
    if x2 - x1 != 0:
        return (y2 - y1) / (x2 - x1)
    return None

def update_table(intersections):
    for row in table.get_children():
        table.delete(row)
    
    for intersection in intersections:
        table.insert("", "end", values=(intersection[0], intersection[1], intersection[2], intersection[3]))

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
root.title("Algoritmo DDA - Triángulo")
root.geometry("900x600")
root.config(bg="#f4f4f9")

frame_controls = tk.Frame(root, bg="#f4f4f9")
frame_controls.pack(side=tk.LEFT, padx=30, pady=30, fill=tk.Y)

frame_graph = tk.Frame(root, bg="#f4f4f9")
frame_graph.pack(side=tk.RIGHT, padx=30, pady=30, expand=True, fill=tk.BOTH)

tk.Label(frame_controls, text="Vértices del Triángulo", font=("Arial", 14, "bold"), bg="#f4f4f9").pack(pady=10)

entries = []
labels = ["Xa:", "Ya:", "Xb:", "Yb:", "Xc:", "Yc:"]
for i, label in enumerate(labels):
    tk.Label(frame_controls, text=label, font=("Arial", 12), bg="#f4f4f9").pack(pady=5)
    entry = tk.Entry(frame_controls, width=8, font=("Arial", 12))
    entry.pack(pady=5)
    entries.append(entry)

entry_xa, entry_ya, entry_xb, entry_yb, entry_xc, entry_yc = entries

tk.Button(frame_controls, text="Generar Triángulo", command=run_dda_triangle, font=("Arial", 12), bg="#4CAF50", fg="white", relief="solid", width=20).pack(pady=20)

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
