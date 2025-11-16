import requests
import time
from datetime import datetime
import urllib.parse

import requests
import time
from datetime import datetime, timedelta
import urllib.parse



def obtener_datos_twelvedata(url_base_path, symbol, api_key, interval, start_date=None, end_date=None, timezone="UTC", verbose=False):
    """
    Obtiene datos de Twelve Data API con soporte para timezone
    """
    timestamp = int(time.time())
    
    # Construir URL base
    url = f"{url_base_path}/time_series?symbol={symbol}&interval={interval}&apikey={api_key}&timezone={timezone}&timestamp={timestamp}"
    
    if start_date:
        url += f"&start_date={start_date}"
    if end_date:
        url += f"&end_date={end_date}"
    
    if verbose:
        print(f"    🌐 Consultando Twelve Data para {symbol}: {url.replace(api_key, 'API_KEY_REDACTED').replace(str(timestamp), 'TIMESTAMP_REDACTED')}")
        print(f"    🕐 Timezone: {timezone}, Timestamp: {timestamp} ({datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')})")
    
    try:
        headers = {
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if verbose:
            print(f"    📥 Respuesta recibida para {symbol} - Status: {response.status_code}")
        
        data = response.json()
        
        # Validar respuesta
        validated_data = _validar_respuesta_api(data, symbol, "Twelve Data", verbose)
        if validated_data:
            return _formatear_datos_salida(validated_data, symbol, "Twelve Data", verbose)
        return None
        
    except Exception as e:
        error_msg = f"Error al obtener datos de Twelve Data para {symbol}: {e}"
        if verbose:
            print(f"    ❌ {error_msg}")
        return None



def obtener_datos_alpha_vantage(symbol, api_key, interval, tiempo_atras=None, timezone="UTC", verbose=False):
    """
    Obtiene datos de Alpha Vantage API
    """
    from helpers.date_utils import traducir_intervalo_alpha_vantage, calcular_outputsize_alpha_vantage

    # Traducir intervalo
    alpha_interval = traducir_intervalo_alpha_vantage(interval)
    
    # Determinar outputsize basado en tiempo_atras
    outputsize = calcular_outputsize_alpha_vantage(tiempo_atras) if tiempo_atras else 'compact'
    
    try:
        if alpha_interval in ['daily', 'weekly', 'monthly']:
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_{alpha_interval.upper()}&symbol={symbol}&apikey={api_key}&outputsize={outputsize}"
        else:
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={alpha_interval}&apikey={api_key}&outputsize={outputsize}"
        
        if verbose:
            print(f"    🌐 Consultando Alpha Vantage para {symbol}: {url.replace(api_key, 'API_KEY_REDACTED')}")
            print(f"    🕐 Intervalo Alpha Vantage: {alpha_interval}, Timezone: {timezone}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)

        if verbose:
            print(f"    📥 Respuesta Alpha Vantage para {symbol} - Status: {response.status_code}")

        data = response.json()
        
        # Procesar respuesta específica de Alpha Vantage
        processed_data = _procesar_respuesta_alpha_vantage(data, alpha_interval, verbose)
        if processed_data:
            validated_data = _validar_respuesta_api(processed_data, symbol, "Alpha Vantage", verbose)
            if validated_data:
                return _formatear_datos_salida(validated_data, symbol, "Alpha Vantage", verbose)
        return None
        
    except Exception as e:
        if verbose:
            print(f"    ❌ Error Alpha Vantage para {symbol}: {e}")
        return None



def obtener_datos_yahoo_finance(symbol, interval, tiempo_atras=None, timezone="UTC", verbose=False):
    """
    Obtiene datos de Yahoo Finance (usando API pública)
    """
    from helpers.date_utils import traducir_intervalo_yahoo, calcular_periodo_yahoo

    try:
        # Traducir intervalo
        yahoo_interval = traducir_intervalo_yahoo(interval)
        
        # Calcular periodo basado en tiempo_atras
        period = calcular_periodo_yahoo(tiempo_atras) if tiempo_atras else '2mo'
        
        # Usar API pública de Yahoo Finance
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={period}&interval={yahoo_interval}"

        if verbose:
            print(f"    🌐 Consultando Yahoo Finance para {symbol}: {url}")
            print(f"    🕐 Intervalo Yahoo: {yahoo_interval}, Periodo: {period}, Timezone: {timezone}")
            if tiempo_atras:
                print(f"    📅 Tiempo atrás configurado: {tiempo_atras}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=30)

        if verbose:
            print(f"    📥 Respuesta Yahoo Finance para {symbol} - Status: {response.status_code}")
        
        data = response.json()
        
        # Procesar respuesta de Yahoo Finance
        processed_data = _procesar_respuesta_yahoo(data, symbol, verbose)
        if processed_data:
            validated_data = _validar_respuesta_api(processed_data, symbol, "Yahoo Finance", verbose)
            if validated_data:
                return _formatear_datos_salida(validated_data, symbol, "Yahoo Finance", verbose)
        return None
        
    except Exception as e:
        if verbose:
            print(f"    ❌ Error Yahoo Finance para {symbol}: {e}")
        return None



def _procesar_respuesta_alpha_vantage(data, interval, verbose=False):
    """Convierte la respuesta de Alpha Vantage al formato estándar"""
    try:
        time_series_key = 'Time Series (Daily)' if interval == 'daily' else f'Time Series ({interval})'
        
        if time_series_key not in data:
            if verbose:
                print(f"    ⚠️  Alpha Vantage - Clave no encontrada: {time_series_key}")
                if 'Error Message' in data:
                    print(f"    ❌ Error Alpha Vantage: {data['Error Message']}")
            return None
        
        time_series = data[time_series_key]
        values = []
        
        for datetime_str, prices in time_series.items():
            # Validar que el formato sea correcto antes de agregar
            try:
                if interval == 'daily':
                    # Para datos diarios: "2025-10-16" -> "2025-10-16 00:00:00"
                    dt_str = f"{datetime_str} 00:00:00"
                else:
                    # Para datos intraday: limpiar formato
                    # Ejemplo: "2025-10-16 04:00:00" (ya está bien)
                    # Si tiene formato incorrecto, limpiarlo
                    if ' ' in datetime_str:
                        date_part, time_part = datetime_str.split(' ')
                        # Tomar solo las primeras 8 caracteres del tiempo (HH:MM:SS)
                        if len(time_part) > 8:
                            time_part = time_part[:8]
                        dt_str = f"{date_part} {time_part}"
                    else:
                        dt_str = f"{datetime_str} 00:00:00"
            
            
                # Probar si el formato es parseable
                datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')

                values.append({
                    'datetime': dt_str,
                    'open': float(prices['1. open']),
                    'high': float(prices['2. high']), 
                    'low': float(prices['3. low']),
                    'close': float(prices['4. close']),
                    'volume': int(float(prices['5. volume']))
                })
            except ValueError as e:
                if verbose:
                    print(f"    ⚠️  Alpha Vantage - Fecha inválida ignorada: {dt_str} - Error: {e}")
                continue
        
        # Ordenar por fecha (más antiguo primero)
        if values:
            values.sort(key=lambda x: x['datetime'])
            return {'values': values}
        else:
            if verbose:
                print(f"    ⚠️  Alpha Vantage - No se pudieron procesar registros válidos")
            return None
        
    except Exception as e:
        if verbose:
            print(f"    ❌ Error procesando Alpha Vantage: {e}")
        return None



def _procesar_respuesta_yahoo(data, symbol, verbose=False):
    """Convierte la respuesta de Yahoo Finance al formato estándar"""
    try:
        if 'chart' not in data or 'result' not in data['chart'] or not data['chart']['result']:
            if verbose:
                print(f"    ❌ Yahoo Finance - Estructura de respuesta inválida para {symbol}")
            return None
        
        result = data['chart']['result'][0]
        timestamps = result['timestamp']
        quotes = result['indicators']['quote'][0]
        
        values = []
        for i, timestamp in enumerate(timestamps):
            dt = datetime.fromtimestamp(timestamp)
            values.append({
                'datetime': dt.strftime('%Y-%m-%d %H:%M:%S'),
                'open': float(quotes['open'][i]) if quotes['open'][i] is not None else 0,
                'high': float(quotes['high'][i]) if quotes['high'][i] is not None else 0,
                'low': float(quotes['low'][i]) if quotes['low'][i] is not None else 0,
                'close': float(quotes['close'][i]) if quotes['close'][i] is not None else 0,
                'volume': int(quotes['volume'][i]) if quotes['volume'][i] is not None else 0
            })
        
        return {'values': values}
        
    except Exception as e:
        if verbose:
            print(f"    ❌ Error procesando Yahoo Finance: {e}")
        return None




def _validar_respuesta_api(data, symbol, api_name, verbose=False):
    """Valida la respuesta de cualquier API"""
    if not data or "values" not in data:
        if verbose:
            print(f"    ❌ {api_name} - Respuesta inválida para {symbol}")
        return None
    
    if not data["values"]:
        if verbose:
            print(f"    ⚠️  {api_name} - No hay datos para {symbol}")
        return None
    
    # Verificar datos futuros/ficticios
    primer_registro = data["values"][0]
    fecha_primer = primer_registro.get('datetime', '')
    
    if fecha_primer:
        try:
            fecha_actual = datetime.now()
            fecha_primer_dt = datetime.strptime(fecha_primer, '%Y-%m-%d %H:%M:%S')
            
            if fecha_primer_dt > fecha_actual + timedelta(hours=24):  # Margen de 24 horas
                print(f"    ⚠️  ALERTA: {api_name} devuelve datos futuros para {symbol}")
                print(f"    ⚠️  Primer registro: {fecha_primer} vs Actual: {fecha_actual.strftime('%Y-%m-%d %H:%M:%S')}")
                return None
                
        except ValueError as e:
            if verbose:
                print(f"    ⚠️  Error parseando fecha {fecha_primer}: {e}")
    
    return data



def _formatear_datos_salida(data, symbol, api_name, verbose=False):
    """Formatea los datos de salida con información adicional"""
    if verbose and data["values"]:
        primer_registro = data["values"][0]
        ultimo_registro = data["values"][-1]
        print(f"    ✅ {api_name} - Datos válidos para {symbol}: {len(data['values'])} registros")
        print(f"    📊 Primer registro: {primer_registro.get('datetime', 'N/A')}")
        print(f"    📊 Último registro: {ultimo_registro.get('datetime', 'N/A')}")
        print(f"    💰 Precio más reciente: {ultimo_registro.get('close', 'N/A')}")
    
    return data



def obtener_mejores_datos(symbol, intervalo, tiempo_atras, config_apis, timezone="America/Bogota", verbose=False):
    """
    Obtiene datos de múltiples APIs y retorna los mejores (con más registros)
    Args:
        symbol: Símbolo a consultar
        intervalo: Intervalo de tiempo
        config_apis: Diccionario con configuraciones de APIs
        verbose: Modo verbose
    
    Returns:
        Mejores datos encontrados o None si todos fallan
    """
    todos_datos = []
    fuentes_info = []
    
    # Twelve Data
    if 'twelvedata' in config_apis:
        # Calcular fechas para Twelve Data
        from helpers.date_utils import calcular_fechas
        start_date, end_date = calcular_fechas(tiempo_atras, timezone=timezone)

        datos_td = obtener_datos_twelvedata(
            config_apis['twelvedata']['url_base_path'],
            symbol,
            config_apis['twelvedata']['api_key'],
            intervalo,
            start_date=start_date,
            end_date=end_date,
            timezone=timezone,
            verbose=verbose
        )
        if datos_td:
            registros_td = len(datos_td['values'])
            todos_datos.append(('Twelve Data', datos_td))
            fuentes_info.append(f"Twelve Data: {registros_td} registros")
    
    # Alpha Vantage
    if 'alpha_vantage' in config_apis and config_apis['alpha_vantage']['api_key']:
        datos_av = obtener_datos_alpha_vantage(
            symbol,
            config_apis['alpha_vantage']['api_key'],
            intervalo,
            tiempo_atras=tiempo_atras,
            timezone=timezone,
            verbose=verbose
        )
        if datos_av:
            registros_av = len(datos_av['values'])
            todos_datos.append(('Alpha Vantage', datos_av))
            fuentes_info.append(f"Alpha Vantage: {registros_av} registros")
    
    # Yahoo Finance
    if 'yahoo_finance' in config_apis:
        datos_yf = obtener_datos_yahoo_finance(
            symbol,
            intervalo,
            tiempo_atras=tiempo_atras,
            timezone=timezone,
            verbose=verbose
        )
        if datos_yf:
            registros_yf = len(datos_yf['values'])
            todos_datos.append(('Yahoo Finance', datos_yf))
            fuentes_info.append(f"Yahoo Finance: {registros_yf} registros")
    
    # Seleccionar los mejores datos (con más registros)
    if todos_datos:
        # Ordenar por cantidad de registros (descendente)
        todos_datos.sort(key=lambda x: len(x[1]['values']) if x[1] and 'values' in x[1] else 0, reverse=True)
        
        mejor_fuente, mejores_datos = todos_datos[0]
        registros_mejor = len(mejores_datos['values'])
        
        if verbose:
            print(f"    📊 Resumen de fuentes para {symbol}:")
            for info in fuentes_info:
                print(f"       • {info}")
            print(f"    🏆 Mejor fuente seleccionada: {mejor_fuente} con {registros_mejor} registros")
        
        return mejores_datos
    
    if verbose:
        print(f"    ❌ Todas las APIs fallaron para {symbol}")
    return None



# Función de compatibilidad hacia atrás
def obtener_historico_mercados_hasta_hoy(url_base_path, symbol, api_key, interval, start_date=None, end_date=None, verbose=False, timezone="UTC"):
    """
    Función legacy para mantener compatibilidad
    """
    return obtener_datos_twelvedata(url_base_path, symbol, api_key, interval, start_date, end_date, timezone, verbose)
