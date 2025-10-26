import pandas as pd
import numpy as np




def calcular_rsi(df, periodo=14, verbose=False, symbol=""):
    """
    Calcula el RSI (Relative Strength Index) para un DataFrame de pandas.
    :param df: DataFrame con datos de mercado.
    :param periodo: Período para calcular el RSI (por defecto 14).
    :param verbose: Si es True, muestra detalles del cálculo
    :param symbol: Símbolo del activo para mensajes debug
    :return: DataFrame con una columna adicional 'RSI'.
    """
    if verbose:
        print(f"\n📊 CÁLCULO RSI PARA {symbol}")
        print(f"   Fórmula: RSI = 100 - (100 / (1 + RS))")
        print(f"   Donde RS = Ganancia Promedio / Pérdida Promedio")
        print(f"   Período: {periodo}")
        if len(df) >= periodo:
            print(f"   📈 Datos utilizados (últimos {periodo+1} cierres):")
            print(f"      Precios Close: {df['Close'].tail(periodo+1).tolist()}")
    
    #  Paso 1: Calcular diferencias diarias
    delta = df['Close'].diff()

    if verbose and len(df) > 1:
        print(f"\n   🔄 PASO 1 - Diferencias diarias (Δ = Close[t] - Close[t-1]):")
        print(f"      Diferencias: {delta.tail(periodo).tolist()}")
    
    # Paso 2: Separar ganancias y pérdidas
    ganancia = delta.where(delta > 0, 0)
    perdida = (-delta).where(delta < 0, 0)
    
    if verbose and len(df) > 1:
        print(f"\n   📊 PASO 2 - Separar ganancias y pérdidas:")
        print(f"      Ganancias (solo Δ > 0): {ganancia.tail(periodo).tolist()}")
        print(f"      Pérdidas (solo Δ < 0, valor absoluto): {perdida.tail(periodo).tolist()}")
    
    # Paso 3: Calcular promedios móviles de ganancias y pérdidas
    ganancia_promedio = ganancia.rolling(window=periodo).mean()
    perdida_promedio = perdida.rolling(window=periodo).mean()

    if verbose and len(df) >= periodo:
        print(f"\n   📈 PASO 3 - Promedios móviles ({periodo} períodos):")
        print(f"      Ganancia Promedio: {ganancia_promedio.tail(5).tolist()}")
        print(f"      Pérdida Promedio: {perdida_promedio.tail(5).tolist()}")
        
        # Mostrar cálculo detallado del primer promedio
        if len(ganancia) >= periodo:
            ganancias_calculo = ganancia.iloc[-periodo:].tolist()
            perdidas_calculo = perdida.iloc[-periodo:].tolist()
            print(f"      Cálculo del último promedio:")
            print(f"        Suma ganancias: {sum(ganancias_calculo):.4f} / {periodo} = {ganancia_promedio.iloc[-1]:.4f}")
            print(f"        Suma pérdidas: {sum(perdidas_calculo):.4f} / {periodo} = {perdida_promedio.iloc[-1]:.4f}")
    
    # Paso 4: Calcular RS (Relative Strength)
    rs = ganancia_promedio / perdida_promedio
    
    if verbose and len(df) >= periodo:
        print(f"\n   ⚖️  PASO 4 - Relative Strength (RS):")
        print(f"      RS = Ganancia Promedio / Pérdida Promedio")
        if not pd.isna(ganancia_promedio.iloc[-1]) and not pd.isna(perdida_promedio.iloc[-1]):
            print(f"      RS = {ganancia_promedio.iloc[-1]:.4f} / {perdida_promedio.iloc[-1]:.4f} = {rs.iloc[-1]:.4f}")
    
    # Paso 5: Calcular RSI
    rsi = 100 - (100 / (1 + rs))
    
    df['RSI'] = rsi
    
    if verbose and len(df) > 0:
        print(f"\n   🎯 PASO 5 - Cálculo final RSI:")
        print(f"      RSI = 100 - (100 / (1 + RS))")
        print(f"      RSI = 100 - (100 / (1 + {rs.iloc[-1]:.4f})) = {rsi.iloc[-1]:.2f}")
        print(f"      RSI = {rsi.tail(periodo).tolist()}")
        #if not pd.isna(rsi.iloc[-1]):
            # Interpretación
            #interpretacion = "⬆️ SOBRECOMPRADO" if rsi.iloc[-1] > 70 else "⬇️ SOBREVENDIDO" if rsi.iloc[-1] < 30 else "➡️ NEUTRO"
            #print(f"      Interpretación: {interpretacion} (RSI: {rsi.iloc[-1]:.2f})")
    
    return df




