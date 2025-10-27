import pandas as pd
import numpy as np
from datetime import datetime
import pytz



# =============================================================================
# FUNCIÓN PRINCIPAL CON **KWARGS (ESCALABLE)
# =============================================================================

def analizar_dataframes(dataframes, verbose=False, **kwargs):
    """
    Función principal que coordina todos los análisis técnicos.
    Usa **kwargs para recibir parámetros de manera escalable.
    """
    resultados = {}
    
    # Extraer parámetros de kwargs con valores por defecto
    rsi_under = kwargs.get('rsi_under', 14)
    rsi_upper = kwargs.get('rsi_upper', 14)
    rsi_periodo = kwargs.get('rsi_periodo', 14)
    macd_periodo_corto = kwargs.get('macd_periodo_corto', 12)
    macd_periodo_largo = kwargs.get('macd_periodo_largo', 26)
    macd_periodo_senal = kwargs.get('macd_periodo_senal', 9)
    media_movil_periodo = kwargs.get('media_movil_periodo', 20)
    bollinger_periodo = kwargs.get('bollinger_periodo', 20)
    bollinger_desviacion = kwargs.get('bollinger_desviacion', 2.0)
    estocastico_periodo = kwargs.get('estocastico_periodo', 14)
    periodo_volatilidad = kwargs.get('periodo_volatilidad', 20)
    combinacion_indicadores = kwargs.get('combinacion_indicadores', ['rsi', 'macd', 'media_movil', 'bollinger', 'estocastico', 'volatilidad'])
    combinacion_nombres = kwargs.get('combinacion_nombres', ['Default_Strategy'])

    
    for symbol, df in dataframes.items():
        if verbose:
            print(f"\n{'='*80}")
            print(f"🎯 ANÁLISIS TÉCNICO COMPLETO PARA: {symbol}")
            print(f"{'='*80}")
            print(f"   Parámetros de configuración:")
            print(f"     - RSI: under={rsi_under}, upper={rsi_upper}, periodo={rsi_periodo}")
            print(f"     - MACD: corto={macd_periodo_corto}, largo={macd_periodo_largo}, señal={macd_periodo_senal}")
            print(f"     - Media Móvil: periodo={media_movil_periodo}")
            print(f"     - Bollinger: periodo={bollinger_periodo}, desviación={bollinger_desviacion}")
            print(f"     - Estocástico: periodo={estocastico_periodo}")
            print(f"     - Volatilidad: periodo={periodo_volatilidad}")
            print(f"     - Combinación: {combinacion_indicadores}")
            print(f"     - Nombres Estrategias: {combinacion_nombres}")
        
        df_analizado = df.copy()
        
        # Aplicar estrategias según la combinación configurada
        if 'rsi' in combinacion_indicadores:
            df_analizado = analizar_estrategia_rsi(df_analizado, rsi_under, rsi_upper, rsi_periodo, verbose)
        if 'macd' in combinacion_indicadores:
            df_analizado = analizar_estrategia_macd(df_analizado, macd_periodo_corto, macd_periodo_largo, macd_periodo_senal, verbose)
        if 'media_movil' in combinacion_indicadores:
            df_analizado = analizar_estrategia_media_movil(df_analizado, media_movil_periodo, verbose)
        if 'bollinger' in combinacion_indicadores:
            df_analizado = analizar_estrategia_bollinger(df_analizado, bollinger_periodo, bollinger_desviacion, verbose)
        if 'estocastico' in combinacion_indicadores:
            df_analizado = analizar_estrategia_estocastico(df_analizado, estocastico_periodo, verbose)
        if 'volatilidad' in combinacion_indicadores:
            df_analizado = analizar_estrategia_volatilidad(df_analizado, periodo_volatilidad, verbose)
        if 'ichimoku' in combinacion_indicadores:
            df_analizado = analizar_estrategia_ichimoku(df_analizado, verbose)
        if 'williams' in combinacion_indicadores:
            df_analizado = analizar_estrategia_williams(df_analizado, estocastico_periodo, verbose)
        if 'adx' in combinacion_indicadores:
            df_analizado = analizar_estrategia_adx(df_analizado, 14, verbose)
        if 'parabolic_sar' in combinacion_indicadores:
            df_analizado = analizar_estrategia_parabolic_sar(df_analizado, verbose)


        # Calcular Estrategia mayoritaria
        df_analizado = calcular_estrategia_mayoritaria(df_analizado, combinacion_indicadores)
        
        resultados[symbol] = df_analizado
        
        # Mostrar tabla de últimos registros (SIEMPRE se muestra)
        mostrar_ultimos_registros(symbol, df_analizado, combinacion_indicadores, combinacion_nombres)
    
    return resultados



# =============================================================================
# ESTRATEGIAS INDIVIDUALES (PARÁMETROS EXPLÍCITOS)
# =============================================================================

