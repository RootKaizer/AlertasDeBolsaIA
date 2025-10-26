import re
from datetime import datetime, timedelta
import urllib.parse

    # Unidades válidas (sin números)
valores_especificos_validos = {
    # Minutos (1-60)
    "1min", "2min", "3min", "4min", "5min", "6min", "7min", "8min", "9min", "10min",
    "11min", "12min", "13min", "14min", "15min", "16min", "17min", "18min", "19min", "20min",
    "21min", "22min", "23min", "24min", "25min", "26min", "27min", "28min", "29min", "30min",
    "31min", "32min", "33min", "34min", "35min", "36min", "37min", "38min", "39min", "40min",
    "41min", "42min", "43min", "44min", "45min", "46min", "47min", "48min", "49min", "50min",
    "51min", "52min", "53min", "54min", "55min", "56min", "57min", "58min", "59min", "60min",
    
    # Horas (1-24)
    "1h", "2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "10h",
    "11h", "12h", "13h", "14h", "15h", "16h", "17h", "18h", "19h", "20h",
    "21h", "22h", "23h", "24h",
    
    # Días (1-365)
    "1day", "2day", "3day", "4day", "5day", "6day", "7day", "8day", "9day", "10day",
    "15day", "20day", "25day", "30day", "45day", "60day", "90day", "120day", "180day", "365day",
    
    # Semanas (1-52)
    "1week", "2week", "3week", "4week", "5week", "6week", "7week", "8week", "9week", "10week",
    "11week", "12week", "13week", "14week", "15week", "16week", "17week", "18week", "19week", "20week",
    "25week", "30week", "35week", "40week", "45week", "50week", "52week",
    
    # Meses (1-12)
    "1month", "2month", "3month", "4month", "5month", "6month", "7month", "8month", "9month", "10month",
    "11month", "12month", "18month", "24month", "36month", "48month", "60month",
    
    # Años (1-100)
    "1year", "2year", "3year", "4year", "5year", "6year", "7year", "8year", "9year", "10year",
    "15year", "20year", "25year", "30year", "40year", "50year", "60year", "70year", "80year", "90year", "100year"
}


def validar_intervalo_date(intervalo):
    """ Valida si el intervalo dado es válido """
    if intervalo in valores_especificos_validos:
        return True
    else:
        # También validar con regex para formatos dinámicos
        patron = r'^(\d+)(min|h|day|week|month|year)$'
        if re.match(patron, intervalo):
            # Verificar límites razonables
            match = re.match(patron, intervalo)
            cantidad = int(match.group(1))
            unidad = match.group(2)
            
            limites = {
                "min": (1, 60),
                "h": (1, 24),
                "day": (1, 365),
                "week": (1, 52),
                "month": (1, 60),  # 5 años en meses
                "year": (1, 100)
            }
            
            if unidad in limites:
                min_val, max_val = limites[unidad]
                if min_val <= cantidad <= max_val:
                    return True
                else:
                    print(f"Error: {intervalo} está fuera de los límites permitidos para {unidad} ({min_val}-{max_val})")
                    return False
            return True
        else:
            print(f"Error: {intervalo} no es un intervalo válido.")
            print(f"Formato válido: <número><unidad> (ej: 15min, 4h, 2day, 3week, 6month, 2year)")
            print(f"Límites: 1-60min, 1-24h, 1-365day, 1-52week, 1-60month, 1-100year")
            return False