def calcular_macd(df, periodo_corto=12, periodo_largo=26, periodo_senal=9, verbose=False, symbol=""):
    """
    Calcula el MACD, la señal MACD y el histograma MACD para un DataFrame de pandas.
    :param df: DataFrame con datos de mercado.
    :param periodo_corto: Período corto para el MACD (por defecto 12).
    :param periodo_largo: Período largo para el MACD (por defecto 26).
    :param periodo_senal: Período para la señal MACD (por defecto 9).
    :param verbose: Si es True, muestra detalles del cálculo
    :param symbol: Símbolo del activo para mensajes debug
    :return: DataFrame con columnas adicionales 'MACD', 'MACD_signal' y 'MACD_hist'.
    """
    if verbose:
        print(f"\n📈 CÁLCULO MACD PARA {symbol}")
        print(f"   Parámetros: EMA_corto={periodo_corto}, EMA_largo={periodo_largo}, Señal={periodo_senal}")
    
    # Paso 1: Calcular EMAs
    if verbose:
        print(f"\n   🔄 PASO 1 - Calcular EMAs (Exponential Moving Average):")
        print(f"      Fórmula: EMA_t = (Precio_t × α) + (EMA_{periodo_corto-1} × (1-α))")
        print(f"      Donde α = 2 / (período + 1)")
    
    ema_corto = df['Close'].ewm(span=periodo_corto, adjust=False).mean()
    ema_largo = df['Close'].ewm(span=periodo_largo, adjust=False).mean()
    
    if verbose and len(df) > 0:
        alpha_corto = 2 / (periodo_corto + 1)
        alpha_largo = 2 / (periodo_largo + 1)
        print(f"      α_corto = 2 / ({periodo_corto} + 1) = {alpha_corto:.4f}")
        print(f"      α_largo = 2 / ({periodo_largo} + 1) = {alpha_largo:.4f}")
        print(f"      EMA({periodo_corto}): {ema_corto.iloc[-1]:.4f}")
        print(f"      EMA({periodo_largo}): {ema_largo.iloc[-1]:.4f}")
    
    # Paso 2: Calcular MACD
    if verbose:
        print(f"\n   📊 PASO 2 - Calcular línea MACD:")
        print(f"      MACD = EMA({periodo_corto}) - EMA({periodo_largo})")
    
    macd = ema_corto - ema_largo
    
    if verbose and len(df) > 0:
        print(f"      MACD = {ema_corto.iloc[-1]:.4f} - {ema_largo.iloc[-1]:.4f} = {macd.iloc[-1]:.4f}")
    
    # Paso 3: Calcular señal MACD
    if verbose:
        print(f"\n   📈 PASO 3 - Calcular línea de Señal:")
        print(f"      Señal = EMA({periodo_senal}) del MACD")
    
    macd_signal = macd.ewm(span=periodo_senal, adjust=False).mean()
    
    if verbose and len(df) > 0:
        alpha_senal = 2 / (periodo_senal + 1)
        print(f"      α_señal = 2 / ({periodo_senal} + 1) = {alpha_senal:.4f}")
        print(f"      Señal MACD: {macd_signal.iloc[-1]:.4f}")
    
    # Paso 4: Calcular histograma MACD
    if verbose:
        print(f"\n   📉 PASO 4 - Calcular Histograma MACD:")
        print(f"      Histograma = MACD - Señal")
    
    macd_hist = macd - macd_signal
    
    if verbose and len(df) > 0:
        print(f"      Histograma = {macd.iloc[-1]:.4f} - {macd_signal.iloc[-1]:.4f} = {macd_hist.iloc[-1]:.4f}")
    
    # Crear y agregar datos a la columna MACD, MACD_signal, MACD_hist en la entrada de datos
    df['MACD'] = macd
    df['MACD_signal'] = macd_signal
    df['MACD_hist'] = macd_hist
    
    if verbose and len(df) > 0:
        print(f"   MACD: {macd.iloc[-1]:.4f}")
        print(f"   Señal MACD: {macd_signal.iloc[-1]:.4f}")
        print(f"   Histograma MACD: {macd_hist.iloc[-1]:.4f}")
        if not pd.isna(macd.iloc[-1]) and not pd.isna(macd_signal.iloc[-1]):
            señal = "🟢 COMPRA" if macd.iloc[-1] > macd_signal.iloc[-1] else "🔴 VENTA" if macd.iloc[-1] < macd_signal.iloc[-1] else "⚪ NEUTRO"
            print(f"   Señal: {señal} (MACD {'>' if macd.iloc[-1] > macd_signal.iloc[-1] else '<' if macd.iloc[-1] < macd_signal.iloc[-1] else '='} Señal)")

    return df