def analizar_estrategia_rsi(df, rsi_under, rsi_upper, rsi_periodo, verbose=False):
    """
    Análisis RSI usando los valores ya calculados en el DataFrame.
    """
    df_analizado = df.copy()
    
    # VERIFICAR que RSI existe en el DataFrame
    if 'RSI' not in df_analizado.columns:
        if verbose:
            print(f"      ❌ RSI no encontrado en el DataFrame")
        return df_analizado
    
    # Estrategia RSI avanzada - USANDO EL RSI YA CALCULADO
    condiciones = [
        (df_analizado['RSI'] < rsi_under),
        (df_analizado['RSI'] > rsi_upper), 
        (df_analizado['RSI'] >= rsi_under) & (df_analizado['RSI'] <= 40),
        (df_analizado['RSI'] >= 60) & (df_analizado['RSI'] <= rsi_upper),
        (df_analizado['RSI'] > 40) & (df_analizado['RSI'] < 60)
    ]
    
    decisiones = ['COMPRA_FUERTE', 'VENTA_FUERTE', 'COMPRA', 'VENTA', 'HOLD']
    df_analizado['estrategia_rsi'] = np.select(condiciones, decisiones, default='HOLD')
    
    # Valores y descripciones
    df_analizado['estrategia_rsi_valor'] = df_analizado['RSI']
    df_analizado['estrategia_rsi_descripcion'] = df_analizado.apply(
        lambda x: f"RSI {x['RSI']:.1f} (Periodo: {rsi_periodo}) - " + 
                 ("SOBREVENTA FUERTE" if x['estrategia_rsi'] == 'COMPRA_FUERTE' else
                  "SOBRECOMPRA FUERTE" if x['estrategia_rsi'] == 'VENTA_FUERTE' else
                  "POSIBLE REVERSIÓN ALCISTA" if x['estrategia_rsi'] == 'COMPRA' else
                  "POSIBLE REVERSIÓN BAJISTA" if x['estrategia_rsi'] == 'VENTA' else
                  "ZONA NEUTRAL") + 
                 f" | Umbrales: {rsi_under}/{rsi_upper}", axis=1
    )
    
    if verbose and len(df_analizado) > 0:
        ultimo = df_analizado.iloc[-1]
        print(f"\n   📊 ANÁLISIS RSI:")
        print(f"      RSI calculado (periodo {rsi_periodo}): {ultimo['RSI']:.2f}")
        print(f"      Umbrales configurados: Compra < {rsi_under}, Venta > {rsi_upper}")
        print(f"      Señal generada: {ultimo['estrategia_rsi']}")
        print(f"      Interpretación: {ultimo['estrategia_rsi_descripcion']}")
    
    return df_analizado



def analizar_estrategia_macd(df, periodo_corto, periodo_largo, periodo_senal, verbose=False):
    """
    Análisis MACD usando los valores ya calculados en el DataFrame.
    """
    df_analizado = df.copy()
    
    # VERIFICAR que MACD existe en el DataFrame
    if 'MACD' not in df_analizado.columns or 'MACD_signal' not in df_analizado.columns:
        if verbose:
            print(f"      ❌ MACD no encontrado en el DataFrame")
        return df_analizado
    
    # USAR LOS VALORES YA CALCULADOS
    df_analizado['MACD_histogram'] = df_analizado['MACD'] - df_analizado['MACD_signal']
    
    # Estrategia MACD
    condiciones = [
        (df_analizado['MACD'] > df_analizado['MACD_signal']) & (df_analizado['MACD_histogram'] > 0),
        (df_analizado['MACD'] < df_analizado['MACD_signal']) & (df_analizado['MACD_histogram'] < 0),
        (df_analizado['MACD'] > df_analizado['MACD_signal']),
        (df_analizado['MACD'] < df_analizado['MACD_signal']),
        (df_analizado['MACD'] == df_analizado['MACD_signal'])
    ]
    
    decisiones = ['COMPRA_FUERTE', 'VENTA_FUERTE', 'COMPRA', 'VENTA', 'HOLD']
    df_analizado['estrategia_macd'] = np.select(condiciones, decisiones, default='HOLD')
    
    # Valores y descripciones
    df_analizado['estrategia_macd_valor'] = df_analizado['MACD_histogram']
    df_analizado['estrategia_macd_descripcion'] = df_analizado.apply(
        lambda x: f"MACD( {periodo_corto}/{periodo_largo}/{periodo_senal}): {x['MACD']:.4f} - " +
                 f"Señal: {x['MACD_signal']:.4f} - Hist: {x['MACD_histogram']:.4f} | " +
                 ("CRUCE ALCISTA FUERTE" if x['estrategia_macd'] == 'COMPRA_FUERTE' else
                  "CRUCE BAJISTA FUERTE" if x['estrategia_macd'] == 'VENTA_FUERTE' else
                  "CRUCE ALCISTA" if x['estrategia_macd'] == 'COMPRA' else
                  "CRUCE BAJISTA" if x['estrategia_macd'] == 'VENTA' else
                  "SIN CRUCE CLARO"), axis=1
    )
    
    if verbose and len(df_analizado) > 0:
        ultimo = df_analizado.iloc[-1]
        print(f"\n   📈 ANÁLISIS MACD:")
        print(f"      Parámetros: EMA({periodo_corto}) - EMA({periodo_largo}), Señal({periodo_senal})")
        print(f"      Línea MACD: {ultimo['MACD']:.4f}")
        print(f"      Línea Señal: {ultimo['MACD_signal']:.4f}")
        print(f"      Histograma: {ultimo['MACD_histogram']:.4f}")
        print(f"      Señal: {ultimo['estrategia_macd']}")
        print(f"      Interpretación: {ultimo['estrategia_macd_descripcion']}")
    
    return df_analizado



