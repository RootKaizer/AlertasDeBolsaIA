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



def calcular_ichimoku(df, conversion_period=9, base_period=26, leading_span_b_period=52, displacement=26, verbose=False, symbol=""):
    """
    Calcula el indicador Ichimoku Cloud para un DataFrame de pandas.
    
    Basado en: 'Ichimoku Charts' de Goichi Hosoda
    Componentes:
    - Tenkan-sen (Conversion Line): (9-period high + 9-period low)/2
    - Kijun-sen (Base Line): (26-period high + 26-period low)/2
    - Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2, desplazado 26 periodos
    - Senkou Span B (Leading Span B): (52-period high + 52-period low)/2, desplazado 26 periodos
    - Chikou Span (Lagging Span): Precio de cierre desplazado -26 periodos
    
    :param df: DataFrame con datos de mercado (debe tener High, Low, Close)
    :param conversion_period: Período para Tenkan-sen (por defecto 9)
    :param base_period: Período para Kijun-sen (por defecto 26)
    :param leading_span_b_period: Período para Senkou Span B (por defecto 52)
    :param displacement: Desplazamiento para spans líderes (por defecto 26)
    :param verbose: Si es True, muestra detalles del cálculo
    :param symbol: Símbolo del activo para mensajes debug
    :return: DataFrame con columnas adicionales de Ichimoku
    """
    if verbose:
        print(f"\n☁️  CÁLCULO ICHIMOKU CLOUD PARA {symbol}")
        print(f"   Parámetros: Conversion={conversion_period}, Base={base_period}, SpanB={leading_span_b_period}, Displacement={displacement}")
    
    # Verificar que tenemos los datos necesarios
    required_columns = ['High', 'Low', 'Close']
    if not all(col in df.columns for col in required_columns):
        if verbose:
            print(f"   ❌ Datos insuficientes para calcular Ichimoku. Se necesitan: {required_columns}")
        return df
    
    # Paso 1: Calcular Tenkan-sen (Conversion Line)
    if verbose:
        print(f"\n   🔄 PASO 1 - Tenkan-sen (Línea de Conversión):")
        print(f"      Tenkan = (Max(High, {conversion_period}) + Min(Low, {conversion_period})) / 2")
    
    tenkan_sen_high = df['High'].rolling(window=conversion_period).max()
    tenkan_sen_low = df['Low'].rolling(window=conversion_period).min()
    df['Ichimoku_Conversion'] = (tenkan_sen_high + tenkan_sen_low) / 2
    
    if verbose and len(df) >= conversion_period:
        print(f"      Tenkan = ({tenkan_sen_high.iloc[-1]:.2f} + {tenkan_sen_low.iloc[-1]:.2f}) / 2 = {df['Ichimoku_Conversion'].iloc[-1]:.2f}")
    
    # Paso 2: Calcular Kijun-sen (Base Line)
    if verbose:
        print(f"\n   📊 PASO 2 - Kijun-sen (Línea Base):")
        print(f"      Kijun = (Max(High, {base_period}) + Min(Low, {base_period})) / 2")
    
    kijun_sen_high = df['High'].rolling(window=base_period).max()
    kijun_sen_low = df['Low'].rolling(window=base_period).min()
    df['Ichimoku_Base'] = (kijun_sen_high + kijun_sen_low) / 2
    
    if verbose and len(df) >= base_period:
        print(f"      Kijun = ({kijun_sen_high.iloc[-1]:.2f} + {kijun_sen_low.iloc[-1]:.2f}) / 2 = {df['Ichimoku_Base'].iloc[-1]:.2f}")
    
    # Paso 3: Calcular Senkou Span A (Leading Span A)
    if verbose:
        print(f"\n   📈 PASO 3 - Senkou Span A (Span Líder A):")
        print(f"      Span A = (Tenkan + Kijun) / 2, desplazado {displacement} periodos")
    
    df['Ichimoku_Senkou_A'] = ((df['Ichimoku_Conversion'] + df['Ichimoku_Base']) / 2).shift(displacement)
    
    if verbose and len(df) >= displacement:
        current_idx = -1
        source_idx = -1 - displacement
        if abs(source_idx) <= len(df):
            tenkan = df['Ichimoku_Conversion'].iloc[source_idx]
            kijun = df['Ichimoku_Base'].iloc[source_idx]
            print(f"      Span A = ({tenkan:.2f} + {kijun:.2f}) / 2 = {df['Ichimoku_Senkou_A'].iloc[current_idx]:.2f} (desplazado)")
    
    # Paso 4: Calcular Senkou Span B (Leading Span B)
    if verbose:
        print(f"\n   📉 PASO 4 - Senkou Span B (Span Líder B):")
        print(f"      Span B = (Max(High, {leading_span_b_period}) + Min(Low, {leading_span_b_period})) / 2, desplazado {displacement}")
    
    senkou_b_high = df['High'].rolling(window=leading_span_b_period).max()
    senkou_b_low = df['Low'].rolling(window=leading_span_b_period).min()
    df['Ichimoku_Senkou_B'] = ((senkou_b_high + senkou_b_low) / 2).shift(displacement)
    
    if verbose and len(df) >= leading_span_b_period + displacement:
        current_idx = -1
        source_idx = -1 - displacement
        if abs(source_idx) <= len(df):
            high_max = senkou_b_high.iloc[source_idx]
            low_min = senkou_b_low.iloc[source_idx]
            print(f"      Span B = ({high_max:.2f} + {low_min:.2f}) / 2 = {df['Ichimoku_Senkou_B'].iloc[current_idx]:.2f} (desplazado)")
    
    # Paso 5: Calcular Chikou Span (Lagging Span)
    if verbose:
        print(f"\n   🔄 PASO 5 - Chikou Span (Span Rezagado):")
        print(f"      Chikou = Precio Close desplazado -{displacement} periodos")
    
    df['Ichimoku_Chikou'] = df['Close'].shift(-displacement)
    
    if verbose and len(df) > displacement:
        current_idx = -1
        future_idx = -1 + displacement
        if future_idx < 0:  # Si hay datos futuros disponibles
            print(f"      Chikou = Close[{future_idx}] = {df['Ichimoku_Chikou'].iloc[current_idx]:.2f}")
    
    if verbose and len(df) > 0:
        print(f"\n   🎯 RESULTADOS ICHIMOKU:")
        if not pd.isna(df['Ichimoku_Conversion'].iloc[-1]):
            print(f"      Tenkan-sen: {df['Ichimoku_Conversion'].iloc[-1]:.2f}")
            print(f"      Kijun-sen: {df['Ichimoku_Base'].iloc[-1]:.2f}")
            if not pd.isna(df['Ichimoku_Senkou_A'].iloc[-1]):
                print(f"      Senkou Span A: {df['Ichimoku_Senkou_A'].iloc[-1]:.2f}")
            if not pd.isna(df['Ichimoku_Senkou_B'].iloc[-1]):
                print(f"      Senkou Span B: {df['Ichimoku_Senkou_B'].iloc[-1]:.2f}")
            
            # Interpretación básica
            precio = df['Close'].iloc[-1]
            tenkan = df['Ichimoku_Conversion'].iloc[-1]
            kijun = df['Ichimoku_Base'].iloc[-1]
            
            if tenkan > kijun:
                tendencia = "🟢 TENDENCIA ALCISTA (Tenkan > Kijun)"
            elif tenkan < kijun:
                tendencia = "🔴 TENDENCIA BAJISTA (Tenkan < Kijun)"
            else:
                tendencia = "⚪ TENDENCIA NEUTRA"
            
            print(f"      Señal: {tendencia}")
    
    return df



