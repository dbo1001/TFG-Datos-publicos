'''
Created on 12 feb. 2019

@author: Sergio
'''
import pandas as pd
from fuentes.Fuente import Fuente, rename
from fuentes.Gini import *

class Irpf2014(Fuente):
    
    renombrar = {
        'muni': 'municipio (local)',
        'prov': 'Codigo Provincia',
        'EjnacD': 'Nacimiento',
        'ca': 'Comunidad Aut'
                
    }
     
    def __init__(self):
        self.url = 'C:\\Users\\Sergio\\Desktop\\TFG-Datos-publicos-master\\fuentes\\MuestraIRPF_2014.csv'
        
        descripcion = 'Datos de irpf 2014'
        super().__init__('irpf2014', 'irpf', descripcion)
    
    @rename(renombrar)   
    def carga(self):
        """
        Devuelve el Dataframe con los códigos
        """
        df = pd.read_csv(self.url, sep='\t', header=0, 
                         usecols=['factor','sexo','prov','muni','ca','EjnacD','Par430','Par445', 'Par17','Par18','Par19', 'Par20', 'Par589', 'Par490', 'Par495', 'Par545', 'Par546', 'Par589', 'dec'] )
        
        
        
        df['Codigo Municipio'] = df['prov'].astype(str).str.zfill(2) + df['muni'].astype(str).str.zfill(3)
        #df['Codigo Municipio'] = df['Codigo Municipio'].astype(float)
        
        
        df['Renta del periodo']=df.Par430 + df.Par445 + df.Par17 + df.Par18 +  df.Par19 +  df.Par20 - df.Par589
        
        
        
        print('ok1')
        lDatos = [list(df['Par430']), list(df['Par445']), list(df['Par490']), list(df['Par495']), list(df['Par545']), list(df['Par546']), list(df['Par589']), list(df['dec'])]
        
        #Datos que no se deben tener en cuenta
        correcto = list()
        for i in range(len(lDatos[0])):
            if (lDatos[0][i] + lDatos[1][i] < 0 or lDatos[2][i] + lDatos[3][i] < 0):
                correcto.append(-1)
            elif (lDatos[4][i] + lDatos[5][i] < 0 or lDatos[5][i] < 0):
                correcto.append(-1)
            elif(lDatos[0][i] + lDatos[1][i] < lDatos[2][i] + lDatos[3][i] or lDatos[2][i] + lDatos[3][i] < lDatos[4][i] + lDatos[5][i] or lDatos[4][i] + lDatos[5][i] <  lDatos[6][i]):
                correcto.append(-1)
            elif(lDatos[7][i] == 'C'):
                correcto.append(2)
            else:
                correcto.append(1)
                
        
        print('ok2')    
                   
        
        
        rentas = list(df['Renta del periodo'])
        for j in range(len(rentas)):
            if correcto[j] == -1:
                rentas[j] = -1
            else:
                rentas[j] = rentas[j]/100
        df['Renta del periodo'] = rentas   
        
                
        print('ok3')
       
            
        
        listaProv = list()
        for e in df['prov']:
            if e not in listaProv:
                listaProv.append(e)
        
        dictG = dict()
        for i in listaProv:
            df2 = df[df['prov']==i]
            G = gini(list(df2['Renta del periodo']))
            dictG[i]=G
        
        print(dictG)
            
        
        
        listaMuni = list()
        df['Codigo Municipio'] = df['Codigo Municipio'].astype(int)
        print(len(df['Codigo Municipio']))
        print(len(df['prov']))
        print(df['Codigo Municipio'].head(3))
        print(df['prov'].head(3))
        print(df['muni'].head(3))
        
        cont=0
        aux = len(df['muni'])
        for e in df['Codigo Municipio']:
            #print(e)
            #print ('\r' + str(cont) + '\/' + str(aux))
            #cont+=1
            if e not in listaMuni:
                listaMuni.append(e)
        
        dictG2 = dict()
        print('ok4')
        cont=0
        aux = len(listaMuni)
        for i in listaMuni:
            #print ('\r' + str(cont) + '\/' + str(aux))
            #cont+=1
            df2 = df[df['Codigo Municipio']==i]
            G = gini(list(df2['Renta del periodo']))
            dictG2[i]=G
        
        print(dictG2)
        
        #df = df.groupby("prov", as_index=False).mean()
        df = df.groupby('Codigo Municipio', as_index=False).mean()

        #df['Gini'] = dictG.values()
        df['Gini'] = dictG2.values()
        
        
        
        #df= pd.read_csv(self.url, sep='\t', header=0, nrows=100, 
                         #usecols=['factor','sexo','prov','muni','ca','EjnacD','Par430','Par445', 'Par17','Par18','Par19', 'Par20', 'Par589' ] )
        
        df['Codigo Municipio'] = df['Codigo Municipio'].astype(str).str.zfill(5)
        df['prov'] = df['prov'].astype(int)
        df['muni'] = df['muni'].astype(int)
        df['prov'] = df['prov'].astype(str).str.zfill(2)
        df['muni'] = df['muni'].astype(str).str.zfill(3)
        return df