def analizar_estrategia_media_movil(df, media_movil_periodo, verbose=False):
    """
    Análisis de Media Móvil usando los valores ya calculados en el DataFrame.
    """
    df_analizado = df.copy()
    
    # VERIFICAR que MA existe en el DataFrame
    if 'MA' not in df_analizado.columns:
        if verbose:
            print(f"      ❌ Media Móvil no encontrada en el DataFrame")
        return df_analizado
    
    # Estrategia Media Móvil
    condiciones = [
        (df_analizado['Close'] > df_analizado['MA']),
        (df_analizado['Close'] < df_analizado['MA']),
        (df_analizado['Close'] == df_analizado['MA'])
    ]
    
    decisiones = ['COMPRA', 'VENTA', 'HOLD']
    df_analizado['estrategia_ma'] = np.select(condiciones, decisiones, default='HOLD')
    
    # Valores y descripciones
    df_analizado['estrategia_ma_valor'] = df_analizado['Close'] - df_analizado['MA']
    df_analizado['estrategia_ma_descripcion'] = df_analizado.apply(
        lambda x: f"Precio: {x['Close']:.2f}, MA({media_movil_periodo}): {x['MA']:.2f} - " +
                 ("PRECIO ARRIBA DE MA" if x['estrategia_ma'] == 'COMPRA' else
                  "PRECIO DEBAJO DE MA" if x['estrategia_ma'] == 'VENTA' else
                  "PRECIO EN LA MA") + 
                 f" | Diferencia: {x['Close'] - x['MA']:.2f}", axis=1
    )
    
    if verbose and len(df_analizado) > 0:
        ultimo = df_analizado.iloc[-1]
        print(f"\n   📊 ANÁLISIS MEDIA MÓVIL:")
        print(f"      Media Móvil (periodo {media_movil_periodo}): {ultimo['MA']:.2f}")
        print(f"      Precio actual: {ultimo['Close']:.2f}")
        print(f"      Diferencia: {ultimo['Close'] - ultimo['MA']:.2f}")
        print(f"      Señal: {ultimo['estrategia_ma']}")
        print(f"      Interpretación: {ultimo['estrategia_ma_descripcion']}")
    
    return df_analizado



def analizar_estrategia_bollinger(df, bollinger_periodo, bollinger_desviacion, verbose=False):
    """
    Análisis Bandas de Bollinger usando los valores ya calculados en el DataFrame.
    """
    df_analizado = df.copy()
    
    # VERIFICAR que Bollinger existe en el DataFrame
    if 'Bollinger_Upper' not in df_analizado.columns or 'Bollinger_Lower' not in df_analizado.columns:
        if verbose:
            print(f"      ❌ Bandas de Bollinger no encontradas en el DataFrame")
        return df_analizado
    
    # Calcular posición relativa dentro de las bandas
    df_analizado['Bollinger_Position'] = (df_analizado['Close'] - df_analizado['Bollinger_Lower']) / (df_analizado['Bollinger_Upper'] - df_analizado['Bollinger_Lower'])
    
    # Estrategia Bollinger
    condiciones = [
        (df_analizado['Close'] > df_analizado['Bollinger_Upper']),
        (df_analizado['Close'] < df_analizado['Bollinger_Lower']),
        (df_analizado['Close'] <= df_analizado['Bollinger_Upper']) & (df_analizado['Close'] >= df_analizado['Bollinger_Lower'])
    ]
    
    decisiones = ['VENTA', 'COMPRA', 'HOLD']
    df_analizado['estrategia_bollinger'] = np.select(condiciones, decisiones, default='HOLD')
    
    # Valores y descripciones
    df_analizado['estrategia_bollinger_valor'] = df_analizado['Bollinger_Position']
    df_analizado['estrategia_bollinger_descripcion'] = df_analizado.apply(
        lambda x: f"Posición: {x['Bollinger_Position']:.2f} - " +
                 ("SOBRECOMPRA" if x['estrategia_bollinger'] == 'VENTA' else
                  "SOBREVENTA" if x['estrategia_bollinger'] == 'COMPRA' else
                  "DENTRO DE BANDAS") + 
                 f" | Bandas({bollinger_periodo}, {bollinger_desviacion}σ)", axis=1
    )
    
    if verbose and len(df_analizado) > 0:
        ultimo = df_analizado.iloc[-1]
        print(f"\n   📏 ANÁLISIS BOLLINGER:")
        print(f"      Parámetros: Periodo={bollinger_periodo}, Desviación={bollinger_desviacion}")
        print(f"      Banda Superior: {ultimo['Bollinger_Upper']:.2f}")
        print(f"      Banda Inferior: {ultimo['Bollinger_Lower']:.2f}")
        print(f"      Precio: {ultimo['Close']:.2f}")
        print(f"      Posición en bandas: {ultimo['Bollinger_Position']:.2f}")
        print(f"      Señal: {ultimo['estrategia_bollinger']}")
        print(f"      Interpretación: {ultimo['estrategia_bollinger_descripcion']}")
    
    return df_analizado



