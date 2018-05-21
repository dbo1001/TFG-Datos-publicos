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

    def __init__(self, url, anios, tabla, descripcion):
        self.url_base = url
        self.anios = anios
        super().__init__('mir', tabla, descripcion)

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
                nombre_excel = '02_{}_1.xlsx'.format(anio)
                excel = comprimido.open(nombre_excel)
                df = pd.read_excel(excel, header=header)
                # Comvierte los códigos a string
                df['Código de Provincia'] = df['Código de Provincia'].astype(str).str.zfill(2)
                df['Código de Municipio'] = df['Código de Municipio'].astype(str).str.zfill(3)
                # Añade el año
                df['Año'] = int(str(anio)[:4])
                # Sustituye los puntos en los nombres de columnas (no soportado por Mongo)
                df.columns = df.columns.str.replace('.', '-')
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
            dataframes.append(df)
        df = pd.concat(dataframes)
        df.reset_index(inplace=True, drop=True)
        return df


class MirCongreso(Mir):
    """
    Resultados electorales del congreso
    """

    def __init__(self):
        url_base = 'http://www.infoelectoral.mir.es/infoelectoral/docxl/02_{}_1.zip'
        anios = [197706, 197903, 198210, 198606, 198910,
                 199306, 199603, 200003, 200403, 200803,
                 201111, 201512, 201606]
        descripcion = 'Resultados electorales del congreso por año por partido del Ministerio del Interior.'
        super().__init__(url_base, anios, 'congreso', descripcion)
