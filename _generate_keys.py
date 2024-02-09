import pickle
from pathlib import Path
import streamlit_authenticator as stauth

# nao esquecer de atualizar a lista de usuarios no _main.py


usernames = ['Carlos Moura','Sheila Santana','Judas Escariodes']
names = ['carlosmoura','sheilasantanta','judas']
passwords = ['admin','admin','admin']

credentials = {"usernames":{}}
        
for uname,name,pwd in zip(usernames,names,passwords):
    user_dict = {"name": name, "password": pwd}
    credentials["usernames"].update({uname: user_dict})

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open('wb') as file:
    pickle.dump(hashed_passwords,file)