def analizar_estrategia_estocastico(df, estocastico_periodo, verbose=False):
    """
    Análisis Estocástico usando los valores ya calculados en el DataFrame.
    """
    df_analizado = df.copy()
    
    # VERIFICAR que Estocástico existe en el DataFrame
    if '%K' not in df_analizado.columns or '%D' not in df_analizado.columns:
        if verbose:
            print(f"      ❌ Estocástico no encontrado en el DataFrame")
        return df_analizado
    
    # Estrategia Estocástico
    condiciones = [
        (df_analizado['%K'] > 80) & (df_analizado['%D'] > 80),
        (df_analizado['%K'] < 20) & (df_analizado['%D'] < 20),
        (df_analizado['%K'] > df_analizado['%D']),
        (df_analizado['%K'] < df_analizado['%D'])
    ]
    
    decisiones = ['VENTA', 'COMPRA', 'COMPRA', 'VENTA']
    df_analizado['estrategia_estocastico'] = np.select(condiciones, decisiones, default='HOLD')
    
    # Valores y descripciones
    df_analizado['estrategia_estocastico_valor'] = (df_analizado['%K'] + df_analizado['%D']) / 2
    df_analizado['estrategia_estocastico_descripcion'] = df_analizado.apply(
        lambda x: f"%K: {x['%K']:.1f}, %D: {x['%D']:.1f} (Periodo: {estocastico_periodo}) - " +
                 ("SOBRECOMPRA" if x['estrategia_estocastico'] == 'VENTA' else
                  "SOBREVENTA" if x['estrategia_estocastico'] == 'COMPRA' else
                  "CRUCE ALCISTA" if x['estrategia_estocastico'] == 'COMPRA' else
                  "CRUCE BAJISTA" if x['estrategia_estocastico'] == 'VENTA' else
                  "ZONA NEUTRAL"), axis=1
    )
    
    if verbose and len(df_analizado) > 0:
        ultimo = df_analizado.iloc[-1]
        print(f"\n   🎯 ANÁLISIS ESTOCÁSTICO:")
        print(f"      Estocástico (periodo {estocastico_periodo}): %K={ultimo['%K']:.2f}, %D={ultimo['%D']:.2f}")
        print(f"      Diferencia: {ultimo['%K'] - ultimo['%D']:.2f}")
        print(f"      Señal: {ultimo['estrategia_estocastico']}")
        print(f"      Interpretación: {ultimo['estrategia_estocastico_descripcion']}")
    
    return df_analizado



def analizar_estrategia_volatilidad(df, periodo_volatilidad=20, verbose=False):
    """
    Análisis de Volatilidad usando los datos del DataFrame.
    """
    df_analizado = df.copy()
    
    # Calcular volatilidad basada en los precios de cierre
    df_analizado['Returns'] = df_analizado['Close'].pct_change()
    df_analizado['Volatility'] = df_analizado['Returns'].rolling(window=periodo_volatilidad).std() * np.sqrt(252) * 100
    
    # Calcular ATR si tenemos datos de High y Low
    if 'High' in df_analizado.columns and 'Low' in df_analizado.columns:
        high_low = df_analizado['High'] - df_analizado['Low']
        high_close = np.abs(df_analizado['High'] - df_analizado['Close'].shift())
        low_close = np.abs(df_analizado['Low'] - df_analizado['Close'].shift())
        true_range = np.maximum(np.maximum(high_low, high_close), low_close)
        df_analizado['ATR'] = true_range.rolling(window=periodo_volatilidad).mean()
        df_analizado['ATR_Percent'] = (df_analizado['ATR'] / df_analizado['Close']) * 100
    else:
        df_analizado['ATR_Percent'] = df_analizado['Volatility'] / 10  # Aproximación
    
    # Estrategia de Volatilidad
    volatilidad_media = df_analizado['Volatility'].mean()
    condiciones = [
        (df_analizado['Volatility'] > volatilidad_media * 1.5) & (df_analizado['Close'] > df_analizado['Close'].shift(5)),
        (df_analizado['Volatility'] > volatilidad_media * 1.5) & (df_analizado['Close'] < df_analizado['Close'].shift(5)),
        (df_analizado['Volatility'] < volatilidad_media * 0.7),
        (df_analizado['ATR_Percent'] > df_analizado['ATR_Percent'].mean())
    ]
    
    decisiones = ['COMPRA', 'VENTA', 'HOLD', 'COMPRA']
    df_analizado['estrategia_volatilidad'] = np.select(condiciones, decisiones, default='HOLD')
    
    # Valores y descripciones
    df_analizado['estrategia_volatilidad_valor'] = df_analizado['Volatility']
    df_analizado['estrategia_volatilidad_descripcion'] = df_analizado.apply(
        lambda x: f"Volatilidad: {x['Volatility']:.1f}%, ATR: {x.get('ATR_Percent', 0):.2f}% - " +
                 ("ALTA VOL + TENDENCIA ALCISTA" if x['estrategia_volatilidad'] == 'COMPRA' else
                  "ALTA VOL + TENDENCIA BAJISTA" if x['estrategia_volatilidad'] == 'VENTA' else
                  "BAJA VOL (BREAKOUT INMINENTE)" if x['estrategia_volatilidad'] == 'HOLD' else
                  "MOVIMIENTO DIRECCIONAL" if x['estrategia_volatilidad'] == 'COMPRA' else
                  "VOLATILIDAD NORMAL"), axis=1
    )
    
    if verbose and len(df_analizado) > 0:
        ultimo = df_analizado.iloc[-1]
        print(f"\n   🌪️  ANÁLISIS VOLATILIDAD:")
        print(f"      Volatilidad Anualizada: {ultimo['Volatility']:.2f}%")
        print(f"      ATR: {ultimo.get('ATR_Percent', 0):.2f}%")
        print(f"      Volatilidad Media: {volatilidad_media:.2f}%")
        print(f"      Señal: {ultimo['estrategia_volatilidad']}")
        print(f"      Interpretación: {ultimo['estrategia_volatilidad_descripcion']}")
    
    return df_analizado



