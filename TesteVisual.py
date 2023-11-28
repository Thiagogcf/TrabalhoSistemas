import tkinter as tk
from tkinter import messagebox, Toplevel
import control as ct
import matplotlib.pyplot as plt
from sympy import simplify, symbols
from sympy.parsing.sympy_parser import parse_expr
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


def getExpr(raw_expr):
    parsed_expr = parse_expr(str(raw_expr))
    simplified_expr = simplify(parsed_expr)
    return simplified_expr


def determinant(r1c1, r1c2, r2c1, r2c2):
    det = simplify((r1c1 * r2c2) - (r2c1 * r1c2))
    return det


def RouthHurwitz(polynomial):
    s = symbols('s')
    degree = len(polynomial) - 1
    routh_array = []

    row1 = [getExpr(polynomial[i]) for i in range(0, degree + 1, 2)]
    row2 = [getExpr(polynomial[i]) for i in range(1, degree + 1, 2)]
    routh_array.append(row1)
    routh_array.append(row2)

    for i in range(2, degree + 1):
        row = []
        for j in range(len(routh_array[0]) - 1):
            a = routh_array[i - 2][0] if len(routh_array[i - 2]) > 0 else 0
            b = routh_array[i - 2][j + 1] if len(routh_array[i - 2]) > j + 1 else 0
            c = routh_array[i - 1][0] if len(routh_array[i - 1]) > 0 else 0
            d = routh_array[i - 1][j + 1] if len(routh_array[i - 1]) > j + 1 else 0
            row.append(determinant(a, b, c, d) / (-c if c != 0 else 1))
        routh_array.append(row)

    return routh_array


def routhArrayToString(routh_array):
    string = ""
    for row in routh_array:
        row_str = "  ".join([str(e) for e in row])
        string += row_str + "\n"
    return string


def plot_root_locus(num, den):
    new_window = Toplevel(window)
    new_window.title("Root Locus Plot")
    sys = ct.TransferFunction(num, den)
    fig, ax = plt.subplots(figsize=(6, 5))
    ct.root_locus(sys, plot=True, ax=ax)
    ax.set_xlabel('Real Axis')
    ax.set_ylabel('Imaginary Axis')
    ax.set_title('Root Locus Plot')
    ax.grid(True)
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def plot_bode(num, den):
    new_window = Toplevel(window)
    new_window.title("Bode Plot")
    sys = ct.TransferFunction(num, den)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 10))
    mag, phase, omega = ct.bode(sys, Plot=False)
    ax1.semilogx(omega, 20 * np.log10(mag))
    ax1.set_xlabel('Frequency [rad/s]')
    ax1.set_ylabel('Magnitude [dB]')
    ax1.set_title('Magnitude Plot')
    ax1.grid(True)
    ax2.semilogx(omega, np.degrees(phase))
    ax2.set_xlabel('Frequency [rad/s]')
    ax2.set_ylabel('Phase [Degrees]')
    ax2.set_title('Phase Plot')
    ax2.grid(True)
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def is_stable(routh_array):
    first_col = [row[0] for row in routh_array if row]  # Obtém a primeira coluna
    sign_changes = sum(np.sign(first_col[:-1]) != np.sign(first_col[1:]))
    return sign_changes == 0


def display_routh(den):
    routh_matrix = RouthHurwitz(den)
    routh_str = routhArrayToString(routh_matrix)
    stability_str = "Sistema Estável" if is_stable(routh_matrix) else "Sistema Instável"
    routh_label.config(text=f"{routh_str}\n{stability_str}")




def on_plot_root_locus():
    try:
        num = [float(x) for x in entry_num.get().split()]
        den = [float(x) for x in entry_den.get().split()]
        plot_root_locus(num, den)
    except Exception as e:
        messagebox.showerror("Erro", str(e))


def on_plot_bode():
    try:
        num = [float(x) for x in entry_num.get().split()]
        den = [float(x) for x in entry_den.get().split()]
        plot_bode(num, den)
    except Exception as e:
        messagebox.showerror("Erro", str(e))


def on_display_routh():
    try:
        den = [float(x) for x in entry_den.get().split()]
        display_routh(den)
    except Exception as e:
        messagebox.showerror("Erro", str(e))


window = tk.Tk()
window.title("Root Locus e Bode Plot")
window.geometry("800x600")

font_style = ("Arial", 12)
label_font_style = ("Arial", 10, "bold")
button_style = {"font": ("Arial", 10, "bold"), "bg": "#4C8BF5", "fg": "white"}

input_frame = tk.Frame(window, pady=20)
input_frame.pack(fill="both")

output_frame = tk.Frame(window)
output_frame.pack(fill="both", expand=True)

tk.Label(input_frame, text="Root Locus e Bode Plot", font=("Arial", 16, "bold")).pack()
tk.Label(input_frame, text="Insira os coeficientes para análise", font=label_font_style).pack()

tk.Label(input_frame, text="Coeficientes do Numerador:", font=label_font_style).pack()
entry_num = tk.Entry(input_frame, font=font_style)
entry_num.pack()

tk.Label(input_frame, text="Coeficientes do Denominador:", font=label_font_style).pack()
entry_den = tk.Entry(input_frame, font=font_style)
entry_den.pack()

submit_button_rl = tk.Button(input_frame, text="Plotar Root Locus", command=on_plot_root_locus, **button_style)
submit_button_rl.pack(pady=5)

submit_button_bode = tk.Button(input_frame, text="Plotar Bode", command=on_plot_bode, **button_style)
submit_button_bode.pack(pady=5)

submit_button_routh = tk.Button(input_frame, text="Exibir Matriz de Routh", command=on_display_routh, **button_style)
submit_button_routh.pack(pady=5)

routh_label = tk.Label(output_frame, text="", font=("Arial", 10), justify=tk.LEFT)
routh_label.pack(side=tk.TOP, pady=10)

window.mainloop()
