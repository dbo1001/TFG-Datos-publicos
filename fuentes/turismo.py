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
import gc

from fuentes.epa import leerMunicipiosCSV 
class Turismo(Fuente):
    
    renombrar = {
        'Codigo_Mapa': 'Codigo Municipio'      
    }
    
    def __init__(self):        
        descripcion = 'Datos de turismo por municipio'
        super().__init__('Datos de turismo', 'Booking', descripcion)
    

    @rename(renombrar)
    def carga(self):
        #si aparece este texto guardar para comprobar despues.
        patron = re.compile('Echa un vistazo a estos otros .*')
        dir = os.path.dirname(__file__)
        url = os.path.join(dir, 'datos\geckodriver.exe')
        driver = webdriver.Firefox(executable_path=url)
        url = 'https://www.booking.com/index.es.html'
        driver.set_page_load_timeout(20)
        driver.get(url)                
        
        #muniDF = leerMunicipiosCSV()
        muniDF = self.leerMunicipiosCSV2()
        
        municipiosDF = muniDF.Municipio
        provinciaDF = muniDF.Provincia
        municipios = list(municipiosDF)
        provincias = list(provinciaDF)

        alojamientos = [-1] * len(municipios)
        t = time.clock()
        no_encontrados = list()
        muniDFaux = pd.DataFrame()
        for i in range (len(municipios)):
            print( i, '/', len(municipios))
            #muniDF = muniDF.drop(muniDF.index[i])
            muniDFaux = muniDFaux.append(muniDF.iloc[i])            
            MaxIntent = 2
            flag = True
            salir = False
            intentos = 0
            while(flag):
                try:
                    elemento = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'ss')))
                    flag = False
                    #elemento = driver.find_element_by_id('ss')
                except Exception:
                    if intentos < MaxIntent:
                        intentos += 1
                        driver.quit()
                        dir = os.path.dirname(__file__)
                        url = os.path.join(dir, 'datos\geckodriver.exe')
                        driver = webdriver.Firefox(executable_path=url)
                        url = 'https://www.booking.com/index.es.html'
                        driver.get(url)
                    else:
                        alojamientos[i] = "0"
                        flag = False
                        salir = True
            if salir == True:
                continue          
            
            elemento.clear()
            elemento.send_keys(municipios[i] + ' ' + provincias[i] )
            elemento.send_keys(Keys.ENTER)
            flag = True
            salir = False
            intentos = 0
            while (flag):
                try:
                    elemento = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "sorth1")))
                    flag = False
                    #elemento = driver.find_element_by_class_name('sorth1')
                except Exception:
                    if intentos < MaxIntent:
                        intentos += 1
                    else:
                        alojamientos[i] = "0"
                        flag = False
                        salir = True
                        driver.quit()
                        dir = os.path.dirname(__file__)
                        url = os.path.join(dir, 'datos\geckodriver.exe')
                        driver = webdriver.Firefox(executable_path=url)
                        url = 'https://www.booking.com/index.es.html'
                        driver.get(url)
                        
            if salir == True:
                continue
            
            elemento2 = None
            
             
            try:
                
                elemento2temp = driver.find_element_by_class_name('sr_item ') 
               
                elemento2 = elemento2temp
                
            except Exception:
                print('error')
                elemento2 = None
            
            texto = elemento.text.upper()
            texto = texto.split(':', 1)[0]
            texto = self.normalize(texto)
            munitexto = self.normalize(municipios[i])
            salir = False
            try:
                if munitexto in texto or texto in munitexto:
                    if elemento2 == None:
                        print(elemento.text, ((time.clock() - t)/(i+1))*len(municipios)/3600,'h')
                        alojamientos[i] = (re.findall(r'\d+', elemento.text))[0]
                    #Si existe comprobar que no sean alojamientos fuera del municipio.
                    else:
                        aloj = (re.findall(r'\d+', elemento.text))[0]
                        otrosAlojamientos = (re.findall(r'\d+', elemento2.text))[0]
                        if aloj != otrosAlojamientos:
                            alojamientos[i] = (re.findall(r'\d+', elemento.text))[0]
                            print(elemento.text, ((time.clock() - t)/(i+1))*len(municipios)/3600,'h')
    
                        else:
                            alojamientos[i] = "0"
                else:
                    print(elemento.text, municipios[i])
                    no_encontrados.append(municipios[i])
                    alojamientos[i] = "0"
            except Exception:
                alojamientos[i] = "0"
                salir = True
                driver.quit()
                dir = os.path.dirname(__file__)
                url = os.path.join(dir, 'datos\geckodriver.exe')
                driver = webdriver.Firefox(executable_path=url)
                url = 'https://www.booking.com/index.es.html'
                driver.get(url)
            
            if salir == True:
                continue    
            try:
                driver.back()
            except Exception:
                driver.quit()
                dir = os.path.dirname(__file__)
                url = os.path.join(dir, 'datos\geckodriver.exe')
                driver = webdriver.Firefox(executable_path=url)
                url = 'https://www.booking.com/index.es.html'
                driver.get(url)
            
            if i%5 == 0 or i == len(municipios)-1:
                if i == 0:
                    muniDFaux['Nº alojamientos'] = alojamientos[i:i+1]
                else:
                    muniDFaux['Nº alojamientos'] = alojamientos[i-4:i+1]

                muniDFaux['Código'] = muniDFaux['Código'].astype(str).str.zfill(5)
                
                dir = os.path.dirname(__file__)
                url = os.path.join(dir, 'datos\\turismoMunicipios.csv')
                
                turismoMuniDF = pd.read_csv(url, sep=';', header=0, encoding="ISO-8859-1", 
                                                dtype={'CodProv': str, 'Codigo Provincia': str,
                                                'Codigo_Mapa': str, 'Código': str,  'Nº alojamientos': int })
                
                turismoMuniDF = turismoMuniDF.append(muniDFaux)
                
                turismoMuniDF['Nº alojamientos'] = turismoMuniDF['Nº alojamientos'].astype(int)
                turismoMuniDF['Código'] = turismoMuniDF['Código'].astype(str).str.zfill(5)
                turismoMuniDF['Codigo Provincia'] = turismoMuniDF['Código'].str[0:2]
                
                turismoMuniDF = turismoMuniDF[['CodProv', 'Codigo Provincia', 'Codigo_Mapa', 'Comunidad Autónoma',
                                               'Código', 'Municipio', 'Nº alojamientos', 'Provincia']]
                
                turismoMuniDF.to_csv(url, sep=';', encoding = "ISO-8859-1")
                
                url = os.path.join(dir, 'datos\MunicipiosCopia.csv')
                muniDFauxAntiguo = pd.read_csv(url, sep=';', header=0, encoding="ISO-8859-1")
                if i != 0:
                    muniDFauxAntiguo = muniDFauxAntiguo[5:]
                else:
                    muniDFauxAntiguo = muniDFauxAntiguo[1:]
                
                muniDFauxAntiguo = muniDFauxAntiguo[['Comunidad Autónoma', 'Provincia', 'Municipio', 'Código',
                                                     'CodProv', 'Codigo_Mapa']]
                muniDFauxAntiguo.to_csv(url, sep=';', encoding = "ISO-8859-1")
                
                muniDFaux = pd.DataFrame()
                print('ok')
                if i%20 == 0:
                    driver.quit()
                    #recolector de basura
                    gc.collect()
                    dir = os.path.dirname(__file__)
                    url = os.path.join(dir, 'datos\geckodriver.exe')
                    driver = webdriver.Firefox(executable_path=url)
                    url = 'https://www.booking.com/index.es.html'
                    driver.get(url)
                
        driver.quit()
        '''
        #municipiosDF = municipiosDF.to_frame()
        muniDF['Nº alojamientos'] = alojamientos
        muniDF['Nº alojamientos'] = muniDF['Nº alojamientos'].astype(int)
        driver.quit()
        print(municipiosDF)
        muniDF['Código'] = muniDF['Código'].astype(str).str.zfill(5)
        muniDF['Codigo Provincia'] = muniDF['Código'].str[0:2]
        dir = os.path.dirname(__file__)
        url = os.path.join(dir, 'datos\\turismoMunicipios.csv')
        muniDF.to_csv(url, sep=';', encoding = "ISO-8859-1")
        
        
        url = os.path.join(dir, 'datos\\noEncontrados.csv')
        noEncontrados = pd.Series(no_encontrados)
        noEncontrados.to_csv(url, sep=';', encoding = "ISO-8859-1")
        '''
        url = os.path.join(dir, 'datos\\turismoMunicipios.csv')
        turismoMuniDF = pd.read_csv(url, sep=';', header=0, encoding="ISO-8859-1", 
                                                dtype={'CodProv': str, 'Codigo Provincia': str,
                                                'Codigo_Mapa': str, 'Código': str,  'Nº alojamientos': int })
        turismoMuniDF = turismoMuniDF.drop(['Código', 'CodProv'], axis = 1)
        turismoMuniDF['Codigo_Mapa'] = turismoMuniDF['Codigo_Mapa'].astype(str).str.zfill(5)
        turismoMuniDF['Codigo Provincia'] = turismoMuniDF['Codigo Provincia'].astype(str).str.zfill(2)
        turismoMuniDF = turismoMuniDF[['Codigo Provincia', 'Codigo_Mapa', 'Comunidad Autónoma',
       'Municipio', 'Nº alojamientos', 'Provincia']]
        return turismoMuniDF
        
        
        
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
            ("ü", "u")
            )
        for a, b in replacements:
            s = s.replace(a, b).replace(a.upper(), b.upper())
        return s
    
    def leerMunicipiosCSV2(self):
        dir = os.path.dirname(__file__)
        url = os.path.join(dir, 'datos\MunicipiosCopia.csv')
        muniDF = pd.read_csv(url, sep=';', header=0, encoding="ISO-8859-1",
                             dtype={'Código': str, 'CodProv': str, 'Codigo_Mapa': str})
        return muniDF 
        
        
        