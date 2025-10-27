# NotificationLogicSender.py
from typing import Union, Tuple, List, Dict, Any
import json
from pathlib import Path
from datetime import datetime
import pytz


def comparar_y_notificar(
    resultados_anteriores: Dict,
    resultados_actuales: Dict,
    estrategia: str,
    mobile_list_notification: str,
    log_whatsapp_message: str,
    verbose: bool = False
) -> Union[str, Tuple[List[str], str]]:
    """
    Compara los resultados anteriores con los actuales y prepara notificaciones si hay cambios.
    """
    if verbose:
        print(f"\n🔍 COMPARANDO RESULTADOS - Estrategia: {estrategia}")
        print(f"   📊 PASO 1 - Verificar datos anteriores:")
    
    if not resultados_anteriores:
        mensaje = "Primera ejecución - No hay resultados anteriores para comparar"
        if verbose:
            print(f"      ❌ {mensaje}")
        return mensaje

    if verbose:
        print(f"      ✅ Resultados anteriores cargados ({len(resultados_anteriores)} símbolos)")
        print(f"\n   📈 PASO 2 - Generar comparación completa:")

    cambios = []
    comparacion_completa = generar_comparacion_completa(resultados_anteriores, resultados_actuales, verbose)
    
    if verbose:
        print(f"      ✅ Comparación generada para {len(comparacion_completa)} símbolos")
        print(f"\n   🔄 PASO 3 - Detectar cambios significativos:")

    # Verificar si hay cambios
    hay_cambios = False
    for mercado, datos in comparacion_completa.items():
        if verbose:
            print(f"      Analizando {mercado}...")
        
        for indicador, valores in datos['analisis_comparativo'].items():
            anterior = valores['anterior'].get('accion', 'N/A')
            actual = valores['actual'].get('accion', 'N/A')
            
            if anterior != actual:
                cambio_msg = f"Cambio en {mercado} ({indicador}): De {anterior} a {actual}"
                cambios.append(cambio_msg)
                hay_cambios = True
                
                if verbose:
                    print(f"        🔄 {cambio_msg}")
            else:
                if verbose:
                    print(f"        ✅ {mercado} ({indicador}): Sin cambios ({anterior})")
    
    if verbose:
        print(f"\n   📊 RESUMEN DE CAMBIOS:")
        print(f"      Total de cambios detectados: {len(cambios)}")
        print(f"      ¿Hay cambios significativos? {'✅ SÍ' if hay_cambios else '❌ NO'}")

    if not hay_cambios:
        resultado = "No se detectaron cambios significativos desde la última ejecución."
        if verbose:
            print(f"\n   📨 PASO 4 - Preparar notificación:")
            print(f"      {resultado}")
        
        numeros = leer_numeros_whatsapp(mobile_list_notification)
        registrar_en_log(log_whatsapp_message, numeros if numeros else [], resultado, list(comparacion_completa.values()), estrategia)
        
        if verbose:
            print(f"      📝 Registrado en log: {len(numeros)} números")
        
        return resultado if not numeros else (numeros, resultado)

    if verbose:
        print(f"\n   📨 PASO 4 - Preparar notificación con cambios:")

    numeros = leer_numeros_whatsapp(mobile_list_notification)
    if not numeros:
        resultado = "No hay números configurados para enviar notificaciones."
        if verbose:
            print(f"      ❌ {resultado}")
        return resultado
    
    # Construir mensaje detallado
    mensaje = f"🔔 *Actualización de Trading ({estrategia})* 🔔\n\n"
    mensaje += "📈 *Cambios detectados:*\n"
    
    for cambio in cambios:
        mensaje += f"• {cambio}\n"
    
    # Agregar resumen de fuerzas de señal
    mensaje += "\n💪 *Resumen de señales actuales:*\n"
    for mercado, datos in comparacion_completa.items():
        fuerza_actual = datos['analisis_comparativo'].get('fuerza_señal', {}).get('actual', {}).get('accion', 'N/A')
        decision_actual = datos['analisis_comparativo'].get('estrategia_combinada', {}).get('actual', {}).get('accion', 'N/A')
        mensaje += f"• {mercado}: {decision_actual} (Fuerza: {fuerza_actual})\n"

    if verbose:
        print(f"      ✅ Mensaje preparado: {len(cambios)} cambios")
        print(f"      📱 Números destino: {len(numeros)}")
        print(f"      📝 Contenido del mensaje:")
        print(f"        {mensaje[:100]}...")  # Mostrar primeros 100 caracteres

    registrar_en_log(log_whatsapp_message, numeros, mensaje, list(comparacion_completa.values()), estrategia)
    
    if verbose:
        print(f"      ✅ Notificación registrada en log")
    
    return numeros, mensaje



