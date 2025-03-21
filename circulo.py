import math
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Función que implementa el algoritmo de punto medio para la circunferencia
def midpoint_circle_algorithm(xc, yc, r):
    x = 0
    y = r
    p = 1 - r  # Parámetro de decisión inicial
    points = []
    
    while x <= y:
        # Se calculan los 8 puntos de simetría
        points.extend([
            (xc + x, yc + y),
            (xc - x, yc + y),
            (xc + x, yc - y),
            (xc - x, yc - y),
            (xc + y, yc + x),
            (xc - y, yc + x),
            (xc + y, yc - x),
            (xc - y, yc - x)
        ])
        # Actualización del parámetro y de las coordenadas
        if p < 0:
            p += 2 * x + 3
        else:
            p += 2 * x - 2 * y + 5
            y -= 1
        x += 1

    points = list(set(points))
    return points

def fill_circle(ax, xc, yc, r):
    for y in range(yc - r, yc + r + 1):
        dx = int(round(math.sqrt(r*r - (y - yc)**2)))
        x_start = xc - dx
        x_end = xc + dx
        ax.hlines(y, x_start, x_end, colors='orange', linewidth=1)

# GRAFICACION DE LA CIRCUNFERENCIA
def plot_circle(canvas, points, xc, yc, r, fill):
    fig, ax = plt.subplots(figsize=(6, 6))
    
    x_vals = [pt[0] for pt in points]
    y_vals = [pt[1] for pt in points]
    ax.scatter(x_vals, y_vals, color='blue', label='Circunferencia', s=10)
    
    #centro
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
    
    for widget in canvas.winfo_children():
        widget.destroy()
    canvas_plot = FigureCanvasTkAgg(fig, master=canvas)
    canvas_plot.draw()
    canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def run_circle():
    try:
        xc = int(entry_xc.get())
        yc = int(entry_yc.get())
        r = int(entry_r.get())
        if r < 0:
            messagebox.showerror("Error", "El radio debe ser un número positivo.")
            return
        
        points = midpoint_circle_algorithm(xc, yc, r)
        fill_option = fill_var.get()
        
        listbox_points.delete(0, tk.END)
        points_sorted = sorted(points, key=lambda p: (p[0], p[1]))
        for pt in points_sorted:
            listbox_points.insert(tk.END, f"({pt[0]}, {pt[1]})")
        
        plot_circle(graph_canvas, points, xc, yc, r, fill_option)
    except ValueError:
        messagebox.showerror("Error", "Ingrese valores enteros válidos.")

def clear_entries():
    entry_xc.delete(0, tk.END)
    entry_yc.delete(0, tk.END)
    entry_r.delete(0, tk.END)
    listbox_points.delete(0, tk.END)
    for widget in graph_canvas.winfo_children():
        widget.destroy()

#TINKER#
root = tk.Tk()
root.title("Algoritmo de Círculo - Punto Medio")
root.geometry("1000x700")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

frame_left = tk.Frame(root, bg="#f0f0f0")
frame_left.pack(side=tk.LEFT, padx=20, pady=20)

frame_right = tk.Frame(root, bg="#ffffff")
frame_right.pack(side=tk.RIGHT, padx=20, pady=20, expand=True, fill=tk.BOTH)

tk.Label(frame_left, text="Parámetros del Círculo", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)

entry_frame = tk.Frame(frame_left, bg="#f0f0f0")
entry_frame.pack(pady=10)

tk.Label(entry_frame, text="Centro X:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky='e')
entry_xc = tk.Entry(entry_frame, font=("Arial", 12), width=5)
entry_xc.grid(row=0, column=1, padx=5, pady=5)

tk.Label(entry_frame, text="Centro Y:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky='e')
entry_yc = tk.Entry(entry_frame, font=("Arial", 12), width=5)
entry_yc.grid(row=1, column=1, padx=5, pady=5)

tk.Label(entry_frame, text="Radio:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5, sticky='e')
entry_r = tk.Entry(entry_frame, font=("Arial", 12), width=5)
entry_r.grid(row=2, column=1, padx=5, pady=5)

fill_var = tk.BooleanVar()
fill_check = tk.Checkbutton(frame_left, text="Rellenar Círculo", variable=fill_var, font=("Arial", 12), bg="#f0f0f0")
fill_check.pack(pady=10)

tk.Button(frame_left, text="Generar Círculo", command=run_circle, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=5)
tk.Button(frame_left, text="Limpiar", command=clear_entries, font=("Arial", 12), bg="#f44336", fg="white").pack(pady=5)

tk.Label(frame_left, text="Puntos del Círculo", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
listbox_points = tk.Listbox(frame_left, width=30, height=15, font=("Arial", 10))
listbox_points.pack(pady=5)

graph_canvas = tk.Frame(frame_right, bg="#ffffff")
graph_canvas.pack(expand=True, fill=tk.BOTH)
tk.Label(frame_right, text="Plano de Coordenadas", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)

root.mainloop()
