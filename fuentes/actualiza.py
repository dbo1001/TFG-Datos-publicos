from fuentes import Database, fuentes


def actualiza_fuentes(config):
    db = Database.Database(
        database=config.MONGO_DBNAME,
        host=config.MONGO_HOST,
        port=config.MONGO_PORT,
        username=config.MONGO_USERNAME,
        password=config.MONGO_PASSWORD,
        authSource=config.MONGO_DBNAME
    )

    # Carga los dataframes de cada fuente de datos
    # en una colección con el nombre de la fuente
    for fuente in fuentes:
        # Instancia la clase y carga el dataframe
        instancia = fuente()
        # Carga el dataframe
        df = instancia.carga()
        coleccion = instancia.coleccion()
        # Inserta el dataframe en la base de datos
        db.carga_datos(df, coleccion)
        print('{} cargado'.format(coleccion))

    db.close()