# =============================================================================
# NUEVAS ESTRATEGIAS AVANZADAS
# =============================================================================

def analizar_estrategia_ichimoku(df, verbose=False):
    """
    Análisis Ichimoku Cloud usando los valores calculados en el DataFrame.
    Basado en: 'Ichimoku Charts' de Goichi Hosoda
    """
    df_analizado = df.copy()
    
    # VERIFICAR que Ichimoku existe en el DataFrame
    if 'Ichimoku_Conversion' not in df_analizado.columns or 'Ichimoku_Base' not in df_analizado.columns:
        if verbose:
            print(f"      ❌ Ichimoku no encontrado en el DataFrame")
        return df_analizado
    
    # Estrategia Ichimoku
    condiciones = [
        # Señal fuerte de compra: Precio arriba de la nube, Tenkan-sen > Kijun-sen, Senkou Span A > Senkou Span B
        (df_analizado['Close'] > df_analizado['Ichimoku_Senkou_A']) & 
        (df_analizado['Close'] > df_analizado['Ichimoku_Senkou_B']) &
        (df_analizado['Ichimoku_Conversion'] > df_analizado['Ichimoku_Base']),
        
        # Señal fuerte de venta: Precio debajo de la nube, Tenkan-sen < Kijun-sen, Senkou Span A < Senkou Span B
        (df_analizado['Close'] < df_analizado['Ichimoku_Senkou_A']) & 
        (df_analizado['Close'] < df_analizado['Ichimoku_Senkou_B']) &
        (df_analizado['Ichimoku_Conversion'] < df_analizado['Ichimoku_Base']),
        
        # Señal de compra: Precio arriba de la nube
        (df_analizado['Close'] > df_analizado['Ichimoku_Senkou_A']) & 
        (df_analizado['Close'] > df_analizado['Ichimoku_Senkou_B']),
        
        # Señal de venta: Precio debajo de la nube
        (df_analizado['Close'] < df_analizado['Ichimoku_Senkou_A']) & 
        (df_analizado['Close'] < df_analizado['Ichimoku_Senkou_B'])
    ]
    
    decisiones = ['COMPRA_FUERTE', 'VENTA_FUERTE', 'COMPRA', 'VENTA']
    df_analizado['estrategia_ichimoku'] = np.select(condiciones, decisiones, default='HOLD')
    
    # Valores y descripciones
    df_analizado['estrategia_ichimoku_valor'] = df_analizado['Ichimoku_Conversion'] - df_analizado['Ichimoku_Base']
    df_analizado['estrategia_ichimoku_descripcion'] = df_analizado.apply(
        lambda x: f"Ichimoku: Tenkan={x['Ichimoku_Conversion']:.2f}, Kijun={x['Ichimoku_Base']:.2f} | " +
                 ("FUERTE TENDENCIA ALCISTA" if x['estrategia_ichimoku'] == 'COMPRA_FUERTE' else
                  "FUERTE TENDENCIA BAJISTA" if x['estrategia_ichimoku'] == 'VENTA_FUERTE' else
                  "TENDENCIA ALCISTA" if x['estrategia_ichimoku'] == 'COMPRA' else
                  "TENDENCIA BAJISTA" if x['estrategia_ichimoku'] == 'VENTA' else
                  "TENDENCIA LATERAL"), axis=1
    )
    
    if verbose and len(df_analizado) > 0:
        ultimo = df_analizado.iloc[-1]
        print(f"\n   ☁️  ANÁLISIS ICHIMOKU:")
        print(f"      Tenkan-sen: {ultimo['Ichimoku_Conversion']:.2f}")
        print(f"      Kijun-sen: {ultimo['Ichimoku_Base']:.2f}")
        print(f"      Nube Superior: {ultimo['Ichimoku_Senkou_A']:.2f}")
        print(f"      Nube Inferior: {ultimo['Ichimoku_Senkou_B']:.2f}")
        print(f"      Señal: {ultimo['estrategia_ichimoku']}")
        print(f"      Interpretación: {ultimo['estrategia_ichimoku_descripcion']}")
    
    return df_analizado



