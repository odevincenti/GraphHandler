import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from file_parser import parse_mc, parse_csv, parse_txt

# AUTOMATIZACIÓN DE GRÁFICOS
'''
Si se guardan todos los archivos respetando un formato, será posible hacer distintos gráficos cambiando sólo unos parámetros
'''
path = r"G:\Mi unidad\Mi PC\Documentos\Materias\ASSD\TP1\\"
circuit = "M5"
f = 100E3
param = 50

# CONFIGURACION DEL GRÁFICO
title = "Gráfico de ejemplo"        # Título del gráfico
xlabel = "Eje x"        # Título del eje x
ylabel = "Eje y"        # Título del eje y

colors = ["blue", "orange", "green"]          # Color de cada curva EN ORDEN
labels = ["Rampa", "Cuadrada", "$V_\{threshold\}$"]          # Label de cada curva EN ORDEN

lims = False                         # Poner en True para customizar los límites
xlim = np.array([0, 0.05])          # Dominio de x
ylim = np.array([-3.5, 5])            # Dominio de y

ticks = False       # Poner en True para customizar los labels
delta = 0.1*(xlim[1] - xlim[0])
xticks = [xlim[0], 2*delta + xlim[0], 4*delta + xlim[0], 6*delta + xlim[0], 8*delta + xlim[0], xlim[1]]
xticklabels = [str(xlim[0]), "", "T", "", "2T", str(xlim[1])]
delta = 0.1*(ylim[1] - ylim[0])
yticks = [ylim[0], 2*delta + ylim[0], 4*delta + ylim[0], 6*delta + ylim[0], 8*delta + ylim[0], ylim[1]]
yticklabels = [str(ylim[0]), "", "$0$", "", "", str(ylim[1])]

# PROCESAMIENTO DE DATOS
data = parse_txt(path + r"Simulaciones\\" + str(circuit) + "_" + str(int(f * 1E-3)) + 'kHz_DC' + str(param) + "_sim.txt")[0]
t = data[0]
y = data[1:]
    

# GRÁFICOS
fig, ax = plt.subplots(1)
ax.set_title(title)
h = []

# Plot
for k in range(len(y)):
    ax.plot(t, y[k], color=colors[k], label=labels[k])

ax.legend(loc="center right")
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
plt.savefig(path + r"Gráficos\\" + str(circuit) + "_" + str(int(f * 1E-3)) + 'kHz_DC' + str(param) + "_sim.jpg", dpi=300)
plt.show()
