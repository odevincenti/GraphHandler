import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from file_parser import parse_mc, parse_csv, parse_txt

# CONFIGURACION DEL GRÁFICO
title = "Gráfico de ejemplo"        # Título del gráfico
xlabel = "Eje x"        # Título del eje x
ylabel = "Eje y"        # Título del eje y

colors = ["silver", "blue", "orange", "green"]          # Color de cada curva EN ORDEN
labels = ["Montecarlo", "Teoría", "Simulación", "Medición"]          # Label de cada curva EN ORDEN

lims = True                         # Poner en True para customizar los límites
xlim = np.array([0, 0.05])          # Dominio de x
ylim = np.array([-3.5, 5])            # Dominio de y

ticks = True       # Poner en True para customizar los labels
delta = 0.1*(xlim[1] - xlim[0])
xticks = [xlim[0], 2*delta + xlim[0], 4*delta + xlim[0], 6*delta + xlim[0], 8*delta + xlim[0], xlim[1]]
xticklabels = [str(xlim[0]), "", "T", "", "2T", str(xlim[1])]
delta = 0.1*(ylim[1] - ylim[0])
yticks = [ylim[0], 2*delta + ylim[0], 4*delta + ylim[0], 6*delta + ylim[0], 8*delta + ylim[0], ylim[1]]
yticklabels = [str(ylim[0]), "", "$0$", "", "", str(ylim[1])]

# AUTOMATIZACIÓN DE GRÁFICOS
'''
Si se guardan todos los archivos respetando un formato, será posible hacer distintos gráficos cambiando sólo unos parámetros
'''
path = r"G:\Unidades compartidas\ASSD - Grupo 1\Graficador\Ejemplos\\"
circuit = "Ej"
param = "Vo"

# CÁLCULO DE CURVA TEÓRICA
f = 1/0.02
A = 3.5
t_teo = np.linspace(0, 0.1, 1000)
y_teo = A*np.sin(2*np.pi*f*t_teo)

# PROCESAMIENTO DE DATOS
t , y = [[], []]
for i in range(len(labels)):
    t.append([])
    y.append([])
t[0], y[0] = parse_mc(path + r"Simulaciones\\"+ circuit + "_" + param + "_mc.txt")[0]
t[1], y[1] = [t_teo, y_teo]
t[2], y[2] = parse_txt(path + r"Simulaciones\\" + circuit + "_" + param + "_sim.txt")[0]
t[3], y[3], x = parse_csv(path + r"Mediciones\\" + circuit + "_" + param + "_med.csv")[0]

# GRÁFICOS
fig, ax = plt.subplots(1)
ax.set_title(title)
h = []

# Plot
for k in range(len(t)):
    if isinstance(t[k][0], float):
        ax.plot(t[k], y[k], color=colors[k])
    else:    
        for i in range(len(t[k])):
            ax.plot(t[k][i], y[k][i], color=colors[k])
    h.append(Line2D([], [], color=colors[k], label=labels[k]))

ax.legend(handles=h)
ax.set_xlabel(xlabel)
ax.set_ylabel(ylabel)
if lims:
    ax.set_xlim(xlim*1.1)
    ax.set_ylim(ylim*1.1)
if ticks:
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels)
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)

ax.grid()
fig.tight_layout()
plt.savefig(path + r"Gráficos\\" + circuit + "_" + param + ".jpg", dpi=300)
plt.show()


