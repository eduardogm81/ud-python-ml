# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 10:21:10 2018

@author: AdminQuark
"""
import pandas as pd
import os

# Primero importamos la librería y hacemos la conexión  con la web de los datos
import urllib3

medals_url = "http://winterolympicsmedals.com/medals.csv"

http = urllib3.PoolManager()
r = http.request('GET', medals_url)
r.status
response = r.data

# El objeto es un string binario, así que lo convertimos a un string decodificándolo en UTF-8
str_data = response.decode('utf-8')

# Dividimos el string en un array de filas, separándolo por intros
lines = str_data.split("\n")

# La primera linea contiene la cabecera así que la extraemos
col_names = lines[0].split(",")
n_cols = len(col_names)

# Generamos un diccionario vacío donde irá la información procesada desde la url externa
counter = 0
main_dict = {}

for col in col_names:
    main_dict[col] = []
    
# Procesamos fila a fila la información para ir rellenando el diccionario con los datos    
for line in lines:
    # nos saltamos la primera linea que es la que contiene la cabecera
    if (counter > 0):
        # Dividimos cada string por las comas como elemento separador
        values = line.strip().split(",")
        # Añadimos cada valor a su respectiva columna del diccionario
        for i in range(len(col_names)):
            main_dict[col_names[i]].append(values[i])
    counter += 1

print("El dataset tiene %d filas y %d columnas" % (counter, n_cols))


# Convertimos el diccionario procesado a Data frame y comprobamos que los datos
# son correctos
medals_df = pd.DataFrame(main_dict)
medals_df.head()


# Elegimos donde guardarlo (en la carpeta athletes es donde tiene más sentido 
# por el contenido del análisis)
cwd = os.getcwd()
mainpath = os.path.join(cwd, "../datasets")
filename = "athletes/downloaded_medals1."
fullpath = os.path.join(mainpath, filename)

# Lo guardamos en CSV, JSON o excel
medals_df.to_csv(fullpath + "csv")
medals_df.to_json(fullpath + "json")
medals_df.to_excel(fullpath + "xls")