def calcular_media_movil(df, periodo=20, verbose=False, symbol=""):
    """
    Calcula la media móvil simple para un DataFrame de pandas.
    :param df: DataFrame con datos de mercado.
    :param periodo: Período para la media móvil (por defecto 20).
    :param verbose: Si es True, muestra detalles del cálculo
    :param symbol: Símbolo del activo para mensajes debug
    :return: DataFrame con una columna adicional 'MA'.
    """
    if verbose:
        print(f"\n📊 CÁLCULO MEDIA MÓVIL SIMPLE PARA {symbol}")
        print(f"   Período: {periodo}")
        if len(df) >= periodo:
            print(f"   📈 Datos utilizados (últimos {periodo} cierres):")
            print(f"      Precios: {df['Close'].tail(periodo).tolist()}")
    
    # Paso 1: Calcular suma de precios
    if verbose and len(df) >= periodo:
        precios_calculo = df['Close'].tail(periodo)
        suma = precios_calculo.sum()
        print(f"\n   ➕ PASO 1 - Suma de precios:")
        print(f"      Suma = {suma:.2f}")
    
    # Paso 2: Calcular media móvil
    if verbose:
        print(f"\n   📐 PASO 2 - Cálculo de media:")
        print(f"      Fórmula: MA = Σ(Precios de Cierre) / {periodo}")
    
    ma = df['Close'].rolling(window=periodo).mean()

    if verbose and len(df) >= periodo:
        print(f"      MA = {suma:.2f} / {periodo} = {ma.iloc[-1]:.4f}")
    
    # Crear y agregar datos a la columna MA en la entrada de datos
    df['MA'] = ma
    
    if verbose and len(df) > 0:
        print(f"\n   🎯 RESULTADO MEDIA MÓVIL:")
        print(f"      Media Móvil ({periodo}): {ma.iloc[-1]:.4f}" if not pd.isna(ma.iloc[-1]) else "      Media Móvil: N/A")
        if not pd.isna(ma.iloc[-1]):
            relación = "🟢 PRECIO > MA" if df['Close'].iloc[-1] > ma.iloc[-1] else "🔴 PRECIO < MA" if df['Close'].iloc[-1] < ma.iloc[-1] else "⚪ PRECIO = MA"
            print(f"      Relación: {relación}")
            print(f"      Precio actual: {df['Close'].iloc[-1]:.2f} vs MA: {ma.iloc[-1]:.2f}")
            diferencia = df['Close'].iloc[-1] - ma.iloc[-1]
            print(f"      Diferencia: {diferencia:+.2f} ({diferencia/ma.iloc[-1]*100:+.2f}%)")
    
    return df




