import streamlit as st
import streamlit_authenticator as st_auth

st.title('Login')

authenticator = st_auth.Authenticate(
    st.secrets["credentials"].to_dict(),
    st.secrets["cookie"]["name"],
    st.secrets["cookie"]["key"],
    st.secrets["cookie"]["expiry_days"],
    st.secrets["preauthorized"])

name, authentication_status, username = authenticator.login('main')
if authentication_status:
    st.switch_page('pages/TrackerChat.py')
elif authentication_status is False:
    st.error('Gebruikersnaam/wachtwoord is incorrect')
elif authentication_status is None:
    st.warning('Voer uw gebruikersnaam en wachtwoord in')