def analizar_estrategia_williams(df, williams_periodo=14, verbose=False):
    """
    Análisis Williams %R.
    Basado en: Larry Williams - 'The Secret of Selecting Stocks'
    """
    df_analizado = df.copy()
    
    # VERIFICAR que Williams %R existe en el DataFrame
    if 'Williams_R' not in df_analizado.columns:
        if verbose:
            print(f"      ❌ Williams %R no encontrado en el DataFrame")
        return df_analizado
    
    # Estrategia Williams %R
    condiciones = [
        (df_analizado['Williams_R'] < -80),  # Sobreventa extrema
        (df_analizado['Williams_R'] > -20),  # Sobrecopra extrema
        (df_analizado['Williams_R'] < -50) & (df_analizado['Williams_R'] > df_analizado['Williams_R'].shift(1)),  # Mejora desde sobreventa
        (df_analizado['Williams_R'] > -50) & (df_analizado['Williams_R'] < df_analizado['Williams_R'].shift(1))   # Empeora desde sobrecompra
    ]
    
    decisiones = ['COMPRA_FUERTE', 'VENTA_FUERTE', 'COMPRA', 'VENTA']
    df_analizado['estrategia_williams'] = np.select(condiciones, decisiones, default='HOLD')
    
    # Valores y descripciones
    df_analizado['estrategia_williams_valor'] = df_analizado['Williams_R']
    df_analizado['estrategia_williams_descripcion'] = df_analizado.apply(
        lambda x: f"Williams %R: {x['Williams_R']:.1f} (Periodo: {williams_periodo}) - " +
                 ("SOBREVENTA EXTREMA" if x['estrategia_williams'] == 'COMPRA_FUERTE' else
                  "SOBRECOMPRA EXTREMA" if x['estrategia_williams'] == 'VENTA_FUERTE' else
                  "MEJORA ALCISTA" if x['estrategia_williams'] == 'COMPRA' else
                  "EMPEORA BAJISTA" if x['estrategia_williams'] == 'VENTA' else
                  "ZONA NEUTRAL"), axis=1
    )
    
    if verbose and len(df_analizado) > 0:
        ultimo = df_analizado.iloc[-1]
        print(f"\n   📉 ANÁLISIS WILLIAMS %R:")
        print(f"      Williams %R: {ultimo['Williams_R']:.2f}")
        print(f"      Umbrales: Compra < -80, Venta > -20")
        print(f"      Señal: {ultimo['estrategia_williams']}")
        print(f"      Interpretación: {ultimo['estrategia_williams_descripcion']}")
    
    return df_analizado



def analizar_estrategia_adx(df, adx_periodo=14, verbose=False):
    """
    Análisis ADX (Average Directional Index).
    Basado en: J. Welles Wilder - 'New Concepts in Technical Trading Systems'
    """
    df_analizado = df.copy()
    
    # VERIFICAR que ADX existe en el DataFrame
    if 'ADX' not in df_analizado.columns or 'DI_Plus' not in df_analizado.columns or 'DI_Minus' not in df_analizado.columns:
        if verbose:
            print(f"      ❌ ADX no encontrado en el DataFrame")
        return df_analizado
    
    # Estrategia ADX
    condiciones = [
        # Fuerte tendencia alcista
        (df_analizado['ADX'] > 25) & (df_analizado['DI_Plus'] > df_analizado['DI_Minus']),
        # Fuerte tendencia bajista
        (df_analizado['ADX'] > 25) & (df_analizado['DI_Plus'] < df_analizado['DI_Minus']),
        # Tendencia alcista débil
        (df_analizado['ADX'] > 20) & (df_analizado['DI_Plus'] > df_analizado['DI_Minus']),
        # Tendencia bajista débil
        (df_analizado['ADX'] > 20) & (df_analizado['DI_Plus'] < df_analizado['DI_Minus'])
    ]
    
    decisiones = ['COMPRA_FUERTE', 'VENTA_FUERTE', 'COMPRA', 'VENTA']
    df_analizado['estrategia_adx'] = np.select(condiciones, decisiones, default='HOLD')
    
    # Valores y descripciones
    df_analizado['estrategia_adx_valor'] = df_analizado['ADX']
    df_analizado['estrategia_adx_descripcion'] = df_analizado.apply(
        lambda x: f"ADX: {x['ADX']:.1f}, DI+: {x['DI_Plus']:.1f}, DI-: {x['DI_Minus']:.1f} - " +
                 ("FUERTE TENDENCIA ALCISTA" if x['estrategia_adx'] == 'COMPRA_FUERTE' else
                  "FUERTE TENDENCIA BAJISTA" if x['estrategia_adx'] == 'VENTA_FUERTE' else
                  "TENDENCIA ALCISTA" if x['estrategia_adx'] == 'COMPRA' else
                  "TENDENCIA BAJISTA" if x['estrategia_adx'] == 'VENTA' else
                  "SIN TENDENCIA CLARA"), axis=1
    )
    
    if verbose and len(df_analizado) > 0:
        ultimo = df_analizado.iloc[-1]
        print(f"\n   📏 ANÁLISIS ADX:")
        print(f"      ADX: {ultimo['ADX']:.2f} (Fuerza tendencia)")
        print(f"      DI+: {ultimo['DI_Plus']:.2f} (Tendencia alcista)")
        print(f"      DI-: {ultimo['DI_Minus']:.2f} (Tendencia bajista)")
        print(f"      Señal: {ultimo['estrategia_adx']}")
        print(f"      Interpretación: {ultimo['estrategia_adx_descripcion']}")
    
    return df_analizado



