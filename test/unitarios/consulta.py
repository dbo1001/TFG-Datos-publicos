import unittest
import pandas as pd
from web import app
from web import consulta


class ConsultaUnitTest(unittest.TestCase):
    """
    Test unitarios relacionados con la consulta
    """

    def setUp(self):
        """
        Antes de las pruebas
        """
        app.testing = True
        self.context = app.app_context()

    def test_fuentes(self):
        """
        Prueba los métodos relacionados con fuentes
        """
        fuentes = ['municipios', 'aeat_renta', 'ine_poblacion', 'sepe_contratos',
                   'sepe_empleo', 'sepe_paro', 'mir_congreso']
        self.assertEqual(consulta.todas_fuentes(), fuentes)

    def test_descripcion_fuente(self):
        """
        Prueba la descripción de una fuente
        """
        fuente = 'aeat_renta'
        descripcion = 'Estadísticas de la renta de la Agencia Tributaria de 2013 a 2015.'
        self.assertTrue(consulta.descripcion_fuente(fuente), descripcion)

        # Fuente no existe
        self.assertRaises(ValueError, consulta.descripcion_fuente, 'no existe')

    def test_columnas(self):
        """
        Comprueba las columnas
        """
        columnas = ['Todas', 'Codigo comunidad', 'Codigo Provincia',
                    'Codigo municipio (local)', 'DC', 'Municipio', 'Codigo Municipio']
        with self.context:
            self.assertEqual(consulta.columnas_coleccion('municipios'), columnas)
            # No existe
            self.assertRaises(AttributeError, consulta.columnas_coleccion, 'no existe')

    def test_todas_columnas(self):
        """
        Prueba que se devuelven las columnas de todas las fuentes
        """
        n_columnas = 106
        with self.context:
            columnas = consulta.todas_columnas()
            self.assertEqual(len(columnas), n_columnas)

    def test_columna_calculada(self):
        """
        Prueba los métodos relacionados con columnas calculadas
        """
        # Test expande
        d = {'col1': [1, 2], 'col2': [3, 4]}
        df = pd.DataFrame(data=d)
        exp = '(col1+col2.mean())/2'
        resultado = "(df['col1']+df['col2'].mean())/2"
        expandido = consulta.expande(df, exp)
        self.assertEqual(expandido, resultado)

        # Columna calculada
        resultado = 5.0
        calculada = consulta.columna_calculada(df, exp)
        self.assertEqual(calculada.sum(), resultado)

    def test_merge_dataframes(self):
        """
        Prueba el método para juntar dos dataframes
        """
        d1 = {'Codigo Municipio': ['09059', '09219'], 'A': [1, 2]}
        d2 = {'Codigo Municipio': ['09059', '09219'], 'B': ['a', 'b']}
        d3 = {'Codigo Municipio': ['09059', '09219'], 'A': [1, 2], 'B': ['a', 'b']}
        df1 = pd.DataFrame(data=d1)
        df2 = pd.DataFrame(data=d2)
        r = pd.DataFrame(data=d3).sort_index(axis=1)
        merge = consulta.merge_dataframes(df1, df2, 'inner').sort_index(axis=1)
        self.assertTrue(merge.equals(r))

    def test_consulta(self):
        """
        Prueba una consulta
        """
        entrada = {
            'fuente': ['municipios'],
            'columna_filtro': ['Municipio'],
            'comparador': ['$eq'],
            'valor': ['Miranda de Ebro'],
            'mostrar': 1000,
            'columna_mostrar': ['Codigo Provincia', 'Codigo Municipio', 'Municipio'],
            'join': 'inner',
            'columna_calculada': ''
        }
        d = {'Codigo Municipio': ['09219'], 'Codigo Provincia': ['09'], 'Municipio': 'Miranda de Ebro'}
        r = pd.DataFrame(data=d).sort_index(axis=1)

        with self.context:
            c = consulta.consulta(entrada).sort_index(axis=1)
            self.assertTrue(c.equals(r))
            # No hay resultados
            entrada['valor'] = ['no existe']
            c = consulta.consulta(entrada)
            self.assertTrue(c.empty)
