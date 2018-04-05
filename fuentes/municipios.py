import pandas as pd
from fuentes.Fuente import Fuente


class Municipios(Fuente):
    """
    Obtiene el código de cada municipio
    """

    def __init__(self):
        self.url = 'http://www.ine.es/daco/daco42/codmun/codmun18/18codmun.xlsx'
        super().__init__('codigos', 'municipios')

    def carga(self):
        """
        Devuelve el Dataframe con los códigos
        """
        # Carga el xls omitiendo la primera fila y como de las columnas tipo string
        df = pd.read_excel(self.url, header=1, dtype=str)
        # Renombra las columnas
        df.columns = ['Codigo comunidad', 'Codigo provincia',
                      'Codigo municipio', 'DC', 'Municipio']
        # Calcula el código de provincia
        df['Codigo'] = df['Codigo provincia'] + df['Codigo municipio']
        return df

    def coleccion(self):
        """
        Nombre de la colección donde se guardan los codigos
        """
        return 'municipios'
