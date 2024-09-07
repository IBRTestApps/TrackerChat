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
if st.session_state["authentication_status"]:
    st.switch_page('pages/TrackerChat.py')
elif st.session_state["authentication_status"] == False:
    st.error('Gebruikersnaam/wachtwoord is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Voer uw gebruikersnaam en wachtwoord in')