def generar_comparacion_completa(anteriores: Dict, actuales: Dict, verbose: bool = False) -> Dict[str, Any]:
    """
    Genera una comparación completa de todos los mercados e indicadores.
    """
    if verbose:
        print(f"      Generando comparación completa...")
    
    todos_mercados = set(anteriores.keys()).union(set(actuales.keys()))
    comparacion = {}
    
    for mercado in todos_mercados:
        if verbose:
            print(f"        Procesando {mercado}...")
        
        datos_anteriores = anteriores.get(mercado, {})
        datos_actuales = actuales.get(mercado, {})
        
        comparacion[mercado] = {
            'mercado': mercado,
            'analisis_comparativo': {}
        }
        
        # Obtener el último registro de cada DataFrame
        if len(datos_anteriores) > 0:
            ultimo_anterior = datos_anteriores.iloc[-1].to_dict()
        else:
            ultimo_anterior = {}
            
        if len(datos_actuales) > 0:
            ultimo_actual = datos_actuales.iloc[-1].to_dict()
        else:
            ultimo_actual = {}
        
        # Comparar solo las columnas de estrategia
        columnas_estrategia = [col for col in ultimo_actual.keys() if 'estrategia' in col or 'fuerza' in col]
        
        for col in columnas_estrategia:
            comparacion[mercado]['analisis_comparativo'][col] = {
                'anterior': {'accion': ultimo_anterior.get(col, 'N/A')},
                'actual': {'accion': ultimo_actual.get(col, 'N/A')}
            }
    
    if verbose:
        print(f"      ✅ Comparación completa generada")
    
    return comparacion



def leer_numeros_whatsapp(ruta_archivo: str) -> List[str]:
    """
    Lee los números de teléfono desde el archivo de configuración.
    """
    try:
        with open(ruta_archivo, 'r') as file:
            numeros = [line.strip() for line in file if line.strip()]
        return numeros
    except Exception as e:
        print(f"Error al leer números WhatsApp: {e}")
        return []
    


def registrar_en_log(log_whatsapp_message, numeros: List[str], mensaje: str, cambios: List[Dict[str, Any]], estrategia: str):
    """Registra los detalles del mensaje enviado en un archivo de log."""
    log_file = Path(log_whatsapp_message)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    tz_bogota = pytz.timezone('America/Bogota')
    fecha_hora = datetime.now(tz_bogota).strftime('%Y-%m-%d %H:%M:%S %Z')
    
    log_entry = {
        'fecha_hora': fecha_hora,
        'estrategia': estrategia,
        'numeros_destino': numeros,
        'mensaje': mensaje,
        'comparacion_completa': cambios
    }
    
    try:
        if not log_file.exists():
            with open(log_file, 'w') as f:
                json.dump([log_entry], f, indent=4, ensure_ascii=False)
        else:
            with open(log_file, 'r+') as f:
                try:
                    data = json.load(f)
                    data.append(log_entry)
                    f.seek(0)
                    json.dump(data, f, indent=4, ensure_ascii=False)
                except json.JSONDecodeError:
                    json.dump([log_entry], f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error al escribir en el archivo de log: {e}")








'''
# Ejemplo de uso para pruebas
if __name__ == "__main__":
    # Datos de prueba
    print("🧪 PROBANDO NOTIFICATION LOGIC CON DEBUG:")
    print("=" * 60)
    
    # Crear DataFrames de prueba con columnas de estrategia
    resultados_test_antes = {
        "AAPL": pd.DataFrame({
            'estrategia_rsi': ['COMPRA', 'HOLD'],
            'estrategia_macd': ['VENTA', 'COMPRA'],
            'estrategia_combinada': ['HOLD', 'COMPRA'],
            'fuerza_señal': [0.2, 0.6]
        }),
        "MSFT": pd.DataFrame({
            'estrategia_rsi': ['VENTA', 'HOLD'],
            'estrategia_macd': ['VENTA', 'VENTA'],
            'estrategia_combinada': ['VENTA', 'VENTA'],
            'fuerza_señal': [-0.8, -0.6]
        })
    }
    
    resultados_test_ahora = {
        "AAPL": pd.DataFrame({
            'estrategia_rsi': ['COMPRA', 'COMPRA'],
            'estrategia_macd': ['COMPRA', 'COMPRA'],
            'estrategia_combinada': ['COMPRA', 'COMPRA'],
            'fuerza_señal': [0.2, 0.8]
        }),
        "MSFT": pd.DataFrame({
            'estrategia_rsi': ['HOLD', 'COMPRA'],
            'estrategia_macd': ['VENTA', 'HOLD'],
            'estrategia_combinada': ['VENTA', 'HOLD'],
            'fuerza_señal': [-0.8, 0.0]
        }),
        "GOOG": pd.DataFrame({
            'estrategia_rsi': ['COMPRA', 'COMPRA'],
            'estrategia_macd': ['COMPRA', 'COMPRA'],
            'estrategia_combinada': ['COMPRA', 'COMPRA'],
            'fuerza_señal': [0.6, 0.6]
        })
    }
    
    # Prueba con debug activado
    resultado = comparar_y_notificar(
        resultados_test_antes,
        resultados_test_ahora,
        "mediano_plazo",
        "/tmp/test_numbers.txt",
        "/tmp/test_log.json",
        verbose=True
    )
    
    print(f"\n🎯 RESULTADO FINAL: {resultado}")
'''