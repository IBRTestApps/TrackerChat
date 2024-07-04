import streamlit as st
import streamlit_authenticator as st_auth

# Initialisatie streamlit authenticator
authenticator = st_auth.Authenticate(
    st.secrets["credentials"].to_dict(),
    st.secrets["cookie"]["name"],
    st.secrets["cookie"]["key"],
    st.secrets["cookie"]["expiry_days"],
    st.secrets["preauthorized"])

if st.session_state["authentication_status"] is None:
    st.switch_page('Login.py')
if st.session_state["authentication_status"]:
    authenticator.logout(location='sidebar')

st.title('Informatie')
st.markdown('TrackerChat bevat per 2-7-2024 de volgende bronnen: \n\n'
            '- Handboek Bouwen onder de Omgevingswet\n\n'
            '- Vergunningsvrij Bouwen onder de Omgevingswet\n\n'
            '- Juridisch Handboek Gebiedsontwikkeling\n\n'
            '- Bouwrecht in Kort Bestek\n\n'
            '- Praktijkboek Wet Kwaliteitsborging voor het Bouwen\n\n'
            '- Jaargangen *Tijdschrift voor Bouwrecht van Juni 2024 tot 2020\n\n'
            '- Specifieke uitgaven TBR m.b.t. Wet Kwaliteitsborging voor het Bouwen')
st.markdown('De chatbot zal proberen een antwoord op uw vraag te genereren met de inhoud uit de bovenstaande '
            'publicaties, en zal daarbij de vindplaats van de tekstfragmenten die het heeft gebruikt voor dit antwoord'
            'weergeven. In de huidige situatie is het echter zo dat de applicatie zal verwijzen naar de desbetreffende'
            'publicatie in de Tracker, niet de precieze vindplaats *in* de publicatie. Dit is - tot op zekere hoogte -'
            'mogelijk, maar nog niet geïmplementeerd.')