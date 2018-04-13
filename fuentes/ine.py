import pandas as pd
from fuentes.Fuente import Fuente


class Ine(Fuente):
    """
    Fuente de datos para el instituto nacional de estadística
    """

    def __init__(self, tabla, descripcion):
        super().__init__('ine', tabla, descripcion)


class InePoblacion(Ine):
    """
    Población por sexo y edad
    """

    def __init__(self):
        self.url_base = 'http://www.ine.es/jaxi/files/_px/es/xls/t20/e245/p05/a2016/l0/000{}002.px?'
        # código de provincias  01 ... 51
        self.codigo_provincias = [format(n, '02d') for n in range(1, 52)]
        descripcion = 'Estadísticas del padron del Instituto nacional de estadística.' \
                      ' Clasificados por edad, sexo y nacionalidad.'
        super().__init__('poblacion', descripcion)

    @staticmethod
    def new_column_names(header, nombre_subtotal, cabecera):
        """
        Renombra las columnas
        """
        # La primera columna (municipio) solo aparece una vez sin modicarse
        columnas = [header[0]]
        anterior = None

        for nombre, tipo in zip(header[1:], cabecera[1:]):
            if isinstance(tipo, str):
                anterior = tipo
            else:
                tipo = anterior
            nuevo_nombre = '-'.join([nombre_subtotal, tipo, nombre])
            columnas.append(nuevo_nombre)

        return columnas

    def procesa_provincia(self, codigo_provincia):
        """
        Lee un documento y lo convierte en un DataFrame
        """
        url = self.url_base.format(codigo_provincia)
        # Carga el excel sin las primeras líneas ni las últimas
        df = pd.read_excel(url, skip_footer=6)

        # Guarda la cabecera para cambiar el nombre de las columnas
        cabecera = df.iloc[5]
        provincia = df.iloc[0, 0]
        df.columns = df.iloc[6]
        # Elimina la cabecera
        df = df[7:]

        # Da un nombre a la primera columna
        df.columns.values[0] = 'Municipio'

        # Filas que empiezan por el código de provincia
        subtotales = df.loc[~df['Municipio'].str.startswith('    ' + codigo_provincia)]
        # Filas que además no contienen 'Total'
        subtotales = subtotales.loc[~subtotales['Municipio'].str.contains('Total')]

        sub_nombre = subtotales['Municipio'].values
        sub_index = subtotales['Municipio'].index

        # Subtotales
        # 0: ambos sexos, 1: hombres, 2: mujeres
        sub_data = []

        for i in range(len(sub_nombre)):
            ini = sub_index[i] + 1
            fin = ini + (sub_index[1] - sub_index[0])
            sub_data.append(df[(df.index > ini) & (df.index < fin - 1)])

        # Cambia las columnas de cada subdata
        for data, nombre, _ in zip(sub_data, sub_nombre, sub_index):
            new_columns = self.new_column_names(data.columns, nombre, cabecera)
            data.columns = new_columns

        # Une todos los sub_data
        data = sub_data[0]

        for s_data in sub_data[1:]:
            # Une los sub_data
            data = data.merge(s_data, on=['Municipio'])

        # Añade la columna Provincia al principio del dataframe final
        data.insert(0, 'Provincia', provincia)

        return data

    def carga(self):
        """
        Devuelve un dataframe después de descargar los datos
        """
        datos_provincias = []

        for provincia in self.codigo_provincias:
            datos_provincia = self.procesa_provincia(provincia)
            datos_provincias.append(datos_provincia)

        # Dataframe con todas las provincias
        datos = pd.concat(datos_provincias)

        # Elimina el código de provincia dejando sólo el nombre
        datos['Provincia'] = datos['Provincia'].str.split('.-').str[-1].str.strip()
        # Elimina el código del municipio
        datos['Codigo Municipio'], datos['Municipio'] = datos['Municipio'].str.split('-', 1).str

        # Elimina los espacios en el código de municipio
        datos['Codigo Municipio'] = datos['Codigo Municipio'].str.strip()

        # Elimina el índice que se ha generado al juntar los dataframes
        datos = datos.reset_index(drop=True)

        return datos
