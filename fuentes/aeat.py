import pandas as pd
from .Fuente import Fuente


class Aeat(Fuente):

    def __init__(self, anios, tabla):
        self.url_aeat = 'http://www.agenciatributaria.es/AEAT/Contenidos_Comunes/La_Agencia_Tributaria/Estadisticas/Publicaciones/sites/'
        self.urls = anios
        super().__init__('aeat', tabla)

    @staticmethod
    def procesa_datos(url):
        df = pd.read_html(url)[0]
        # Cambia el nombre de la primera columna
        df.rename(columns={'Unnamed: 0': 'Municipio'}, inplace=True)
        # Elimina el total, comunidades y provincias
        df = df[df['Municipio'].str.match(r'.+-[0-9]{5}')]
        # Elimina el código de provincia
        df['Municipio'] = df['Municipio'].str.split('-').str[0]
        return df

    def carga(self):
        dataframes = []
        for anio, url in self.urls:
            url = self.url_aeat + url
            df = self.procesa_datos(url)
            df['Año'] = anio
            dataframes.append(df)
        df = pd.concat(dataframes)
        df = df.reset_index(drop=True)
        return df


class AeatRenta(Aeat):

    def __init__(self):
        anios = (
            (2013, 'irpfmunicipios/2013/jrubikf6d2fcd70c4d0ec216836abfe9f974b4309c26da4.html'),
            (2014, 'irpfmunicipios/2014/jrubik4e93d46e7e85aa3dd4296c3fb35c28a0723d87a0.html'),
            (2015, 'irpfmunicipios/2015/jrubik1ba3b6ffb879f0b4654305cde4f7da3038a346e9.html')
        )
        super().__init__(anios, 'renta')