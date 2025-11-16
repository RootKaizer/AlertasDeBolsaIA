import requests
import time
from datetime import datetime, timedelta
import pytz
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
            # Procesar con el nuevo formateo (similar a Yahoo)
            processed_data = _procesar_respuesta_twelve_data(validated_data, symbol, verbose)
            if processed_data:
                return _formatear_datos_salida(processed_data, symbol, "Twelve Data", verbose)
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



def _procesar_respuesta_twelve_data(data, symbol, verbose=False):
    """Convierte la respuesta de Twelve Data al formato estándar (similar a Yahoo)"""
    try:
        if 'values' not in data:
            if verbose:
                print(f"    ❌ Twelve Data - Estructura de respuesta inválida para {symbol}")
            return None
        
        values = []
        for registro in data['values']:
            values.append({
                'datetime': registro['datetime'],
                'open': float(registro['open']) if registro['open'] is not None else 0,
                'high': float(registro['high']) if registro['high'] is not None else 0,
                'low': float(registro['low']) if registro['low'] is not None else 0,
                'close': float(registro['close']) if registro['close'] is not None else 0,
                'volume': int(registro['volume']) if registro['volume'] is not None else 0
            })
        
        # Ordenar por fecha (más reciente primero)
        if values:
            values.sort(key=lambda x: x['datetime'], reverse=True)
            
            if verbose:
                print(f"    ✅ Twelve Data - Procesados {len(values)} registros para {symbol}")
                
            return {'values': values}
        else:
            if verbose:
                print(f"    ⚠️  Twelve Data - No se pudieron procesar registros válidos para {symbol}")
            return None
        
    except Exception as e:
        if verbose:
            print(f"    ❌ Error procesando Twelve Data: {e}")
        return None


