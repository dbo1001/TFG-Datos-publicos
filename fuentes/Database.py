import json
from pymongo import MongoClient


class Database:
    """
    Carga datos de DataFrames de pandas en la base de datos.
    """

    def __init__(self, database, coleccion, *args, **kwargs):
        self.client = MongoClient(*args, **kwargs)
        self.db = self.client[database][coleccion]

    def carga_datos(self, df, nombre_fuente):
        """
        Carga los datos de un dataframe en la base de datos.
        """
        # Borra la colección
        # db.drop()

        # Convierte el DataFrame a json
        df_json = json.loads(df.T.to_json()).values()

        # Inserta los datos en el documetno de la base de datos
        self.db.insert_many(df_json)

    def close(self):
        """
        Cierra la conexión con la base de datos.
        """
        self.client.close()
