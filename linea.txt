import math
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Función para el algoritmo DDA (entero y flotante)
def dda_algorithm(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    
    if steps == 0:
        return [(x1, y1)], [(float(x1), float(y1))], dx, dy
    
    x_inc = dx / steps
    y_inc = dy / steps
    
    x, y = x1, y1
    
    points_int = []    # Puntos con round (enteros)
    points_float = []  # Puntos en flotante

    for _ in range(int(steps) + 1):
        points_int.append((round(x), round(y)))
        points_float.append((x, y))
        x += x_inc
        y += y_inc
    
    return points_int, points_float, dx, dy

# Función para clasificar el caso de la pendiente
def classify_case(dx, dy):
    if dx == 0:
        return "Pendiente indefinida (línea vertical)", None
    m = dy / dx
    if m > 1:
        return "Pendiente positiva > 1", m
    elif 0 < m <= 1:
        return "Pendiente positiva <= 1", m
    elif -1 <= m < 0:
        return "Pendiente negativa >= -1", m
    elif m < -1:
        return "Pendiente negativa < -1", m
    else:
        # m == 0
        return "Pendiente 0 (línea horizontal)", m

# Función para graficar la línea usando los puntos flotantes
def plot_line(canvas, points_float):
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Extrae las coordenadas flotantes en listas separadas
    x_vals = [p[0] for p in points_float]
    y_vals = [p[1] for p in points_float]
    
    ax.plot(x_vals, y_vals, marker='o', linestyle='-', color='b', label='Línea DDA (float)')
    
    for px, py in points_float:
        ax.text(px, py, f'({px:.1f},{py:.1f})', fontsize=8, ha='right')
    
    # ========== MARCAS DE PUNTO INICIAL (INICIO) Y FINAL (FIN) ==========
    ax.scatter([x_vals[0]], [y_vals[0]], 
               color='lime', s=200, marker='o', label='Inicio')  # Punto de inicio
    ax.scatter([x_vals[-1]], [y_vals[-1]], 
               color='magenta', s=200, marker='x', label='Fin')  # Punto final
    
    ax.set_title('Generación de Línea con Algoritmo DDA')
    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    ax.grid(color='gray', linestyle='--', linewidth=0.5)
    
    x_min, x_max = min(x_vals), max(x_vals)
    y_min, y_max = min(y_vals), max(y_vals)
    margin_x = (x_max - x_min) * 0.1 if x_max != x_min else 1
    margin_y = (y_max - y_min) * 0.1 if y_max != y_min else 1
    ax.set_xlim(x_min - margin_x, x_max + margin_x)
    ax.set_ylim(y_min - margin_y, y_max + margin_y)
    
    ax.set_aspect('equal', adjustable='box')
    
    ax.legend()
    
    for widget in canvas.winfo_children():
        widget.destroy()
    
    canvas_plot = FigureCanvasTkAgg(fig, master=canvas)
    canvas_plot.draw()
    canvas_plot.get_tk_widget().pack()

def run_dda():
    try:
        x1 = int(entry_x1.get())
        y1 = int(entry_y1.get())
        x2 = int(entry_x2.get())
        y2 = int(entry_y2.get())
        
        points_int, points_float, dx, dy = dda_algorithm(x1, y1, x2, y2)
        case_desc, m = classify_case(dx, dy)
        
        # Calculamos el ángulo en grados con atan2
        if dx == 0 and dy == 0:
            # Ambos puntos son iguales (sin línea)
            angle_deg = 0.0
        else:
            angle_rad = math.atan2(dy, dx)
            angle_deg = math.degrees(angle_rad)
        
        # DETECCIÓN DE DIRECCIÓN
        if x2 > x1:
            dir_x = "izquierda a derecha"
        elif x2 < x1:
            dir_x = "derecha a izquierda"
        else:
            dir_x = "sin cambio horizontal"
        
        if y2 > y1:
            dir_y = "abajo a arriba"
        elif y2 < y1:
            dir_y = "arriba a abajo"
        else:
            dir_y = "sin cambio vertical"
        
        direction_text = f"Dirección: {dir_x}, {dir_y}"
        
        if m is not None:
            result_text.set(
                f"{case_desc}\n"
                f"Pendiente: {m:.2f}\n"
                f"Inclinación: {angle_deg:.2f}°\n"
                f"{direction_text}"
            )
        else:
            result_text.set(
                f"{case_desc}\n"
                f"Inclinación: {angle_deg:.2f}°\n"
                f"{direction_text}"
            )

        # Mostramos los puntos enteros en la lista
        coord_list.delete(0, tk.END)
        for p in points_int:
            coord_list.insert(tk.END, f"{p}")
        
        plot_line(graph_canvas, points_float)
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores enteros válidos.")

# Función para limpiar las entradas y resultados
def clear_entries():
    for entry in [entry_x1, entry_y1, entry_x2, entry_y2]:
        entry.delete(0, tk.END)
    result_text.set("")
    coord_list.delete(0, tk.END)
    for widget in graph_canvas.winfo_children():
        widget.destroy()

# Configuración de la ventana principal
root = tk.Tk()
root.title("Algoritmo DDA - Generación de Líneas")
root.geometry("1000x700")
root.resizable(False, False)
root.configure(bg='#f0f0f0')

# Frame izquierdo para controles
frame_left = tk.Frame(root, bg='#f0f0f0')
frame_left.pack(side=tk.LEFT, padx=20, pady=20)

# Frame derecho para el gráfico
frame_right = tk.Frame(root, bg='#ffffff')
frame_right.pack(side=tk.RIGHT, padx=20, pady=20, expand=True, fill=tk.BOTH)

# Título de coordenadas
tk.Label(frame_left, text="Coordenadas", font=("Arial", 12, "bold"), bg='#f0f0f0').pack()

# Frame para entradas
entry_frame = tk.Frame(frame_left, bg='#f0f0f0')
entry_frame.pack()

# Entradas para coordenadas
for i, (label, var) in enumerate(zip(["x1:", "y1:", "x2:", "y2:"],
                                     ["entry_x1", "entry_y1", "entry_x2", "entry_y2"])):
    tk.Label(entry_frame, text=label, font=("Arial", 10), bg='#f0f0f0').grid(row=i, column=0, padx=5, pady=5)
    globals()[var] = tk.Entry(entry_frame, font=("Arial", 10), width=5)
    globals()[var].grid(row=i, column=1, padx=5, pady=5)

# Botones para generar línea y limpiar
tk.Button(frame_left, text="Generar Línea", command=run_dda,
          font=("Arial", 10), bg='#4CAF50', fg='white').pack(pady=10)
tk.Button(frame_left, text="Limpiar", command=clear_entries,
          font=("Arial", 10), bg='#f44336', fg='white').pack()

# Resultados
tk.Label(frame_left, text="Resultados", font=("Arial", 12, "bold"), bg='#f0f0f0').pack(pady=5)
result_text = tk.StringVar()
tk.Label(frame_left, textvariable=result_text, font=("Arial", 10), bg='#f0f0f0', justify=tk.LEFT).pack()

# Lista de puntos de la línea (discretos)
tk.Label(frame_left, text="Puntos de la Línea", font=("Arial", 12, "bold"), bg='#f0f0f0').pack(pady=5)
coord_list = tk.Listbox(frame_left, height=10, width=20, font=("Arial", 10))
coord_list.pack()

# Canvas para el gráfico
graph_canvas = tk.Frame(frame_right, bg='#ffffff')
graph_canvas.pack(expand=True, fill=tk.BOTH)

# Título del gráfico
tk.Label(frame_right, text="Plano de Coordenadas", font=("Arial", 14, "bold"), bg='#ffffff').pack()

root.mainloop()
