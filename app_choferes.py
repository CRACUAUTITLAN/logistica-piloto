# app_choferes.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from utils.maps_utils import coordenadas_a_direccion, generar_mapa
from utils.pdf_generator import generar_pdf

st.set_page_config(page_title="Ruta de Entregas", page_icon="🚚")
st.title("📦 Consulta de Ruta por Vehículo")

# Obtener fecha actual para buscar el archivo del día
hoy = datetime.now().date()

vehiculo = st.selectbox("Selecciona tu número de vehículo:", [1, 2, 3, 4])
archivo = f"logistica/vehiculo_{vehiculo}_{hoy}.csv"

if os.path.isfile(archivo):
    df = pd.read_csv(archivo)
    df = df.reset_index(drop=True)

    # Agregar columna con direcciones legibles
    st.subheader("📍 Entregas del día")
    with st.spinner("Obteniendo direcciones..."):
        df["Direccion"] = df.apply(lambda row: coordenadas_a_direccion(row["Latitud"], row["Longitud"]), axis=1)

    df_mostrar = df[["Articulo", "Direccion"]]
    st.dataframe(df_mostrar, use_container_width=True)

    # Botón para ver el mapa
    if st.button("🗺️ Ver mapa de entregas"):
        st.components.v1.html(generar_mapa(df), height=500)

    # Botón para descargar el PDF
    if st.button("📄 Descargar PDF con ruta"):
        ruta_pdf = generar_pdf(df, vehiculo, hoy)
        with open(ruta_pdf, "rb") as file:
            st.download_button(
                label="Descargar ruta en PDF",
                data=file,
                file_name=os.path.basename(ruta_pdf),
                mime="application/pdf"
            )
else:
    st.warning("⚠️ Aún no hay ruta generada para este vehículo el día de hoy.")
