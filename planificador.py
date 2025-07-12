# planificador.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime, timedelta
import os

# Autenticación con Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1qoux5KkmNoYXRrw9FOPHJR53Hie9kIUXETBRiQNmvFw/edit").sheet1

# Leer todos los datos
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Fecha de ayer (los pedidos que se entregarán mañana)
ayer = (datetime.now() - timedelta(days=1)).date()
df['FechaCaptura'] = pd.to_datetime(df['FechaCaptura']).dt.date
df_ayer = df[df['FechaCaptura'] == ayer]

# Verificamos si hay pedidos
if df_ayer.empty:
    print("⚠️ No hay pedidos para planificar.")
    exit()

# Configuración
N_VEHICULOS = 4
df_ayer = df_ayer.reset_index(drop=True)

# Asignación simple por bloques
pedidos_por_carro = len(df_ayer) // N_VEHICULOS
restantes = len(df_ayer) % N_VEHICULOS

inicio = 0
carpetas_generadas = []

fecha_entrega = datetime.now().date()
logistica_path = "logistica"
os.makedirs(logistica_path, exist_ok=True)

for i in range(N_VEHICULOS):
    fin = inicio + pedidos_por_carro + (1 if i < restantes else 0)
    df_carro = df_ayer.iloc[inicio:fin]
    if not df_carro.empty:
        archivo = f"{logistica_path}/vehiculo_{i+1}_{fecha_entrega}.csv"
        df_carro.to_csv(archivo, index=False)
        carpetas_generadas.append(archivo)
    inicio = fin

print("✅ Archivos generados:", carpetas_generadas)