def calcular_bandas_bollinger(df, periodo=20, desviacion=2, verbose=False, symbol=""):
    """
    Calcula las Bandas de Bollinger para un DataFrame de pandas.
    :param df: DataFrame con datos de mercado.
    :param periodo: Período para la media móvil (por defecto 20).
    :param desviacion: Desviación estándar para las bandas (por defecto 2).
    :return: DataFrame con columnas adicionales 'Bollinger_Upper' y 'Bollinger_Lower'.
    """
    if verbose:
        print(f"\n📏 CÁLCULO BANDAS BOLLINGER PARA {symbol}")
        print(f"   Parámetros: Período={periodo}, Desviación={desviacion}")
    
    # Paso 1: Calcular media móvil central
    if verbose:
        print(f"\n   📊 PASO 1 - Media móvil central:")
        print(f"      Banda Media = SMA({periodo})")
    
    bollinger_ma = df['Close'].rolling(window=periodo).mean()
    
    if verbose and len(df) >= periodo:
        print(f"      Banda Media = {bollinger_ma.iloc[-1]:.4f}")
    
    # Paso 2: Calcular desviación estándar
    if verbose:
        print(f"\n   📐 PASO 2 - Desviación estándar:")
        print(f"      Fórmula: σ = √[Σ(Precio - Media)² / N]")
    
    std = df['Close'].rolling(window=periodo).std()
    
    if verbose and len(df) >= periodo:
        print(f"      Desviación Estándar (σ): {std.iloc[-1]:.4f}")
    
    # Paso 3: Calcular bandas superior e inferior
    if verbose:
        print(f"\n   📈 PASO 3 - Bandas superior e inferior:")
        print(f"      Banda Superior = Media + ({desviacion} × σ)")
        print(f"      Banda Inferior = Media - ({desviacion} × σ)")
    
    bollinger_upper = bollinger_ma + (std * desviacion)
    bollinger_lower = bollinger_ma - (std * desviacion)
    
    if verbose and len(df) >= periodo:
        print(f"      Banda Superior = {bollinger_ma.iloc[-1]:.4f} + ({desviacion} × {std.iloc[-1]:.4f}) = {bollinger_upper.iloc[-1]:.4f}")
        print(f"      Banda Inferior = {bollinger_ma.iloc[-1]:.4f} - ({desviacion} × {std.iloc[-1]:.4f}) = {bollinger_lower.iloc[-1]:.4f}")
    
    # Crear y agregar datos a la columna Bollinger_MA, Bollinger_Upper, Bollinger_Lower en la entrada de datos
    df['Bollinger_MA'] = bollinger_ma
    df['Bollinger_Upper'] = bollinger_upper
    df['Bollinger_Lower'] = bollinger_lower
    
    if verbose and len(df) > 0:
        print(f"\n   🎯 RESULTADOS BANDAS BOLLINGER:")
        if not pd.isna(bollinger_ma.iloc[-1]):
            print(f"      Banda Media: {bollinger_ma.iloc[-1]:.4f}")
            print(f"      Banda Superior: {bollinger_upper.iloc[-1]:.4f}")
            print(f"      Banda Inferior: {bollinger_lower.iloc[-1]:.4f}")
            print(f"      Ancho de bandas: {bollinger_upper.iloc[-1] - bollinger_lower.iloc[-1]:.4f}")
            print(f"      Precio actual: {df['Close'].iloc[-1]:.4f}")
            
            precio = df['Close'].iloc[-1]
            if precio > bollinger_upper.iloc[-1]:
                posición = "🔴 SOBRE COMPRA (por encima de banda superior)"
            elif precio < bollinger_lower.iloc[-1]:
                posición = "🟢 SOBRE VENTA (por debajo de banda inferior)"
            else:
                posición = "⚪ DENTRO DE LAS BANDAS"
                # Calcular posición relativa dentro de las bandas
                rango_total = bollinger_upper.iloc[-1] - bollinger_lower.iloc[-1]
                posicion_relativa = (precio - bollinger_lower.iloc[-1]) / rango_total * 100
                posición += f" ({posicion_relativa:.1f}% desde abajo)"
            print(f"      Posición: {posición}")
    
    return df
    




