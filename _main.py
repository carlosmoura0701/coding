import pickle
from pathlib import Path
from streamlit_option_menu import option_menu
from streamlit_extras.dataframe_explorer import dataframe_explorer
from pandas import DataFrame
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
from PIL import Image
import xlwings as xw
import yaml
import time

import pandas as pd
import streamlit as st
import numpy as numpy
from datetime import datetime
from datetime import time
import os
from pandas import DataFrame
# --- functions --- #

from functions import resumeDbChoice
from functions import dfCreate
from functions import toExcelModified
from functions import dfPop
from functions import resumeDfCreate
from functions import removeRegisterFromDb
from functions import sorted_directory_listing_with_os_listdir
from functions import renameFiles
from functions import dateEditor
from functions import resumeDfCreate
from functions import hourCalculator
from functions import hourToMinute

# --- pipes --- #

# pip install streamlit-option-menu
# pip install openpyxl
# pip install streamlit-authenticator==0.1.5
# pip install pandas requests
# pip install pandas
# pip install jupyter
   
# ------- paths ------- #
        
resume_db_path = 'hoursManager/resumeDb/'
employee_resume_db_path = 'hoursManager/csv/_resume.csv'

db_path = 'hoursManager/db/'
employee_path = 'hoursManager/csv/_employees.csv'

# ----------------------- main ----------------------- #
    
st.set_page_config(page_title='Hours Manager',layout='centered',page_icon='clock430')

# autenticação de usuário