def _procesar_respuesta_alpha_vantage(data, interval, verbose=False):
    """Convierte la respuesta de Alpha Vantage al formato estándar"""
    try:
        # VERIFICAR PRIMERO SI HAY ERRORES O MENSAJES INFORMATIVOS
        if 'Information' in data:
            info_msg = data['Information']
            if verbose:
                print(f"    💡 Alpha Vantage - Información: {info_msg}")
            
            # Detectar mensaje de límite de API
            if 'rate limit' in info_msg.lower() or 'requests per day' in info_msg.lower():
                # Extraer el número de peticiones diarias del mensaje
                import re
                match = re.search(r'(\d+)\s*requests per day', info_msg)
                if match:
                    daily_limit = match.group(1)
                    print(f"    🚫 ALERTA: Límite de Alpha Vantage alcanzado - {daily_limit} peticiones por día")
                    print(f"    💡 Solución: Esperar 24 horas o actualizar a plan premium")
                else:
                    print(f"    🚫 ALERTA: Límite de API de Alpha Vantage alcanzado")
                    print(f"    💡 Mensaje: {info_msg}")
            
            return None
        
        if 'Error Message' in data:
            error_msg = data['Error Message']
            if verbose:
                print(f"    ❌ Alpha Vantage - Error: {error_msg}")
            return None
        
        if 'Note' in data:
            note_msg = data['Note']
            if verbose:
                print(f"    ⚠️  Alpha Vantage - Nota: {note_msg}")
            
            # Detectar mensajes de límite en la nota también
            if 'rate limit' in note_msg.lower() or 'call frequency' in note_msg.lower():
                print(f"    🚫 ALERTA: Límite de frecuencia de Alpha Vantage")
                print(f"    💡 Mensaje: {note_msg}")
            
            return None
        

        # Obtener timezone de los metadatos
        time_zone = data.get("Meta Data", {}).get("6. Time Zone", "US/Eastern")
        if verbose:
            print(f"    🌍 Alpha Vantage - Timezone original: {time_zone}")
        
        # Determinar la clave correcta para la serie temporal
        # Alpha Vantage usa diferentes formatos para diferentes intervalos
        if interval == 'daily':
            time_series_key = 'Time Series (Daily)'
        elif interval == 'weekly':
            time_series_key = 'Weekly Time Series'
        elif interval == 'monthly':
            time_series_key = 'Monthly Time Series'
        else:
            # Para datos intraday: "Time Series (60min)"
            time_series_key = f'Time Series ({interval})'
        
        if verbose:
            print(f"    🔍 Alpha Vantage - Buscando clave: '{time_series_key}'")
        
        # Debug: mostrar todas las claves disponibles
        available_keys = list(data.keys())
        if verbose:
            print(f"    📋 Alpha Vantage - Claves disponibles: {available_keys}")
        
        if time_series_key not in data:
            if verbose:
                print(f"    ⚠️  Alpha Vantage - Clave no encontrada: '{time_series_key}'")
                print(f"    🔍 Alpha Vantage - Las claves disponibles son: {available_keys}")
                if 'Error Message' in data:
                    print(f"    ❌ Error Alpha Vantage: {data['Error Message']}")
                if 'Note' in data:
                    print(f"    💡 Nota Alpha Vantage: {data['Note']}")
            return None
        
        time_series = data[time_series_key]
        
        if verbose:
            print(f"    ✅ Alpha Vantage - Clave encontrada, procesando {len(time_series)} registros")
        
        # Mapear timezones de Alpha Vantage a zonas pytz
        tz_mapping = {
            'US/Eastern': 'US/Eastern',
            'US/Central': 'US/Central', 
            'US/Pacific': 'US/Pacific',
            'UTC': 'UTC',
            'EST': 'US/Eastern',
            'EDT': 'US/Eastern',
            'CST': 'US/Central',
            'CDT': 'US/Central',
            'PST': 'US/Pacific',
            'PDT': 'US/Pacific'
        }
        
        tz_name = tz_mapping.get(time_zone, 'US/Eastern')
        exchange_tz = pytz.timezone(tz_name)
        utc_tz = pytz.UTC
        
        values = []
        processed_count = 0
        
        for datetime_str, prices in time_series.items():
            # Validar que el formato sea correcto antes de agregar
            try:
                # Parsear la fecha en la timezone del exchange
                if interval == 'daily':
                    # Formato: "2025-11-14"
                    dt_naive = datetime.strptime(datetime_str, '%Y-%m-%d')
                    # Asignar timezone del exchange (horario de mercado)
                    dt_exchange = exchange_tz.localize(dt_naive)
                else:
                    # Formato: "2025-11-14 20:00:00"
                    dt_naive = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
                    # Asignar timezone del exchange
                    dt_exchange = exchange_tz.localize(dt_naive)
                
                # Convertir a UTC
                dt_utc = dt_exchange.astimezone(utc_tz)

                values.append({
                    'datetime': dt_utc.strftime('%Y-%m-%d %H:%M:%S'),
                    'open': float(prices['1. open']),
                    'high': float(prices['2. high']), 
                    'low': float(prices['3. low']),
                    'close': float(prices['4. close']),
                    'volume': int(float(prices['5. volume']))
                })

                processed_count += 1

            except ValueError as e:
                if verbose:
                    print(f"    ⚠️  Alpha Vantage - Fecha inválida ignorada: {datetime_str} - Error: {e}")
                continue
            except KeyError as e:
                if verbose:
                    print(f"    ⚠️  Alpha Vantage - Campo faltante en {datetime_str}: {e}")
                continue
        
        # Ordenar por fecha (más reciente primero)
        if values:
            values.sort(key=lambda x: x['datetime'], reverse=True)
            
            if verbose:
                print(f"    🔄 Alpha Vantage - Convertido de {time_zone} a UTC")
                print(f"    ✅ Alpha Vantage - Procesados {processed_count} registros válidos de {len(time_series)} totales")
                # Mostrar ejemplo de conversión
                if values:
                    primer_valor = values[0]
                    ultimo_valor = values[-1]
                    primer_fecha_original = list(time_series.keys())[0]
                    print(f"    📊 Primer registro: {primer_fecha_original} {time_zone} -> {primer_valor['datetime']} UTC")
                    print(f"    📊 Último registro: {list(time_series.keys())[-1]} {time_zone} -> {ultimo_valor['datetime']} UTC")
                    print(f"    💰 Precio más reciente: {primer_valor['close']}")
            
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

        # Obtener timezone de la respuesta
        meta = result.get('meta', {})
        timezone = meta.get('timezone', 'UTC')
        gmt_offset = meta.get('gmtoffset', 0)  # Offset en segundos (-18000 = -5 horas para EST)
        
        values = []
        for i, timestamp in enumerate(timestamps):
            # CORRECCIÓN: Ajustar el timestamp restando el offset para convertirlo a UTC
            # Yahoo timestamps están en hora local del exchange, necesitamos convertirlos a UTC
            timestamp_utc = timestamp - gmt_offset
            
            # Convertir a datetime UTC
            dt_utc = datetime.utcfromtimestamp(timestamp_utc)
            
            # Formatear como string UTC
            dt_str = dt_utc.strftime('%Y-%m-%d %H:%M:%S')
            values.append({
                'datetime': dt_str,
                'open': float(quotes['open'][i]) if quotes['open'][i] is not None else 0,
                'high': float(quotes['high'][i]) if quotes['high'][i] is not None else 0,
                'low': float(quotes['low'][i]) if quotes['low'][i] is not None else 0,
                'close': float(quotes['close'][i]) if quotes['close'][i] is not None else 0,
                'volume': int(quotes['volume'][i]) if quotes['volume'][i] is not None else 0
            })
        
        # Ordenar por fecha (más reciente primero)
        if values:
            values.sort(key=lambda x: x['datetime'], reverse=True)
            
            if verbose:
                print(f"    🌍 Yahoo Finance - Timezone original: {timezone} (offset: {gmt_offset})")
                print(f"    🔄 Convertido a UTC para {symbol}")
                
            return {'values': values}
        else:
            if verbose:
                print(f"    ⚠️  Yahoo Finance - No se pudieron procesar registros válidos para {symbol}")
            return None
        
    except Exception as e:
        if verbose:
            print(f"    ❌ Error procesando Yahoo Finance: {e}")
        return None




