import pickle
from pathlib import Path
from streamlit_option_menu import option_menu
import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
import csv
import numpy as numpy
import requests
import altair as alt
from datetime import datetime
from datetime import time
import os
import numpy as np

# --- pipes --- #

# pip install streamlit-option-menu
# pip install openpyxl
# pip install streamlit-authenticator==0.1.5
# pip install pandas requests
# pip install pandas
# pip install jupyter

# ----------------------- funções ----------------------- #

# colocar lembrete de pagamento

# def calculaHoras(): <- Passar por toda a tabela calcular todas as horas (somar por linha)

def hourToMinute(min): # calculadora de minutos para horas
    h=min//60
    m=min%60
    total = time(h,m,0)
    return(total)

def hourCalculator(col): # recebe a coluna para calcular o total de horas e minutos nela
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
        'Total hours worked':[datetime],
        'Daily rate':[int],
        'Regular hours':[datetime],
        'Total Payable':[float]},
        index=[])
    return resume 

def resumeDfPop():
        df.loc[0,'Name'] = name,
        df.loc[0,'Month'] = datetime(2024, 1, 1),
        df.loc[0,'Designation'] = designation,
        df.loc[0,'Total hours worked']= datetime(2024, 1, 1),
        df.loc[0,'Daily rate'] = 0,
        df.loc[0,'Regular hours'] = hours,
        df.loc[0,'Total Payable'] = 0

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

def dfPop(): # populando o df
    for i in range(1,32):
        df.loc[i,'Name'] = name
        df.loc[i,'Date'] = datetime(2024, 1, i)
        df.loc[i,'Start time'] = datetime(2024,1,i,0)
        df.loc[i,'Finish time'] = datetime(2024,1,i,0)                   
        df.loc[i,'Regular hours'] = hours               
        df.loc[i,'Sick'] = False               
        df.loc[i,'Vacation'] = False               
        df.loc[i,'Holiday'] = False                
        df.loc[i,'Other hours'] = datetime(2024,1,1,0)
        df.loc[i,'TOTAL HOURS'] = datetime(2024,1,1,0)

def toExcelModified(joined_path): # salvando o novo registro 
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
         
# ----------------------- main ----------------------- #
    
st.set_page_config(page_title='Hours Manager',layout='centered',page_icon='clock430')

# autenticação de usuário

names = ['Carlos Moura','Sheila Santana','Judas Escariodes']
usernames = ['carlosmoura','sheilasantanta','judas']

# carregamento de senha

file_path = Path(__file__).parent / 'hashed_pw.pkl'
with file_path.open('rb') as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, 'login_cookie','adqecd', cookie_expiry_days=30) # tempo para senha salva expirar

name, authentication_status, username = authenticator.login('Login','main')

# condicionais login

if authentication_status == False:
    st.error('Username/password is incorrect')
if authentication_status == None:
    st.warning('Please enter your user name and password')

