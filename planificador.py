import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def planificar_logistica_simple(df, hora_inicio="08:00"):
    df = df.copy()
    df["Latitud"] = df["Latitud"].astype(float)
    df["Longitud"] = df["Longitud"].astype(float)

    origen = (19.667923496820304, -99.20018003699839)  # Agencia CRA Cuautitlan
    num_vehiculos = 4
    tiempo_por_entrega = timedelta(minutes=15)
    tiempo_entre_pedidos = timedelta(minutes=15)
    hora_inicio = pd.to_datetime(hora_inicio)

    df["distancia"] = df.apply(
        lambda row: np.sqrt((row["Latitud"] - origen[0])**2 + (row["Longitud"] - origen[1])**2),
        axis=1
    )

    df = df.sort_values("distancia").reset_index(drop=True)
    pedidos_por_vehiculo = np.array_split(df, num_vehiculos)
    asignaciones = []

    for i, pedidos in enumerate(pedidos_por_vehiculo):
        pedidos = pedidos.reset_index(drop=True)
        tiempo_actual = hora_inicio
        tiempos = []

        for idx in range(len(pedidos)):
            if idx > 0:
                tiempo_actual += tiempo_entre_pedidos
            tiempos.append(tiempo_actual.strftime("%H:%M"))
            tiempo_actual += tiempo_por_entrega

        duracion_total = tiempo_actual - hora_inicio
        if duracion_total > timedelta(hours=3.5):
            pedidos["Hora comida"] = [""] * (len(pedidos) // 2) + ["13:00"] + [""] * (len(pedidos) - len(pedidos) // 2 - 1)
        else:
            pedidos["Hora comida"] = ""

        pedidos["Hora estimada entrega"] = tiempos
        pedidos["Vehículo"] = f"Vehículo {i+1}"
        asignaciones.append(pedidos)

    return asignaciones

# --- EJECUCIÓN DIARIA ---

hoy = datetime.now()
meses = {
    "january": "enero", "february": "febrero", "march": "marzo", "april": "abril",
    "may": "mayo", "june": "junio", "july": "julio", "august": "agosto",
    "september": "septiembre", "october": "octubre", "november": "noviembre", "december": "diciembre"
}
mes_nombre = meses[hoy.strftime("%B").lower()]
anio = str(hoy.year)
archivo_csv = f"pedidos/{mes_nombre}_{anio}.csv"
ruta_output = "logistica"
os.makedirs(ruta_output, exist_ok=True)

if os.path.isfile(archivo_csv):
    df = pd.read_csv(archivo_csv)
    rutas = planificar_logistica_simple(df)
    fecha_manana = (hoy + timedelta(days=1)).strftime("%Y-%m-%d")

    for i, vehiculo_df in enumerate(rutas):
        nombre_archivo = f"{ruta_output}/vehiculo_{i+1}_{fecha_manana}.csv"
        vehiculo_df.to_csv(nombre_archivo, index=False)
        print(f"✅ Ruta generada para Vehículo {i+1}: {nombre_archivo}")
else:
    print("⚠️ No se encontró el archivo de pedidos del mes.")
