# app_entregas.py
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Captura de pedidos", page_icon="🛒")
st.title("📦 Captura de Pedidos")
st.write("Ingresa los datos de cada venta realizada hoy:")

# Conectar a Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1qoux5KkmNoYXRrw9FOPHJR53Hie9kIUXETBRiQNmvFw/edit").sheet1

# Obtener fecha de hoy
hoy = datetime.now()
dia = str(hoy.day)
fecha_str = hoy.strftime("%Y-%m-%d %H:%M:%S")

# Formulario
with st.form("captura_formulario"):
    nombre_vendedor = st.text_input("👤 Nombre del Vendedor")
    articulo = st.text_input("🛍️ Artículo vendido")
    latitud = st.text_input("📍 Latitud de entrega", help="Ej. 19.6678")
    longitud = st.text_input("📍 Longitud de entrega", help="Ej. -99.1998")
    enviar = st.form_submit_button("Guardar pedido")

    if enviar:
        if articulo and latitud and longitud and nombre_vendedor:
            fila = [dia, nombre_vendedor, articulo, latitud, longitud, fecha_str]
            sheet.append_row(fila)
            st.success("✅ Pedido guardado correctamente en Google Sheets")
        else:
            st.warning("⚠️ Completa todos los campos antes de guardar.")

# Mostrar tabla actual
st.subheader("📋 Pedidos capturados")
datos = sheet.get_all_records()
df = pd.DataFrame(datos)
st.dataframe(df)
