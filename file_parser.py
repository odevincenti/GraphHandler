import numpy as np
import os

def parse_csv(path):
    '''
    parse_csv: Parsea el csv de la medición de la Digilent
    Devuelve data, labels y units.
    '''
    if not check_file(os.path.normpath(path), ".csv"):
        raise(FileNotFoundError("Hubo un error al buscar el archivo " + os.path.normpath(path)))

    file = open(os.path.normpath(path), "r")
    l = file.readline()
    if l.find(",") != -1: sep = ","
    else: sep = ";"
    labels = l.split(sep)
    data = [[] for i in labels]
    units = __get_units(labels)
    l = file.readline()
    while l != '\n' and l != '':
        l = l.split(sep)
        for j in range(len(data)):
            data[j].append(float(l[j]))
        l = file.readline()
    file.close()

    return data, labels, units

def parse_txt(path):
    '''
    parse_txt: Parsea el txt de la simulación de LTSpice
    Devuelve data y labels
    '''
    if not check_file(os.path.normpath(path), ".txt"):
        raise(FileNotFoundError("Hubo un error al buscar el archivo " + os.path.normpath(path)))

    file = open(os.path.normpath(path), "r")

    l = file.readline()
    labels = l.split("\t")
    labels[-1] = labels[-1].removesuffix("\n")

    data = [[] for i in labels]

    l = file.readline()
    while l != "\n" and l != "":
        l = l.split("\t")
        if "#" in '\t'.join(l):
            l = file.readline()
            continue
        for i in range(len(data)):
            data[i].append(float(l[i]))
        l = file.readline()
    file.close()

    return data, labels

def parse_mc(path):
    '''
    parse_mc: Parsea el txt de la simulación de Montecarlo de LTSpice
    Devuelve data y labels
    '''
    if not check_file(os.path.normpath(path), ".txt"):
        raise(FileNotFoundError("Hubo un error al buscar el archivo " + os.path.normpath(path)))

    file = open(os.path.normpath(path), "r")

    l = file.readline()
    labels = l.split("\t")
    labels[-1] = labels[-1].removesuffix("\n")

    l = file.readline()
    j1 = l.find("/")
    j2 = l.find(")")
    runs = int(l[j1 + 1: j2])

    data = [[] for i in labels]

    for k in range(runs):
        for i in range(len(data)):
            data[i].append([])
        l = file.readline()
        while l.find('Run') == -1  and l != "" and l != "\n":
            l = l.split("\t")
            for i in range(len(data)):
                data[i][k].append(float(l[i]))
            l = file.readline()
    file.close()

    return data, labels

def check_file(path, ex):
    '''
    check_file: Revisa que el archivo exista, tenga la extensión correspondiente y el formato adecuado
    Devuelve False en caso de error
    '''
    r = True
    ext = os.path.splitext(path)[1]
    if ext != ex:
        print("El archivo de la medición no es " + ex)
        r = False
    if not os.path.isfile(path):
        print("El archivo" + path + "no existe")
        r = False
    elif not os.access(path, os.R_OK):
        print("El archivo no es legible")
        r = False
    return r

def format_unit(x, d = 2):
    '''
    format_unit: Obtiene la unidad correcta y escala el número para que sea más fácil de leer
    Recibe a x como número y la devuelve como string
    '''
    y = np.abs(x)
    if y < 1E-9:
        m = "p"         # Pico
        x = x / 1E-12
    elif y < 1E-6:
        m = "n"         # Nano
        x = x / 1E-9
    elif y < 1E-3:
        m = "u"         # Micro
        x = x / 1E-6
    elif y < 1:
        m = "m"         # Mili
        x = x / 1E-3
    elif y < 1E3:
        m = ""          # Normal
    elif y < 1E6:
        m = "k"         # Kilo
        x = x / 1E3
    elif y < 1E9:
        m = "M"         # Mega
        x = x / 1E6
    else:
        m = "G"         # Giga
        x = x / 1E9
    return "{:.{p}f}".format(x, p=d) + m

def __get_units(labels):
    units = []
    for i in range(len(labels)):
        j1 = labels[i].find("(")
        j2 = labels[i].find(")")
        labels[i] = labels[i][0: j1 - 1]
        units.append(labels[i][j1 + 1: j2])
        labels[i] = labels[i][j2 + 2:]
    return units