def calcular_williams_r(df, periodo=14, verbose=False, symbol=""):
    """
    Calcula el indicador Williams %R para un DataFrame de pandas.
    
    Basado en: Larry Williams - 'The Secret of Selecting Stocks'
    Fórmula: %R = (Highest High - Close) / (Highest High - Lowest Low) * -100
    
    :param df: DataFrame con datos de mercado (debe tener High, Low, Close)
    :param periodo: Período para el cálculo (por defecto 14)
    :param verbose: Si es True, muestra detalles del cálculo
    :param symbol: Símbolo del activo para mensajes debug
    :return: DataFrame con columna adicional 'Williams_R'
    """
    if verbose:
        print(f"\n📉 CÁLCULO WILLIAMS %R PARA {symbol}")
        print(f"   Período: {periodo}")
        print(f"   Fórmula: %R = (Highest High - Close) / (Highest High - Lowest Low) × -100")
    
    # Verificar que tenemos los datos necesarios
    required_columns = ['High', 'Low', 'Close']
    if not all(col in df.columns for col in required_columns):
        if verbose:
            print(f"   ❌ Datos insuficientes para calcular Williams %R. Se necesitan: {required_columns}")
        return df
    
    # Paso 1: Calcular Highest High y Lowest Low del período
    if verbose:
        print(f"\n   📈 PASO 1 - Calcular máximos y mínimos del período {periodo}:")
        print(f"      Highest High = max(High[{periodo}])")
        print(f"      Lowest Low = min(Low[{periodo}])")
    
    highest_high = df['High'].rolling(window=periodo).max()
    lowest_low = df['Low'].rolling(window=periodo).min()
    
    if verbose and len(df) >= periodo:
        print(f"      Highest High: {highest_high.iloc[-1]:.2f}")
        print(f"      Lowest Low: {lowest_low.iloc[-1]:.2f}")
    
    # Paso 2: Calcular Williams %R
    if verbose:
        print(f"\n   📊 PASO 2 - Calcular Williams %R:")
        print(f"      %R = (Highest High - Close) / (Highest High - Lowest Low) × -100")
    
    williams_r = ((highest_high - df['Close']) / (highest_high - lowest_low)) * -100
    
    if verbose and len(df) >= periodo:
        numerador = highest_high.iloc[-1] - df['Close'].iloc[-1]
        denominador = highest_high.iloc[-1] - lowest_low.iloc[-1]
        print(f"      %R = ({highest_high.iloc[-1]:.2f} - {df['Close'].iloc[-1]:.2f}) / ({highest_high.iloc[-1]:.2f} - {lowest_low.iloc[-1]:.2f}) × -100")
        print(f"          = {numerador:.2f} / {denominador:.2f} × -100 = {williams_r.iloc[-1]:.2f}")
    
    df['Williams_R'] = williams_r
    
    if verbose and len(df) > 0:
        print(f"\n   🎯 RESULTADO WILLIAMS %R:")
        if not pd.isna(williams_r.iloc[-1]):
            print(f"      Williams %R: {williams_r.iloc[-1]:.2f}")
            
            r_value = williams_r.iloc[-1]
            if r_value <= -80:
                señal = "🟢 SOBREVENTA EXTREMA (%R ≤ -80)"
            elif r_value >= -20:
                señal = "🔴 SOBRECOMPRA EXTREMA (%R ≥ -20)"
            elif r_value <= -50:
                señal = "🟢 POSIBLE REVERSIÓN ALCISTA (%R ≤ -50)"
            elif r_value >= -50:
                señal = "🔴 POSIBLE REVERSIÓN BAJISTA (%R ≥ -50)"
            else:
                señal = "⚪ ZONA NEUTRA"
            
            print(f"      Señal: {señal}")
    
    return df