def convertir_a_segundos(intervalo):
    """Convierte un intervalo de tiempo a segundos de manera dinámica"""
    # Factores de conversión base
    conversion = {
        "min": 60,
        "h": 60 * 60,
        "day": 24 * 60 * 60,
        "week": 7 * 24 * 60 * 60,
        "month": 30 * 24 * 60 * 60,  # Aproximación: 30 días por mes
        "year": 365 * 24 * 60 * 60   # Aproximación: 365 días por año
    }
    
    # Parsear el intervalo
    match = re.match(r"(\d+)([a-zA-Z]+)", intervalo)
    if not match:
        print(f"Error: No se pudo parsear el intervalo: {intervalo}")
        return None
        
    cantidad, unidad = match.groups()
    cantidad = int(cantidad)
    
    if unidad not in conversion:
        print(f"Error: Unidad no válida: {unidad}")
        print(f"Unidades válidas: min, h, day, week, month, year")
        return None
    
    # Calcular segundos
    segundos = cantidad * conversion[unidad]
    
    # Información debug opcional
    print(f"Conversión: {intervalo} = {cantidad} {unidad} = {segundos} segundos ({segundos/86400:.2f} días)")
    
    return segundos



def calcular_fechas(intervalo):
    """Calcula las fechas de inicio y fin basadas en el intervalo"""
    print(f"\n📅 CALCULANDO FECHAS PARA INTERVALO: {intervalo}")
    
    # Primero validar el intervalo
    if not validar_intervalo_date(intervalo):
        print(f"❌ Intervalo no válido: {intervalo}")
        return None, None
    
    segundos = convertir_a_segundos(intervalo)
    if segundos is None:
        print(f"❌ Error en conversión de intervalo: {intervalo}")
        return None, None
        
    end_date = datetime.now()
    start_date = end_date - timedelta(seconds=segundos)
    
    # Calcular diferencia en días, meses y años para mejor visualización
    dias_totales = segundos / 86400
    meses_aprox = dias_totales / 30
    años_aprox = dias_totales / 365
    
    print(f"📍 Rango temporal calculado:")
    print(f"   • Inicio: {start_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   • Fin:    {end_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   • Duración: {dias_totales:.1f} días ({meses_aprox:.1f} meses, {años_aprox:.2f} años)")
    
    # Formatear para API
    end_date_str = end_date.strftime("%Y-%m-%dT%H:%M")
    start_date_str = start_date.strftime("%Y-%m-%dT%H:%M")
    end_date_encoded = urllib.parse.quote(end_date_str)
    start_date_encoded = urllib.parse.quote(start_date_str)
    
    print(f"🔗 Fechas codificadas para API:")
    print(f"   • Start: {start_date_encoded}")
    print(f"   • End:   {end_date_encoded}")
    
    return start_date_encoded, end_date_encoded



def generar_rango_fechas_descripcion(intervalo):
    """Genera una descripción legible del rango de fechas"""
    if not validar_intervalo_date(intervalo):
        return f"Intervalo inválido: {intervalo}"
    
    segundos = convertir_a_segundos(intervalo)
    if segundos is None:
        return f"Error en intervalo: {intervalo}"
    
    end_date = datetime.now()
    start_date = end_date - timedelta(seconds=segundos)
    
    dias = segundos / 86400
    if dias < 1:
        return f"Últimas {segundos/3600:.1f} horas"
    elif dias < 30:
        return f"Últimos {dias:.0f} días"
    elif dias < 365:
        return f"Últimos {dias/30:.1f} meses"
    else:
        return f"Últimos {dias/365:.1f} años"



# Función adicional para mostrar todos los intervalos válidos
def mostrar_intervalos_validos():
    """Muestra ejemplos de intervalos válidos"""
    print("\n📋 INTERVALOS VÁLIDOS DISPONIBLES:")
    print("Minutos: 1min - 60min (ej: 15min, 30min, 45min)")
    print("Horas:   1h - 24h (ej: 1h, 4h, 8h, 24h)")
    print("Días:    1day - 365day (ej: 1day, 7day, 30day, 90day)")
    print("Semanas: 1week - 52week (ej: 1week, 4week, 12week, 52week)")
    print("Meses:   1month - 60month (ej: 1month, 3month, 6month, 12month)")
    print("Años:    1year - 100year (ej: 1year, 2year, 5year, 10year)")