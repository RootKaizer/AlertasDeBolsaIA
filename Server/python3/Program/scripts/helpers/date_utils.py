import re
from datetime import datetime, timedelta
import urllib.parse

valores_time_series_validos = {"1min", "5min", "15min", "30min", "45min", "1h", "2h", "4h", "8h", "1day", "1week", "1month", "1year"}

def validar_intervalo_date(intervalo):
    """ Valida si el intervalo dado es válido """
    if intervalo not in valores_time_series_validos:
        print(f"Error: {intervalo} no es un intervalo válido.")
        print(f"Valores válidos: {valores_time_series_validos}")
        return False
    return True


def convertir_a_segundos(intervalo):
    conversion = {
        "min": 60,
        "h": 60 * 60,
        "day": 24 * 60 * 60,
        "week": 7 * 24 * 60 * 60,
        "month": 30 * 24 * 60 * 60,
        "year": 365 * 24 * 60 * 60
    }
    match = re.match(r"(\d+)([a-zA-Z]+)", intervalo)
    if not match:
        return None
    cantidad, unidad = match.groups()
    cantidad = int(cantidad)
    if unidad not in conversion:
        return None
    return cantidad * conversion[unidad]

def calcular_fechas(intervalo):
    segundos = convertir_a_segundos(intervalo)
    if segundos is None:
        return None, None
    end_date = datetime.now()
    start_date = end_date - timedelta(seconds=segundos)
    end_date_str = end_date.strftime("%Y-%m-%dT%H:%M")
    start_date_str = start_date.strftime("%Y-%m-%dT%H:%M")
    end_date_encoded = urllib.parse.quote(end_date_str)
    start_date_encoded = urllib.parse.quote(start_date_str)
    return start_date_encoded, end_date_encoded