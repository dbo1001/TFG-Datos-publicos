import re
import pandas as pd
from web import mongo
from fuentes import fuentes
from functools import reduce


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


def descripcion_fuente(coleccion):
    """
    Devuelve la descripción de una fuente
    """
    index = todas_fuentes().index(coleccion)
    fuente = fuentes[index]()
    return fuente.descripcion()


def consulta(entrada):
    """
    Devuelve el dataframe de la consulta
    """
    fuentes_entrada = entrada['fuente']
    columnas = entrada['columna_filtro']
    comparadores = entrada['comparador']
    valores = entrada['valor']
    mostrar = entrada['columna_mostrar']
    max_filas = entrada['max_filas']
    df_fuentes = []

    # Si no se ha seleccionado una columna a mostrar, muestra todas
    if not mostrar:
        mostrar = None

    for fuente, columna, comparador, valor in zip(fuentes_entrada, columnas, comparadores, valores):
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
                "$and": [{columna: busqueda}]
            }

        cursor = mongo.db[fuente].find(filtro, mostrar).limit(max_filas)
        df = pd.DataFrame.from_records(cursor, exclude=['_id'])
        df_fuentes.append(df)

    # Combina las consultaslo
    df = reduce(merge_dataframes, df_fuentes)

    return df


def merge_dataframes(df1, df2):
    df_merge = pd.merge(df1, df2, how='inner', on='Codigo Municipio')
    return df_merge
