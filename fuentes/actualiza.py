from fuentes import Database, Municipios, fuentes
import pandas as pd


def actualiza_fuentes(config):
    """
    Actualiza todas las fuentes de datos
    """
    db = Database.Database(
        database=config.MONGO_DBNAME,
        host=config.MONGO_HOST,
        port=config.MONGO_PORT,
        username=config.MONGO_USERNAME,
        password=config.MONGO_PASSWORD,
        authSource=config.MONGO_DBNAME
    )

    municipios = carga_fuente(Municipios, db)
    codigos = municipios.loc[:, ['Municipio', 'Codigo Municipio']]

    # Carga los dataframes de cada fuente de datos
    # en una colección con el nombre de la fuente
    for fuente in fuentes:
        carga_fuente(fuente, db, codigos)

    db.close()


def carga_fuente(fuente, db, codigos=None):
    """
    Carga una fuente de datos
    """
    # Instancia la clase y carga el dataframe
    instancia = fuente()
    df = instancia.carga()
    # Añade el código de municipio
    if codigos is not None:
        df = aniade_codigo_municipio(df, codigos)
    # Inserta el dataframe en la base de datos
    coleccion = instancia.coleccion()
    db.carga_datos(df, coleccion)
    print('{} cargado'.format(coleccion))
    # Devuelve el dataframe si no se añade el código de municipio
    if codigos is None:
        return df


def aniade_codigo_municipio(df, codigos):
    """
    Añade el código de municipio al dataframe
    """
    # Solo si no existe
    if 'Codigo Municipio' not in df and 'Municipio' in df:
        df = pd.merge(df, codigos, how='left')
    return df