# login == true    
if authentication_status:
    # ------- paths ------- #
    resume_db_path = '/home/carlos/Dropbox/code/employees/resumeDb'
    employee_resume_db_path = '/home/carlos/Dropbox/code/employees/csv/_resume.csv'

    db_path = '/home/carlos/Dropbox/code/employees/db'
    employee_path = '/home/carlos/Dropbox/code/employees/csv/_employees.csv'
    
    authenticator.logout('Logout','sidebar')
    st.sidebar.title(f'Welcome {name}')

    with st.sidebar:
        selected = option_menu(
            menu_title=None, # obrigatório ou None
            options=['Resume','New Employee','Attendance']
        )
        
    if selected == 'Resume':

        st.title(f'{selected}')

        with st.container():
            st.subheader('Registered employees')
            st.write('List of employees and salaries')
            df = pd.read_csv(employee_path,sep=';')
            st.table(df)

        menu = ['January','February','March','April','May','June','July','August','Setember','October','November','December']
        choice = st.selectbox('Select the month',menu)

        if(choice == 'January'):
                st.write('oi')
                dfTempLen = pd.read_csv(employee_path,sep=';')
                
                readLen = int(len(dfTempLen))

                st.write('Len: ',readLen)

                df = pd.DataFrame()
                
                for i in range(readLen):
                    
                    a_path = resume_db_path
                    a_file = str(i) + ".xlsx"
                    joined_path = os.path.join(a_path, a_file)

                    xls = pd.ExcelFile(joined_path) 
                    dfTemp = pd.read_excel(xls, 'January')

                    st.write(dfTemp)

    if selected == 'New Employee': 
        st.title(f'{selected}')
        st.subheader('Registered employees')

        df = pd.read_csv(employee_path,sep=';') # concat[df,df2]
        dfResume = pd.read_csv(employee_resume_db_path,sep=';') # concat[dfResume,df3]

        st.table(df)

        st.subheader('Register new employee')
        form = st.form('Options_form')

        user_name = form.text_input('Name')
        user_designation = form.text_input('Designation')
        user_hours = form.number_input('Regular hours',format='%.0f')
        daily_rate = form.number_input('Daily rate',format='%.1f')
        
        dict = { # dicionario para o banco de dados principal
            'Name':[user_name],
            'Designation':[user_designation],
            'Regular hours':[user_hours],
            'Daily rate':daily_rate}
        
        
        dict2 = { # dicionario para o banco de dados do resumo
            'Name':[user_name],
            'Month':[datetime],
            'Designation':[user_designation],
            'Total hours worked':[datetime],
            'Daily rate':daily_rate,
            'Regular hours':[user_hours],
            'Total Payable':[int]}  
        
        button_press = form.form_submit_button()
            
        if button_press: 
            # ------- criando o banco de dados principal -------#

            df2 = pd.DataFrame(dict) # df do dicionario do banco de dados principal
                    
            dfTemp = pd.concat([df, df2],ignore_index = True) 
            dfTemp.to_csv(employee_path,index=False,sep=';') #index = False <-- cuidado com a criação de índice dentro de índice!
            
            dfLastIndex = len(dfTemp)-1
            strDfLastIndex = str(dfLastIndex) # transformando o índice do último elemento que foi registrado em uma string
            employee = dfTemp.loc[dfLastIndex]
                    
            hours = employee[2]
            name = employee[0]

            df = dfCreate()
            dfPop()  
            
            a_path = db_path # caminho para o banco de dados principal
            a_file = strDfLastIndex + ".xlsx" # criando o nome do arquivo

            joined_path = os.path.join(a_path, a_file) # jundando o índice do último elemento que foi registrado ao nome do arquivo.xlsx
            
            toExcelModified(joined_path) #salvando banco de dados de horas

            # ------- criando o banco de dados do resumo -------#

            df3 = pd.DataFrame(dict2) # df do dicionario do banco de dados do resumo

            dfTemp2 = pd.concat([dfResume,df3],ignore_index = True) 
            dfTemp2.to_csv(employee_resume_db_path,index=False,sep=';')
                        
            dfLastIndex = len(dfTemp)-1
            strDfLastIndex = str(dfLastIndex) # transformando o índice do último elemento que foi registrado em uma string
            employee = dfTemp.loc[dfLastIndex]

            name = employee[0]
            designation = employee[1]
            hours = employee[2]

            df = resumeDfCreate()
            resumeDfPop()

            a_path = resume_db_path # caminho para o banco de dados do resumo
            a_file = strDfLastIndex + ".xlsx" # criando o nome do arquivo

            joined_path = os.path.join(a_path, a_file) # jundando o índice do último elemento que foi registrado ao nome do arquivo.xlsx
            
            toExcelModified(joined_path) #salvando banco de dados de horas

            st.rerun()     

        else: 
            st.write('Please fill in the form')

        st.title('Remove employee')
        form = st.form('Remove_employee')
        dfNames = pd.read_csv(employee_path,sep=';')
        user_index = form.number_input('index',format='%.0f')
        button_press = form.form_submit_button()
        removeIndex = user_index

        if button_press:

            # ------- dropando o registro do _employees.csv ------- #

            intRemoveIndex = int(removeIndex)
            strRemoveIndex= str(intRemoveIndex)
            df = pd.read_csv(employee_path,sep=';')
            dfIndex = df.iloc[intRemoveIndex]
            name = dfIndex[0]

            dfTemp = df.drop(removeIndex) # removendo o registro da tabela de nomes
            dfTemp.to_csv(employee_path,index=False,sep=';') #index = False <-- cuidado com a criação de índice dentro de índice!

            # ------- dropando o registro do _resume.csv ------- #

            intRemoveIndex = int(removeIndex)
            strRemoveIndex= str(intRemoveIndex)
            df2 = pd.read_csv(employee_resume_db_path,sep=';'
                              )
            dfIndex = df.iloc[intRemoveIndex]
            name = dfIndex[0]

            dfTemp = df2.drop(removeIndex)
            dfTemp.to_csv(employee_resume_db_path,index=False,sep=';')

            # ------- removendo o registro do banco de dados principal ------- #

            a_path = db_path # removendo o registro da pasta de arquivos de nomes
            a_file = strRemoveIndex + ".xlsx" # criando o nome do arquivo selecionado para remoção

            joined_path = os.path.join(a_path, a_file)          
            os.remove(joined_path)

            os.chdir(db_path)
             
            for count, f in enumerate(os.listdir()): #restaurando o índice dos arquivos .xlsx
                f_name, f_ext = os.path.splitext(f)
                f_name = str(count)
 
                new_name = f'{f_name}{f_ext}'
                os.rename(f, new_name)

            # ------- removendo o registro do banco do resumo ------- #

            a_path = resume_db_path # removendo o registro da pasta de arquivos de nomes
            a_file = strRemoveIndex + ".xlsx" # criando o nome do arquivo selecionado para remoção

            joined_path = os.path.join(a_path, a_file)          
            os.remove(joined_path)

            os.chdir(resume_db_path)
             
            for count, f in enumerate(os.listdir()): #restaurando o índice dos arquivos .xlsx
                f_name, f_ext = os.path.splitext(f)
                f_name = str(count)
 
                new_name = f'{f_name}{f_ext}'
                os.rename(f, new_name)

            st.rerun()     
        else: 
            st.write('Please fill in the form')

    if selected == 'Attendance':
            st.title('Attendance')
                        
            menu = ['January','February','March','April','May','June','July','August','Setember','October','November','December']
            choice = st.sidebar.selectbox('Select the month',menu)

            if choice == 'January':
                st.header(choice + ' timesheet')
                dfNames = pd.read_csv(employee_path,sep=';')
                names = dfNames['Name']

                selectedEmployee = st.selectbox('Select the employee',names) # selecionando o funcionário desejado pelo label
                rowIndex = dfNames.index[dfNames['Name'] == selectedEmployee].tolist()# retornando uma lista com o índice e o nome do funcionário selecionado
                employeeIndex = rowIndex[0] # índice numérico do funcionário selecionado

                # ------- lendo e salvando em variaveis os presets anteriores dos registros do banco de dados ------- #

                a_path = db_path
                a_file = str(employeeIndex) + ".xlsx"
                joined_path = os.path.join(a_path, a_file)

                xls = pd.ExcelFile(joined_path) 

                df1 = pd.read_excel(xls, 'January')
                df2 = pd.read_excel(xls, 'February')
                df3 = pd.read_excel(xls, 'March')
                df4 = pd.read_excel(xls, 'April')
                df5 = pd.read_excel(xls, 'May')
                df6 = pd.read_excel(xls, 'June')
                df7 = pd.read_excel(xls, 'July')
                df8 = pd.read_excel(xls, 'August')
                df9 = pd.read_excel(xls, 'Setember')
                df10 = pd.read_excel(xls, 'October')
                df11 = pd.read_excel(xls, 'November')
                df12 = pd.read_excel(xls, 'December')

                # ------- lendo e salvando os presets anteriores dos registros do banco de dados do resumo ------- #

                b_path = resume_db_path
                b_file = str(employeeIndex) + ".xlsx"
                joined_pathb = os.path.join(b_path, b_file)

                xlsb = pd.ExcelFile(joined_pathb) # salvando os presets anteriores dos registros do banco de dados

                df1b = pd.read_excel(xls, 'January')
                df2b = pd.read_excel(xls, 'February')
                df3b = pd.read_excel(xls, 'March')
                df4b = pd.read_excel(xls, 'April')
                df5b = pd.read_excel(xls, 'May')
                df6b = pd.read_excel(xls, 'June')
                df7b = pd.read_excel(xls, 'July')
                df8b = pd.read_excel(xls, 'August')
                df9b = pd.read_excel(xls, 'Setember')
                df10b = pd.read_excel(xls, 'October')
                df11b = pd.read_excel(xls, 'November')
                df12b = pd.read_excel(xls, 'December')    
                
                df_edited = st.data_editor( # data_editor <- permite a edição dos registros do df
                    df1,
                    column_config={
                    'Name': st.column_config.TextColumn(
                    'Name'),

                    'Date': st.column_config.DatetimeColumn(
                    'Date',
                    min_value=datetime(2023, 6, 1),
                    max_value=datetime(2025, 1, 1),
                    format='D MMM YYYY',
                    step=60),

                    'Start time': st.column_config.TimeColumn(
                    'Start time',
                    min_value=time(0, 0, 0),
                    max_value=time(23, 0, 0),
                    format='HH:mm a',
                    step=60),

                    'Finish time': st.column_config.TimeColumn(
                    'Finish time',
                    min_value=time(0,0,0),
                    max_value=time(23,0,0),
                    format='HH:mm a',
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
                    max_value=time(23,0,0),
                    format='HH:mm',
                    step=60), 

                    },
                    hide_index=True,
                    disabled=('Name', 'Date','TOTAL HOURS'),width=1000
                    )                

                form = st.form('str',border=False)
                                
                resume = resumeDfCreate()

                totalNormalTime = hourCalculator(9) # coluna de horas totais
                totalExtraTime = hourCalculator(8) # coluna de horas extras

                resume.loc[0,'Name'] = df_edited.loc[0,'Name']
                resume.loc[0,'Month'] = choice
                resume.loc[0,'Designation'] =  dfNames.loc[0,'Designation'] 
                resume.loc[0,'Regular hours'] =  dfNames.loc[0,'Regular hours']
                resume.loc[0,'Total hours worked'] = hourToMinute(totalNormalTime)
                resume.loc[0,'Daily rate'] = dfNames.loc[0,'Daily rate'] 
                
                hourPayment = ((resume.loc[0,'Total hours worked']).hour)*((dfNames.loc[0,'Daily rate']/dfNames.loc[0,'Regular hours'])) # totalHorasTrabalhada  (diaria/totalDiasDiaria)

                totalHours = hourPayment # total pago por hora

                totalMinutes = ((dfNames.loc[0,'Daily rate']/dfNames.loc[0,'Regular hours'])/60)*(resume.loc[0,'Total hours worked'].minute) # total pago por minuto (diaria/totalDiasDiaria/60)*quantidade de minutos que sobrou

                totalPayable = totalHours + totalMinutes # pagamento total, ja calculado horas e minutos trabalhados

                resume.loc[0,'Total Payable'] = totalPayable

                st.header('Hours Resume')
                st.write('All hours worked with all other hours within')
                
                st.dataframe(resume,hide_index=True)
                
                for i in range(len(df_edited)): # atualizando todos os registros da tabela confome as regras
                    
                    sick = df_edited.iloc[i,5] 
                    vacation = df_edited.iloc[i,6]
                    holiday = df_edited.iloc[i,7]

                    temp = str(df_edited.iloc[i,2])
                    temp2 = type(df_edited.iloc[i,2])

                    if((sick or vacation or holiday) == True): # resetando os valores em caso de nulo
                        df_edited.iloc[i,2] = datetime(2024,1,1,0)
                        df_edited.iloc[i,3] = datetime(2024,1,1,0)
                        df_edited.iloc[i,8] = datetime(2024,1,1,0)
                        df_edited.iloc[i,9] = datetime(2024,1,1,0)
                    else:
                        startTime = df_edited.iloc[i,2] # começo do horário de trabalho
                        endTime = df_edited.iloc[i,3] # final do horário de trabalho
                        extraHours = df_edited.iloc[i,8] # hora extra

                        hoursTotal = endTime - startTime + extraHours # hora total trabalhada, horaFinal - horaInicial + horaExtra
                        hoursTotalStr = hoursTotal # hora total convertida em str (manipulação de datas sempre é feita com strings)
                        df_edited.iloc[i,9] = hoursTotalStr # inserindo o total de horas na coluna 'TOTAL HOURS'

                button_press = form.form_submit_button()
                
                if button_press:

                    with pd.ExcelWriter(joined_path) as excel_writer: # salvando as mudancas somente do mes requerido no banco de dados principal
                        df_edited.to_excel(excel_writer, sheet_name='January', index=False)
                        df2.to_excel(excel_writer, sheet_name='February', index=False)
                        df3.to_excel(excel_writer, sheet_name='March', index=False)
                        df4.to_excel(excel_writer, sheet_name='April', index=False)
                        df5.to_excel(excel_writer, sheet_name='May', index=False)
                        df6.to_excel(excel_writer, sheet_name='June', index=False)
                        df7.to_excel(excel_writer, sheet_name='July', index=False)
                        df8.to_excel(excel_writer, sheet_name='August', index=False)
                        df9.to_excel(excel_writer, sheet_name='Setember', index=False)
                        df10.to_excel(excel_writer, sheet_name='October', index=False)
                        df11.to_excel(excel_writer, sheet_name='November', index=False)
                        df12.to_excel(excel_writer, sheet_name='December', index=False)
                        
                    with pd.ExcelWriter(joined_pathb) as excel_writer: # salvando as mudancas somente do mes requerido no banco de dados do resumo
                        resume.to_excel(excel_writer, sheet_name='January', index=False)
                        df2.to_excel(excel_writer, sheet_name='February', index=False)
                        df3.to_excel(excel_writer, sheet_name='March', index=False)
                        df4.to_excel(excel_writer, sheet_name='April', index=False)
                        df5.to_excel(excel_writer, sheet_name='May', index=False)
                        df6.to_excel(excel_writer, sheet_name='June', index=False)
                        df7.to_excel(excel_writer, sheet_name='July', index=False)
                        df8.to_excel(excel_writer, sheet_name='August', index=False)
                        df9.to_excel(excel_writer, sheet_name='Setember', index=False)
                        df10.to_excel(excel_writer, sheet_name='October', index=False)
                        df11.to_excel(excel_writer, sheet_name='November', index=False)
                        df12.to_excel(excel_writer, sheet_name='December', index=False)
                        
                        st.rerun()
             
            if choice == 'February':
                st.header(choice + ' timesheet')
                dfNames = pd.read_csv(r'C:\Users\889612123\Documents\GitHub\coding\coding\employees\csv\_employees.csv',sep=';')
                names = dfNames['Name']

                selectedEmployee = st.selectbox('Select the employee',names) # selecionando o funcionário desejado pelo label
                rowIndex = dfNames.index[dfNames['Name'] == selectedEmployee].tolist()# retornando uma lista com o índice e o nome do funcionário selecionado
                employeeIndex = rowIndex[0] # índice numérico do funcionário selecionado
                employeeIndexStr = str(employeeIndex)

                a_path = r'C:\Users\889612123\Documents\GitHub\coding\coding\employees\db'
                a_file = employeeIndexStr + ".xlsx"
                joined_path = os.path.join(a_path, a_file)

                xls = pd.ExcelFile(joined_path)

                df1 = pd.read_excel(xls, 'January')
                df2 = pd.read_excel(xls, 'February')
                df3 = pd.read_excel(xls, 'March')
                df4 = pd.read_excel(xls, 'April')
                df5 = pd.read_excel(xls, 'May')
                df6 = pd.read_excel(xls, 'June')
                df7 = pd.read_excel(xls, 'July')
                df8 = pd.read_excel(xls, 'August')
                df9 = pd.read_excel(xls, 'Setember')
                df10 = pd.read_excel(xls, 'October')
                df11 = pd.read_excel(xls, 'November')
                df12 = pd.read_excel(xls, 'December')  
                    
                df_edited = st.data_editor( # data_editor <- permite a edição dos registros do df
                    df2,
                    column_config={
                    'Name': st.column_config.TextColumn(
                    'Name'),
                    'Date': st.column_config.DatetimeColumn(
                    'Date',
                    min_value=datetime(2023, 6, 1),
                    max_value=datetime(2025, 1, 1),
                    format='D MMM YYYY',
                    step=60),

                    'Start time': st.column_config.TimeColumn(
                    'Start time',
                    min_value=time(8, 0, 0),
                    max_value=time(19, 0, 0),
                    format='hh:mm a',
                    step=60),

                    'Finish time': st.column_config.TimeColumn(
                    'Finish time',
                    min_value=time(8,0,0),
                    max_value=time(19,0,0),
                    format='hh:mm a',
                    step=60),
                    },
                    hide_index=True,
                    disabled=('Name', 'Date'),
                    )                

                form = st.form('str',border=False)
  
                button_press = form.form_submit_button()



                if button_press:
                    with pd.ExcelWriter(joined_path) as excel_writer:
                        df1.to_excel(excel_writer, sheet_name='January', index=False)
                        df_edited.to_excel(excel_writer, sheet_name='February', index=False)
                        df3.to_excel(excel_writer, sheet_name='March', index=False)
                        df4.to_excel(excel_writer, sheet_name='April', index=False)
                        df5.to_excel(excel_writer, sheet_name='May', index=False)
                        df6.to_excel(excel_writer, sheet_name='June', index=False)
                        df7.to_excel(excel_writer, sheet_name='July', index=False)
                        df8.to_excel(excel_writer, sheet_name='August', index=False)
                        df9.to_excel(excel_writer, sheet_name='Setember', index=False)
                        df10.to_excel(excel_writer, sheet_name='October', index=False)
                        df11.to_excel(excel_writer, sheet_name='November', index=False)
                        df12.to_excel(excel_writer, sheet_name='December', index=False)
                        st.rerun()                
            if choice == 'March':
                st.header(choice + ' timesheet')    
            if choice == 'April':
                st.header(choice + ' timesheet')    
            if choice == 'May':
                st.header(choice + ' timesheet')    
            if choice == 'July':
                st.header(choice + ' timesheet')    
            if choice == 'August':
                st.header(choice + ' timesheet')    
            if choice == 'Setember':
                st.header(choice + ' timesheet')    
            if choice == 'October':
                st.header(choice + ' timesheet')     
            if choice == 'November':
                st.header(choice + ' timesheet')    
            if choice == 'December':
                st.header(choice + ' timesheet')         