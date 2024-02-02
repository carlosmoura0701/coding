import pandas as pd
import streamlit as st
import numpy as numpy
from datetime import datetime
from datetime import time
import os
from pandas import DataFrame

def hourToMinute(min): # calculadora de minutos para horas
    h=min//60
    m=min%60

    return "%02d:%02d" % (h, m) 

def hourCalculator(col,df_edited): # recebe a coluna para calcular o total de horas e minutos nela
    hour = int(0)
    minute = int(0)
    totalMinutes = int(0)            

    for i in range(len(df_edited)): #retornando horas e minutos totais trabalhados 
        hour += df_edited.iloc[i,col].hour
        minute += df_edited.iloc[i,col].minute
        totalMinutes = hour*60 + minute
    return(totalMinutes) 

def resumeDfCreate():
    resume = pd.DataFrame({
        'Name':[],
        'Month':[datetime],
        'Designation':[],
        'Total hours worked':[],
        'Daily rate':[int],
        'Regular hours':[datetime],
        'Total Payable':[float]},index=[])
    return resume 

def dfCreate(): # <- criação do df
    df = pd.DataFrame({
    'Name':[],
    'Date': [datetime], 
    'Start time': [datetime],
    'Finish time': [datetime],
    'Regular hours': [int],
    'Sick': [bool],
    'Vacation': [bool],
    'Holiday': [bool],
    'Other hours': [datetime],
    'TOTAL HOURS': [datetime]},index=[])
    return df

def dfPop(month,amount_of_days,name,hours): # populando o df

    df = pd.DataFrame()
    for i in range(1,amount_of_days+1):
        df.loc[i,'Name'] = name
        df.loc[i,'Date'] = datetime(2024, month, i)
        df.loc[i,'Start time'] = datetime(2024,month,i,0)
        df.loc[i,'Finish time'] = datetime(2024,month,i,0)                   
        df.loc[i,'Regular hours'] = hours               
        df.loc[i,'Sick'] = False               
        df.loc[i,'Vacation'] = False               
        df.loc[i,'Holiday'] = False                
        df.loc[i,'Other hours'] = datetime(2024,month,1,0)
        df.loc[i,'TOTAL HOURS'] = datetime(2024,month,1,0)
    return df

def toExcelModified(joined_path,df): # salvando o novo registro 
    with pd.ExcelWriter(joined_path) as writer:
        df.to_excel(writer, sheet_name='January', index=False)
        df.to_excel(writer, sheet_name='February', index=False)
        df.to_excel(writer, sheet_name='March', index=False)
        df.to_excel(writer, sheet_name='April', index=False)
        df.to_excel(writer, sheet_name='May', index=False)
        df.to_excel(writer, sheet_name='June', index=False)
        df.to_excel(writer, sheet_name='July', index=False)
        df.to_excel(writer, sheet_name='August', index=False)
        df.to_excel(writer, sheet_name='Setember', index=False)
        df.to_excel(writer, sheet_name='October', index=False)
        df.to_excel(writer, sheet_name='November', index=False)
        df.to_excel(writer, sheet_name='December', index=False)                    

def resumeDbChoice(choice,employee_resume_db_path,resume_db_path):
    cont = 0
    dfTempLen = pd.read_csv(employee_resume_db_path)
    readLen = int(len(dfTempLen))
    
    for i in range(readLen): # imprimindo o resumo de um funcionarios cadastrados
        
        a_path = resume_db_path
        a_file = str(i) + ".xlsx"
        joined_path = os.path.join(a_path, a_file)

        xls = pd.ExcelFile(joined_path) 
        dfTemp = pd.read_excel(xls, choice)

        cont = cont + dfTemp.iloc[0,6]

        st.dataframe(dfTemp,width=3000,hide_index=True)

    dict = { # dicionario para o banco de dados principal
        'Total to be paid:':[cont]}
    
    df = pd.DataFrame(dict)
    st.dataframe(df,hide_index=True)

def sorted_directory_listing_with_os_listdir(directory):
    items = os.listdir(directory)
    sorted_items = sorted(items)
    return sorted_items

def renameFiles(list,path):

    count = 0
    
    for count in range(len(list)):
   
        source = path + list[count]
        destination = path + str(count) + ".xlsx"
        os.rename(source, destination)

        count += 1

def removeRegisterFromDb(path,removeIndex):

    a_file = removeIndex + '.xlsx'

    joined_path = os.path.join(path, a_file)          
    os.remove(joined_path)

def dateEditor(df):
    df_edited = st.data_editor( # data_editor <- permite a edição dos registros do df
    df, # ----------- VARIA CONFORME O MES ----------- #
    column_config={
    'Name': st.column_config.TextColumn(
    'Name'),

    'Date': st.column_config.DatetimeColumn(
    'Date',
    min_value=datetime(2023,6,1),
    max_value=datetime(2025,1,1),
    format='D MMM YYYY',
    step=60),

    'Start time': st.column_config.TimeColumn(
    'Start time',
    min_value=time(0,0,10),
    #max_value=time(23,0,0),
    format='hh:mm a',
    step=60),

    'Finish time': st.column_config.TimeColumn(
    'Finish time',
    min_value=time(0,0,10),
    #max_value=time(23,0,0),
    format='hh:mm a',
    step=60),
    
    'Other hours': st.column_config.TimeColumn(
    'Other hours',
    min_value=time(0,0,0),
    max_value=time(23,0,0),
    format='HH:mm',
    step=60),

    'TOTAL HOURS': st.column_config.TimeColumn(
    'TOTAL HOURS',
    min_value=time(0,0,0),
    #max_value=time(23,0,0),
    format='HH:mm',
    step=60), 

    },
    hide_index=True,
    disabled=('Name', 'Date','TOTAL HOURS'),width=1000
    )                

    return df_edited
