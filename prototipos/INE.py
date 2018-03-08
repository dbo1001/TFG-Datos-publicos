import requests
import pandas as pd


# Mezcla las dos cabeceras en una sola
def new_column_names(header, nombre_subtotal, cabecera):
    # La primera columna (municipio) solo aparece una vez sin modicarse
    columnas = [header[0]]
    anterior = None

    for nombre, tipo in zip(header[1:], cabecera[1:]):
        if type(tipo) is str:
            anterior = tipo
        else:
            tipo = anterior
        nuevo_nombre = '-'.join([nombre_subtotal, tipo, nombre])
        columnas.append(nuevo_nombre)

    return columnas


def procesa_provincia(codigo_provincia, url_provincia):
    # Carga el excel sin las primeras líneas ni las últimas
    df = pd.read_excel(url_provincia, skip_footer=6)

    # Guarda la cabecera para cambiar el nombre de las columnas
    cabecera = df.iloc[5]
    provincia = df.iloc[0, 0]
    df.columns = df.iloc[6]
    # Elimina la cabecera
    df = df[7:]

    # Da un nombre a la primera columna
    df.columns.values[0] = 'Municipio'

    # Filas que empiezan por el código de provincia
    subtotales = df.loc[~df['Municipio'].str.startswith('    ' + codigo_provincia)]
    # Filas que además no contienen 'Total'
    subtotales = subtotales.loc[~subtotales['Municipio'].str.contains('Total')]

    sub_nombre = subtotales['Municipio'].values
    sub_index = subtotales['Municipio'].index

    # Subtotales
    # 0: ambos sexos, 1: hombres, 2: mujeres
    sub_data = []

    for i in range(len(sub_nombre)):
        ini = sub_index[i] + 1
        fin = ini + (sub_index[1] - sub_index[0])
        sub_data.append(df[(df.index > ini) & (df.index < fin - 1)])

    # Cambia las columnas de cada subdata
    for data, nombre, index in zip(sub_data, sub_nombre, sub_index):
        new_columns = new_column_names(data.columns, nombre, cabecera)
        data.columns = new_columns

    # Une todos los sub_data
    data = sub_data[0]

    for s_data in sub_data[1:]:
        # Une los sub_data
        data = data.merge(s_data, on=['Municipio'])

    # Añade la columna Provincia al principio del dataframe final
    data.insert(0, 'Provincia', provincia)

    return data


# código de provincias  01 ... 51
codigo_provincias = [format(n, '02d') for n in range(1, 52)]

url_base = 'http://www.ine.es/jaxi/files/_px/es/xls/t20/e245/p05/a2016/l0/000{}002.px?'
url_provincias = [url_base.format(c) for c in codigo_provincias]

datos_provincias = []

for provincia in zip(codigo_provincias, url_provincias):
    datos_provincia = procesa_provincia(*provincia)
    datos_provincias.append(datos_provincia)

# Dataframe con todas las provincias
datos = pd.concat(datos_provincias)

# Elimina el código de provincia dejando sólo el nombre
datos['Provincia'] = datos['Provincia'].str.split('.-').str[-1].str.strip()
# Elimina el código del municipio
datos['Municipio'] = datos['Municipio'].str.split('-').str[-1]

# Elimina el índice que se ha generado al juntar los dataframes
datos = datos.reset_index(drop=True)

# datos.to_excel("Todas_Provincias.xls")