def calcular_estocastico(df, periodo=14, verbose=False, symbol=""):
    """
    Calcula el indicador Estocástico para un DataFrame de pandas.
    :param df: DataFrame con datos de mercado.
    :param periodo: Período para el cálculo (por defecto 14).
    :param verbose: Si es True, muestra detalles del cálculo
    :param symbol: Símbolo del activo para mensajes debug
    :return: DataFrame con columnas adicionales '%K' y '%D'.
    """
    if verbose:
        print(f"\n🎯 CÁLCULO ESTOCÁSTICO PARA {symbol}")
        print(f"   Período: {periodo}")
        if len(df) >= periodo:
            print(f"   📊 Datos utilizados (últimos {periodo} períodos):")
            print(f"      Highs: {df['High'].tail(periodo).tolist()}")
            print(f"      Lows: {df['Low'].tail(periodo).tolist()}")
            print(f"      Closes: {df['Close'].tail(periodo).tolist()}")
    
    # Paso 1: Calcular mínimos y máximos del período
    if verbose:
        print(f"\n   📈 PASO 1 - Calcular rangos del período:")
        print(f"      Mínimo {periodo} = min(Lows[{periodo}])")
        print(f"      Máximo {periodo} = max(Highs[{periodo}])")
    
    lowest_low = df['Low'].rolling(window=periodo).min()
    highest_high = df['High'].rolling(window=periodo).max()
    
    if verbose and len(df) >= periodo:
        print(f"      Mínimo {periodo}: {lowest_low.iloc[-1]:.2f}")
        print(f"      Máximo {periodo}: {highest_high.iloc[-1]:.2f}")
    
    # Paso 2: Calcular %K
    if verbose:
        print(f"\n   📊 PASO 2 - Calcular %K (Línea rápida):")
        print(f"      Fórmula: %K = 100 × (Cierre - Mínimo{periodo}) / (Máximo{periodo} - Mínimo{periodo})")
    
    k = 100 * (df['Close'] - lowest_low) / (highest_high - lowest_low)
    
    if verbose and len(df) >= periodo:
        numerador = df['Close'].iloc[-1] - lowest_low.iloc[-1]
        denominador = highest_high.iloc[-1] - lowest_low.iloc[-1]
        print(f"      %K = 100 × ({df['Close'].iloc[-1]:.2f} - {lowest_low.iloc[-1]:.2f}) / ({highest_high.iloc[-1]:.2f} - {lowest_low.iloc[-1]:.2f})")
        print(f"          = 100 × {numerador:.2f} / {denominador:.2f} = {k.iloc[-1]:.2f}")
    
    # Paso 3: Calcular %D (media móvil de %K)
    if verbose:
        print(f"\n   📈 PASO 3 - Calcular %D (Línea lenta):")
        print(f"      %D = SMA(3) de %K")
    
    d = k.rolling(window=3).mean()
    
    if verbose and len(df) >= 3:
        print(f"      %D = promedio de últimos 3 valores %K")
        if len(k) >= 3:
            k_values = k.tail(3).tolist()
            print(f"      %D = ({k_values[0]:.2f} + {k_values[1]:.2f} + {k_values[2]:.2f}) / 3 = {d.iloc[-1]:.2f}")
    
    # Crear y agregar datos a la columna (Línea rápida)%K, (Línea lenta)%D en la entrada de datos
    df['%K'] = k
    df['%D'] = d
    
    if verbose and len(df) > 0:
        print(f"\n   🎯 RESULTADOS ESTOCÁSTICO:")
        if not pd.isna(k.iloc[-1]):
            print(f"      %K (Línea rápida): {k.iloc[-1]:.2f}")
            print(f"      %D (Línea lenta): {d.iloc[-1]:.2f}" if not pd.isna(d.iloc[-1]) else "      %D: N/A")
            
            k_value = k.iloc[-1]
            d_value = d.iloc[-1] if not pd.isna(d.iloc[-1]) else 0
            
            if k_value > 80 and d_value > 80:
                señal = "🔴 SOBRECOMPRADO (ambos > 80)"
            elif k_value < 20 and d_value < 20:
                señal = "🟢 SOBREVENDIDO (ambos < 20)"
            elif k_value > d_value:
                señal = "🟢 CRUCE ALCISTA (%K > %D)"
            elif k_value < d_value:
                señal = "🔴 CRUCE BAJISTA (%K < %D)"
            else:
                señal = "⚪ NEUTRO"
            print(f"      Señal: {señal}")
    
    return df




'''
# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo de datos simulados
    datos_historicos = {
        "AAPL": {
            "values": [
                {"datetime": "2025-03-10 15:30:00", "open": "226.99", "high": "228.64", "low": "226.5", "close": "227.54", "volume": "8057482"},
                {"datetime": "2025-03-10 13:30:00", "open": "225.24", "high": "227.51", "low": "224.42", "close": "226.97", "volume": "12470689"}
            ]
        }
    }
    
    # Convertir a DataFrame
    dataframes = convertir_a_dataframe(datos_historicos)
    for symbol, df in dataframes.items():
        print(f"\n{'='*60}")
        print(f"PRUEBA DE CÁLCULOS CON DEBUG PARA {symbol}")
        print(f"{'='*60}")
        
        # Probar cada función con verbose=True
        df = calcular_rsi(df, verbose=True, symbol=symbol)
        df = calcular_macd(df, verbose=True, symbol=symbol)
        df = calcular_media_movil(df, verbose=True, symbol=symbol)
        df = calcular_bandas_bollinger(df, verbose=True, symbol=symbol)
        df = calcular_estocastico(df, verbose=True, symbol=symbol)
        
        print(f"\nDatos de {symbol} con métricas calculadas:")
        print(df)
'''