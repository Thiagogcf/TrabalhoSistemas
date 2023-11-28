import tkinter as tk
from tkinter import messagebox
import control as ct
import matplotlib.pyplot as plt
from sympy import simplify, symbols
from sympy.parsing.sympy_parser import parse_expr
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Funções auxiliares para manipulação de expressões
def getExpr(raw_expr):
    parsed_expr = parse_expr(str(raw_expr))
    simplified_expr = simplify(parsed_expr)
    return simplified_expr

def determinant(r1c1, r1c2, r2c1, r2c2):
    det = simplify((r1c1 * r2c2) - (r2c1 * r1c2))
    return det

# Função para implementar o critério de Routh-Hurwitz
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

# Função para plotar os gráficos de Root Locus e Bode
def plot_graphs(num, den):
    sys = ct.TransferFunction(num, den)

    fig, axs = plt.subplots(2, figsize=(12, 10))

    # Plot do Root Locus
    ct.root_locus(sys, plot=True, ax=axs[0])
    axs[0].set_xlabel('Real Axis')
    axs[0].set_ylabel('Imaginary Axis')
    axs[0].set_title('Root Locus Plot')
    axs[0].grid(True)

    # Plot do Bode
    mag, phase, omega = ct.bode(sys, dB=True, Plot=False)
    axs[1].semilogx(omega, 20 * np.log10(mag))
    axs[1].set_xlabel('Frequency [rad/s]')
    axs[1].set_ylabel('Magnitude [dB]')
    axs[1].set_title('Bode Plot')
    axs[1].grid(True)

    plt.tight_layout()
    return fig

# Função para processar os dados inseridos pelo usuário
def on_submit():
    try:
        num = [float(x) for x in entry_num.get().split()]
        den = [float(x) for x in entry_den.get().split()]
        fig = plot_graphs(num, den)
        canvas = FigureCanvasTkAgg(fig, master=output_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Interface gráfica Tkinter
window = tk.Tk()
window.title("Root Locus e Bode Plot")
window.geometry("800x600")  # Tamanho da janela

# Estilos
font_style = ("Arial", 12)
label_font_style = ("Arial", 10, "bold")
button_style = {"font": ("Arial", 10, "bold"), "bg": "#4C8BF5", "fg": "white"}

# Frames
input_frame = tk.Frame(window, pady=20)
input_frame.pack(fill="both")

output_frame = tk.Frame(window)
output_frame.pack(fill="both", expand=True)

# Componentes do Frame de Entrada
tk.Label(input_frame, text="Root Locus e Bode Plot", font=("Arial", 16, "bold")).pack()
tk.Label(input_frame, text="Insira os coeficientes para análise", font=label_font_style).pack()

tk.Label(input_frame, text="Coeficientes do Numerador:", font=label_font_style).pack()
entry_num = tk.Entry(input_frame, font=font_style)
entry_num.pack()

tk.Label(input_frame, text="Coeficientes do Denominador:", font=label_font_style).pack()
entry_den = tk.Entry(input_frame, font=font_style)
entry_den.pack()

submit_button = tk.Button(input_frame, text="Plotar Gráficos", command=on_submit, **button_style)
submit_button.pack(pady=10)

window.mainloop()
