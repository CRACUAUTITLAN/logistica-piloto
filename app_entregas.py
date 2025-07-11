import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 🛠️ Configuración de la página
st.set_page_config(page_title="Captura de pedidos", page_icon="🛒")
st.title("📦 Captura de Pedidos")
st.write("Ingresa los datos de cada venta realizada hoy:")

# 🗓️ Obtener fecha de hoy
hoy = datetime.now()
dia = str(hoy.day)
meses = {
    "january": "enero", "february": "febrero", "march": "marzo", "april": "abril",
    "may": "mayo", "june": "junio", "july": "julio", "august": "agosto",
    "september": "septiembre", "october": "octubre", "november": "noviembre", "december": "diciembre"
}
mes_nombre = meses[hoy.strftime("%B").lower()]
anio = str(hoy.year)

# 📁 Crear ruta del archivo
carpeta_pedidos = "pedidos"
os.makedirs(carpeta_pedidos, exist_ok=True)
archivo_csv = os.path.join(carpeta_pedidos, f"{mes_nombre}_{anio}.csv")

# 📋 Formulario de captura
with st.form("captura_formulario"):
    nombre_vendedor = st.text_input("🧑‍💼 Nombre del Vendedor")
    articulo = st.text_input("🛍️ Artículo vendido")
    latitud = st.text_input("📍 Latitud de entrega", help="Ej. 19.6678")
    longitud = st.text_input("📍 Longitud de entrega", help="Ej. -99.1998")
    enviar = st.form_submit_button("Guardar pedido")

    if enviar:
        if nombre_vendedor and articulo and latitud and longitud:
            nuevo = pd.DataFrame([[dia, nombre_vendedor, articulo, latitud, longitud]],
                                 columns=["Día", "Vendedor", "Artículo", "Latitud", "Longitud"])

            if not os.path.isfile(archivo_csv):
                nuevo.to_csv(archivo_csv, index=False)
            else:
                nuevo.to_csv(archivo_csv, mode="a", index=False, header=False)

            st.success("✅ Pedido guardado correctamente")
        else:
            st.warning("⚠️ Completa todos los campos antes de guardar.")

# 📊 Mostrar pedidos capturados del mes
if os.path.isfile(archivo_csv):
    st.subheader(f"📋 Pedidos capturados en {mes_nombre.upper()} {anio}")
    df = pd.read_csv(archivo_csv)
    st.dataframe(df)
