import unittest
import os
import pandas as pd
from web import app
from web import mapa


class MapaUnitTest(unittest.TestCase):
    """
    Test unitarios relacionados con la representación de mapas
    """

    def setUp(self):
        """
        Antes de las pruebas
        """
        app.testing = True

    def test_agrupa_df(self):
        """
        Prueba los valores de un dataframe
        """
        d = {'Codigo Provincia': ['09', '09'], 'Número de habitantes': [20000, 30000]}
        df = pd.DataFrame(data=d)
        resultados = (
            ('mean', 25000),
            ('sum', 50000),
            ('count', 2)
        )

        for metodo, valor in resultados:
            agrupados = mapa.agrupa_df(df, metodo).sort_index(axis=1)
            d = {'Codigo Provincia': ['09'], 'Número de habitantes': [valor]}
            r = pd.DataFrame(data=d).sort_index(axis=1)
            self.assertTrue(agrupados.equals(r))

    def test_visualiza_mapa(self):
        """
        Prueba el método para visualizar el mapa
        """
        os.chdir('..')
        columna = 'Número de habitantes'
        d = {'Codigo Provincia': ['09'], columna: [50000]}
        df = pd.DataFrame(data=d)
        m = mapa.visualiza_mapa(df, columna, 'provincias', 'mean')
        bounds = [[27.639545, -18.161222], [43.792351, 4.327785]]
        self.assertEqual(m.get_bounds(), bounds)
