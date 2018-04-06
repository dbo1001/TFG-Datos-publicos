import re
import pandas as pd
from web import mongo
from fuentes import fuentes


def todas_fuentes():
    """
    Lista todas las fuentes
    """
    lista_fuentes = [fuente().coleccion() for fuente in fuentes]
    return lista_fuentes


def todas_columnas():
    """
    Lista todas las columnas de todas las fuentes
    """
    columnas = ['Todas']
    for fuente in todas_fuentes():
        cols = columnas_coleccion(fuente)
        columnas.extend(cols)
    return set(columnas)


def columnas_coleccion(coleccion):
    """
    Lista todas las columnas de una colección
    """
    return ['Todas'] + list(mongo.db[coleccion].find_one().keys())[1:]


def consulta(fuente, columna, mostrar, comparador, valor):
    """
    Devuelve el dataframe de la consulta
    """
    if columna == 'Todas':
        # Mustra todas las filas
        filtro = {}
    else:
        if comparador == '$eq':
            busqueda = re.compile(valor, re.IGNORECASE)
        else:
            valor = float(valor)
            busqueda = {comparador: valor}

        filtro = {
            columna: busqueda
        }

    # Si no se ha seleccionado una columna a mostrar, muestra todas
    if not mostrar:
        mostrar = None

    cursor = mongo.db[fuente].find(filtro, mostrar)
    df = pd.DataFrame.from_records(cursor, exclude=['_id'])

    return df
