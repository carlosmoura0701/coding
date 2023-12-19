import pickle
from pathlib import Path
from streamlit_option_menu import option_menu

import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth

st.set_page_config(page_title="Hours Manager",layout="centered")

# autenticação de usuário

names = ["Carlos Moura","Sheila Santana"]
usernames = ["carlosmoura","sheilasantanta"]

# carregamento de senha

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open('rb') as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "login_cookie","adqecd", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login","main")

# condicionais login

if authentication_status == False:
    st.error("Username/password is incorrect")
if authentication_status == None:
    st.warning("Please enter your user name and password")    
# login == true    
if authentication_status:

    authenticator.logout("Logout","sidebar")
    st.sidebar.title(f"Welcome {name}")

# menu lateral
    with st.sidebar:
        selected = option_menu(
            menu_title=None, #obrigatório ou None
            options=["Resume","New Employee","Rain"]
        )

    if selected == "Resume":
        st.title(f"You have selected {selected}")

        with st.container():
            st.subheader("Funcionários cadastrados")
            st.write("Relação de funcionários, salários e horas trabalhadas")

            df = pd.read_csv("coding/employees/csv/pay.csv",sep=";",decimal=",")
            df

        with st.container():
            st.subheader("Rendimento por Hectar")
            st.write("Rendimento por hectar / anos")

            df = pd.read_csv("coding/employees/csv/opReport1.csv",sep=";",decimal=",")
            df

    if selected == "New Employee":
            st.title(f"You have selected {selected}")

    if selected == "Rain":
            st.title(f"You have selected {selected}")
            with st.container():
                st.subheader("Chuva")
                st.write("mm de chuva / anos")

                df = pd.read_csv("coding/employees/csv/chuva.csv",sep=";",decimal=",")
                df

                st.write("---")
                dados = pd.read_csv("coding/employees/csv/chuva.csv",sep=";",decimal=",")
                st.area_chart(dados,x="mes",y="total")

