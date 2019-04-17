'''
Created on 12 feb. 2019

@author: Sergio
'''
import pandas as pd
import numpy as np
import datetime
from fuentes.Fuente import Fuente, rename
from fuentes.Gini import *

class Irpf2014(Fuente):
    
    renombrar = {
        'muni': 'municipio (local)',
        'prov': 'Codigo Provincia',
        'EjnacD': 'Edad Media',
        'ca': 'Comunidad Aut',
        'sexo':'ratio sexo'        
    }
     
    def __init__(self):
        self.url = 'C:\\Users\\Sergio\\Desktop\\TFG-Datos-publicos-master\\fuentes\\MuestraIRPF_2014.csv'
        
        descripcion = 'Datos de irpf 2014'
        super().__init__('irpf2014', 'irpf', descripcion)
    

    def obtenerDatosCorrectos(self, lDatos):
        #Datos que no se deben tener en cuenta
        correcto = list()
        for i in range(len(lDatos[0])):
            if (lDatos[0][i] + lDatos[1][i] < 0 or lDatos[2][i] + lDatos[3][i] < 0):
                correcto.append(-1)
            elif (lDatos[4][i] + lDatos[5][i] < 0 or lDatos[5][i] < 0):
                correcto.append(-1)
            elif (lDatos[0][i] + lDatos[1][i] < lDatos[2][i] + lDatos[3][i] or lDatos[2][i] + lDatos[3][i] < lDatos[4][i] + lDatos[5][i] or lDatos[4][i] + lDatos[5][i] < lDatos[6][i]):
                correcto.append(-1)
            elif (lDatos[7][i] == 'C'):
                correcto.append(2)
            else:
                correcto.append(1)
        
        return correcto
    
    def obtenerActividadEmpresarial(self, df):
        
        url = 'C:\\Users\\Sergio\\Desktop\\TFG-Datos-publicos-master\\fuentes\\ActividadEmpresarial.csv'
        actividad = pd.read_csv(url, sep=';', header=0, encoding = "ISO-8859-1", dtype={'Sección': str,'División': str,'Agrupación': str,
                                                                                         'Grupo': str, 'Epígrafe' : str})
        #print(df.head(5))
        #print(actividad.head(30))
        nombresActividades = [None] * len(df)
        print('v1')
        for i in range(len(df)):
            secciones = list()
            if df['P087_1'][i] > 0:
                secciones.append(df['P087_1'][i])
                if df['P087_2'][i] > 0:
                    secciones.append(df['P087_2'][i]) 
                    if df['P087_3'][i] > 0:
                        secciones.append(df['P087_3'][i]) 
                        if df['P087_4'][i] > 0:
                            secciones.append(df['P087_4'][i]) 
                            if df['P087_5'][i] > 0:
                                secciones.append(df['P087_5'][i])
                                if df['P087_6'][i] > 0:
                                    secciones.append(df['P087_6'][i]) 
            
            numActiv = len(secciones)
            #print('-------')
            #print(numActiv)
            print('v2')
            for j in range(numActiv):
                seccion = str(int(secciones[j]))
                grupo = df['P088_'+str(int(j + 1))].astype(str)
                grupo = grupo[i]
                aux = actividad[actividad['Sección'] == seccion]
                if len(grupo) > 0 and len(aux) > 1:
                    aux = aux[aux['División'] == grupo[0]]
                if len(grupo) > 1 and len(aux) > 1:
                    aux = aux[aux['Agrupación'] == grupo[0:2]]
                if len(grupo) > 2 and len(aux) > 1:
                    aux = aux[aux['Grupo'] == grupo[0:3]] 
                if len(grupo) > 3 and len(aux) > 1:
                    aux = aux[aux['Epígrafe'] == (grupo[0:3]+','+grupo[3])]
                    
            if numActiv > 0:
                nombresActividades[i] = aux['Denominación']
            else:
                nombresActividades[i] = '-'      
            
            if i == 4:
                print('AQUI')
                print(secciones)
                print('AQUI')
                print(aux)
                print('AQUI')
                print(grupo)
                print('AQUI fin')  
            
            if i == 5:
                print('AQUI2')
                print(secciones)
                print('AQUI2')
                print(aux)
                print('AQUI2')
                print(grupo)
                print('AQUI2')     
            
            if i%10 == 0:
                print(i,'/',len(df))
                if i == 20:
                    break  
                
        #print(nombresActividades)
        print('v3')
        return nombresActividades
        
    @rename(renombrar)   
    def carga(self):
        """
        Devuelve el Dataframe con los códigos
        """
        df = pd.read_csv(self.url, sep='\t', header=0, 
                         usecols=['factor','sexo','prov','muni','ca','EjnacD','Par430','Par445', 'Par17',
                                  'Par18','Par19', 'Par20', 'Par589', 'Par490', 'Par495', 'Par545', 'Par546',
                                  'dec', 'P087_1', 'P087_2','P087_3','P087_4','P087_5','P087_6','P088_1',
                                  'P088_2','P088_3','P088_4','P088_5','P088_6'])
        
        #dtype={'P088_1': str,'P088_2': str,'P088_3': str,'P088_4': str,'P088_5': str,
        #'P088_6': str}
        
        print('Irpf2014: csv leido')
        print('Irpf2014: Obteniendo actividades empresariales')

        #actividades = self.obtenerActividadEmpresarial(df)
        #df['Actividad Empresarial'] = actividades
        
        print('Irpf2014: Calculando Rentas')

        df['Codigo Municipio'] = df['prov'].astype(str).str.zfill(2) + df['muni'].astype(str).str.zfill(3)
        #df['Codigo Municipio'] = df['Codigo Municipio'].astype(float)
        
        df['Renta total'] = df.Par430 + df.Par445 + df.Par17 + df.Par18 +  df.Par19 +  df.Par20
        df['Renta despues imp'] = df['Renta total'] - df.Par589
        
        
        
        lDatos = [list(df['Par430']), list(df['Par445']), list(df['Par490']), list(df['Par495']), list(df['Par545']), list(df['Par546']), list(df['Par589']), list(df['dec'])]
        
        correcto = self.obtenerDatosCorrectos(lDatos)
                
        rentas = list(df['Renta despues imp'])
        for j in range(len(rentas)):
            if correcto[j] == -1:
                rentas[j] = -1
            else:
                rentas[j] = rentas[j]/100
        df['Renta despues imp'] = rentas   
        
                
        print('Irpf2014: Obteniendo municipios')
        
        dictG1, dictG2, df = self.obtenerCodigoMunicipio(df)
        
        print('Irpf2014: guardando datos')
        
        df = df.drop(['Par430','Par445', 'Par17','Par18','Par19', 'Par20',
                      'Par589', 'Par490', 'Par495', 'Par545', 'Par546', 'P087_1',
                      'P087_2','P087_3','P087_4','P087_5','P087_6','P088_1',
                      'P088_2','P088_3','P088_4','P088_5','P088_6' ], axis = 1)
        
        #print(df.head(25))
        
        df = df.groupby('Codigo Municipio', as_index=False).mean().round(2)

        df['Gini antes imp'] = dictG1.values()
        df['Gini despues imp'] = dictG2.values()
        
        df['IRS'] = df['Gini antes imp'] -  df['Gini despues imp']
        df['IRS'] =  df['IRS'].round(6)
        
        nombres = self.obtenerNombreMunicipio(df)

        df['Nombre Municipio'] = nombres
        
        anno = datetime.datetime.now()
        anno = int(anno.year)
        
        df['EjnacD'] = anno - df['EjnacD']       
        df['Codigo Municipio'] = df['Codigo Municipio'].astype(str).str.zfill(5)
        df['sexo'] = df['sexo'] - 1
        df['prov'] = df['prov'].astype(int)
        df['muni'] = df['muni'].astype(int)
        df['prov'] = df['prov'].astype(str).str.zfill(2)
        df['muni'] = df['muni'].astype(str).str.zfill(3)
        

        return df
    
    
    
    def obtenerNombreMunicipio(self, df):
        url= 'C:\\Users\\Sergio\\Desktop\\TFG-Datos-publicos-master\\fuentes\\Municipios.csv'
        muniDF = pd.read_csv(url, sep=';', header=0, encoding = "ISO-8859-1")
        print('Irpf2014: Obteniendo nombres municipio')
        nombres = list()
        for i in range(len(df)):
            nombre = muniDF[muniDF.Código == df['Codigo Municipio'][i]]
            nombre = list(nombre.Municipio)
            try:
                nombres.append(nombre[0])
            except IndexError:
                nombres.append('-')
        return nombres
    
    def obtenerCodigoMunicipio(self, df):
        listaMuni = list()
        df['Codigo Municipio'] = df['Codigo Municipio'].astype(int)
        cont = 0
        aux = len(df['muni'])
        for e in df['Codigo Municipio']:

            if e not in listaMuni:
                listaMuni.append(e)
        
        dictG1 = dict()
        dictG2 = dict()
        print('Irpf2014: Calculando Gini')
        cont = 0
        aux = len(listaMuni)
        for i in listaMuni:
            #print ('\r' + str(cont) + '\/' + str(aux))
            #cont+=1
            df2 = df[df['Codigo Municipio'] == i]
            G1 = gini(list(df2['Renta total']))
            G2 = gini(list(df2['Renta despues imp']))
            dictG1[i] = G1
            dictG2[i] = G2
        
        return dictG1, dictG2, df
    
    

