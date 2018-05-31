import pandas as pd
import requests
import io
from fuentes.Fuente import Fuente, rename, to_numeric
from zipfile import ZipFile


class Mir(Fuente):
    """
    Fuente de datos para el ministerio del interior
    """

    renombrar = {
        'Código de Provincia': 'Codigo Provincia',
        'Código de Municipio': 'Codigo Municipio'
    }

    posiciones = (
        ('Izquierda', ['PODEMOS', 'EQUO', 'IC-V', 'PCE', 'EH Bildu', 'BLOC-EV', 'BLOC-IDPV-EV-EE', 'BLOC-VERDS',
                       'COMPROMÍS-Q', 'EV-AE', 'EV-AV', 'EV-LV', 'ERC', 'ERC-CATSÍ', 'ESQUERRA', 'ERC-CATSI',
                       'PCPE', 'CUP', 'aralar', 'IA', 'IU', 'ANC']),
        ('Centroizquierda', ['PSOE', 'PSC', 'PS', 'PSA', 'PSA-PA', 'NC', 'EA']),
        ('Centroderecha', ['CIU', 'PDP', 'ERC', 'PDeCAT', 'PNV', 'CDC', 'CCa-PNC', 'DC', 'PAR', 'UPL']),
        ('Derecha', ['PP', 'C\'s', 'AP', 'UPN', 'FAC'])
    )

    def __init__(self, url, anios, tabla, descripcion):
        self.url_base = url
        self.anios = anios
        super().__init__('mir', tabla, descripcion)

    @staticmethod
    def categoriza_partidos(df, posicion, lista):
        """
        Categoriza partidos políticos según su posición
        """
        comunes = df.columns.intersection(lista)
        df[posicion] = df[comunes].sum(axis=1)
        df.drop(comunes, axis=1, inplace=True)
        return df

    @staticmethod
    def categoriza_otros(df):
        """
        Categoriza los partidos políticos con posición desconocida
        """
        columnas = ['Nombre de Comunidad', 'Código de Provincia', 'Nombre de Provincia',
                    'Código de Municipio', 'Nombre de Municipio', 'Población',
                    'Número de mesas', 'Total censo electoral', 'Total votantes',
                    'Votos válidos', 'Papeletas a candidaturas', 'Votos en blanco',
                    'Votos nulos', 'Izquierda', 'Centroizquierda', 'Centroderecha',
                    'Derecha', 'Año']
        df['Otros'] = df.drop(columnas).sum(axis=1)
        df = df[columnas + ['Otros']]
        return df

    @staticmethod
    def procesa_datos(url, anio):
        """
        Lee un documento y lo convierte en un DataFrame
        """
        header = 5
        while True:
            try:
                r = requests.get(url)
                comprimido = ZipFile(io.BytesIO(r.content))
                nombre_excel = '04_{}_1.xlsx'.format(anio)
                excel = comprimido.open(nombre_excel)
                df = pd.read_excel(excel, header=header, skipfooter=6)
                df.fillna(0, inplace=True)
                # Comvierte los códigos a string
                df['Código de Provincia'] = df['Código de Provincia'].astype(str).str.zfill(2)
                df['Código de Municipio'] = df['Código de Municipio'].astype(str).str.zfill(3)
                df['Nombre de Provincia'] = df['Nombre de Provincia'].str.strip()
                df['Nombre de Municipio'] = df['Nombre de Municipio'].str.strip()
                # Añade el año
                df['Año'] = int(str(anio)[:4])
                # Sustituye los puntos en los nombres de columnas (no soportado por Mongo)
                df.columns = df.columns.str.replace('.', '')
                df.columns = df.columns.str.strip()
                break
            # Puede tener varias filas en blanco por encima de la tabla
            except KeyError as ex:
                header += 1
                if header == 10:
                    raise ex
        return df

    @rename(renombrar)
    def carga(self):
        """
        Devuelve un dataframe después de descargar los datos
        """
        dataframes = []
        for anio in self.anios:
            url = self.url_base.format(anio)
            df = self.procesa_datos(url, anio)
            # Categoriza los partidos
            for pos, poslist in self.posiciones:
                df = self.categoriza_partidos(df, pos, poslist)
            df = self.categoriza_otros(df)
            print('Elecciones {}', anio)
            dataframes.append(df)
        df = pd.concat(dataframes)
        df.reset_index(inplace=True, drop=True)
        return df


class MirElecciones(Mir):
    """
    Resultados electorales del congreso
    """

    def __init__(self):
        url_base = 'http://www.infoelectoral.mir.es/infoelectoral/docxl/04_{}_1.zip'
        anios = [198706, 199105, 199505, 199906, 200305, 200705, 201105]
        descripcion = 'Resultados de elecciones municipales por año por partido del Ministerio del Interior.'
        super().__init__(url_base, anios, 'elecciones', descripcion)
