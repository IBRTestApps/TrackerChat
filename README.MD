# IBR Tracker Retrieval-Augmented Chat App

Deze repository bevat programmacode voor een AI-aanvulling ob de _IBR Tracker_ database van het Instituut voor Bouwrecht.

## Belangrijk
- De app verwacht API-toegang tot een *large language model* en een vectordatabase. In dit geval OpenAI GPT en Pinecone. Zonder API-toegang werkt de app _niet_
- Bij lokaal gebruik: start de applicatie via terminal-commando _streamlit run ^bestand^_
- De app is gebouwd om via Streamlit gedraaid te worden, lokaal of via _Streamlit Community Cloud_. In de applicatie wordt gebruik gemaakt van _Streamlit Authenticator_ om gebruikers te authenticeren. Credentials en instelligen voor deze module worden voor test/lokaal gebruik opgeslagen in een YAML-bestand of in TOML-formaat in .streamlit/secrets.toml. Deze bestanden zijn om veiligheidswege niet opgenomen in deze repository. Als je de app lokaal wil gebruiken, gebruik dan één van deze opties, en pas de code aan. Zie https://github.com/mkhorasani/Streamlit-Authenticator/blob/main/README.md
- Bij gebruik via _Streamlit Community Cloud_: Voeg credentials/API-informatie e.d. toe via secrets menu onder *settings* in Streamlit-account.
