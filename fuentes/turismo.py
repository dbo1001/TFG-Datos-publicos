import pandas as pd
import time
from fuentes.Fuente import Fuente, rename
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re

from fuentes.epa import leerMunicipiosCSV 
class Turismo(Fuente):
    
    renombrar = {
        'Código': 'Codigo Municipio'      
    }
    
    def __init__(self):        
        descripcion = 'Datos de turismo por municipio'
        super().__init__('Datos de turismo', 'turismo', descripcion)
    

    def obtenerDestinosPopulares(self):
        driver = webdriver.Firefox(executable_path=r"C:\Users\Sergio\My Documents\LiClipse Workspace\TFG-Datos-publicos\TFG-Datos-publicos\fuentes\datos\geckodriver.exe")
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
        t = time.clock()
        #a = self.obtenerDestinosPopulares()
        driver = webdriver.Firefox(executable_path=r"C:\Users\Sergio\My Documents\LiClipse Workspace\TFG-Datos-publicos\TFG-Datos-publicos\fuentes\datos\geckodriver.exe")
        url = 'https://www.booking.com/index.es.html'
        driver.set_page_load_timeout(15)
        driver.get(url)                
        
        muniDF = leerMunicipiosCSV()
        municipiosDF = muniDF.Municipio
        municipios = list(municipiosDF)
        alojamientos = [-1] * len(municipios)
        print(len(municipios))
        for i in range (len(municipios)):
            elemento = driver.find_element_by_id('ss')
            elemento.clear()
            elemento.send_keys(municipios[i])
            time.sleep(1)
            elemento.send_keys(Keys.ENTER)
            
            try:
                time.sleep(1)
                elemento = driver.find_element_by_class_name('sorth1')
            except Exception as ex:
                try:
                    time.sleep(1)
                    elemento = driver.find_element_by_class_name('sorth1')
                except Exception as ex2:
                    alojamientos[i] = 0
                    continue
                

            
            texto = elemento.text.upper()
            texto = self.normalize(texto)
            munitexto = self.normalize(municipios[i])
            
            if munitexto in texto:
                print(elemento.text)
                print(re.findall(r'\d+', elemento.text))
                alojamientos[i] = (re.findall(r'\d+', elemento.text))[0]
            else:
                print(elemento.text, municipios[i], '-')
                alojamientos[i] = "-1"
            driver.back()
            if i == 20:
                break
        print(time.clock() - t)
        #municipiosDF = municipiosDF.to_frame()
        muniDF['Nº alojamientos'] = alojamientos
        muniDF['Nº alojamientos'] = muniDF['Nº alojamientos'].astype(int)
        driver.quit()
        print(municipiosDF)
        muniDF['Código'] = muniDF['Código'].astype(str).str.zfill(5)
        muniDF['Codigo Provincia'] = muniDF['Código'].str[0:2]
        muniDF.to_csv(r'C:\Users\Sergio\Desktop\turismoMunicipios.csv', sep=';', encoding = "ISO-8859-1")
        
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
        
        
        
        