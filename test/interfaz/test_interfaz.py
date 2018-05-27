import unittest
from os import path
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


class InterfazTest(unittest.TestCase):
    """
    Test de interfaz con selenium
    """

    def setUp(self):
        """
        Antes de las pruebas
        """
        ruta = path.join(path.dirname(__file__), 'webdrivers')
        firefox_path = path.join(ruta, 'geckodriver')
        chrome_path = path.join(ruta, 'chromedriver')
        self.drivers = (
            webdriver.Firefox(executable_path=firefox_path),
            webdriver.Chrome(executable_path=chrome_path),
        )
        self.url = 'http://localhost:5000/'

    def tearDown(self):
        """
        Cierra los navegadores
        """
        for driver in self.drivers:
            driver.close()

    def carga_pagina(self, driver, ruta):
        """
        Carga una página en el driver
        """
        url = path.join(self.url, ruta)
        driver.get(url)

    def test_consulta_principal(self):
        """
        Comprueba que carga correctamente la página de consulta
        """
        for driver in self.drivers:
            self.carga_pagina(driver, 'consulta')
            heading = driver.find_element_by_class_name('panel-heading')
            self.assertEqual(heading.text, 'Consulta')

    def test_consulta(self):
        """
        Prueba una consulta vacía
        """
        for driver in self.drivers:
            # Vacía
            self.carga_pagina(driver, 'consulta')
            boton = driver.find_element_by_class_name('btn')
            boton.click()
            tabla = driver.find_element_by_tag_name('table')
            alerta = driver.find_element_by_class_name('alert')
            self.assertIn('Mostrando', alerta.text)
            self.assertIsNotNone(tabla)
            th = driver.find_elements_by_tag_name('th')
            self.assertEqual(len(th), 7)

            # Mostrando todas las columnas
            self.carga_pagina(driver, 'consulta')
            boton = driver.find_element_by_class_name('btn')
            filas = driver.find_element_by_name('mostrar')
            filas.send_keys(10000)
            boton.click()
            self.assertRaises(NoSuchElementException, driver.find_element_by_class_name, 'alert')

    def test_exporta_consulta(self):
        """
        Exporta una consulta
        """
        for driver in self.drivers:
            self.carga_pagina(driver, 'consulta')
            boton = driver.find_element_by_class_name('btn')
            boton.click()
            csv_btn, json_btn = driver.find_elements_by_class_name('btn')
            csv_href = csv_btn.get_attribute('href')
            json_href = json_btn.get_attribute('href')
            self.assertIn('/consulta/descarga/csv', csv_href)
            self.assertIn('/consulta/descarga/json', json_href)

    def test_columna_calculada(self):
        """
        Prueba las columnas calculadas
        """
        for driver in self.drivers:
            # Ok
            self.carga_pagina(driver, 'consulta')
            boton = driver.find_element_by_class_name('btn')
            fuente = Select(driver.find_element_by_name('fuente-0'))
            columna = Select(driver.find_element_by_name('columna_filtro-0'))
            valor = driver.find_element_by_name('valor-0')
            calculada = driver.find_element_by_name('columna_calculada')
            fuente.select_by_visible_text('municipios')
            columna.select_by_visible_text('Municipio')
            valor.send_keys('Agurain/Salvatierra')
            calculada.send_keys('Codigo Provincia + Codigo comunidad')
            boton.click()
            td = driver.find_elements_by_tag_name('td')[7]
            self.assertEqual(td.text, '0116')

    def test_columna_calculada_mal(self):
        """
        Prueba una columna calculada con un campo incorrecto
        """
        for driver in self.drivers:
            # Mal construida
            self.carga_pagina(driver, 'consulta')
            calculada = driver.find_element_by_name('columna_calculada')
            calculada.send_keys('Codigo Provincia + algo que no se puede hacer / 2')
            boton = driver.find_element_by_class_name('btn')
            boton.click()
            alerta = driver.find_element_by_class_name('alert')
            self.assertIn('Columna calculada no válida', alerta.text)

    def test_join_consulta(self):
        """
        Prueba hacer join entre fuentes
        """
        for driver in self.drivers:
            self.carga_pagina(driver, 'consulta')
            boton = driver.find_element_by_class_name('btn')
            columna = Select(driver.find_element_by_name('columna_filtro-0'))
            valor = driver.find_element_by_name('valor-0')
            columna.select_by_visible_text('Municipio')
            valor.send_keys('Miranda de Ebro')
            add = driver.find_element_by_id('add-subconsulta')
            add.click()
            fuente = Select(driver.find_element_by_name('fuente-1'))
            fuente.select_by_visible_text('aeat_renta')
            join = Select(driver.find_element_by_name('join'))
            join.select_by_visible_text('inner')
            boton.click()

            th = driver.find_elements_by_tag_name('th')
            self.assertEqual(len(th), 15)

    def test_mapa(self):
        """
        Prueba que los mapas se cargan correctamente
        """
        for driver in self.drivers:
            # Carga la consulta
            self.carga_pagina(driver, 'consulta')
            boton = driver.find_element_by_class_name('btn')
            fuente = Select(driver.find_element_by_name('fuente-0'))
            fuente.select_by_visible_text('aeat_renta')
            boton.click()
            driver.implicitly_wait(3)

            # Carga el mapa
            metodo = Select(driver.find_element_by_id('metodo-mapa'))
            territorio = Select(driver.find_element_by_id('territorio'))
            metodo.select_by_visible_text('sum')
            territorio.select_by_visible_text('provincias')
            toggle = driver.find_element_by_class_name('dropdown-toggle')
            toggle.click()
            dropdown = driver.find_element_by_class_name('dropdown-menu')
            link = dropdown.find_elements_by_tag_name('a')[3]
            link.click()
            driver.implicitly_wait(3)

            heading = driver.find_element_by_class_name('panel-heading')
            iframe = driver.find_element_by_tag_name('iframe')
            mapa = iframe.get_attribute('src')
            self.assertEqual(heading.text, 'Mapa')
            self.assertTrue(len(mapa) > 10000)
