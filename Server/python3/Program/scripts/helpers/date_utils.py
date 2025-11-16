import re
from datetime import datetime, timedelta
import urllib.parse
import pytz

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



def calcular_fechas(intervalo, timezone="UTC"):
    """Calcula las fechas de inicio y fin basadas en el intervalo"""
    print(f"\n📅 CALCULANDO FECHAS PARA INTERVALO: {intervalo}")
    
    # Primero validar el intervalo
    if not validar_intervalo_date(intervalo):
        print(f"❌ Intervalo no válido: {intervalo}")
        return None, None
    
    # Configurar timezone
    try:
        tz = pytz.timezone(timezone)
    except:
        print(f"⚠️  Timezone {timezone} no válido, usando UTC")
        tz = pytz.UTC
    
    segundos = convertir_a_segundos(intervalo)
    if segundos is None:
        print(f"❌ Error en conversión de intervalo: {intervalo}")
        return None, None
    
    #traer datos del doble de tiempo para haci tiener datos completos del tiempo atras
    doble_segundos = 2*segundos
        
    # Usar datetime.now() con timezone
    end_date = datetime.now(tz)
    start_date = end_date - timedelta(seconds=segundos)
    
    # Calcular diferencia en días, meses y años para mejor visualización
    dias_totales = segundos / 86400
    meses_aprox = dias_totales / 30
    años_aprox = dias_totales / 365
    
    print(f"📍 Rango temporal calculado:")
    print(f"   • Inicio: {start_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   • Fin:    {end_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   • Duración: {dias_totales:.1f} días ({meses_aprox:.1f} meses, {años_aprox:.2f} años)")
    print(f"   • Momento actual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
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




def traducir_intervalo_alpha_vantage(intervalo):
    """
    Traduce el intervalo estándar al formato de Alpha Vantage
    """
    mapeo_intervalos = {
        # Minutos (1-60)
        "1min": "1min", "2min": "1min", "3min": "1min", "4min": "1min", "5min": "5min",
        "6min": "1min", "7min": "1min", "8min": "1min", "9min": "1min", "10min": "1min",
        "11min": "1min", "12min": "1min", "13min": "1min", "14min": "1min", "15min": "15min",
        "16min": "1min", "17min": "1min", "18min": "1min", "19min": "1min", "20min": "1min",
        "21min": "1min", "22min": "1min", "23min": "1min", "24min": "1min", "25min": "1min",
        "26min": "1min", "27min": "1min", "28min": "1min", "29min": "1min", "30min": "30min",
        "31min": "1min", "32min": "1min", "33min": "1min", "34min": "1min", "35min": "1min",
        "36min": "1min", "37min": "1min", "38min": "1min", "39min": "1min", "40min": "1min",
        "41min": "1min", "42min": "1min", "43min": "1min", "44min": "1min", "45min": "1min",
        "46min": "1min", "47min": "1min", "48min": "1min", "49min": "1min", "50min": "1min",
        "51min": "1min", "52min": "1min", "53min": "1min", "54min": "1min", "55min": "1min",
        "56min": "1min", "57min": "1min", "58min": "1min", "59min": "1min", "60min": "1min",
        
        # Horas (1-24) - Alpha Vantage solo soporta 1min, 5min, 15min, 30min, 60min
        "1h": "60min", "2h": "60min", "3h": "60min", "4h": "60min", "5h": "60min",
        "6h": "60min", "7h": "60min", "8h": "60min", "9h": "60min", "10h": "60min",
        "11h": "60min", "12h": "60min", "13h": "60min", "14h": "60min", "15h": "60min",
        "16h": "60min", "17h": "60min", "18h": "60min", "19h": "60min", "20h": "60min",
        "21h": "60min", "22h": "60min", "23h": "60min", "24h": "60min",
        
        # Días, semanas, meses, años - Alpha Vantage tiene funciones separadas
        "1day": "daily", "2day": "daily", "3day": "daily", "4day": "daily", "5day": "daily",
        "6day": "daily", "7day": "daily", "8day": "daily", "9day": "daily", "10day": "daily",
        "15day": "daily", "20day": "daily", "25day": "daily", "30day": "daily", "45day": "daily",
        "60day": "daily", "90day": "daily", "120day": "daily", "180day": "daily", "365day": "daily",
        
        "1week": "weekly", "2week": "weekly", "3week": "weekly", "4week": "weekly", "5week": "weekly",
        "6week": "weekly", "7week": "weekly", "8week": "weekly", "9week": "weekly", "10week": "weekly",
        "11week": "weekly", "12week": "weekly", "13week": "weekly", "14week": "weekly", "15week": "weekly",
        "16week": "weekly", "17week": "weekly", "18week": "weekly", "19week": "weekly", "20week": "weekly",
        "25week": "weekly", "30week": "weekly", "35week": "weekly", "40week": "weekly", "45week": "weekly",
        "50week": "weekly", "52week": "weekly",
        
        "1month": "monthly", "2month": "monthly", "3month": "monthly", "4month": "monthly", "5month": "monthly",
        "6month": "monthly", "7month": "monthly", "8month": "monthly", "9month": "monthly", "10month": "monthly",
        "11month": "monthly", "12month": "monthly", "18month": "monthly", "24month": "monthly", "36month": "monthly",
        "48month": "monthly", "60month": "monthly",
        
        "1year": "monthly", "2year": "monthly", "3year": "monthly", "4year": "monthly", "5year": "monthly",
        "6year": "monthly", "7year": "monthly", "8year": "monthly", "9year": "monthly", "10year": "monthly",
        "15year": "monthly", "20year": "monthly", "25year": "monthly", "30year": "monthly", "40year": "monthly",
        "50year": "monthly", "60year": "monthly", "70year": "monthly", "80year": "monthly", "90year": "monthly", "100year": "monthly"
    }
    return mapeo_intervalos.get(intervalo, '60min')



def traducir_intervalo_yahoo(intervalo):
    """
    Traduce el intervalo estándar al formato de Yahoo Finance
    """
    mapeo_intervalos = {
        # Minutos (1-60) - Yahoo soporta 1m, 2m, 5m, 15m, 30m, 60m, 90m
        "1min": "1m", "2min": "2m", "3min": "2m", "4min": "2m", "5min": "5m",
        "6min": "5m", "7min": "5m", "8min": "5m", "9min": "5m", "10min": "5m",
        "11min": "5m", "12min": "5m", "13min": "5m", "14min": "5m", "15min": "15m",
        "16min": "15m", "17min": "15m", "18min": "15m", "19min": "15m", "20min": "15m",
        "21min": "15m", "22min": "15m", "23min": "15m", "24min": "15m", "25min": "15m",
        "26min": "15m", "27min": "15m", "28min": "15m", "29min": "15m", "30min": "30m",
        "31min": "30m", "32min": "30m", "33min": "30m", "34min": "30m", "35min": "30m",
        "36min": "30m", "37min": "30m", "38min": "30m", "39min": "30m", "40min": "30m",
        "41min": "30m", "42min": "30m", "43min": "30m", "44min": "30m", "45min": "30m",
        "46min": "30m", "47min": "30m", "48min": "30m", "49min": "30m", "50min": "30m",
        "51min": "30m", "52min": "30m", "53min": "30m", "54min": "30m", "55min": "30m",
        "56min": "30m", "57min": "30m", "58min": "30m", "59min": "30m", "60min": "60m",
        
        # Horas (1-24) - Yahoo usa 60m para horas
        "1h": "60m", "2h": "60m", "3h": "60m", "4h": "60m", "5h": "60m",
        "6h": "60m", "7h": "60m", "8h": "60m", "9h": "60m", "10h": "60m",
        "11h": "60m", "12h": "60m", "13h": "60m", "14h": "60m", "15h": "60m",
        "16h": "60m", "17h": "60m", "18h": "60m", "19h": "60m", "20h": "60m",
        "21h": "60m", "22h": "60m", "23h": "60m", "24h": "60m",
        
        # Días, semanas, meses
        "1day": "1d", "2day": "1d", "3day": "1d", "4day": "1d", "5day": "1d",
        "6day": "1d", "7day": "1d", "8day": "1d", "9day": "1d", "10day": "1d",
        "15day": "1d", "20day": "1d", "25day": "1d", "30day": "1d", "45day": "1d",
        "60day": "1d", "90day": "1d", "120day": "1d", "180day": "1d", "365day": "1d",
        
        "1week": "1wk", "2week": "1wk", "3week": "1wk", "4week": "1wk", "5week": "1wk",
        "6week": "1wk", "7week": "1wk", "8week": "1wk", "9week": "1wk", "10week": "1wk",
        "11week": "1wk", "12week": "1wk", "13week": "1wk", "14week": "1wk", "15week": "1wk",
        "16week": "1wk", "17week": "1wk", "18week": "1wk", "19week": "1wk", "20week": "1wk",
        "25week": "1wk", "30week": "1wk", "35week": "1wk", "40week": "1wk", "45week": "1wk",
        "50week": "1wk", "52week": "1wk",
        
        "1month": "1mo", "2month": "1mo", "3month": "1mo", "4month": "1mo", "5month": "1mo",
        "6month": "1mo", "7month": "1mo", "8month": "1mo", "9month": "1mo", "10month": "1mo",
        "11month": "1mo", "12month": "1mo", "18month": "1mo", "24month": "1mo", "36month": "1mo",
        "48month": "1mo", "60month": "1mo",
        
        "1year": "1y", "2year": "1y", "3year": "1y", "4year": "1y", "5year": "1y",
        "6year": "1y", "7year": "1y", "8year": "1y", "9year": "1y", "10year": "1y",
        "15year": "1y", "20year": "1y", "25year": "1y", "30year": "1y", "40year": "1y",
        "50year": "1y", "60year": "1y", "70year": "1y", "80year": "1y", "90year": "1y", "100year": "1y"
    }
    return mapeo_intervalos.get(intervalo, '60m')



def calcular_periodo_yahoo(tiempo_atras):
    """
    Calcula el parámetro 'range' para Yahoo Finance basado en tiempo_atras
    """
    # Convertir tiempo_atras a segundos para determinar el rango
    segundos = convertir_a_segundos(tiempo_atras)
    if segundos is None:
        return '2mo'  # Por defecto
    
    dias = segundos / 86400
    
    if dias <= 1:
        return '1d'
    elif dias <= 2:
        return '2d'
    elif dias <= 5:
        return '5d'
    elif dias <= 7:
        return '7d'
    elif dias <= 10:
        return '10d'
    elif dias <= 15:
        return '15d'
    elif dias <= 20:
        return '20d'
    elif dias <= 25:
        return '1mo'  # 1 mes ≈ 30 días
    elif dias <= 30:
        return '1mo'
    elif dias <= 45:
        return '3mo'  # 3 meses ≈ 90 días
    elif dias <= 60:
        return '3mo'
    elif dias <= 90:
        return '3mo'
    elif dias <= 120:
        return '6mo'  # 6 meses ≈ 180 días
    elif dias <= 180:
        return '6mo'
    elif dias <= 240:
        return '6mo'
    elif dias <= 270:
        return '6mo'
    elif dias <= 300:
        return '1y'   # 1 año ≈ 365 días
    elif dias <= 365:
        return '1y'
    elif dias <= 400:
        return '1y'
    elif dias <= 450:
        return '1y'
    elif dias <= 500:
        return '1y'
    elif dias <= 520:  # 52 semanas
        return '1y'
    elif dias <= 545:  # 18 meses ≈ 545 días
        return '2y'
    elif dias <= 730:  # 2 años
        return '2y'
    elif dias <= 900:  # 30 meses
        return '2y'
    elif dias <= 1095: # 3 años
        return '5y'
    elif dias <= 1460: # 4 años
        return '5y'
    elif dias <= 1825: # 5 años
        return '5y'
    elif dias <= 2190: # 6 años
        return '10y'
    elif dias <= 2555: # 7 años
        return '10y'
    elif dias <= 2920: # 8 años
        return '10y'
    elif dias <= 3285: # 9 años
        return '10y'
    elif dias <= 3650: # 10 años
        return '10y'
    elif dias <= 5475: # 15 años
        return '10y'
    elif dias <= 7300: # 20 años
        return '10y'
    elif dias <= 9125: # 25 años
        return '10y'
    elif dias <= 10950: # 30 años
        return '10y'
    elif dias <= 14600: # 40 años
        return '10y'
    elif dias <= 18250: # 50 años
        return '10y'
    elif dias <= 21900: # 60 años
        return '10y'
    elif dias <= 25550: # 70 años
        return '10y'
    elif dias <= 29200: # 80 años
        return '10y'
    elif dias <= 32850: # 90 años
        return '10y'
    elif dias <= 36500: # 100 años
        return '10y'
    else:
        return '10y' 



def calcular_outputsize_alpha_vantage(tiempo_atras):
    """
    Determina si usar 'compact' o 'full' para Alpha Vantage
    para TODOS los valores posibles de valores_especificos_validos
    """
    segundos = convertir_a_segundos(tiempo_atras)
    if segundos is None:
        return 'compact'
    
    dias = segundos / 86400
    
    # Alpha Vantage: 
    # - compact = últimos 100 datos puntos
    # - full = datos históricos completos
    
    # Si el período requerido es mayor a lo que cubren 100 datos puntos, usar full
    # Para intervalos intraday (1min-60min), 100 datos pueden cubrir pocos días
    # Para intervalos diarios/semanales/mensuales, 100 datos cubren más tiempo
    
    if 'min' in tiempo_atras or 'h' in tiempo_atras:
        # Para intervalos cortos (minutos/horas)
        if dias > 7:  # Si necesitamos más de 7 días de datos intraday
            return 'full'
        else:
            return 'compact'
    elif 'day' in tiempo_atras:
        # Para intervalos diarios
        dias_num = int(tiempo_atras.replace('day', ''))
        if dias_num > 100:  # Si necesitamos más de 100 días
            return 'full'
        else:
            return 'compact'
    elif 'week' in tiempo_atras:
        # Para intervalos semanales
        semanas_num = int(tiempo_atras.replace('week', ''))
        if semanas_num > 20:  # Si necesitamos más de 20 semanas (~5 meses)
            return 'full'
        else:
            return 'compact'
    elif 'month' in tiempo_atras:
        # Para intervalos mensuales
        meses_num = int(tiempo_atras.replace('month', ''))
        if meses_num > 12:  # Si necesitamos más de 12 meses
            return 'full'
        else:
            return 'compact'
    elif 'year' in tiempo_atras:
        # Para intervalos anuales - siempre usar full para datos históricos largos
        return 'full'
    else:
        # Por defecto para casos no cubiertos
        if dias > 30:
            return 'full'
        else:
            return 'compact'