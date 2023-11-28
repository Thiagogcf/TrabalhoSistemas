import control as ct
import matplotlib.pyplot as plt
from sympy import simplify
from sympy import latex
from sympy.parsing.sympy_parser import parse_expr


def plot_root_locus_and_bode():
    # Get numerator coefficients from the user
    num_str = input("digite os coeficientes do numerador (separado por espaço): ")
    num = [float(x) for x in num_str.split()]

    # Get denominator coefficients from the user
    den_str = input("digite os coeficientes do denominador (separado por espaço): ")
    den = [float(x) for x in den_str.split()]

    # Create the transfer function
    sys = ct.TransferFunction(num, den)

    # Plot the root locus
    plt.figure(figsize=(12, 5))  # Adjust the figure size as needed
    plt.subplot(1, 2, 1)  # Create a subplot for the root locus
    locus = ct.root_locus(sys, plot=True)
    plt.xlabel('Real Axis')
    plt.ylabel('Imaginary Axis')
    plt.title('Root Locus Plot')
    plt.grid(True)
    plt.show()

    # Plot the Bode plot
    plt.subplot(1, 2, 2)  # Create a subplot for the Bode plot
    mag, phase, omega = ct.bode_plot(sys, dB=True, omega_limits=(1e-2, 1e2), omega_num=1000)
    plt.xlabel('Frequency [rad/s]')
    plt.ylabel('Magnitude [dB]')
    plt.title('Bode Plot')
    plt.grid(True)

    # Adjust layout for better spacing
    plt.tight_layout()

    # Show the plot
    plt.show()


def getExpr(raw_expr):
    parsed_expr = parse_expr(str(raw_expr))
    simplified_expr = simplify(parsed_expr)
    return simplified_expr


def determinant(r1c1, r1c2, r2c1, r2c2):
    det = simplify((r1c1 * r2c2) - (r2c1 * r1c2))
    return det


def printRouthArray(RouthArray):
    for row in RouthArray:
        print(str(row[0]), end='\n * ')
        print('\t | \t', end='')
        for colNum in range(1, len(row)):
            print(str(row[colNum]), '\t\t', end='')
    print('')


def exprArrToStrArr(expr_arr):
    str_arr = expr_arr.copy()
    for i in range(len(str_arr)):
        for j in range(len(str_arr[i])):
            str_arr[i][j] = str(str_arr[i][j]).replace('**', '^')
    return str_arr


def ToLaTeX(str_arr):
    latex_arr = str_arr.copy()
    for i in range(len(latex_arr)):
        for j in range(len(latex_arr[i])):
            latex_arr[i][j] = '$$' + latex(latex_arr[i][j]) + '$$'
    return latex_arr


def RouthHurwitz(polynomial):
    degree = len(polynomial) - 1

    row1 = []
    expr = getExpr(f's ** {degree}')
    row1.append(expr)

    for i in range(degree, -1, -2):
        expr = getExpr(polynomial[i])
        row1.append(expr)

    row2 = []
    expr = getExpr(f's ** {degree - 1}')
    row2.append(expr)

    for i in range(degree - 1, -1, -2):
        expr = getExpr(polynomial[i])
        row2.append(expr)

    if len(row1) > len(row2):
        row2.append(getExpr(0))

    cols = len(row1)
    RouthArray = [row1, row2]

    rowIndex = 2
    for i in range(degree - 2, -1, -1):
        row = [0] * (cols)
        row[0] = getExpr(f's ** {i}')

        for colIndex in range(1, cols):
            try:
                r1c1 = RouthArray[rowIndex - 2][1]
            except IndexError:
                r1c1 = 0

            try:
                r1c2 = RouthArray[rowIndex - 2][colIndex + 1]
            except IndexError:
                r1c2 = 0

            try:
                r2c1 = RouthArray[rowIndex - 1][1]
            except IndexError:
                r2c1 = 0

            try:
                r2c2 = RouthArray[rowIndex - 1][colIndex + 1]
            except IndexError:
                r2c2 = 0

            b = determinant(r1c1, r1c2, r2c1, r2c2) / (-r2c1)
            b = simplify(b)
            row[colIndex] = b

        RouthArray.append(row)
        rowIndex += 1

    return RouthArray


def getden():
    return den


if __name__ == '__main__':
    # (K * a) + (K + 6)s + 11s^2 + 6s^3 + s^4
    arr = ['K * a', 'K + 6', '11', '6', '1']
    # K - 18 + 9s + 8s^2 + s^3
    arr2 = ['K - 18', 9, 8, 1]
    RouthHurwitz(arr2)
# Call the function to plot the root locus and Bode plot

plot_root_locus_and_bode()

L = list(map(int, input("Digite os valores do denominador separado por espaco\n").split()))
print("\nValores", L)
printRouthArray(RouthHurwitz(L))
