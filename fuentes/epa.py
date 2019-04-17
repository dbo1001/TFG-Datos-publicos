'''
Created on 5 mar. 2019

@author: Sergio
'''
import pandas as pd
from fuentes.Fuente import Fuente, rename

class Epa(Fuente):
    
    def __init__(self):        
        descripcion = 'Datos de paro por municipio'
        super().__init__('Datos de paro', 'epa', descripcion)
    
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
        all_names = []
        
        patron_busqueda = '/[A-z]*[-]*[A-z]*[-]*[A-z]*[-]*[A-z]*[-]*[A-z]*[-]*[A-z]*[-]*[A-z]*'
        patron_busqueda2 = '">[a-zA-ZñÑáéíóúÁÉÍÓÚàèìòùÀÈÌÒÙ,\s\-]+'
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
                if (cc_aa_actual == 'islas-baleares'):
                    urls_provs = [url_ccaa+ "/" + 'illes-balears']
                
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
                
                n = re.compile(patron_busqueda2)
                urls_muns = []
                
                # Provincias uni-municipales
                if len(municipios_html) == 0:
                    urls_muns = [url_prov+"/"+prov_actual]
                    names = [prov_actual]
                    
                else:        
                    mun_names_raw = p.findall(str(municipios_html[0]))
                    names = n.findall(str(municipios_html[0]))
                    
                    names.pop(0)
                    for i in range(len(names)):
                        names[i] = names[i][2:] 
                    #print(names)
                    mun_names = [name.split("/")[6] for name in mun_names_raw]
                
                    urls_muns = [url_prov+"/"+name for name in mun_names]
                
                all_names.extend(names)
                #print(names)
                all_uls.extend(urls_muns)
        # ojo, comunidades si tienen separadores, provincias y municipios noooooooo
    
        
        print('Guardando paro municipios')
        url= 'C:\\Users\\Sergio\\Desktop\\TFG-Datos-publicos-master\\fuentes\\Municipios.csv'
        muniDF = pd.read_csv(url, sep=';', header=0, encoding = "ISO-8859-1")
        html_page = list()
        listaMuni = list()
        import locale
        locale.setlocale(locale.LC_NUMERIC, 'Spanish_Spain.1252')
        for i in range(len(all_uls)):
            auxhtml = pd.read_html(all_uls[i], thousands = '.', decimal = ',')[0]
            
            if(i == 200):
                break
            
            if (len(auxhtml) > 0):#En algunos municipios no hay tabla.
                if(i%10 == 0):
                    print(i,'/',len(all_uls))
                #html_page.append(pd.read_html(all_uls[i]))
                auxhtml = auxhtml.drop(columns='Nº de parados registrados')
                auxhtml.columns = ['Fecha', 'Tasa de paro', 'Numero de parados', 'Población']
                
                municipio = all_names[i].upper()

                listaMuni.append(municipio)
                
                aux = muniDF[muniDF.Municipio == municipio].Código.astype(str).str.zfill(5)
                
                if(len(aux) > 0):
                    auxhtml['Codigo Municipio'] = [aux.values[0]]*len(auxhtml)
                else:
                    #print('rebuscando ',municipio, all_uls[i])
                    if ',' in municipio:
                        municipio = municipio.replace(', ', ' (')  
                        municipio = municipio + ')'          
                        aux = muniDF[muniDF.Municipio == municipio].Código.astype(str).str.zfill(5)
                        auxhtml['Codigo Municipio'] = [aux.values[0]]*len(auxhtml)          
                        if(len(aux) == 0):
                            print('no encontrado ',municipio)
                    else:
                        print('no encontrado ',municipio, all_uls[i])
                        
                #html_page.append(auxhtml)
                
                if i == 0:
                    df_F = auxhtml.iloc[[0]]
                    
                else:
                    df_F = df_F.append(auxhtml.iloc[[0]], ignore_index = True)
                    
            
        
        for j in range(len(df_F['Tasa de paro'].values)):
            
            df_F['Tasa de paro'][j] = locale.atof(df_F['Tasa de paro'][j][:-1])
            
        
        
        df_F['Tasa de paro'] = df_F['Tasa de paro'].astype(float)
        #auxdf = df_F.groupby('Codigo Municipio', as_index=False).mean().round(2)
        
        
        df_F['Codigo Municipio'] = df_F['Codigo Municipio'].astype(str).str.zfill(5)
        df_F['Codigo Provincia'] = df_F['Codigo Municipio']
        for j in range(len(df_F['Codigo Municipio'])):
            df_F['Codigo Provincia'][j] = df_F['Codigo Municipio'][j][:2]
        print(len(listaMuni))
        print(len(df_F))
        df_F['Municipio'] = listaMuni
       
        df_F.to_csv(r'C:\Users\Sergio\Desktop\epaMunicipios.csv', sep=';', encoding = "ISO-8859-1")
        print('ok epa')
        return df_F
        
        