def calcular_adx(df, periodo=14, verbose=False, symbol=""):
    """
    Calcula el ADX (Average Directional Index) para un DataFrame de pandas.
    
    Basado en: J. Welles Wilder - 'New Concepts in Technical Trading Systems'
    Componentes:
    - +DI (Positive Directional Indicator)
    - -DI (Negative Directional Indicator) 
    - ADX (Average Directional Movement Index)
    
    :param df: DataFrame con datos de mercado (debe tener High, Low, Close)
    :param periodo: Período para el cálculo (por defecto 14)
    :param verbose: Si es True, muestra detalles del cálculo
    :param symbol: Símbolo del activo para mensajes debug
    :return: DataFrame con columnas adicionales 'ADX', 'DI_Plus', 'DI_Minus'
    """
    if verbose:
        print(f"\n📏 CÁLCULO ADX (Average Directional Index) PARA {symbol}")
        print(f"   Período: {periodo}")
    
    # Verificar que tenemos los datos necesarios
    required_columns = ['High', 'Low', 'Close']
    if not all(col in df.columns for col in required_columns):
        if verbose:
            print(f"   ❌ Datos insuficientes para calcular ADX. Se necesitan: {required_columns}")
        return df
    
    # Paso 1: Calcular True Range (TR)
    if verbose:
        print(f"\n   🔄 PASO 1 - Calcular True Range (TR):")
        print(f"      TR = max(High - Low, |High - Close_prev|, |Low - Close_prev|)")
    
    high_low = df['High'] - df['Low']
    high_close_prev = abs(df['High'] - df['Close'].shift(1))
    low_close_prev = abs(df['Low'] - df['Close'].shift(1))
    
    tr = pd.concat([high_low, high_close_prev, low_close_prev], axis=1).max(axis=1)
    
    if verbose and len(df) > 1:
        print(f"      TR actual: {tr.iloc[-1]:.2f}")
    
    # Paso 2: Calcular Directional Movement (+DM y -DM)
    if verbose:
        print(f"\n   📈 PASO 2 - Calcular Directional Movement:")
        print(f"      +DM = High - High_prev (si > 0 y > |Low - Low_prev|)")
        print(f"      -DM = Low_prev - Low (si > 0 y > |High - High_prev|)")
    
    up_move = df['High'] - df['High'].shift(1)
    down_move = df['Low'].shift(1) - df['Low']
    
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
    
    # Convertir a Series de pandas
    plus_dm = pd.Series(plus_dm, index=df.index)
    minus_dm = pd.Series(minus_dm, index=df.index)
    
    if verbose and len(df) > 1:
        print(f"      +DM: {plus_dm.iloc[-1]:.2f}")
        print(f"      -DM: {minus_dm.iloc[-1]:.2f}")
    
    # Paso 3: Calcular smoothed averages usando el método de Wilder
    if verbose:
        print(f"\n   📊 PASO 3 - Calcular promedios suavizados (método Wilder):")
        print(f"      Usando factor de suavizado: 1/{periodo}")
    
    # True Range smoothed
    tr_smooth = tr.ewm(alpha=1/periodo, adjust=False).mean()
    
    # Directional Movement smoothed
    plus_dm_smooth = plus_dm.ewm(alpha=1/periodo, adjust=False).mean()
    minus_dm_smooth = minus_dm.ewm(alpha=1/periodo, adjust=False).mean()
    
    # Paso 4: Calcular +DI y -DI
    if verbose:
        print(f"\n   ⚖️  PASO 4 - Calcular +DI y -DI:")
        print(f"      +DI = 100 × (+DM_smooth / TR_smooth)")
        print(f"      -DI = 100 × (-DM_smooth / TR_smooth)")
    
    plus_di = 100 * (plus_dm_smooth / tr_smooth)
    minus_di = 100 * (minus_dm_smooth / tr_smooth)
    
    if verbose and len(df) >= periodo:
        print(f"      +DI = 100 × ({plus_dm_smooth.iloc[-1]:.2f} / {tr_smooth.iloc[-1]:.2f}) = {plus_di.iloc[-1]:.2f}")
        print(f"      -DI = 100 × ({minus_dm_smooth.iloc[-1]:.2f} / {tr_smooth.iloc[-1]:.2f}) = {minus_di.iloc[-1]:.2f}")
    
    # Paso 5: Calcular DX y ADX
    if verbose:
        print(f"\n   📐 PASO 5 - Calcular DX y ADX:")
        print(f"      DX = 100 × |(+DI - -DI)| / (+DI + -DI)")
        print(f"      ADX = EMA({periodo}) de DX")
    
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx = dx.ewm(alpha=1/periodo, adjust=False).mean()
    
    if verbose and len(df) >= periodo:
        print(f"      DX = 100 × |{plus_di.iloc[-1]:.2f} - {minus_di.iloc[-1]:.2f}| / ({plus_di.iloc[-1]:.2f} + {minus_di.iloc[-1]:.2f})")
        print(f"          = {dx.iloc[-1]:.2f}")
        print(f"      ADX = {adx.iloc[-1]:.2f}")
    
    df['ADX'] = adx
    df['DI_Plus'] = plus_di
    df['DI_Minus'] = minus_di
    
    if verbose and len(df) > 0:
        print(f"\n   🎯 RESULTADOS ADX:")
        if not pd.isna(adx.iloc[-1]):
            print(f"      ADX: {adx.iloc[-1]:.2f} (Fuerza de tendencia)")
            print(f"      +DI: {plus_di.iloc[-1]:.2f} (Tendencia alcista)")
            print(f"      -DI: {minus_di.iloc[-1]:.2f} (Tendencia bajista)")
            
            # Interpretación
            adx_value = adx.iloc[-1]
            plus_di_value = plus_di.iloc[-1]
            minus_di_value = minus_di.iloc[-1]
            
            if adx_value > 25:
                fuerza = "FUERTE TENDENCIA"
                if plus_di_value > minus_di_value:
                    direccion = "🟢 ALCISTA (+DI > -DI)"
                else:
                    direccion = "🔴 BAJISTA (-DI > +DI)"
            elif adx_value > 20:
                fuerza = "TENDENCIA MODERADA"
                direccion = "🟡 DIRECCIÓN INDEFINIDA"
            else:
                fuerza = "SIN TENDENCIA CLARA"
                direccion = "⚪ MERCADO LATERAL"
            
            print(f"      Interpretación: {fuerza}, {direccion}")
    
    return df