def analizar_estrategia_parabolic_sar(df, verbose=False):
    """
    Análisis Parabolic SAR.
    Basado en: J. Welles Wilder - 'The Parabolic Time/Price System'
    """
    df_analizado = df.copy()
    
    # VERIFICAR que Parabolic SAR existe en el DataFrame
    if 'Parabolic_SAR' not in df_analizado.columns:
        if verbose:
            print(f"      ❌ Parabolic SAR no encontrado en el DataFrame")
        return df_analizado
    
    # Estrategia Parabolic SAR
    condiciones = [
        (df_analizado['Close'] > df_analizado['Parabolic_SAR']),  # Precio arriba del SAR - tendencia alcista
        (df_analizado['Close'] < df_analizado['Parabolic_SAR'])   # Precio debajo del SAR - tendencia bajista
    ]
    
    decisiones = ['COMPRA', 'VENTA']
    df_analizado['estrategia_parabolic_sar'] = np.select(condiciones, decisiones, default='HOLD')
    
    # Valores y descripciones
    df_analizado['estrategia_parabolic_sar_valor'] = df_analizado['Close'] - df_analizado['Parabolic_SAR']
    df_analizado['estrategia_parabolic_sar_descripcion'] = df_analizado.apply(
        lambda x: f"SAR: {x['Parabolic_SAR']:.2f}, Precio: {x['Close']:.2f} - " +
                 ("TENDENCIA ALCISTA" if x['estrategia_parabolic_sar'] == 'COMPRA' else
                  "TENDENCIA BAJISTA" if x['estrategia_parabolic_sar'] == 'VENTA' else
                  "CAMBIO DE TENDENCIA"), axis=1
    )
    
    if verbose and len(df_analizado) > 0:
        ultimo = df_analizado.iloc[-1]
        print(f"\n   🎯 ANÁLISIS PARABOLIC SAR:")
        print(f"      Parabolic SAR: {ultimo['Parabolic_SAR']:.2f}")
        print(f"      Precio: {ultimo['Close']:.2f}")
        print(f"      Diferencia: {ultimo['Close'] - ultimo['Parabolic_SAR']:.2f}")
        print(f"      Señal: {ultimo['estrategia_parabolic_sar']}")
        print(f"      Interpretación: {ultimo['estrategia_parabolic_sar_descripcion']}")
    
    return df_analizado



# =============================================================================
# ESTRATEGIA MAYORITARIA ACTUALIZADA
# =============================================================================

def calcular_estrategia_mayoritaria(df, combinacion_indicadores):
    """
    Calcula la Estrategia mayoritaria basada en las estrategias individuales de la combinación.
    """
    df_combinado = df.copy()
    
    # Filtrar solo las estrategias de la combinación actual
    estrategias = []
    for indicador in combinacion_indicadores:
        nombre_estrategia = f'estrategia_{indicador}'
        if nombre_estrategia in df_combinado.columns:
            estrategias.append(nombre_estrategia)
    
    def calcular_consenso(row):
        # Ponderar señales fuertes vs débiles
        compras_fuertes = sum(2 for estrategia in estrategias if row.get(estrategia) == 'COMPRA_FUERTE')
        ventas_fuertes = sum(2 for estrategia in estrategias if row.get(estrategia) == 'VENTA_FUERTE')
        compras = sum(1 for estrategia in estrategias if row.get(estrategia) == 'COMPRA')
        ventas = sum(1 for estrategia in estrategias if row.get(estrategia) == 'VENTA')
        
        total_compras = compras_fuertes + compras
        total_ventas = ventas_fuertes + ventas
        
        if total_compras > total_ventas and total_compras >= len(estrategias) * 0.4:
            return 'COMPRA_FUERTE' if compras_fuertes >= len(estrategias) * 0.3 else 'COMPRA'
        elif total_ventas > total_compras and total_ventas >= len(estrategias) * 0.4:
            return 'VENTA_FUERTE' if ventas_fuertes >= len(estrategias) * 0.3 else 'VENTA'
        else:
            return 'HOLD'
    
    df_combinado['estrategia_mayoritaria'] = df_combinado.apply(calcular_consenso, axis=1)
    
    # Calcular fuerza de señal
    def calcular_fuerza_señal(row):
        señales = [row.get(estrategia, 'HOLD') for estrategia in estrategias]
        fuerza = sum(
            2 if s == 'COMPRA_FUERTE' else 
            1 if s == 'COMPRA' else
            -2 if s == 'VENTA_FUERTE' else
            -1 if s == 'VENTA' else 0
            for s in señales
        )
        return fuerza / (len(estrategias) * 2)  # Normalizar entre -1 y 1
    
    df_combinado['fuerza_señal'] = df_combinado.apply(calcular_fuerza_señal, axis=1)
    
    return df_combinado



# =============================================================================
# MOSTRAR ÚLTIMOS REGISTROS ACTUALIZADO
# =============================================================================

