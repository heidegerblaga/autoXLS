import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Ustawienia autoryzacji OAuth2
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("ścieżka_do_pliku_z_kluczami.json", scope)
client = gspread.authorize(creds)

# Otwórz arkusz Google
sheet = client.open("nazwa_arkusza").sheet1

# Wyświetl dane z arkusza Google na stronie Streamlit
data = sheet.get_all_records()
st.write(data)