def _validar_respuesta_api(data, symbol, api_name, verbose=False):
    """Valida la respuesta de cualquier API y convierte timezone si es necesario"""
    if not data or "values" not in data:
        if verbose:
            print(f"    ❌ {api_name} - Respuesta inválida para {symbol}")
        return None
    
    if not data["values"]:
        if verbose:
            print(f"    ⚠️  {api_name} - No hay datos para {symbol}")
        return None
    
    # Para Twelve Data, verificar si necesitamos convertir timezone
    if api_name == "Twelve Data" and "meta" in data:
        exchange_timezone = data["meta"].get("exchange_timezone", "UTC")
        if exchange_timezone != "UTC":
            if verbose:
                print(f"    🌍 Twelve Data - Convirtiendo de {exchange_timezone} a UTC")
            data = _convertir_twelve_data_a_utc(data, exchange_timezone, verbose)
    
    # Verificar datos futuros/ficticios
    primer_registro = data["values"][0]
    fecha_primer = primer_registro.get('datetime', '')
    
    if fecha_primer:
        try:
            fecha_actual = datetime.now()
            fecha_primer_dt = datetime.strptime(fecha_primer, '%Y-%m-%d %H:%M:%S')
            
            # Calcular diferencia con fecha actual
            diferencia = fecha_actual - fecha_primer_dt
            horas_retraso = diferencia.total_seconds() / 3600
            
            if horas_retraso > 24:  # Más de 24 horas de retraso
                print(f"    ⚠️  ALERTA: {api_name} tiene {horas_retraso:.1f} horas de retraso para {symbol}")
                print(f"    ⚠️  Último dato: {fecha_primer} vs Actual: {fecha_actual.strftime('%Y-%m-%d %H:%M:%S')}")
                # No retornar None, solo mostrar advertencia
                
            if fecha_primer_dt > fecha_actual + timedelta(hours=24):
                print(f"    ⚠️  ALERTA: {api_name} devuelve datos futuros para {symbol}")
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
    
    # VERIFICACIÓN DE FECHAS
        from datetime import datetime
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"    ⏰ Fecha actual del sistema: {fecha_actual}")
    
    return data



def _convertir_twelve_data_a_utc(data, exchange_timezone, verbose=False):
    """Convierte las fechas de Twelve Data de la timezone del exchange a UTC"""
    try:
        import pytz
        from datetime import datetime
        
        # Mapear timezones
        tz_mapping = {
            'America/New_York': 'US/Eastern',
            'America/Chicago': 'US/Central',
            'America/Los_Angeles': 'US/Pacific',
            'America/Denver': 'US/Mountain',
            'UTC': 'UTC'
        }
        
        tz_name = tz_mapping.get(exchange_timezone, exchange_timezone)
        exchange_tz = pytz.timezone(tz_name)
        utc_tz = pytz.UTC
        
        values_convertidos = []
        
        for registro in data["values"]:
            datetime_str = registro['datetime']
            
            try:
                # Parsear la fecha en la timezone del exchange
                dt_naive = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
                dt_exchange = exchange_tz.localize(dt_naive)
                
                # Convertir a UTC
                dt_utc = dt_exchange.astimezone(utc_tz)
                
                # Crear nuevo registro con fecha UTC
                nuevo_registro = registro.copy()
                nuevo_registro['datetime'] = dt_utc.strftime('%Y-%m-%d %H:%M:%S')
                values_convertidos.append(nuevo_registro)
                
            except Exception as e:
                if verbose:
                    print(f"    ⚠️  Error convirtiendo fecha {datetime_str}: {e}")
                # Si hay error, mantener el registro original
                values_convertidos.append(registro)
        
        # Actualizar los datos con las fechas convertidas
        data["values"] = values_convertidos
        
        if verbose and values_convertidos:
            primer_original = data["values"][0]['datetime'] if data["values"] else "N/A"
            print(f"    ✅ Twelve Data - Conversión completada: {exchange_timezone} -> UTC")
            print(f"    📊 Ejemplo: {datetime_str} -> {values_convertidos[0]['datetime']}")
        
        return data
        
    except Exception as e:
        if verbose:
            print(f"    ❌ Error en conversión de timezone Twelve Data: {e}")
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
