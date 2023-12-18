import pickle
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth

st.set_page_config(page_title="Hours Manager",layout="centered")

# user authentication

names = ["Carlos Moura","Sheila Santana"]
usernames = ["carlosmoura","sheilasantanta"]

# passwords load

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open('rb') as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "login_cookie","adqecd", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login","main")


if authentication_status == False:
    st.error("Username/password is incorrect")
if authentication_status == None:
    st.warning("Please enter your user name and password")    
if authentication_status:

    authenticator.logout("Logout","sidebar")
    st.sidebar.title(f"Welcome {name}")

    add_selectbox = st.sidebar.selectbox("O que você gostaria de fazer?",("Criar Novo Funcionario", "Pesquisar Funcionario","Visualizar todos"),)

    with st.container():
        st.subheader("Funcionários cadastrados")
        st.write("Relação de funcionários, salários e horas trabalhadas")

        df = pd.read_csv(r"C:\Users\889612123\Documents\GitHub\coding\employees\csv\pay.csv",sep=";",decimal=",")
        df

    with st.container():
        st.subheader("Rendimento por Hectar")
        st.write("Rendimento por hectar / anos")

        df = pd.read_csv(r"C:\Users\889612123\Documents\GitHub\coding\employees\csv\opReport1.csv",sep=";",decimal=",")
        df

    with st.container():
        st.subheader("Chuva")
        st.write("mm de chuva / anos")

        df = pd.read_csv(r"C:\Users\889612123\Documents\GitHub\coding\employees\csv\chuva.csv",sep=";",decimal=",")
        df

        st.write("---")
        dados = pd.read_csv(r"C:\Users\889612123\Documents\GitHub\coding\employees\csv\chuva.csv",sep=";",decimal=",")
        st.area_chart(dados,x="mes",y="total")




#st.write("Teste de [link](https://www.google.com/)")    
      