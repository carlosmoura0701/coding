import pickle
from pathlib import Path

import streamlit_authenticator as stauth

# nao esquecer de atualizar a lista de usuarios no _main.py

names = ['Carlos Moura','Sheila Santana','Judas Escariodes']
usernames = ['carlosmoura','sheilasantanta','judas']
passwords = ['','','']

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open('wb') as file:
    pickle.dump(hashed_passwords,file)

    