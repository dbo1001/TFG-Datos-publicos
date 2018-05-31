import re
import pandas as pd
from flask import flash
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


def expande(df, exp):
    """
    Expande una expresión con las columnas de un dataframe
    """
    columnas = df.columns.values
    reemplazos = ["df['" + col + "']" for col in columnas]
    return reduce(lambda a, kv: a.replace(*kv), zip(columnas, reemplazos), exp)


def columna_calculada(df, exp):
    """
    Crea una serie con datos calculados a partir de la expresión.
    """
    series = None
    try:
        # Alguna expresión
        if exp:
            expandida = expande(df, exp)
            # No se puede usar literal_eval porque estamos usando objetos de pandas
            series = eval(expandida)
            return series
    except (AttributeError, NameError, SyntaxError, TypeError, ValueError):
        flash('Columna calculada no válida')
    return series


def consulta(entrada):
    """
    Devuelve el dataframe de la consulta
    """
    fuentes_entrada = entrada['fuente']
    columnas = entrada['columna_filtro']
    comparadores = entrada['comparador']
    valores = entrada['valor']
    mostrar = entrada['columna_mostrar']
    join = entrada['join']
    exp_calculada = entrada['columna_calculada']
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
                try:
                    busqueda = float(valor)
                except ValueError:
                    try:
                        busqueda = re.compile(valor, re.IGNORECASE)
                    except re.error:
                        flash('Expresión no válida')
                        return pd.DataFrame()
            else:
                valor = float(valor)
                busqueda = {comparador: valor}

            filtro = {
                columna: busqueda
            }

        limite = 500000
        cursor = mongo.db[fuente].find(filtro, mostrar, limit=limite)
        if cursor.count() >= limite:
            flash('Has llegado al límite de columnas ({}).'.format(limite))
        df = pd.DataFrame.from_records(cursor, exclude=['_id'])
        df_fuentes.append(df)

    # Combina las consultaslo
    df = reduce(lambda x, y: merge_dataframes(x, y, join), df_fuentes)

    # Añade la columna calculada
    calculada = columna_calculada(df, exp_calculada)
    if calculada is not None:
        df = df.assign(Calculada=calculada)

    return df


def merge_dataframes(df1, df2, join):
    # Columnas que no están en el df1, pero si en el 2. Y la columna del join
    columnas = list(df2.columns.difference(df1.columns)) + ['Codigo Municipio']
    df_merge = pd.merge(df1, df2[columnas], how=join, on='Codigo Municipio')
    return df_merge
