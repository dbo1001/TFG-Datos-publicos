import pandas as pd
from fuentes.Fuente import Fuente, rename
import os
import traceback
class Epa(Fuente):
    """
    Fuente de datos de Datosmacro
    """
    
    def __init__(self):        
        descripcion = 'Datos de paro por municipio'
        super().__init__('Datos de paro', 'epa', descripcion)
    

    def obtenerUrlNames(self):
        """
        Devuelve una lista con todas las URLs a cargar.
        """
        import warnings
        warnings.filterwarnings("ignore")
        from urllib.request import urlopen
        from bs4 import BeautifulSoup
        url1 = "https://datosmacro.expansion.com/paro/espana/municipios/andalucia/almeria/abla"
        html = urlopen(url1)
        bsObj = BeautifulSoup(html.read())
    #-
        ccaas = bsObj.findAll('div', attrs={'class':'flg flg-039'})
        ccaasStr = [str(item) for item in ccaas]
        allccaaSrt = ''.join(ccaasStr)
        import re
        p = re.compile('/ccaa/[A-z]*[-]*[A-z]*[-]*[A-z]*')
        ccaa_names_raw = p.findall(allccaaSrt)
    #-
        ccaa_names = [name.split("/")[2] for name in ccaa_names_raw]
        urls_ccaa = ["https://datosmacro.expansion.com/paro/espana/municipios/" + name for name in ccaa_names]
    #-
        all_uls = []
        all_names = []
        patron_busqueda = '/[A-z]*[-]*[A-z]*[-]*[A-z]*[-]*[A-z]*[-]*[A-z]*[-]*[A-z]*[-]*[A-z]*'
        patron_busqueda2 = '">[a-zA-ZñÑáéíóúÁÉÍÓÚàèìòùÀÈÌÒÙ,\s\-]+'
        for url_ccaa in urls_ccaa[:]:
            html = urlopen(url_ccaa)
            bsObj = BeautifulSoup(html.read())
            cc_aa_actual = url_ccaa.split("/")[6]
            print("Exploring ", cc_aa_actual)
            provincias_html = bsObj.findAll('select', attrs={'id':'prov'})

            p = re.compile('value="/paro/espana/municipios/' + cc_aa_actual + patron_busqueda)
            urls_provs = []
            if len(provincias_html) == 0:
                # comunidad uni-provincial eje asturias/asturias
                urls_provs = [url_ccaa + "/" + cc_aa_actual]
                if (cc_aa_actual == 'islas-baleares'):
                    urls_provs = [url_ccaa + "/" + 'illes-balears']
            else:
                prov_names_raw = p.findall(str(provincias_html[0]))
                prov_names = [name.split("/")[5] for name in prov_names_raw]
                urls_provs = [url_ccaa + "/" + name for name in prov_names]
            for url_prov in urls_provs[:]:
                html_p = urlopen(url_prov)
                bsObj_p = BeautifulSoup(html_p.read())
                prov_actual = url_prov.split("/")[7]
                municipios_html = bsObj_p.findAll('select', attrs={'id':'muni'})
                p = re.compile('value="/paro/espana/municipios/' + cc_aa_actual + '/' + prov_actual + patron_busqueda)
                n = re.compile(patron_busqueda2)
                urls_muns = []
                # Provincias uni-municipales
                if len(municipios_html) == 0:
                    urls_muns = [url_prov + "/" + prov_actual]
                    names = [prov_actual]
                else:
                    mun_names_raw = p.findall(str(municipios_html[0]))
                    names = n.findall(str(municipios_html[0]))
                    names.pop(0)
                    for i in range(len(names)):
                        names[i] = names[i][2:]
                    
                    mun_names = [name.split("/")[6] for name in mun_names_raw]
                    urls_muns = [url_prov + "/" + name for name in mun_names]
                all_names.extend(names)
                all_uls.extend(urls_muns)
        
        return all_uls, all_names

    def carga(self):
        """
        Realiza el webscrapiing y devuelve el DataFrame procesado.
        """
        dir = os.path.dirname(__file__)
        url = os.path.join(dir, 'datos\epaMunicipios.csv')
        
        if os.path.isfile(url):
            df_F = pd.read_csv(url, sep=';', header=0, encoding="ISO-8859-1",
                                                dtype={'Codigo Municipio': str, 'Fecha': str,
                                                'Numero de parados': int, 'Población': int,  'Tasa de paro': str })
            
            df_F = df_F.dropna(axis = 0)
            df_F = df_F.reset_index()
            
            df_F['Tasa de paro'] = df_F['Tasa de paro'].str.strip('%')
            df_F['Tasa de paro'] = df_F['Tasa de paro'].str.replace(',', '.')
            df_F['Tasa de paro'] = df_F['Tasa de paro'].astype(float)
            df_F['Tasa de paro'] = df_F['Tasa de paro']/100
            
            df_F['Codigo Municipio'] = df_F['Codigo Municipio'].astype(str).str.zfill(5)
            
            df_F['Codigo Provincia'] = df_F['Codigo Municipio'].str[0:2]
            
            muniDF = leerMunicipiosCSV()
            muniDF['Codigo_Mapa'] = muniDF['Codigo_Mapa'].astype(str).str.zfill(5)
            nombres = list()
            for i in range(len(df_F)):
                nomDF = muniDF[muniDF['Codigo_Mapa'] == df_F['Codigo Municipio'][i]]
                nombres.append(nomDF['Municipio'].iloc[0])
                
                
            df_F['Nombre Municipio'] = nombres
            df_F = df_F[['Nombre Municipio', 'Codigo Municipio', 'Codigo Provincia', 'Fecha', 'Numero de parados', 'Población',  'Tasa de paro' ]]  
            return df_F
            
        else:
                
            all_uls, all_names = self.obtenerUrlNames()
           
            print('Guardando paro municipios')
            muniDF = leerMunicipiosCSV()
            html_page = list()
            listaMuni = list()
            import locale
            locale.setlocale(locale.LC_NUMERIC, 'Spanish_Spain.1252')
            
            for i in range(len(all_uls)):
                
                try:
                    auxhtml = pd.read_html(all_uls[i], thousands = '.', decimal = ',')[0]
                    
                    if (len(auxhtml) > 0):#En algunos municipios no hay tabla.
                        if(i%100 == 0):
                            print(i,'/',len(all_uls))
                        auxhtml = auxhtml.drop(columns='Nº de parados registrados')
                        auxhtml.columns = ['Fecha', 'Tasa de paro', 'Numero de parados', 'Población']
                        
                        municipio = all_names[i].upper()
        
                        listaMuni.append(municipio)
                        
                        aux = muniDF[muniDF.Municipio == municipio].Codigo_Mapa.astype(str).str.zfill(5)
                        
                        if(len(aux) > 0):
                            auxhtml['Codigo Municipio'] = [aux.values[0]]*len(auxhtml)
                        else:
                            if ',' in municipio:
                                municipio = municipio.replace(', ', ' (')  
                                municipio = municipio + ')'          
                                aux = muniDF[muniDF.Municipio == municipio].Codigo_Mapa.astype(str).str.zfill(5)
                                if len(aux) > 0:
                                    auxhtml['Codigo Municipio'] = [aux.values[0]]*len(auxhtml)
                                                
                        if i == 0:
                            df_F = auxhtml.loc[auxhtml['Fecha'] == '2015']
                                                
                            
                        else:
                            df_F = df_F.append(auxhtml.loc[auxhtml['Fecha'] == '2015'], ignore_index = True)
                except Exception:
                    print(all_uls[i])
                    continue
                
            
            dir = os.path.dirname(__file__)
            url = os.path.join(dir, 'datos\epaMunicipios.csv')
            df_F.to_csv(url, sep=';', encoding = "ISO-8859-1")
              
            df_F = df_F.dropna(axis = 0)
            df_F = df_F.reset_index()
            
            df_F['Tasa de paro'] = df_F['Tasa de paro'].str.strip('%')
            df_F['Tasa de paro'] = df_F['Tasa de paro'].str.replace(',', '.')
            df_F['Tasa de paro'] = df_F['Tasa de paro'].astype(float)
            df_F['Tasa de paro'] = df_F['Tasa de paro']/100
            df_F['Codigo Municipio'] = df_F['Codigo Municipio'].astype(str).str.zfill(5)
            df_F['Codigo Provincia'] = df_F['Codigo Municipio'].str[0:2]
            
            return df_F



def leerMunicipiosCSV():
    """
    Lee el archivo y devuelve el DataFrame
    """
    dir = os.path.dirname(__file__)
    url = os.path.join(dir, 'datos\Municipios.csv')
    muniDF = pd.read_csv(url, sep=';', header=0, encoding="ISO-8859-1")
    return muniDF

        
        
