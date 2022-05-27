# -*- coding: utf-8 -*-
"""
Created on Thu May 26 17:29:51 2022

@author: HP
"""

'''
        ETAPA 0: Preparar e importar librerías

'''

# Ruta del directorio: D:\upp

ruta='D:\pedidos\pedido1'

# Ruta de archivos de entrada: D:\upp\Input

ruta_input=ruta+'\Input'

# Ruta de archivos de salida: D:\upp\Output

ruta_output=ruta+'\Output'

# Importar librería Pandas

import pandas as pd

# Importar librería dbfread

from dbfread import DBF

'''
        ETAPA 1: Generar base de Censo 2921

'''

# Importar Censo 2021

# Generar DBF

b_dbf=DBF(ruta_input+'/Local_Sec200.dbf')

# Generar dataframe

enc = pd.DataFrame(iter(b_dbf))

# Importar base de dirección

bas = pd.read_excel(ruta_input+ '/PADRON DE SSEE BASICOS - nivel inicial.xlsx',header=2)

# Eliminar la variable de comprobación

del bas['Unnamed: 21']
del bas['Unnamed: 22']
del bas['Unnamed: 23']
del bas['Unnamed: 24']

# Verificar varibles de la encuesta

print(enc.columns.values)

# Variables de interés

ser=enc[['CODLOCAL','P202','P202_E','P207','P207_E','P209','P209_E','P225']]
ser.loc[(ser['P225']=='SI'),'P225'] = '1'
ser.loc[(ser['P225']=='NO'),'P225'] = '0'

# Renombrar variable

ser.rename(columns={'CODLOCAL':'codlocal'},inplace=True)

# Pasar a integer

ser.codlocal=ser.codlocal.astype(int)

# Verificar tipo de variables

print(bas.dtypes)
print(ser.dtypes)

# Combinar bases usando left

bas_ser=pd.merge(bas, ser, on =['codlocal'], how ='left')

# Importar base para conectividad

bc = pd.read_excel(ruta_input+ '/base_VF_2705.xlsx')

# Variables de interés

con=bc[['Código de local escolar','acceso_internet_fijo']]

# Renombrar variable

con.rename(columns={'Código de local escolar':'codlocal'},inplace=True)

# Combinar bases usando left

bas_ser_con=pd.merge(bas_ser, con, on =['codlocal'], how ='left')

# Exportar base

bas_ser_con.to_excel(ruta_output+'/base_servicios.xlsx', sheet_name='base' , index= False)