names = ['John Smith', 'Rebecca Briggs','Carlos Moura']
usernames = ['jsmith', 'rbriggs','carlos']
hashed_passwords = ['$2b$12$2vKbwaZ.WHQnmymAx9/UTuL/HGNSBPkhrpoeli3wFdPNORq3tdE/q',
              '$2b$12$dKiLcB0jTRITp1IUjazuOOsSQbLp5bUC.OszxxiGAmzKl6uFOd482',
              '$2b$12$Cu/SbGPORkT0n1Lzf7U82OYz6QlS4wtofviy5u5NlpwGIeqtOsxiO']

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    'some_cookie_name_asddasd', 'some_signature_key_dsadsa*&', cookie_expiry_days=30)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:

    with st.sidebar:

        image = Image.open('/home/carlos/Dropbox/code/employees/hours_manager_1.0/images/logo.png')
        st.image(image)

        st.sidebar.title('Welcome *%s*' % (name))
        authenticator.logout('Logout','sidebar')

        selected = option_menu(
            menu_title=None, # obrigatório ou None
            options=['Resume','New Employee','Remove employee','Attendance']
        )
        
    if selected == 'Resume':
        
        st.title(f'{selected}')

        with st.container():
            st.subheader('Registered employees')
            df = pd.read_csv(employee_path,sep=';')

        try:
            if(len(df)==0):
                st.warning('No registered employees',icon="⚠️")
                st.stop()
            else:

                st.dataframe(df,hide_index=True)
                st.subheader('Amount payable resume')
                st.write('Resume of amount payable per month')  

               

                menu = ['January','February','March','April','May','June','July','August','Setember','October','November','December']
                choice = st.selectbox('Select the month',menu)

                if(choice == 'January'):
                    resumeDbChoice(choice,employee_resume_db_path,resume_db_path)
                if(choice == 'February'):
                    resumeDbChoice(choice,employee_resume_db_path,resume_db_path)        
                if(choice == 'March'):
                    resumeDbChoice(choice,employee_resume_db_path,resume_db_path)
                if(choice == 'April'):
                    resumeDbChoice(choice,employee_resume_db_path,resume_db_path)
                if(choice == 'May'):
                    resumeDbChoice(choice,employee_resume_db_path,resume_db_path)
                if(choice == 'June'):
                    resumeDbChoice(choice,employee_resume_db_path,resume_db_path)
                if(choice == 'July'):
                    resumeDbChoice(choice,employee_resume_db_path,resume_db_path)
                if(choice == 'August'):
                    resumeDbChoice(choice,employee_resume_db_path,resume_db_path)
                if(choice == 'Setember'):
                    resumeDbChoice(choice,employee_resume_db_path,resume_db_path)
                if(choice == 'October'):
                    resumeDbChoice(choice,employee_resume_db_path,resume_db_path)
                if(choice == 'November'):
                    resumeDbChoice(choice,employee_resume_db_path,resume_db_path)
                if(choice == 'December'):
                    resumeDbChoice(choice,employee_resume_db_path,resume_db_path)
        except:
            st.warning('Error')

    if selected == 'New Employee': 
        st.title(f'{selected}')
        st.subheader('Registered employees')

        df = pd.read_csv(employee_path,sep=';') # concat[df,df2]
        dfResume = pd.read_csv(employee_resume_db_path,sep=';') # concat[dfResume,df3]

        st.dataframe(df,hide_index=True,width=10000)

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
            'Name':[user_name].astype('object'),
            'Month':[None].astype('object'),
            'Designation':[user_designation].astype('object'),
            'Total hours worked':[None].astype('object'),
            'Daily rate':[daily_rate].astype('object'),
            'Regular hours':[user_hours].astype('object'),
            'Total Payable':[0].astype('object')}  
        
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
                     
            a_path = db_path # caminho para o banco de dados principal
            a_file = strDfLastIndex + ".xlsx" # criando o nome do arquivo

            joined_path = os.path.join(a_path, a_file) # jundando o índice do último elemento que foi registrado ao nome do arquivo.xlsx
            
            toExcelModified(joined_path,df) #salvando banco de dados de horas

            with pd.ExcelWriter(joined_path) as excel_writer: # salvando as mudancas somente do mes requerido no banco de dados principal
                dfPop(1,31,name,hours).to_excel(excel_writer, sheet_name='January', index=False)
                dfPop(2,29,name,hours).to_excel(excel_writer, sheet_name='February', index=False)
                dfPop(3,31,name,hours).to_excel(excel_writer, sheet_name='March', index=False)
                dfPop(4,30,name,hours).to_excel(excel_writer, sheet_name='April', index=False)
                dfPop(5,31,name,hours).to_excel(excel_writer, sheet_name='May', index=False)
                dfPop(6,30,name,hours).to_excel(excel_writer, sheet_name='June', index=False)
                dfPop(7,31,name,hours).to_excel(excel_writer, sheet_name='July', index=False)
                dfPop(8,31,name,hours).to_excel(excel_writer, sheet_name='August', index=False)
                dfPop(9,30,name,hours).to_excel(excel_writer, sheet_name='Setember', index=False)
                dfPop(10,31,name,hours).to_excel(excel_writer, sheet_name='October', index=False)
                dfPop(11,30,name,hours).to_excel(excel_writer, sheet_name='November', index=False)
                dfPop(12,31,name,hours).to_excel(excel_writer, sheet_name='December', index=False)

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
            
            a_path = resume_db_path # caminho para o banco de dados do resumo
            a_file = strDfLastIndex + ".xlsx" # criando o nome do arquivo

            joined_path = os.path.join(a_path, a_file) # jundando o índice do último elemento que foi registrado ao nome do arquivo.xlsx
            
            toExcelModified(joined_path,df) #salvando banco de dados de horas

            with pd.ExcelWriter(joined_path) as excel_writer: # salvando as mudancas somente do mes requerido no banco de dados do resumo
                df3.to_excel(excel_writer, sheet_name='January', index=False)
                df3.to_excel(excel_writer, sheet_name='February', index=False)
                df3.to_excel(excel_writer, sheet_name='March', index=False)
                df3.to_excel(excel_writer, sheet_name='April', index=False)
                df3.to_excel(excel_writer, sheet_name='May', index=False)
                df3.to_excel(excel_writer, sheet_name='June', index=False)
                df3.to_excel(excel_writer, sheet_name='July', index=False)
                df3.to_excel(excel_writer, sheet_name='August', index=False)
                df3.to_excel(excel_writer, sheet_name='Setember', index=False)
                df3.to_excel(excel_writer, sheet_name='October', index=False)
                df3.to_excel(excel_writer, sheet_name='November', index=False)
                df3.to_excel(excel_writer, sheet_name='December', index=False)

            st.rerun()     

        else: 
            st.write('Please fill in the form')

    if selected == 'Remove employee':

        df = pd.read_csv(employee_path,sep=';') # concat[df,df2]
        st.title('Remove employee')
        st.subheader('Registered employees') 

        try:
            if(len(df)==0):
                st.warning('No registered employees',icon="⚠️")
                st.stop()
            else:

                dfResume = pd.read_csv(employee_resume_db_path,sep=';') # concat[dfResume,df3]
                st.dataframe(df,hide_index=True,width=3000)

                dfNames = pd.read_csv(employee_path,sep=';')
                names = dfNames['Name']

                selectedEmployee = st.selectbox('Select the employee to remove',names) # selecionando o funcionário desejado pelo label
                rowIndex = dfNames.index[dfNames['Name'] == selectedEmployee].tolist()# retornando uma lista com o índice e o nome do funcionário selecionado
                user_index = rowIndex[0] 
                
                form = st.form('Remove_employee')
                button_press = form.form_submit_button()
                
                if button_press:

                    intRemoveIndex = int(user_index)
                    strRemoveIndex= str(intRemoveIndex)

                    # ------- dropando o registro do _employees.csv ------- #

                    df = pd.read_csv(employee_path,sep=';')
                    dfIndex = df.iloc[intRemoveIndex]
                
                    dfTemp = df.drop(intRemoveIndex) # removendo o registro da tabela de nomes
                    dfTemp.to_csv(employee_path,index=False,sep=';') #index = False <-- cuidado com a criação de índice dentro de índice!

                    # ------- dropando o registro do _resume.csv ------- #

                    df2 = pd.read_csv(employee_resume_db_path,sep=';')

                    dfIndex = df.iloc[intRemoveIndex]
                
                    dfTemp = df2.drop(intRemoveIndex)
                    dfTemp.to_csv(employee_resume_db_path,index=False,sep=';')

                    # ------- removendo o registro do db ------- #

                    removeRegisterFromDb(db_path,strRemoveIndex)

                    # ------- removendo o registro do db do resumo ------- #

                    removeRegisterFromDb(resume_db_path,strRemoveIndex)

                    # ------- restaurando o indice do db e do resume db ------- #


                    ordered_db_list = sorted_directory_listing_with_os_listdir(db_path)
                    renameFiles(ordered_db_list,db_path)

                    ordered_resume_db_list = sorted_directory_listing_with_os_listdir(resume_db_path)          
                    renameFiles(ordered_resume_db_list,resume_db_path)

                    st.rerun()
        except:      
            
            st.rerun()

    if selected == 'Attendance':
            st.title('Attendance')
                        
            menu = ['January','February','March','April','May','June','July','August','Setember','October','November','December']
            choice = st.selectbox('Select the month',menu)

            if choice == 'January':  
                    
                    st.header(choice + ' timesheet')
                    dfNames = pd.read_csv(employee_path,sep=';')
                    names = dfNames['Name']

                    selectedEmployee = st.selectbox('Select the employee',names) # selecionando o funcionário desejado pelo label
                    rowIndex = dfNames.index[dfNames['Name'] == selectedEmployee].tolist()# retornando uma lista com o índice e o nome do funcionário selecionado
                    
                    try:
                        employeeIndex = rowIndex[0] # índice numérico do funcionário selecionado
                    except:
                        st.warning('No registered employees',icon="⚠️")
                        st.stop()
                    
                    # ------- lendo e salvando em variaveis os presets anteriores dos registros do banco de dados ------- #
                    form01 = st.form(key = '01',border=False)
                    with(form01):

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

                        df1b = pd.read_excel(xlsb, 'January')
                        df2b = pd.read_excel(xlsb, 'February')
                        df3b = pd.read_excel(xlsb, 'March')
                        df4b = pd.read_excel(xlsb, 'April')
                        df5b = pd.read_excel(xlsb, 'May')
                        df6b = pd.read_excel(xlsb, 'June')
                        df7b = pd.read_excel(xlsb, 'July')
                        df8b = pd.read_excel(xlsb, 'August')
                        df9b = pd.read_excel(xlsb, 'Setember')
                        df10b = pd.read_excel(xlsb, 'October')
                        df11b = pd.read_excel(xlsb, 'November')
                        df12b = pd.read_excel(xlsb, 'December')    
                    
                        df_edited = dateEditor(df1)
                                                        
                        resume = resumeDfCreate()

                        totalNormalTime = hourCalculator(9,df_edited) # coluna de horas totais
                        totalExtraTime = hourCalculator(8,df_edited) # coluna de horas extras

                        daily_rate_local = dfNames.loc[0,'Daily rate'] 
                        regular_hours_local = dfNames.loc[0,'Regular hours']

                        resume.loc[0,'Name'] = df_edited.loc[0,'Name']
                        resume.loc[0,'Month'] = choice
                        resume.loc[0,'Designation'] =  dfNames.loc[0,'Designation'] 
                        resume.loc[0,'Regular hours'] = regular_hours_local 
                        resume.loc[0,'Total hours worked'] = hourToMinute(totalNormalTime) 
                        resume.loc[0,'Daily rate'] = daily_rate_local
                        
                        payablePerMinute = (daily_rate_local / (regular_hours_local*60))*totalNormalTime # calculo do valor a ser recebido por todos os minutos trabalhados no mes

                        resume.loc[0,'Total Payable'] = payablePerMinute
                        
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
                        
                        with pd.ExcelWriter(joined_path) as writer: # salvando as mudancas somente do mes requerido no banco de dados principal
                            df_edited.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            df2.to_excel(writer, sheet_name='February', index=False)
                            df3.to_excel(writer, sheet_name='March', index=False)
                            df4.to_excel(writer, sheet_name='April', index=False)
                            df5.to_excel(writer, sheet_name='May', index=False)
                            df6.to_excel(writer, sheet_name='June', index=False)
                            df7.to_excel(writer, sheet_name='July', index=False)
                            df8.to_excel(writer, sheet_name='August', index=False)
                            df9.to_excel(writer, sheet_name='Setember', index=False)
                            df10.to_excel(writer, sheet_name='October', index=False)
                            df11.to_excel(writer, sheet_name='November', index=False)
                            df12.to_excel(writer, sheet_name='December', index=False)
                            
                        with pd.ExcelWriter(joined_pathb) as writer: # salvando as mudancas somente do mes requerido no banco de dados do resumo
                            resume.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            df2b.to_excel(writer, sheet_name='February', index=False)
                            df3b.to_excel(writer, sheet_name='March', index=False)
                            df4b.to_excel(writer, sheet_name='April', index=False)
                            df5b.to_excel(writer, sheet_name='May', index=False)
                            df6b.to_excel(writer, sheet_name='June', index=False)
                            df7b.to_excel(writer, sheet_name='July', index=False)
                            df8b.to_excel(writer, sheet_name='August', index=False)
                            df9b.to_excel(writer, sheet_name='Setember', index=False)
                            df10b.to_excel(writer, sheet_name='October', index=False)
                            df11b.to_excel(writer, sheet_name='November', index=False)
                            df12b.to_excel(writer, sheet_name='December', index=False)

                    submitted = form01.form_submit_button("Submit")     
                    if submitted:
                        st.rerun() 

                    st.header('Hours Resume')
                    st.write('All hours worked with all other hours within')
                    st.dataframe(resume,hide_index=True,width=3000)  
 
            if choice == 'February':
                                
                    st.header(choice + ' timesheet')
                    dfNames = pd.read_csv(employee_path,sep=';')
                    names = dfNames['Name']

                    selectedEmployee = st.selectbox('Select the employee',names) # selecionando o funcionário desejado pelo label
                    rowIndex = dfNames.index[dfNames['Name'] == selectedEmployee].tolist()# retornando uma lista com o índice e o nome do funcionário selecionado
                    
                    try:
                        employeeIndex = rowIndex[0] # índice numérico do funcionário selecionado
                    except:
                        st.warning('No registered employees',icon="⚠️")
                        st.stop()
                    
                    # ------- lendo e salvando em variaveis os presets anteriores dos registros do banco de dados ------- #
                    form02 = st.form(key = '02',border=False)
                    with(form02):

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

                        df1b = pd.read_excel(xlsb, 'January')
                        df2b = pd.read_excel(xlsb, 'February')
                        df3b = pd.read_excel(xlsb, 'March')
                        df4b = pd.read_excel(xlsb, 'April')
                        df5b = pd.read_excel(xlsb, 'May')
                        df6b = pd.read_excel(xlsb, 'June')
                        df7b = pd.read_excel(xlsb, 'July')
                        df8b = pd.read_excel(xlsb, 'August')
                        df9b = pd.read_excel(xlsb, 'Setember')
                        df10b = pd.read_excel(xlsb, 'October')
                        df11b = pd.read_excel(xlsb, 'November')
                        df12b = pd.read_excel(xlsb, 'December')    
                    
                        df_edited = dateEditor(df2)
                                                        
                        resume = resumeDfCreate()

                        totalNormalTime = hourCalculator(9,df_edited) # coluna de horas totais
                        totalExtraTime = hourCalculator(8,df_edited) # coluna de horas extras

                        daily_rate_local = dfNames.loc[0,'Daily rate'] 
                        regular_hours_local = dfNames.loc[0,'Regular hours']

                        resume.loc[0,'Name'] = df_edited.loc[0,'Name']
                        resume.loc[0,'Month'] = choice
                        resume.loc[0,'Designation'] =  dfNames.loc[0,'Designation'] 
                        resume.loc[0,'Regular hours'] = regular_hours_local 
                        resume.loc[0,'Total hours worked'] = hourToMinute(totalNormalTime) 
                        resume.loc[0,'Daily rate'] = daily_rate_local
                        
                        payablePerMinute = (daily_rate_local / (regular_hours_local*60))*totalNormalTime # calculo do valor a ser recebido por todos os minutos trabalhados no mes

                        resume.loc[0,'Total Payable'] = payablePerMinute
                        
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
                        
                        with pd.ExcelWriter(joined_path) as writer: # salvando as mudancas somente do mes requerido no banco de dados principal
                            df1.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            df_edited.to_excel(writer, sheet_name='February', index=False)
                            df3.to_excel(writer, sheet_name='March', index=False)
                            df4.to_excel(writer, sheet_name='April', index=False)
                            df5.to_excel(writer, sheet_name='May', index=False)
                            df6.to_excel(writer, sheet_name='June', index=False)
                            df7.to_excel(writer, sheet_name='July', index=False)
                            df8.to_excel(writer, sheet_name='August', index=False)
                            df9.to_excel(writer, sheet_name='Setember', index=False)
                            df10.to_excel(writer, sheet_name='October', index=False)
                            df11.to_excel(writer, sheet_name='November', index=False)
                            df12.to_excel(writer, sheet_name='December', index=False)
                            
                        with pd.ExcelWriter(joined_pathb) as writer: # salvando as mudancas somente do mes requerido no banco de dados do resumo
                            df1b.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            resume.to_excel(writer, sheet_name='February', index=False)
                            df3b.to_excel(writer, sheet_name='March', index=False)
                            df4b.to_excel(writer, sheet_name='April', index=False)
                            df5b.to_excel(writer, sheet_name='May', index=False)
                            df6b.to_excel(writer, sheet_name='June', index=False)
                            df7b.to_excel(writer, sheet_name='July', index=False)
                            df8b.to_excel(writer, sheet_name='August', index=False)
                            df9b.to_excel(writer, sheet_name='Setember', index=False)
                            df10b.to_excel(writer, sheet_name='October', index=False)
                            df11b.to_excel(writer, sheet_name='November', index=False)
                            df12b.to_excel(writer, sheet_name='December', index=False)

                    submitted = form02.form_submit_button("Submit")     
                    if submitted:
                        st.rerun() 

                    st.header('Hours Resume')
                    st.write('All hours worked with all other hours within')
                    st.dataframe(resume,hide_index=True,width=3000)                                     

            if choice == 'March':

                    st.header(choice + ' timesheet')
                    dfNames = pd.read_csv(employee_path,sep=';')
                    names = dfNames['Name']

                    selectedEmployee = st.selectbox('Select the employee',names) # selecionando o funcionário desejado pelo label
                    rowIndex = dfNames.index[dfNames['Name'] == selectedEmployee].tolist()# retornando uma lista com o índice e o nome do funcionário selecionado
                    
                    try:
                        employeeIndex = rowIndex[0] # índice numérico do funcionário selecionado
                    except:
                        st.warning('No registered employees',icon="⚠️")
                        st.stop()
                    
                    # ------- lendo e salvando em variaveis os presets anteriores dos registros do banco de dados ------- #
                    form03 = st.form(key = '03',border=False)
                    with(form03):

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

                        df1b = pd.read_excel(xlsb, 'January')
                        df2b = pd.read_excel(xlsb, 'February')
                        df3b = pd.read_excel(xlsb, 'March')
                        df4b = pd.read_excel(xlsb, 'April')
                        df5b = pd.read_excel(xlsb, 'May')
                        df6b = pd.read_excel(xlsb, 'June')
                        df7b = pd.read_excel(xlsb, 'July')
                        df8b = pd.read_excel(xlsb, 'August')
                        df9b = pd.read_excel(xlsb, 'Setember')
                        df10b = pd.read_excel(xlsb, 'October')
                        df11b = pd.read_excel(xlsb, 'November')
                        df12b = pd.read_excel(xlsb, 'December')    
                    
                        df_edited = dateEditor(df3)
                                                        
                        resume = resumeDfCreate()

                        totalNormalTime = hourCalculator(9,df_edited) # coluna de horas totais
                        totalExtraTime = hourCalculator(8,df_edited) # coluna de horas extras

                        daily_rate_local = dfNames.loc[0,'Daily rate'] 
                        regular_hours_local = dfNames.loc[0,'Regular hours']

                        resume.loc[0,'Name'] = df_edited.loc[0,'Name']
                        resume.loc[0,'Month'] = choice
                        resume.loc[0,'Designation'] =  dfNames.loc[0,'Designation'] 
                        resume.loc[0,'Regular hours'] = regular_hours_local 
                        resume.loc[0,'Total hours worked'] = hourToMinute(totalNormalTime) 
                        resume.loc[0,'Daily rate'] = daily_rate_local
                        
                        payablePerMinute = (daily_rate_local / (regular_hours_local*60))*totalNormalTime # calculo do valor a ser recebido por todos os minutos trabalhados no mes

                        resume.loc[0,'Total Payable'] = payablePerMinute
                        
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
                        
                        with pd.ExcelWriter(joined_path) as writer: # salvando as mudancas somente do mes requerido no banco de dados principal
                            df1.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            df2.to_excel(writer, sheet_name='February', index=False)
                            df_edited.to_excel(writer, sheet_name='March', index=False)
                            df4.to_excel(writer, sheet_name='April', index=False)
                            df5.to_excel(writer, sheet_name='May', index=False)
                            df6.to_excel(writer, sheet_name='June', index=False)
                            df7.to_excel(writer, sheet_name='July', index=False)
                            df8.to_excel(writer, sheet_name='August', index=False)
                            df9.to_excel(writer, sheet_name='Setember', index=False)
                            df10.to_excel(writer, sheet_name='October', index=False)
                            df11.to_excel(writer, sheet_name='November', index=False)
                            df12.to_excel(writer, sheet_name='December', index=False)
                            
                        with pd.ExcelWriter(joined_pathb) as writer: # salvando as mudancas somente do mes requerido no banco de dados do resumo
                            df1b.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            df2b.to_excel(writer, sheet_name='February', index=False)
                            resume.to_excel(writer, sheet_name='March', index=False)
                            df4b.to_excel(writer, sheet_name='April', index=False)
                            df5b.to_excel(writer, sheet_name='May', index=False)
                            df6b.to_excel(writer, sheet_name='June', index=False)
                            df7b.to_excel(writer, sheet_name='July', index=False)
                            df8b.to_excel(writer, sheet_name='August', index=False)
                            df9b.to_excel(writer, sheet_name='Setember', index=False)
                            df10b.to_excel(writer, sheet_name='October', index=False)
                            df11b.to_excel(writer, sheet_name='November', index=False)
                            df12b.to_excel(writer, sheet_name='December', index=False)

                    submitted = form03.form_submit_button("Submit")     
                    if submitted:
                        st.rerun() 

                    st.header('Hours Resume')
                    st.write('All hours worked with all other hours within')
                    st.dataframe(resume,hide_index=True,width=3000)  

            if choice == 'April':

                    st.header(choice + ' timesheet')
                    dfNames = pd.read_csv(employee_path,sep=';')
                    names = dfNames['Name']

                    selectedEmployee = st.selectbox('Select the employee',names) # selecionando o funcionário desejado pelo label
                    rowIndex = dfNames.index[dfNames['Name'] == selectedEmployee].tolist()# retornando uma lista com o índice e o nome do funcionário selecionado
                    
                    try:
                        employeeIndex = rowIndex[0] # índice numérico do funcionário selecionado
                    except:
                        st.warning('No registered employees',icon="⚠️")
                        st.stop()
                    
                    # ------- lendo e salvando em variaveis os presets anteriores dos registros do banco de dados ------- #
                    form04 = st.form(key = '04',border=False)
                    with(form04):

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

                        df1b = pd.read_excel(xlsb, 'January')
                        df2b = pd.read_excel(xlsb, 'February')
                        df3b = pd.read_excel(xlsb, 'March')
                        df4b = pd.read_excel(xlsb, 'April')
                        df5b = pd.read_excel(xlsb, 'May')
                        df6b = pd.read_excel(xlsb, 'June')
                        df7b = pd.read_excel(xlsb, 'July')
                        df8b = pd.read_excel(xlsb, 'August')
                        df9b = pd.read_excel(xlsb, 'Setember')
                        df10b = pd.read_excel(xlsb, 'October')
                        df11b = pd.read_excel(xlsb, 'November')
                        df12b = pd.read_excel(xlsb, 'December')    
                    
                        df_edited = dateEditor(df4)
                                                        
                        resume = resumeDfCreate()

                        totalNormalTime = hourCalculator(9,df_edited) # coluna de horas totais
                        totalExtraTime = hourCalculator(8,df_edited) # coluna de horas extras

                        daily_rate_local = dfNames.loc[0,'Daily rate'] 
                        regular_hours_local = dfNames.loc[0,'Regular hours']

                        resume.loc[0,'Name'] = df_edited.loc[0,'Name']
                        resume.loc[0,'Month'] = choice
                        resume.loc[0,'Designation'] =  dfNames.loc[0,'Designation'] 
                        resume.loc[0,'Regular hours'] = regular_hours_local 
                        resume.loc[0,'Total hours worked'] = hourToMinute(totalNormalTime) 
                        resume.loc[0,'Daily rate'] = daily_rate_local
                        
                        payablePerMinute = (daily_rate_local / (regular_hours_local*60))*totalNormalTime # calculo do valor a ser recebido por todos os minutos trabalhados no mes

                        resume.loc[0,'Total Payable'] = payablePerMinute
                        
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
                        
                        with pd.ExcelWriter(joined_path) as writer: # salvando as mudancas somente do mes requerido no banco de dados principal
                            df1.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            df2.to_excel(writer, sheet_name='February', index=False)
                            df3.to_excel(writer, sheet_name='March', index=False)
                            df_edited.to_excel(writer, sheet_name='April', index=False)
                            df5.to_excel(writer, sheet_name='May', index=False)
                            df6.to_excel(writer, sheet_name='June', index=False)
                            df7.to_excel(writer, sheet_name='July', index=False)
                            df8.to_excel(writer, sheet_name='August', index=False)
                            df9.to_excel(writer, sheet_name='Setember', index=False)
                            df10.to_excel(writer, sheet_name='October', index=False)
                            df11.to_excel(writer, sheet_name='November', index=False)
                            df12.to_excel(writer, sheet_name='December', index=False)
                            
                        with pd.ExcelWriter(joined_pathb) as writer: # salvando as mudancas somente do mes requerido no banco de dados do resumo
                            df1b.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            df2b.to_excel(writer, sheet_name='February', index=False)
                            df3b.to_excel(writer, sheet_name='March', index=False)
                            resume.to_excel(writer, sheet_name='April', index=False)
                            df5b.to_excel(writer, sheet_name='May', index=False)
                            df6b.to_excel(writer, sheet_name='June', index=False)
                            df7b.to_excel(writer, sheet_name='July', index=False)
                            df8b.to_excel(writer, sheet_name='August', index=False)
                            df9b.to_excel(writer, sheet_name='Setember', index=False)
                            df10b.to_excel(writer, sheet_name='October', index=False)
                            df11b.to_excel(writer, sheet_name='November', index=False)
                            df12b.to_excel(writer, sheet_name='December', index=False)

                    submitted = form04.form_submit_button("Submit")     
                    if submitted:
                        st.rerun() 

                    st.header('Hours Resume')
                    st.write('All hours worked with all other hours within')
                    st.dataframe(resume,hide_index=True,width=3000)  

            if choice == 'May':

                    st.header(choice + ' timesheet')
                    dfNames = pd.read_csv(employee_path,sep=';')
                    names = dfNames['Name']

                    selectedEmployee = st.selectbox('Select the employee',names) # selecionando o funcionário desejado pelo label
                    rowIndex = dfNames.index[dfNames['Name'] == selectedEmployee].tolist()# retornando uma lista com o índice e o nome do funcionário selecionado
                    
                    try:
                        employeeIndex = rowIndex[0] # índice numérico do funcionário selecionado
                    except:
                        st.warning('No registered employees',icon="⚠️")
                        st.stop()
                    
                    # ------- lendo e salvando em variaveis os presets anteriores dos registros do banco de dados ------- #
                    form05 = st.form(key = '05',border=False)
                    with(form05):

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

                        df1b = pd.read_excel(xlsb, 'January')
                        df2b = pd.read_excel(xlsb, 'February')
                        df3b = pd.read_excel(xlsb, 'March')
                        df4b = pd.read_excel(xlsb, 'April')
                        df5b = pd.read_excel(xlsb, 'May')
                        df6b = pd.read_excel(xlsb, 'June')
                        df7b = pd.read_excel(xlsb, 'July')
                        df8b = pd.read_excel(xlsb, 'August')
                        df9b = pd.read_excel(xlsb, 'Setember')
                        df10b = pd.read_excel(xlsb, 'October')
                        df11b = pd.read_excel(xlsb, 'November')
                        df12b = pd.read_excel(xlsb, 'December')    
                    
                        df_edited = dateEditor(df5)
                                                        
                        resume = resumeDfCreate()

                        totalNormalTime = hourCalculator(9,df_edited) # coluna de horas totais
                        totalExtraTime = hourCalculator(8,df_edited) # coluna de horas extras

                        daily_rate_local = dfNames.loc[0,'Daily rate'] 
                        regular_hours_local = dfNames.loc[0,'Regular hours']

                        resume.loc[0,'Name'] = df_edited.loc[0,'Name']
                        resume.loc[0,'Month'] = choice
                        resume.loc[0,'Designation'] =  dfNames.loc[0,'Designation'] 
                        resume.loc[0,'Regular hours'] = regular_hours_local 
                        resume.loc[0,'Total hours worked'] = hourToMinute(totalNormalTime) 
                        resume.loc[0,'Daily rate'] = daily_rate_local
                        
                        payablePerMinute = (daily_rate_local / (regular_hours_local*60))*totalNormalTime # calculo do valor a ser recebido por todos os minutos trabalhados no mes

                        resume.loc[0,'Total Payable'] = payablePerMinute
                        
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
                        
                        with pd.ExcelWriter(joined_path) as writer: # salvando as mudancas somente do mes requerido no banco de dados principal
                            df1.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            df2.to_excel(writer, sheet_name='February', index=False)
                            df3.to_excel(writer, sheet_name='March', index=False)
                            df4.to_excel(writer, sheet_name='April', index=False)
                            df_edited.to_excel(writer, sheet_name='May', index=False)
                            df6.to_excel(writer, sheet_name='June', index=False)
                            df7.to_excel(writer, sheet_name='July', index=False)
                            df8.to_excel(writer, sheet_name='August', index=False)
                            df9.to_excel(writer, sheet_name='Setember', index=False)
                            df10.to_excel(writer, sheet_name='October', index=False)
                            df11.to_excel(writer, sheet_name='November', index=False)
                            df12.to_excel(writer, sheet_name='December', index=False)
                            
                        with pd.ExcelWriter(joined_pathb) as writer: # salvando as mudancas somente do mes requerido no banco de dados do resumo
                            df1b.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            df2b.to_excel(writer, sheet_name='February', index=False)
                            df3b.to_excel(writer, sheet_name='March', index=False)
                            df4b.to_excel(writer, sheet_name='April', index=False)
                            resume.to_excel(writer, sheet_name='May', index=False)
                            df6b.to_excel(writer, sheet_name='June', index=False)
                            df7b.to_excel(writer, sheet_name='July', index=False)
                            df8b.to_excel(writer, sheet_name='August', index=False)
                            df9b.to_excel(writer, sheet_name='Setember', index=False)
                            df10b.to_excel(writer, sheet_name='October', index=False)
                            df11b.to_excel(writer, sheet_name='November', index=False)
                            df12b.to_excel(writer, sheet_name='December', index=False)

                    submitted = form05.form_submit_button("Submit")     
                    if submitted:
                        st.rerun() 

                    st.header('Hours Resume')
                    st.write('All hours worked with all other hours within')
                    st.dataframe(resume,hide_index=True,width=3000)  

            if choice == 'June':

                    st.header(choice + ' timesheet')
                    dfNames = pd.read_csv(employee_path,sep=';')
                    names = dfNames['Name']

                    selectedEmployee = st.selectbox('Select the employee',names) # selecionando o funcionário desejado pelo label
                    rowIndex = dfNames.index[dfNames['Name'] == selectedEmployee].tolist()# retornando uma lista com o índice e o nome do funcionário selecionado
                    
                    try:
                        employeeIndex = rowIndex[0] # índice numérico do funcionário selecionado
                    except:
                        st.warning('No registered employees',icon="⚠️")
                        st.stop()
                    
                    # ------- lendo e salvando em variaveis os presets anteriores dos registros do banco de dados ------- #
                    form06 = st.form(key = '06',border=False)
                    with(form06):

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

                        df1b = pd.read_excel(xlsb, 'January')
                        df2b = pd.read_excel(xlsb, 'February')
                        df3b = pd.read_excel(xlsb, 'March')
                        df4b = pd.read_excel(xlsb, 'April')
                        df5b = pd.read_excel(xlsb, 'May')
                        df6b = pd.read_excel(xlsb, 'June')
                        df7b = pd.read_excel(xlsb, 'July')
                        df8b = pd.read_excel(xlsb, 'August')
                        df9b = pd.read_excel(xlsb, 'Setember')
                        df10b = pd.read_excel(xlsb, 'October')
                        df11b = pd.read_excel(xlsb, 'November')
                        df12b = pd.read_excel(xlsb, 'December')    
                    
                        df_edited = dateEditor(df6)
                                                        
                        resume = resumeDfCreate()

                        totalNormalTime = hourCalculator(9,df_edited) # coluna de horas totais
                        totalExtraTime = hourCalculator(8,df_edited) # coluna de horas extras

                        daily_rate_local = dfNames.loc[0,'Daily rate'] 
                        regular_hours_local = dfNames.loc[0,'Regular hours']

                        resume.loc[0,'Name'] = df_edited.loc[0,'Name']
                        resume.loc[0,'Month'] = choice
                        resume.loc[0,'Designation'] =  dfNames.loc[0,'Designation'] 
                        resume.loc[0,'Regular hours'] = regular_hours_local 
                        resume.loc[0,'Total hours worked'] = hourToMinute(totalNormalTime) 
                        resume.loc[0,'Daily rate'] = daily_rate_local
                        
                        payablePerMinute = (daily_rate_local / (regular_hours_local*60))*totalNormalTime # calculo do valor a ser recebido por todos os minutos trabalhados no mes

                        resume.loc[0,'Total Payable'] = payablePerMinute
                        
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
                        
                        with pd.ExcelWriter(joined_path) as writer: # salvando as mudancas somente do mes requerido no banco de dados principal
                            df1.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            df2.to_excel(writer, sheet_name='February', index=False)
                            df3.to_excel(writer, sheet_name='March', index=False)
                            df4.to_excel(writer, sheet_name='April', index=False)
                            df5.to_excel(writer, sheet_name='May', index=False)
                            df_edited.to_excel(writer, sheet_name='June', index=False)
                            df7.to_excel(writer, sheet_name='July', index=False)
                            df8.to_excel(writer, sheet_name='August', index=False)
                            df9.to_excel(writer, sheet_name='Setember', index=False)
                            df10.to_excel(writer, sheet_name='October', index=False)
                            df11.to_excel(writer, sheet_name='November', index=False)
                            df12.to_excel(writer, sheet_name='December', index=False)
                            
                        with pd.ExcelWriter(joined_pathb) as writer: # salvando as mudancas somente do mes requerido no banco de dados do resumo
                            df1b.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            df2b.to_excel(writer, sheet_name='February', index=False)
                            df3b.to_excel(writer, sheet_name='March', index=False)
                            df4b.to_excel(writer, sheet_name='April', index=False)
                            df5b.to_excel(writer, sheet_name='May', index=False)
                            resume.to_excel(writer, sheet_name='June', index=False)
                            df7b.to_excel(writer, sheet_name='July', index=False)
                            df8b.to_excel(writer, sheet_name='August', index=False)
                            df9b.to_excel(writer, sheet_name='Setember', index=False)
                            df10b.to_excel(writer, sheet_name='October', index=False)
                            df11b.to_excel(writer, sheet_name='November', index=False)
                            df12b.to_excel(writer, sheet_name='December', index=False)

                    submitted = form06.form_submit_button("Submit")     
                    if submitted:
                        st.rerun() 

                    st.header('Hours Resume')
                    st.write('All hours worked with all other hours within')
                    st.dataframe(resume,hide_index=True,width=3000)  

            if choice == 'July':

                    st.header(choice + ' timesheet')
                    dfNames = pd.read_csv(employee_path,sep=';')
                    names = dfNames['Name']

                    selectedEmployee = st.selectbox('Select the employee',names) # selecionando o funcionário desejado pelo label
                    rowIndex = dfNames.index[dfNames['Name'] == selectedEmployee].tolist()# retornando uma lista com o índice e o nome do funcionário selecionado
                    
                    try:
                        employeeIndex = rowIndex[0] # índice numérico do funcionário selecionado
                    except:
                        st.warning('No registered employees',icon="⚠️")
                        st.stop()
                    
                    # ------- lendo e salvando em variaveis os presets anteriores dos registros do banco de dados ------- #
                    form07 = st.form(key = '07',border=False)
                    with(form07):

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

                        df1b = pd.read_excel(xlsb, 'January')
                        df2b = pd.read_excel(xlsb, 'February')
                        df3b = pd.read_excel(xlsb, 'March')
                        df4b = pd.read_excel(xlsb, 'April')
                        df5b = pd.read_excel(xlsb, 'May')
                        df6b = pd.read_excel(xlsb, 'June')
                        df7b = pd.read_excel(xlsb, 'July')
                        df8b = pd.read_excel(xlsb, 'August')
                        df9b = pd.read_excel(xlsb, 'Setember')
                        df10b = pd.read_excel(xlsb, 'October')
                        df11b = pd.read_excel(xlsb, 'November')
                        df12b = pd.read_excel(xlsb, 'December')    
                    
                        df_edited = dateEditor(df7)
                                                        
                        resume = resumeDfCreate()

                        totalNormalTime = hourCalculator(9,df_edited) # coluna de horas totais
                        totalExtraTime = hourCalculator(8,df_edited) # coluna de horas extras

                        daily_rate_local = dfNames.loc[0,'Daily rate'] 
                        regular_hours_local = dfNames.loc[0,'Regular hours']

                        resume.loc[0,'Name'] = df_edited.loc[0,'Name']
                        resume.loc[0,'Month'] = choice
                        resume.loc[0,'Designation'] =  dfNames.loc[0,'Designation'] 
                        resume.loc[0,'Regular hours'] = regular_hours_local 
                        resume.loc[0,'Total hours worked'] = hourToMinute(totalNormalTime) 
                        resume.loc[0,'Daily rate'] = daily_rate_local
                        
                        payablePerMinute = (daily_rate_local / (regular_hours_local*60))*totalNormalTime # calculo do valor a ser recebido por todos os minutos trabalhados no mes

                        resume.loc[0,'Total Payable'] = payablePerMinute
                        
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
                        
                        with pd.ExcelWriter(joined_path) as writer: # salvando as mudancas somente do mes requerido no banco de dados principal
                            df1.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            df2.to_excel(writer, sheet_name='February', index=False)
                            df3.to_excel(writer, sheet_name='March', index=False)
                            df4.to_excel(writer, sheet_name='April', index=False)
                            df5.to_excel(writer, sheet_name='May', index=False)
                            df6.to_excel(writer, sheet_name='June', index=False)
                            df_edited.to_excel(writer, sheet_name='July', index=False)
                            df8.to_excel(writer, sheet_name='August', index=False)
                            df9.to_excel(writer, sheet_name='Setember', index=False)
                            df10.to_excel(writer, sheet_name='October', index=False)
                            df11.to_excel(writer, sheet_name='November', index=False)
                            df12.to_excel(writer, sheet_name='December', index=False)
                            
                        with pd.ExcelWriter(joined_pathb) as writer: # salvando as mudancas somente do mes requerido no banco de dados do resumo
                            df1b.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            df2b.to_excel(writer, sheet_name='February', index=False)
                            df3b.to_excel(writer, sheet_name='March', index=False)
                            df4b.to_excel(writer, sheet_name='April', index=False)
                            df5b.to_excel(writer, sheet_name='May', index=False)
                            df6b.to_excel(writer, sheet_name='June', index=False)
                            resume.to_excel(writer, sheet_name='July', index=False)
                            df8b.to_excel(writer, sheet_name='August', index=False)
                            df9b.to_excel(writer, sheet_name='Setember', index=False)
                            df10b.to_excel(writer, sheet_name='October', index=False)
                            df11b.to_excel(writer, sheet_name='November', index=False)
                            df12b.to_excel(writer, sheet_name='December', index=False)

                    submitted = form07.form_submit_button("Submit")     
                    if submitted:
                        st.rerun() 

                    st.header('Hours Resume')
                    st.write('All hours worked with all other hours within')
                    st.dataframe(resume,hide_index=True,width=3000)  

            if choice == 'August':

                    st.header(choice + ' timesheet')
                    dfNames = pd.read_csv(employee_path,sep=';')
                    names = dfNames['Name']

                    selectedEmployee = st.selectbox('Select the employee',names) # selecionando o funcionário desejado pelo label
                    rowIndex = dfNames.index[dfNames['Name'] == selectedEmployee].tolist()# retornando uma lista com o índice e o nome do funcionário selecionado
                    
                    try:
                        employeeIndex = rowIndex[0] # índice numérico do funcionário selecionado
                    except:
                        st.warning('No registered employees',icon="⚠️")
                        st.stop()
                    
                    # ------- lendo e salvando em variaveis os presets anteriores dos registros do banco de dados ------- #
                    form08 = st.form(key = '08',border=False)
                    with(form08):

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

                        df1b = pd.read_excel(xlsb, 'January')
                        df2b = pd.read_excel(xlsb, 'February')
                        df3b = pd.read_excel(xlsb, 'March')
                        df4b = pd.read_excel(xlsb, 'April')
                        df5b = pd.read_excel(xlsb, 'May')
                        df6b = pd.read_excel(xlsb, 'June')
                        df7b = pd.read_excel(xlsb, 'July')
                        df8b = pd.read_excel(xlsb, 'August')
                        df9b = pd.read_excel(xlsb, 'Setember')
                        df10b = pd.read_excel(xlsb, 'October')
                        df11b = pd.read_excel(xlsb, 'November')
                        df12b = pd.read_excel(xlsb, 'December')    
                    
                        df_edited = dateEditor(df8)
                                                        
                        resume = resumeDfCreate()

                        totalNormalTime = hourCalculator(9,df_edited) # coluna de horas totais
                        totalExtraTime = hourCalculator(8,df_edited) # coluna de horas extras

                        daily_rate_local = dfNames.loc[0,'Daily rate'] 
                        regular_hours_local = dfNames.loc[0,'Regular hours']

                        resume.loc[0,'Name'] = df_edited.loc[0,'Name']
                        resume.loc[0,'Month'] = choice
                        resume.loc[0,'Designation'] =  dfNames.loc[0,'Designation'] 
                        resume.loc[0,'Regular hours'] = regular_hours_local 
                        resume.loc[0,'Total hours worked'] = hourToMinute(totalNormalTime) 
                        resume.loc[0,'Daily rate'] = daily_rate_local
                        
                        payablePerMinute = (daily_rate_local / (regular_hours_local*60))*totalNormalTime # calculo do valor a ser recebido por todos os minutos trabalhados no mes

                        resume.loc[0,'Total Payable'] = payablePerMinute
                        
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
                        
                        with pd.ExcelWriter(joined_path) as writer: # salvando as mudancas somente do mes requerido no banco de dados principal
                            df1.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            df2.to_excel(writer, sheet_name='February', index=False)
                            df3.to_excel(writer, sheet_name='March', index=False)
                            df4.to_excel(writer, sheet_name='April', index=False)
                            df5.to_excel(writer, sheet_name='May', index=False)
                            df6.to_excel(writer, sheet_name='June', index=False)
                            df7.to_excel(writer, sheet_name='July', index=False)
                            df_edited.to_excel(writer, sheet_name='August', index=False)
                            df9.to_excel(writer, sheet_name='Setember', index=False)
                            df10.to_excel(writer, sheet_name='October', index=False)
                            df11.to_excel(writer, sheet_name='November', index=False)
                            df12.to_excel(writer, sheet_name='December', index=False)
                            
                        with pd.ExcelWriter(joined_pathb) as writer: # salvando as mudancas somente do mes requerido no banco de dados do resumo
                            df1b.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            df2b.to_excel(writer, sheet_name='February', index=False)
                            df3b.to_excel(writer, sheet_name='March', index=False)
                            df4b.to_excel(writer, sheet_name='April', index=False)
                            df5b.to_excel(writer, sheet_name='May', index=False)
                            df6b.to_excel(writer, sheet_name='June', index=False)
                            df7b.to_excel(writer, sheet_name='July', index=False)
                            resume.to_excel(writer, sheet_name='August', index=False)
                            df9b.to_excel(writer, sheet_name='Setember', index=False)
                            df10b.to_excel(writer, sheet_name='October', index=False)
                            df11b.to_excel(writer, sheet_name='November', index=False)
                            df12b.to_excel(writer, sheet_name='December', index=False)

                    submitted = form08.form_submit_button("Submit")     
                    if submitted:
                        st.rerun() 

                    st.header('Hours Resume')
                    st.write('All hours worked with all other hours within')
                    st.dataframe(resume,hide_index=True,width=3000)               

            if choice == 'Setember':

                    st.header(choice + ' timesheet')
                    dfNames = pd.read_csv(employee_path,sep=';')
                    names = dfNames['Name']

                    selectedEmployee = st.selectbox('Select the employee',names) # selecionando o funcionário desejado pelo label
                    rowIndex = dfNames.index[dfNames['Name'] == selectedEmployee].tolist()# retornando uma lista com o índice e o nome do funcionário selecionado
                    
                    try:
                        employeeIndex = rowIndex[0] # índice numérico do funcionário selecionado
                    except:
                        st.warning('No registered employees',icon="⚠️")
                        st.stop()
                    
                    # ------- lendo e salvando em variaveis os presets anteriores dos registros do banco de dados ------- #
                    form09 = st.form(key = '09',border=False)
                    with(form09):

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

                        df1b = pd.read_excel(xlsb, 'January')
                        df2b = pd.read_excel(xlsb, 'February')
                        df3b = pd.read_excel(xlsb, 'March')
                        df4b = pd.read_excel(xlsb, 'April')
                        df5b = pd.read_excel(xlsb, 'May')
                        df6b = pd.read_excel(xlsb, 'June')
                        df7b = pd.read_excel(xlsb, 'July')
                        df8b = pd.read_excel(xlsb, 'August')
                        df9b = pd.read_excel(xlsb, 'Setember')
                        df10b = pd.read_excel(xlsb, 'October')
                        df11b = pd.read_excel(xlsb, 'November')
                        df12b = pd.read_excel(xlsb, 'December')    
                    
                        df_edited = dateEditor(df9)
                                                        
                        resume = resumeDfCreate()

                        totalNormalTime = hourCalculator(9,df_edited) # coluna de horas totais
                        totalExtraTime = hourCalculator(8,df_edited) # coluna de horas extras

                        daily_rate_local = dfNames.loc[0,'Daily rate'] 
                        regular_hours_local = dfNames.loc[0,'Regular hours']

                        resume.loc[0,'Name'] = df_edited.loc[0,'Name']
                        resume.loc[0,'Month'] = choice
                        resume.loc[0,'Designation'] =  dfNames.loc[0,'Designation'] 
                        resume.loc[0,'Regular hours'] = regular_hours_local 
                        resume.loc[0,'Total hours worked'] = hourToMinute(totalNormalTime) 
                        resume.loc[0,'Daily rate'] = daily_rate_local
                        
                        payablePerMinute = (daily_rate_local / (regular_hours_local*60))*totalNormalTime # calculo do valor a ser recebido por todos os minutos trabalhados no mes

                        resume.loc[0,'Total Payable'] = payablePerMinute
                        
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
                        
                        with pd.ExcelWriter(joined_path) as writer: # salvando as mudancas somente do mes requerido no banco de dados principal
                            df1.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            df2.to_excel(writer, sheet_name='February', index=False)
                            df3.to_excel(writer, sheet_name='March', index=False)
                            df4.to_excel(writer, sheet_name='April', index=False)
                            df5.to_excel(writer, sheet_name='May', index=False)
                            df6.to_excel(writer, sheet_name='June', index=False)
                            df7.to_excel(writer, sheet_name='July', index=False)
                            df8.to_excel(writer, sheet_name='August', index=False)
                            df_edited.to_excel(writer, sheet_name='Setember', index=False)
                            df10.to_excel(writer, sheet_name='October', index=False)
                            df11.to_excel(writer, sheet_name='November', index=False)
                            df12.to_excel(writer, sheet_name='December', index=False)
                            
                        with pd.ExcelWriter(joined_pathb) as writer: # salvando as mudancas somente do mes requerido no banco de dados do resumo
                            df1b.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            df2b.to_excel(writer, sheet_name='February', index=False)
                            df3b.to_excel(writer, sheet_name='March', index=False)
                            df4b.to_excel(writer, sheet_name='April', index=False)
                            df5b.to_excel(writer, sheet_name='May', index=False)
                            df6b.to_excel(writer, sheet_name='June', index=False)
                            df7b.to_excel(writer, sheet_name='July', index=False)
                            df8b.to_excel(writer, sheet_name='August', index=False)
                            resume.to_excel(writer, sheet_name='Setember', index=False)
                            df10b.to_excel(writer, sheet_name='October', index=False)
                            df11b.to_excel(writer, sheet_name='November', index=False)
                            df12b.to_excel(writer, sheet_name='December', index=False)

                    submitted = form09.form_submit_button("Submit")     
                    if submitted:
                        st.rerun() 

                    st.header('Hours Resume')
                    st.write('All hours worked with all other hours within')
                    st.dataframe(resume,hide_index=True,width=3000)  

            if choice == 'October':

                    st.header(choice + ' timesheet')
                    dfNames = pd.read_csv(employee_path,sep=';')
                    names = dfNames['Name']

                    selectedEmployee = st.selectbox('Select the employee',names) # selecionando o funcionário desejado pelo label
                    rowIndex = dfNames.index[dfNames['Name'] == selectedEmployee].tolist()# retornando uma lista com o índice e o nome do funcionário selecionado
                    
                    try:
                        employeeIndex = rowIndex[0] # índice numérico do funcionário selecionado
                    except:
                        st.warning('No registered employees',icon="⚠️")
                        st.stop()
                    
                    # ------- lendo e salvando em variaveis os presets anteriores dos registros do banco de dados ------- #
                    form10 = st.form(key = '10',border=False)
                    with(form10):

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

                        df1b = pd.read_excel(xlsb, 'January')
                        df2b = pd.read_excel(xlsb, 'February')
                        df3b = pd.read_excel(xlsb, 'March')
                        df4b = pd.read_excel(xlsb, 'April')
                        df5b = pd.read_excel(xlsb, 'May')
                        df6b = pd.read_excel(xlsb, 'June')
                        df7b = pd.read_excel(xlsb, 'July')
                        df8b = pd.read_excel(xlsb, 'August')
                        df9b = pd.read_excel(xlsb, 'Setember')
                        df10b = pd.read_excel(xlsb, 'October')
                        df11b = pd.read_excel(xlsb, 'November')
                        df12b = pd.read_excel(xlsb, 'December')    
                    
                        df_edited = dateEditor(df10)
                                                        
                        resume = resumeDfCreate()

                        totalNormalTime = hourCalculator(9,df_edited) # coluna de horas totais
                        totalExtraTime = hourCalculator(8,df_edited) # coluna de horas extras

                        daily_rate_local = dfNames.loc[0,'Daily rate'] 
                        regular_hours_local = dfNames.loc[0,'Regular hours']

                        resume.loc[0,'Name'] = df_edited.loc[0,'Name']
                        resume.loc[0,'Month'] = choice
                        resume.loc[0,'Designation'] =  dfNames.loc[0,'Designation'] 
                        resume.loc[0,'Regular hours'] = regular_hours_local 
                        resume.loc[0,'Total hours worked'] = hourToMinute(totalNormalTime) 
                        resume.loc[0,'Daily rate'] = daily_rate_local
                        
                        payablePerMinute = (daily_rate_local / (regular_hours_local*60))*totalNormalTime # calculo do valor a ser recebido por todos os minutos trabalhados no mes

                        resume.loc[0,'Total Payable'] = payablePerMinute
                        
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
                        
                        with pd.ExcelWriter(joined_path) as writer: # salvando as mudancas somente do mes requerido no banco de dados principal
                            df1.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            df2.to_excel(writer, sheet_name='February', index=False)
                            df3.to_excel(writer, sheet_name='March', index=False)
                            df4.to_excel(writer, sheet_name='April', index=False)
                            df5.to_excel(writer, sheet_name='May', index=False)
                            df6.to_excel(writer, sheet_name='June', index=False)
                            df7.to_excel(writer, sheet_name='July', index=False)
                            df8.to_excel(writer, sheet_name='August', index=False)
                            df9.to_excel(writer, sheet_name='Setember', index=False)
                            df_edited.to_excel(writer, sheet_name='October', index=False)
                            df11.to_excel(writer, sheet_name='November', index=False)
                            df12.to_excel(writer, sheet_name='December', index=False)
                            
                        with pd.ExcelWriter(joined_pathb) as writer: # salvando as mudancas somente do mes requerido no banco de dados do resumo
                            df1b.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            df2b.to_excel(writer, sheet_name='February', index=False)
                            df3b.to_excel(writer, sheet_name='March', index=False)
                            df4b.to_excel(writer, sheet_name='April', index=False)
                            df5b.to_excel(writer, sheet_name='May', index=False)
                            df6b.to_excel(writer, sheet_name='June', index=False)
                            df7b.to_excel(writer, sheet_name='July', index=False)
                            df8b.to_excel(writer, sheet_name='August', index=False)
                            df9b.to_excel(writer, sheet_name='Setember', index=False)
                            resume.to_excel(writer, sheet_name='October', index=False)
                            df11b.to_excel(writer, sheet_name='November', index=False)
                            df12b.to_excel(writer, sheet_name='December', index=False)

                    submitted = form10.form_submit_button("Submit")     
                    if submitted:
                        st.rerun() 

                    st.header('Hours Resume')
                    st.write('All hours worked with all other hours within')
                    st.dataframe(resume,hide_index=True,width=3000)  

            if choice == 'November':

                    st.header(choice + ' timesheet')
                    dfNames = pd.read_csv(employee_path,sep=';')
                    names = dfNames['Name']

                    selectedEmployee = st.selectbox('Select the employee',names) # selecionando o funcionário desejado pelo label
                    rowIndex = dfNames.index[dfNames['Name'] == selectedEmployee].tolist()# retornando uma lista com o índice e o nome do funcionário selecionado
                    
                    try:
                        employeeIndex = rowIndex[0] # índice numérico do funcionário selecionado
                    except:
                        st.warning('No registered employees',icon="⚠️")
                        st.stop()
                    
                    # ------- lendo e salvando em variaveis os presets anteriores dos registros do banco de dados ------- #
                    form11 = st.form(key = '11',border=False)
                    with(form11):

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

                        df1b = pd.read_excel(xlsb, 'January')
                        df2b = pd.read_excel(xlsb, 'February')
                        df3b = pd.read_excel(xlsb, 'March')
                        df4b = pd.read_excel(xlsb, 'April')
                        df5b = pd.read_excel(xlsb, 'May')
                        df6b = pd.read_excel(xlsb, 'June')
                        df7b = pd.read_excel(xlsb, 'July')
                        df8b = pd.read_excel(xlsb, 'August')
                        df9b = pd.read_excel(xlsb, 'Setember')
                        df10b = pd.read_excel(xlsb, 'October')
                        df11b = pd.read_excel(xlsb, 'November')
                        df12b = pd.read_excel(xlsb, 'December')    
                    
                        df_edited = dateEditor(df11)
                                                        
                        resume = resumeDfCreate()

                        totalNormalTime = hourCalculator(9,df_edited) # coluna de horas totais
                        totalExtraTime = hourCalculator(8,df_edited) # coluna de horas extras

                        daily_rate_local = dfNames.loc[0,'Daily rate'] 
                        regular_hours_local = dfNames.loc[0,'Regular hours']

                        resume.loc[0,'Name'] = df_edited.loc[0,'Name']
                        resume.loc[0,'Month'] = choice
                        resume.loc[0,'Designation'] =  dfNames.loc[0,'Designation'] 
                        resume.loc[0,'Regular hours'] = regular_hours_local 
                        resume.loc[0,'Total hours worked'] = hourToMinute(totalNormalTime) 
                        resume.loc[0,'Daily rate'] = daily_rate_local
                        
                        payablePerMinute = (daily_rate_local / (regular_hours_local*60))*totalNormalTime # calculo do valor a ser recebido por todos os minutos trabalhados no mes

                        resume.loc[0,'Total Payable'] = payablePerMinute
                        
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
                        
                        with pd.ExcelWriter(joined_path) as writer: # salvando as mudancas somente do mes requerido no banco de dados principal
                            df1.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            df2.to_excel(writer, sheet_name='February', index=False)
                            df3.to_excel(writer, sheet_name='March', index=False)
                            df4.to_excel(writer, sheet_name='April', index=False)
                            df5.to_excel(writer, sheet_name='May', index=False)
                            df6.to_excel(writer, sheet_name='June', index=False)
                            df7.to_excel(writer, sheet_name='July', index=False)
                            df8.to_excel(writer, sheet_name='August', index=False)
                            df9.to_excel(writer, sheet_name='Setember', index=False)
                            df10.to_excel(writer, sheet_name='October', index=False)
                            df_edited.to_excel(writer, sheet_name='November', index=False)
                            df12.to_excel(writer, sheet_name='December', index=False)
                            
                        with pd.ExcelWriter(joined_pathb) as writer: # salvando as mudancas somente do mes requerido no banco de dados do resumo
                            df1b.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            df2b.to_excel(writer, sheet_name='February', index=False)
                            df3b.to_excel(writer, sheet_name='March', index=False)
                            df4b.to_excel(writer, sheet_name='April', index=False)
                            df5b.to_excel(writer, sheet_name='May', index=False)
                            df6b.to_excel(writer, sheet_name='June', index=False)
                            df7b.to_excel(writer, sheet_name='July', index=False)
                            df8b.to_excel(writer, sheet_name='August', index=False)
                            df9b.to_excel(writer, sheet_name='Setember', index=False)
                            df10b.to_excel(writer, sheet_name='October', index=False)
                            resume.to_excel(writer, sheet_name='November', index=False)
                            df12b.to_excel(writer, sheet_name='December', index=False)

                    submitted = form11.form_submit_button("Submit")     
                    if submitted:
                        st.rerun() 

                    st.header('Hours Resume')
                    st.write('All hours worked with all other hours within')
                    st.dataframe(resume,hide_index=True,width=3000)  

            if choice == 'December':

                    st.header(choice + ' timesheet')
                    dfNames = pd.read_csv(employee_path,sep=';')
                    names = dfNames['Name']

                    selectedEmployee = st.selectbox('Select the employee',names) # selecionando o funcionário desejado pelo label
                    rowIndex = dfNames.index[dfNames['Name'] == selectedEmployee].tolist()# retornando uma lista com o índice e o nome do funcionário selecionado
                    
                    try:
                        employeeIndex = rowIndex[0] # índice numérico do funcionário selecionado
                    except:
                        st.warning('No registered employees',icon="⚠️")
                        st.stop()
                    
                    # ------- lendo e salvando em variaveis os presets anteriores dos registros do banco de dados ------- #
                    form12 = st.form(key = '12',border=False)
                    with(form12):

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

                        df1b = pd.read_excel(xlsb, 'January')
                        df2b = pd.read_excel(xlsb, 'February')
                        df3b = pd.read_excel(xlsb, 'March')
                        df4b = pd.read_excel(xlsb, 'April')
                        df5b = pd.read_excel(xlsb, 'May')
                        df6b = pd.read_excel(xlsb, 'June')
                        df7b = pd.read_excel(xlsb, 'July')
                        df8b = pd.read_excel(xlsb, 'August')
                        df9b = pd.read_excel(xlsb, 'Setember')
                        df10b = pd.read_excel(xlsb, 'October')
                        df11b = pd.read_excel(xlsb, 'November')
                        df12b = pd.read_excel(xlsb, 'December')    
                    
                        df_edited = dateEditor(df12)
                                                        
                        resume = resumeDfCreate()

                        totalNormalTime = hourCalculator(9,df_edited) # coluna de horas totais
                        totalExtraTime = hourCalculator(8,df_edited) # coluna de horas extras

                        daily_rate_local = dfNames.loc[0,'Daily rate'] 
                        regular_hours_local = dfNames.loc[0,'Regular hours']

                        resume.loc[0,'Name'] = df_edited.loc[0,'Name']
                        resume.loc[0,'Month'] = choice
                        resume.loc[0,'Designation'] =  dfNames.loc[0,'Designation'] 
                        resume.loc[0,'Regular hours'] = regular_hours_local 
                        resume.loc[0,'Total hours worked'] = hourToMinute(totalNormalTime) 
                        resume.loc[0,'Daily rate'] = daily_rate_local
                        
                        payablePerMinute = (daily_rate_local / (regular_hours_local*60))*totalNormalTime # calculo do valor a ser recebido por todos os minutos trabalhados no mes

                        resume.loc[0,'Total Payable'] = payablePerMinute
                        
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
                        
                        with pd.ExcelWriter(joined_path) as writer: # salvando as mudancas somente do mes requerido no banco de dados principal
                            df1.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            df2.to_excel(writer, sheet_name='February', index=False)
                            df3.to_excel(writer, sheet_name='March', index=False)
                            df4.to_excel(writer, sheet_name='April', index=False)
                            df5.to_excel(writer, sheet_name='May', index=False)
                            df6.to_excel(writer, sheet_name='June', index=False)
                            df7.to_excel(writer, sheet_name='July', index=False)
                            df8.to_excel(writer, sheet_name='August', index=False)
                            df9.to_excel(writer, sheet_name='Setember', index=False)
                            df10.to_excel(writer, sheet_name='October', index=False)
                            df11.to_excel(writer, sheet_name='November', index=False)
                            df_edited.to_excel(writer, sheet_name='December', index=False)
                            
                        with pd.ExcelWriter(joined_pathb) as writer: # salvando as mudancas somente do mes requerido no banco de dados do resumo
                            df1b.to_excel(writer, sheet_name='January', index=False) # ----------- VARIA CONFORME O MES ----------- #
                            df2b.to_excel(writer, sheet_name='February', index=False)
                            df3b.to_excel(writer, sheet_name='March', index=False)
                            df4b.to_excel(writer, sheet_name='April', index=False)
                            df5b.to_excel(writer, sheet_name='May', index=False)
                            df6b.to_excel(writer, sheet_name='June', index=False)
                            df7b.to_excel(writer, sheet_name='July', index=False)
                            df8b.to_excel(writer, sheet_name='August', index=False)
                            df9b.to_excel(writer, sheet_name='Setember', index=False)
                            df10b.to_excel(writer, sheet_name='October', index=False)
                            df11b.to_excel(writer, sheet_name='November', index=False)
                            resume.to_excel(writer, sheet_name='December', index=False)

                    submitted = form12.form_submit_button("Submit")     
                    if submitted:
                        st.rerun() 

                    st.header('Hours Resume')
                    st.write('All hours worked with all other hours within')
                    st.dataframe(resume,hide_index=True,width=3000)                  

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