def calcular_parabolic_sar(df, acceleration=0.02, maximum=0.2, verbose=False, symbol=""):
    """
    Calcula el Parabolic SAR para un DataFrame de pandas.
    
    Basado en: J. Welles Wilder - 'The Parabolic Time/Price System'
    Fórmula compleja que sigue la tendencia y se acelera con el tiempo
    
    :param df: DataFrame con datos de mercado (debe tener High, Low)
    :param acceleration: Factor de aceleración inicial (por defecto 0.02)
    :param maximum: Factor de aceleración máximo (por defecto 0.2)
    :param verbose: Si es True, muestra detalles del cálculo
    :param symbol: Símbolo del activo para mensajes debug
    :return: DataFrame con columna adicional 'Parabolic_SAR'
    """
    if verbose:
        print(f"\n🎯 CÁLCULO PARABOLIC SAR PARA {symbol}")
        print(f"   Parámetros: Acceleration={acceleration}, Maximum={maximum}")
        print(f"   Algoritmo: Sigue la tendencia y se acelera en dirección de la tendencia")
    
    # Verificar que tenemos los datos necesarios
    required_columns = ['High', 'Low']
    if not all(col in df.columns for col in required_columns):
        if verbose:
            print(f"   ❌ Datos insuficientes para calcular Parabolic SAR. Se necesitan: {required_columns}")
        return df
    
    # Inicializar arrays para el cálculo
    high = df['High'].values
    low = df['Low'].values
    sar = np.zeros(len(df))
    trend = np.zeros(len(df))
    ep = np.zeros(len(df))
    af = np.zeros(len(df))
    
    # Inicializar primeros valores
    sar[0] = low[0]  # SAR inicial
    trend[0] = 1     # 1 = tendencia alcista, -1 = tendencia bajista
    ep[0] = high[0]  # Extreme Point
    af[0] = acceleration  # Acceleration Factor
    
    # Calcular Parabolic SAR para cada período
    for i in range(1, len(df)):
        # SAR anterior
        sar_prev = sar[i-1]
        trend_prev = trend[i-1]
        ep_prev = ep[i-1]
        af_prev = af[i-1]
        
        # Calcular SAR provisional
        sar_provisional = sar_prev + af_prev * (ep_prev - sar_prev)
        
        if trend_prev == 1:  # Tendencias alcistas
            sar[i] = min(sar_provisional, low[i-1], low[i-2] if i >= 2 else low[i-1])
            
            # Verificar reversión
            if low[i] < sar[i]:
                trend[i] = -1
                sar[i] = max(high[i], high[i-1])
                ep[i] = low[i]
                af[i] = acceleration
            else:
                trend[i] = 1
                if high[i] > ep_prev:
                    ep[i] = high[i]
                    af[i] = min(af_prev + acceleration, maximum)
                else:
                    ep[i] = ep_prev
                    af[i] = af_prev
                    
        else:  # Tendencias bajistas
            sar[i] = max(sar_provisional, high[i-1], high[i-2] if i >= 2 else high[i-1])
            
            # Verificar reversión
            if high[i] > sar[i]:
                trend[i] = 1
                sar[i] = min(low[i], low[i-1])
                ep[i] = high[i]
                af[i] = acceleration
            else:
                trend[i] = -1
                if low[i] < ep_prev:
                    ep[i] = low[i]
                    af[i] = min(af_prev + acceleration, maximum)
                else:
                    ep[i] = ep_prev
                    af[i] = af_prev
    
    df['Parabolic_SAR'] = sar
    
    if verbose and len(df) > 0:
        print(f"\n   🎯 RESULTADO PARABOLIC SAR:")
        print(f"      Parabolic SAR actual: {sar[-1]:.2f}")
        
        # Interpretación
        current_sar = sar[-1]
        current_close = df['Close'].iloc[-1] if 'Close' in df.columns else (df['High'].iloc[-1] + df['Low'].iloc[-1]) / 2
        
        if current_close > current_sar:
            señal = "🟢 TENDENCIA ALCISTA (Precio > SAR)"
        else:
            señal = "🔴 TENDENCIA BAJISTA (Precio < SAR)"
        
        print(f"      Precio: {current_close:.2f}")
        print(f"      Señal: {señal}")
        print(f"      Factor de Aceleración actual: {af[-1]:.3f}")
    
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