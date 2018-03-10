from fuentes import Database, fuentes


db = Database.Database(
    database='datos',
    host='localhost',
    port=27017,
    username=None,
    password=None
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
