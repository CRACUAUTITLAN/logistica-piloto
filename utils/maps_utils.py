# utils/maps_utils.py
import requests
import os
from dotenv import load_dotenv
import folium
from folium.plugins import MarkerCluster
import base64

load_dotenv()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def coordenadas_a_direccion(lat, lon):
    # Ejemplo: Ubicación de la agencia 19.6679, -99.2001
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={API_KEY}"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        if data["results"]:
            return data["results"][0]["formatted_address"]
    return "Dirección no encontrada"

def generar_mapa(df):
    lat_prom = df["Latitud"].astype(float).mean()
    lon_prom = df["Longitud"].astype(float).mean()
    mapa = folium.Map(location=[lat_prom, lon_prom], zoom_start=11)
    cluster = MarkerCluster().add_to(mapa)

    for i, row in df.iterrows():
        direccion = coordenadas_a_direccion(row["Latitud"], row["Longitud"])
        folium.Marker(
            location=[row["Latitud"], row["Longitud"]],
            popup=f"{row['Articulo']}<br>{direccion}",
            tooltip=row["Articulo"]
        ).add_to(cluster)

    return mapa._repr_html_()
