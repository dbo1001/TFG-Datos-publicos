import pandas as pd
from fuentes.Fuente import Fuente
from fuentes.ine import Ine
from fuentes import Database
from config import Config as config
from fuentes.ine import InePoblacion
from fuentes.mir import MirEleccionesGenerales
import numpy as np
import math
class Sklearn(Fuente):
    
    def __init__(self):        
        descripcion = ''
        super().__init__('sklearn', 'predicciones', descripcion)
        
        
    def obtenerDatosIne(self):
        
        dfo = self.lee_dataframe(InePoblacion)
        #print(dfo)
        df = dfo[['Provincia', 'Municipio', 'Ambos sexos-Total-Total', 'Codigo Municipio', 'Codigo Provincia']].copy()
        
        df['Ambos sexos-Total-Menores de 16 años'] = dfo['Ambos sexos-Total-Menores de 16 años'] / dfo['Ambos sexos-Total-Total']
        df['Ambos sexos-Total-De 16 a 64 años'] = dfo['Ambos sexos-Total-De 16 a 64 años'] / dfo['Ambos sexos-Total-Total']
        df['Ambos sexos-Total-De 65 y más años'] = dfo['Ambos sexos-Total-De 65 y más años'] / dfo['Ambos sexos-Total-Total']
        df['Ambos sexos-extranjeros-Total'] = dfo['Ambos sexos-extranjeros-Total'] / dfo['Ambos sexos-Total-Total']
        df['Ambos sexos-extranjeros-Menores de 16 años'] = dfo['Ambos sexos-extranjeros-Menores de 16 años'] / dfo['Ambos sexos-Total-Total']
        df['Ambos sexos-extranjeros-De 16 a 64 años'] = dfo['Ambos sexos-extranjeros-De 16 a 64 años'] / dfo['Ambos sexos-Total-Total']
        df['Ambos sexos-extranjeros-De 65 y más años'] = dfo['Ambos sexos-extranjeros-De 65 y más años'] / dfo['Ambos sexos-Total-Total']
        df['Hombres-Total-Total'] = dfo['Hombres-Total-Total'] / dfo['Ambos sexos-Total-Total']
        df['Hombres-Total-Menores de 16 años'] = dfo['Hombres-Total-Menores de 16 años'] / dfo['Ambos sexos-Total-Total']
        df['Hombres-Total-De 16 a 64 años'] = dfo['Hombres-Total-De 16 a 64 años'] / dfo['Ambos sexos-Total-Total']
        df['Hombres-Total-De 65 y más años'] = dfo['Hombres-Total-De 65 y más años'] / dfo['Ambos sexos-Total-Total']
        df['Hombres-extranjeros-Total'] = dfo['Hombres-extranjeros-Total'] / dfo['Ambos sexos-Total-Total']
        df['Hombres-extranjeros-Menores de 16 años'] = dfo['Hombres-extranjeros-Menores de 16 años'] / dfo['Ambos sexos-Total-Total']
        df['Hombres-extranjeros-De 16 a 64 años'] = dfo['Hombres-extranjeros-De 16 a 64 años'] / dfo['Ambos sexos-Total-Total']
        df['Hombres-extranjeros-De 65 y más años'] = dfo['Hombres-extranjeros-De 65 y más años'] / dfo['Ambos sexos-Total-Total']
        
        return df
        
    def obtenerDatosMir(self):
        
        dfo = self.lee_dataframe(MirEleccionesGenerales)
        
        df = dfo[dfo.Año == 2015]
        df = df.dropna(axis = 'columns')
        
        df['Codigo Municipio'] = df['Codigo Provincia'].astype(str).str.zfill(2) + df['Codigo Municipio'].astype(str).str.zfill(3)
        df = df.drop(['_id', 'Nombre de Municipio', 'Nombre de Provincia', 'Codigo Provincia'], axis = 1)
        
        columnas_principio = ['Año', 'Codigo Municipio', 'Nombre de Comunidad', 'Número de mesas', 'Población',
                       'Total censo electoral', 'Total votantes', 'Votos a candidaturas',
                       'Votos en blanco', 'Votos nulos', 'Votos válidos']
        #Reordenar columnas
        df = df[[c for c in columnas_principio if c in df] + [c for c in df if c not in columnas_principio]]
        
        #print(df.columns.values)
        return df
       
    def lee_dataframe(self, fuente):
        db = Database.Database(
            database=config.MONGO_DBNAME,
            host=config.MONGO_HOST,
            port=config.MONGO_PORT,
            username=config.MONGO_USERNAME,
            password=config.MONGO_PASSWORD,
            authSource=config.MONGO_DBNAME
        )
        coleccion = fuente().coleccion()
        df = db.lee_datos(coleccion)
        df = pd.DataFrame(list(df.find()))        
        return df
    
    def carga(self):

        df_Ine = self.obtenerDatosIne()
        df_Mir = self.obtenerDatosMir() #hacer escalas 
        enero16 ={ # Modificado, a las coaliciones les doy la media aritmetica
        "PP": 8.28,
        "PSOE": 4.49,
        "PODEMOS": 2.26,
        'IU-UPeC': 2.27,  #sOLO iu
        "PODEMOS-COM": 2.42, # media de Podemos, compromis 
        "C's": 6.65,
        "EN COMÚ": 2.73, # En comu Podems
        "ERC-CATSI": 3.01, #Solo ERC
        "DL": 6.34,    #Democràcia i Llibertat
        "EAJ-PNV": 5.97,
        "EH Bildu": 2.92,
        "PODEMOS-En": 2.32,#Media podemos en marea
        "CCa-PNC": 5.96 #CC
    }

        
        df_Mir = df_Mir.apply(lambda x: self.procesa_municipio(x,enero16),axis=1)
        
        df_Ine = pd.merge(df_Ine, df_Mir, on='Codigo Municipio')
        print(df_Ine.head(3))
        print(df_Ine.columns)
        
        #time.sleep(20)
        return df_Ine
    


    def weighted_avg_and_std(self, values, weights):

        average = np.average(values, weights=weights)
        # Fast and numerically precise:
        variance = np.average((values-average)**2, weights=weights)
        return (average, math.sqrt(variance))
    
    
    def procesa_municipio(self, municipioDF, partido_escala):
        
        values_dict ={}
        
        
        primer_partido_idx = 11
                   
        comunidad = municipioDF["Nombre de Comunidad"]
        #provinciaC = municipioDF["Código de Provincia"]
        #provincia = municipioDF["Nombre de Provincia"]
        municipioC = municipioDF["Codigo Municipio"]
        #municipioN = municipioDF["Nombre de Municipio"]
        
        total = int(municipioDF["Total censo electoral"])
        votos = int(municipioDF["Total votantes"])
        nulos = int(municipioDF["Votos en blanco"])
        blancos = int(municipioDF["Votos nulos"])
        a_candidaturas = int(municipioDF["Votos a candidaturas"])
        
        a_candidaturas_mayoritarias = 0
        partidos = municipioDF[primer_partido_idx:].index
        for partido in partidos:
            escala = partido_escala.get(partido)
            if escala is not None:
                a_candidaturas_mayoritarias += municipioDF[partido]
                
                valor = values_dict.get(escala)
                if valor is None:
                    values_dict[escala]=0
                values_dict[escala] += municipioDF[partido]
                
                
        values = list(values_dict.keys())
        weights = list(values_dict.values())
        
        weighted_avg, weighted_std = self.weighted_avg_and_std(values,weights)
        
        index = ["Nombre de Comunidad","Codigo Municipio",  
                 "Participacion","Blancos","Nulos","ACandidaturas",
                 "%CandMayoritarias","EscalaAvg","EscalaStd"]
        # cambia para que estén tambien todos lso datos que ayudan a hacer el merge
        vals = [comunidad,municipioC,votos/total,blancos/votos,nulos/votos,
                a_candidaturas/votos,a_candidaturas_mayoritarias/votos,
                weighted_avg,weighted_std]
        
        return pd.Series(vals,index)
                
