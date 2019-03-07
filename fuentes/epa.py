'''
Created on 5 mar. 2019

@author: Sergio
'''
import pandas as pd
from fuentes.Fuente import Fuente, rename

class Epa(Fuente):
    
    def __init__(self):        
        descripcion = 'Datos de paro por municipio'
        super().__init__('Datos de para', 'epa', descripcion)
    
    def carga(self):
        
        import warnings
        warnings.filterwarnings("ignore")
        
        
        from urllib.request import urlopen
        from bs4 import BeautifulSoup
        
        url1 ="https://datosmacro.expansion.com/paro/espana/municipios/andalucia/almeria/abla"
        html = urlopen(url1)
        
        bsObj = BeautifulSoup(html.read())
        
        #-
        ccaas = bsObj.findAll('div', attrs = {'class': 'flg flg-039'} )
        ccaasStr = [str(item) for item in ccaas]
        allccaaSrt = ''.join(ccaasStr)
        
        import re
        p = re.compile('/ccaa/[A-z]*[-]*[A-z]*[-]*[A-z]*')
        ccaa_names_raw = p.findall(allccaaSrt)
        
        #-
        ccaa_names = [name.split("/")[2] for name in ccaa_names_raw]
        
        urls_ccaa = ["https://datosmacro.expansion.com/paro/espana/municipios/"+name for name in ccaa_names]
        
        #-
        
        all_uls = []
        
        patron_busqueda = '/[A-z]*[-]*[A-z]*[-]*[A-z]*[-]*[A-z]*[-]*[A-z]*[-]*[A-z]*[-]*[A-z]*'
        
        for url_ccaa in urls_ccaa[:]:
            html = urlopen(url_ccaa)
            bsObj = BeautifulSoup(html.read())
            cc_aa_actual = url_ccaa.split("/")[6]
            print("Exploring ",cc_aa_actual)
            
            provincias_html = bsObj.findAll('select', attrs = {'id': 'prov'} )
            # hay tantos [-]*[A-z]* por las-palmas-de-gran-canarias
            p = re.compile('value="/paro/espana/municipios/'+cc_aa_actual +patron_busqueda)
            
            urls_provs = []
            
            if len(provincias_html) ==0:
                # comunidad uni provincial eje asturias/asturias
                urls_provs = [url_ccaa+"/"+cc_aa_actual]
                
            else: 
                prov_names_raw = p.findall(str(provincias_html[0]))
                prov_names = [name.split("/")[5] for name in prov_names_raw]
        
                urls_provs = [url_ccaa+"/"+name for name in prov_names]
        
            for url_prov in urls_provs[:]:
                html_p = urlopen(url_prov)
                bsObj_p = BeautifulSoup(html_p.read())
                
                prov_actual = url_prov.split("/")[7]
                
                municipios_html = bsObj_p.findAll('select', attrs = {'id': 'muni'} )
                
                p = re.compile('value="/paro/espana/municipios/'+cc_aa_actual +'/'+prov_actual+patron_busqueda)
                
                urls_muns = []
                
                # Provincias uni-municipales
                if len(municipios_html) ==0:
                    urls_muns = [url_prov+"/"+prov_actual]
                else:        
                    mun_names_raw = p.findall(str(municipios_html[0]))
                    mun_names = [name.split("/")[6] for name in mun_names_raw]
                
                    urls_muns = [url_prov+"/"+name for name in mun_names]
                
                
                all_uls.extend(urls_muns)
        # ojo, comunidades si tienen separadores, provincias y municipios noooooooo
        
        #-
        
        html_page = pd.read_html(all_uls[0]) 
        
        df_F = html_page[0].drop(columns='Nº de parados registrados')
        df_F.columns = ['Fecha', 'Tasa de paro', 'Numero de parados', 'Población']
        
        return df_F
        
        
