import pandas as pd
from fuentes.Fuente import Fuente


class Sepe(Fuente):
    """
    Fuente de datos para el Servicio Público de Empleo Estatal
    """

    def __init__(self, url, anios, tabla):
        url_sepe = 'https://sede.sepe.gob.es/es/portaltrabaja/resources/sede/datos_abiertos/datos/'
        self.url = url_sepe + url
        self.anios = anios
        super().__init__('sepe', tabla)

    @staticmethod
    def procesa_datos(url):
        df = pd.read_csv(url, sep=';', encoding='latin1', header=1)
        # Elimina columnas innecesarias
        df.drop('Código mes ', axis=1, inplace=True)
        return df

    def carga(self):
        dataframes = []
        for anio in self.anios:
            url = self.url.format(anio)
            df = self.procesa_datos(url)
            dataframes.append(df)
            print(url)
        df = pd.concat(dataframes)
        # Renombra columnas
        df.rename({
            'mes': 'Fecha',
            ' Municipio': 'Municipio'
        })
        # Restaura los índices
        df = df.reset_index(drop=True)
        return df


class SepeContratos(Sepe):
    """
    Contratos por sexo y por edades por cada municipio
    """

    def __init__(self):
        url = 'Contratos_por_municipios_{}_csv.csv'
        anios = range(2006, 2019)
        super().__init__(url, anios, 'contratos')


class SepeEmpleo(Sepe):
    """
    Demandantes de empleo por sexo y por edades por cada municipio
    """

    def __init__(self):
        url = 'Dtes_empleo_por_municipios_{}_csv.csv'
        anios = range(2006, 2019)
        super().__init__(url, anios, 'empleo')


class SepeParo(Sepe):
    """
    Paro por sexo y por edades por cada municipio
    """

    def __init__(self):
        url = 'Paro_por_municipios_{}_csv.csv'
        anios = range(2006, 2019)
        super().__init__(url, anios, 'paro')