def mostrar_ultimos_registros(symbol, df_trading, combinacion_indicadores, combinacion_nombres):
    """
    Muestra los 10 últimos registros con formato completo, filtrando por la combinación de estrategia.
    """
    print(f"\n📊 ÚLTIMOS 10 REGISTROS - {symbol}")
    print(f"🎯 COMBINACIÓN ESTRATÉGICA: {', '.join(combinacion_nombres)}")
    print("=" * 120)
    
    # Filtrar columnas según la combinación de estrategia
    columnas_estrategia = []
    for indicador in combinacion_indicadores:
        columna = f'estrategia_{indicador}'
        if columna in df_trading.columns:
            columnas_estrategia.append(columna)
    
    columnas_basicas = ['datetime', 'Close']
    
    # Agregar la Estrategia mayoritaria al final
    columnas_mostrar = columnas_basicas + columnas_estrategia + ['estrategia_mayoritaria', 'fuerza_señal']
    
    # Tomar los últimos 10 registros
    df_reciente = df_trading[columnas_mostrar].tail(10)
    
    if len(df_reciente) == 0:
        print("No hay datos disponibles")
        return
    
    # Formatear fechas
    def formatear_fecha(fecha):
        try:
            if hasattr(fecha, 'strftime'):
                # Si ya tiene timezone, convertir a string
                if hasattr(fecha, 'tzinfo') and fecha.tzinfo is not None:
                    return fecha.strftime('%Y-%m-%d %H:%M:%S%z')
                else:
                    return fecha.strftime('%Y-%m-%d %H:%M:%S')
            else:
                return str(fecha)
        except:
            return str(fecha)
    
    df_reciente['datetime_formatted'] = df_reciente['datetime'].apply(formatear_fecha)
    
    # Encabezados
    headers = ["Fecha", "Precio"]
    headers.extend([col.replace('estrategia_', '').upper()[:8] for col in columnas_estrategia])
    headers.extend(["MAYORITARIA", "FUERZA"])
    
    # Imprimir tabla
    print(" | ".join(f"{header:>12}" for header in headers))
    print("-" * (len(headers) * 14))
    
    for idx, row in df_reciente.iterrows():
        # Fila básica
        fecha_str = row['datetime_formatted']
        if len(fecha_str) > 16:  # Si es muy larga, acortar
            fecha_str = fecha_str[11:16]  # Solo hora:minuto
        
        fila = [fecha_str, f"{row['Close']:.2f}"]
        
        # Decisiones de estrategia
        for col in columnas_estrategia:
            decision = row[col]
            # Acortar decisiones para la tabla
            if decision == 'COMPRA_FUERTE':
                fila.append("C_F")
            elif decision == 'VENTA_FUERTE':
                fila.append("V_F") 
            elif decision == 'COMPRA':
                fila.append("C")
            elif decision == 'VENTA':
                fila.append("V")
            else:
                fila.append("H")
        
        # Estrategia mayoritaria y fuerza
        decision_mayoritaria = row['estrategia_mayoritaria']
        if decision_mayoritaria == 'COMPRA_FUERTE':
            fila.append("C_F")
        elif decision_mayoritaria == 'VENTA_FUERTE':
            fila.append("V_F")
        elif decision_mayoritaria == 'COMPRA':
            fila.append("C")
        elif decision_mayoritaria == 'VENTA':
            fila.append("V")
        else:
            fila.append("H")
        
        fila.append(f"{row['fuerza_señal']:.2f}")
        
        print(" | ".join(f"{item:>12}" for item in fila))
    
    print(f"\nTotal registros mostrados: {len(df_reciente)}")
    
    # Mostrar descripciones completas solo para el último registro
    if len(df_reciente) > 0:
        print(f"\n📝 DESCRIPCIONES COMPLETAS (Último registro):")
        ultimo = df_trading.iloc[-1]
        # Filtrar descripciones según la combinación
        columnas_desc = []
        for indicador in combinacion_indicadores:
            col_desc = f'estrategia_{indicador}_descripcion'
            if col_desc in df_trading.columns:
                columnas_desc.append(col_desc)
        
        for col in columnas_desc:
            if col in df_trading.columns and not pd.isna(ultimo[col]):
                nombre = col.replace('estrategia_', '').replace('_descripcion', '').upper()
                print(f"   {nombre}: {ultimo[col]}")
    
    print("=" * 120)




'''
# Ejemplo de uso para pruebas
if __name__ == "__main__":
    # Datos de prueba
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', periods=50, freq='H')
    
    datos_prueba = {
        "BTC-USD": pd.DataFrame({
            'datetime': dates,
            'Close': np.cumsum(np.random.randn(50) * 100) + 50000,
            'High': np.cumsum(np.random.randn(50) * 100) + 50200,
            'Low': np.cumsum(np.random.randn(50) * 100) + 49800,
            'Volume': np.random.randint(1000000, 5000000, 50),
            'RSI': np.random.uniform(20, 80, 50),
            'MACD': np.random.normal(0, 50, 50),
            'MACD_signal': np.random.normal(0, 45, 50),
            'MA': np.cumsum(np.random.randn(50) * 80) + 50000,
            'Bollinger_Upper': np.cumsum(np.random.randn(50) * 100) + 50500,
            'Bollinger_Lower': np.cumsum(np.random.randn(50) * 100) + 49500,
            '%K': np.random.uniform(0, 100, 50),
            '%D': np.random.uniform(0, 100, 50)
        })
    }
    
    print("🧪 PROBANDO ANÁLISIS TÉCNICO CON **KWARGS:")
    
    # Parámetros de prueba
    parametros_prueba = {
        'rsi_periodo': 14,
        'macd_periodo_corto': 12,
        'macd_periodo_largo': 26,
        'macd_periodo_senal': 9,
        'media_movil_periodo': 20,
        'bollinger_periodo': 20,
        'bollinger_desviacion': 2.0,
        'estocastico_periodo': 14,
        'periodo_volatilidad': 20
    }
    
    resultados = analizar_dataframes(datos_prueba, rsi_under=30, rsi_upper=70, verbose=True, **parametros_prueba)
'''