# utils/pdf_generator.py
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER
import os

def generar_pdf(df, vehiculo, fecha):
    nombre_pdf = f"logistica/ruta_vehiculo_{vehiculo}_{fecha}.pdf"
    doc = SimpleDocTemplate(nombre_pdf, pagesize=LETTER)
    estilos = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph(f"Ruta de entregas - Vehículo {vehiculo} - Fecha: {fecha}", estilos['Title']))
    elementos.append(Spacer(1, 12))

    for i, row in df.iterrows():
        direccion = row.get("Direccion", "Sin dirección")
        elementos.append(Paragraph(f"{i+1}. {row['Articulo']} - {direccion}", estilos["Normal"]))
        elementos.append(Spacer(1, 8))

    doc.build(elementos)
    return nombre_pdf
