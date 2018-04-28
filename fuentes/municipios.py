import pandas as pd
from fuentes.Fuente import Fuente, rename


class Municipios(Fuente):
    """
    Obtiene el código de cada municipio
    """

    renombrar = {
        'Codigo municipio': 'Codigo municipio (local)',
        'Codigo': 'Codigo Municipio'
    }

    def __init__(self):
        self.url = 'http://www.ine.es/daco/daco42/codmun/codmun18/18codmun.xlsx'
        descripcion = 'Lista de municipios con sus códigos de comunidad, provincia y municipio ' \
        'del instituto nacional de estadística'
        super().__init__('municipios', descripcion=descripcion)

    @rename(renombrar)
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
