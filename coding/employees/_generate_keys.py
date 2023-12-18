import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["Carlos Moura","Sheila Santana"]
usernames = ["carlosmoura","sheilasantanta"]
passwords = ["admin","sheila"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open('wb') as file:
    pickle.dump(hashed_passwords,file)

    