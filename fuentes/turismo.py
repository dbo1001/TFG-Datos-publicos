import pandas as pd
import time
from fuentes.Fuente import Fuente, rename
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import os

from fuentes.epa import leerMunicipiosCSV 
class Turismo(Fuente):
    
    renombrar = {
        'Código': 'Codigo Municipio'      
    }
    
    def __init__(self):        
        descripcion = 'Datos de turismo por municipio'
        super().__init__('Datos de turismo', 'turismo', descripcion)
    

    def obtenerDestinosPopulares(self):
        dir = os.path.dirname(__file__)
        url = os.path.join(dir, 'datos\geckodriver.exe')
        driver = webdriver.Firefox(executable_path=url)
        url = 'https://www.tripadvisor.es/Tourism-g2361626-Province_of_Seville_Andalucia-Vacations.html'
        driver.set_page_load_timeout(10)
        driver.get(url)
        time.sleep(2)
        flag = True
        while flag:
            try:
                elemento = driver.find_element_by_class_name("morePopularCitiesWrap")
                print(elemento.location)
                elemento.click()
            except Exception as ex:
                flag = False
                print('ok')
        
        elemento = driver.find_element_by_class_name('popularCities')
        urlsElements = elemento.find_elements_by_tag_name('a')
        print(len(urlsElements))
        urls = list()
        for url in urlsElements:
            #print(url.get_attribute('href'))
            urls.append(url.get_attribute('href'))
        
        driver.quit()
        time.sleep(30)
        return urls
    @rename(renombrar)
    def carga(self):
        #a = self.obtenerDestinosPopulares()
        dir = os.path.dirname(__file__)
        url = os.path.join(dir, 'datos\geckodriver.exe')
        driver = webdriver.Firefox(executable_path=url)
        url = 'https://www.booking.com/index.es.html'
        driver.set_page_load_timeout(30)
        driver.get(url)                
        
        muniDF = leerMunicipiosCSV()
        municipiosDF = muniDF.Municipio
        municipios = list(municipiosDF)
        alojamientos = [-1] * len(municipios)
        print(len(municipios))
        t = time.clock()

        for i in range (len(municipios)):
            MaxIntent = 3
            flag = True
            intentos = 0
            while(flag):
                try:
                    elemento = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ss')))
                    flag = False
                    #elemento = driver.find_element_by_id('ss')
                except TimeoutException:
                    if intentos < MaxIntent:
                        intentos += 1
                        driver.get(url)
                    else:
                        alojamientos[i] = "-1"
                        driver.get(url)
                        continue
            elemento.clear()
            elemento.send_keys(municipios[i])
            elemento.send_keys(Keys.ENTER)
            flag = True
            intentos = 0
            while (flag):
                try:
                    elemento = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sorth1")))
                    flag = False
                    #elemento = driver.find_element_by_class_name('sorth1')
                except TimeoutException:
                    if intentos < MaxIntent:
                        intentos += 1
                    else:
                        alojamientos[i] = "-1"
                        driver.get(url)
                        continue
                       
                        
            texto = elemento.text.upper()
            texto = self.normalize(texto)
            munitexto = self.normalize(municipios[i])
            
            if munitexto in texto:
                print(elemento.text)
                #print(re.findall(r'\d+', elemento.text))
                alojamientos[i] = (re.findall(r'\d+', elemento.text))[0]
            else:
                print(elemento.text, municipios[i], '-')
                alojamientos[i] = -1
            driver.back()
            if i == 5:
                break

        print(time.clock() - t)
        #municipiosDF = municipiosDF.to_frame()
        muniDF['Nº alojamientos'] = alojamientos
        muniDF['Nº alojamientos'] = muniDF['Nº alojamientos'].astype(int)
        driver.quit()
        print(municipiosDF)
        muniDF['Código'] = muniDF['Código'].astype(str).str.zfill(5)
        muniDF['Codigo Provincia'] = muniDF['Código'].str[0:2]
        #dir = os.path.dirname(__file__)
        url = os.path.join(dir, 'datos\\turismoMunicipios.csv')
        muniDF.to_csv(url, sep=';', encoding = "ISO-8859-1")
        
        return muniDF
        
        
        
    def normalize(self, s):
        replacements = (
            ("á", "a"),
            ("é", "e"),
            ("í", "i"),
            ("ó", "o"),
            ("ú", "u"),
            ("à", "a"),
            ("è", "e"),
            ("í", "i"),
            ("ò", "o"),
            ("ù", "u"),
            )
        for a, b in replacements:
            s = s.replace(a, b).replace(a.upper(), b.upper())
        return s
        
        
        
        