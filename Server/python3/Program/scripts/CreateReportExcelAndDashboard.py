"""
CreateReportExcelAndDashboard.py
Script para generar reportes en Excel, CSV y dashboards gráficos interactivos.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import numpy as np
import os
from datetime import datetime
import warnings
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
warnings.filterwarnings('ignore')

# Configuración de estilo
plt.style.use('seaborn-v0_8')
COLORES = {
    'compra_fuerte': '#00FF00',
    'compra': '#90EE90', 
    'hold': '#FFFF00',
    'venta': '#FFB6C1',
    'venta_fuerte': '#FF0000',
    'vela_alcista': '#00FF00',
    'vela_bajista': '#FF0000',
    'grid': '#F0F0F0',
    'texto': '#333333',
    'bollinger_upper': '#FF6B6B',
    'bollinger_lower': '#4ECDC4',
    'bollinger_band': 'rgba(255,107,107,0.2)',
    'fibonacci': '#8A2BE2',
    'stochastic': '#FF69B4',
    'ichimoku': '#1E90FF',
    'williams': '#32CD32',
    'adx': '#FF4500',
    'sar': '#00CED1',
    'volume': '#4169E1'
}

def generar_reporte_excel_dashboard(resultados_trading, estrategia, user_name, verbose=False):
    """
    Función principal que genera reportes Excel, CSV y dashboards gráficos.
    """
    
    if verbose:
        print(f"\n📊 GENERANDO REPORTES EXCEL, CSV Y DASHBOARD")
        print(f"   Estrategia: {estrategia}")
        print(f"   Usuario: {user_name}")
        print(f"   Símbolos a procesar: {len(resultados_trading)}")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivos_generados = []
    
    try:
        # Paso 1: Generar archivo Excel con todos los datos ordenados
        #if verbose:
        #    print(f"   📈 Paso 1: Generando archivo Excel...")
        
        #archivo_excel = generar_archivo_excel(resultados_trading, estrategia, user_name, timestamp, verbose)
        #if archivo_excel:
        #    archivos_generados.append(archivo_excel)
        
        # Paso 2: Generar archivos CSV por símbolo
        if verbose:
            print(f"   📊 Paso 2: Generando archivos CSV...")
        
        archivos_csv = generar_archivos_csv(resultados_trading, user_name, timestamp, estrategia, verbose)
        archivos_generados.extend(archivos_csv)
        
        # Paso 3: Generar gráficos interactivos individuales por símbolo
        if verbose:
            print(f"   📊 Paso 3: Generando gráficos interactivos individuales...")
        
        for symbol, df in resultados_trading.items():
            if len(df) > 0:
                archivo_individual = generar_grafico_interactivo_individual(
                    symbol, df, estrategia, user_name, timestamp, verbose
                )
                if archivo_individual:
                    archivos_generados.append(archivo_individual)
        
        if verbose:
            print(f"   ✅ Reportes generados exitosamente: {len(archivos_generados)} archivos")
        
        return archivos_generados
        
    except Exception as e:
        if verbose:
            print(f"   ❌ Error generando reportes: {e}")
        return []

def generar_archivo_excel(resultados_trading, estrategia, user_name, timestamp, verbose=False):
    """
    Genera archivo Excel con todos los datos de trading ordenados por fecha.
    """
    try:
        nombre_archivo = f"{user_name}_reporte_{estrategia}_{timestamp}.xlsx"
        ruta_archivo = f"/app/tmp/{nombre_archivo}"
        
        with pd.ExcelWriter(ruta_archivo, engine='openpyxl') as writer:
            # Hoja 1: Resumen ejecutivo
            df_resumen = crear_resumen_ejecutivo(resultados_trading, verbose)
            df_resumen.to_excel(writer, sheet_name='Resumen_Ejecutivo', index=False)
            
            # Hoja 2: Datos completos por símbolo (ordenados por fecha descendente)
            for symbol, df in resultados_trading.items():
                if len(df) > 0:
                    # Filtrar columnas relevantes
                    columnas_relevantes = [col for col in df.columns if any(x in col for x in [
                        'datetime', 'Open', 'High', 'Low', 'Close', 'Volume', 
                        'RSI', 'MACD', 'MA', 'estrategia', 'fuerza', 'Bollinger',
                        'Fibonacci', 'Stochastic', 'Ichimoku', 'Williams', 'ADX', 'SAR'
                    ])]
                    df_filtrado = df[columnas_relevantes].copy()
                    
                    # Ordenar por fecha más reciente primero
                    if 'datetime' in df_filtrado.columns:
                        df_filtrado = df_filtrado.sort_values('datetime', ascending=False)
                    
                    df_filtrado.to_excel(writer, sheet_name=f'Datos_{symbol}', index=False)
            
            # Hoja 3: Señales de trading (ordenadas por fecha descendente)
            df_señales = extraer_señales_trading(resultados_trading, verbose)
            if 'Fecha_Hora' in df_señales.columns:
                df_señales = df_señales.sort_values('Fecha_Hora', ascending=False)
            df_señales.to_excel(writer, sheet_name='Señales_Trading', index=False)
        
        if verbose:
            print(f"      ✅ Excel generado: {nombre_archivo}")
        
        return ruta_archivo
        
    except Exception as e:
        if verbose:
            print(f"      ❌ Error generando Excel: {e}")
        return None

def crear_resumen_ejecutivo(resultados_trading, verbose=False):
    """
    Crea DataFrame con resumen ejecutivo de todas las estrategias.
    """
    datos_resumen = []
    
    for symbol, df in resultados_trading.items():
        if len(df) > 0:
            ultimo = df.iloc[-1]
            
            # Extraer señales de estrategia
            señales_estrategia = {}
            for col in df.columns:
                if col.startswith('estrategia_') and not col.endswith(('_valor', '_descripcion')):
                    if col in ultimo:
                        señales_estrategia[col] = ultimo[col]
            
            # Contar señales
            compras = sum(1 for s in señales_estrategia.values() if 'COMPRA' in str(s))
            ventas = sum(1 for s in señales_estrategia.values() if 'VENTA' in str(s))
            holds = sum(1 for s in señales_estrategia.values() if 'HOLD' in str(s))
            
            datos_resumen.append({
                'Símbolo': symbol,
                'Último Precio': ultimo.get('Close', 'N/A'),
                'Señal Mayoritaria': ultimo.get('estrategia_mayoritaria', 'N/A'),
                'Fuerza Señal': ultimo.get('fuerza_señal', 'N/A'),
                'Total Estrategias': len(señales_estrategia),
                'Señales COMPRA': compras,
                'Señales VENTA': ventas,
                'Señales HOLD': holds,
                'RSI Actual': ultimo.get('RSI', 'N/A'),
                'MACD Actual': ultimo.get('MACD', 'N/A'),
                'Timestamp': ultimo.get('datetime', 'N/A')
            })
    
    return pd.DataFrame(datos_resumen)

def extraer_señales_trading(resultados_trading, verbose=False):
    """
    Extrae todas las señales de trading para análisis.
    """
    datos_señales = []
    
    for symbol, df in resultados_trading.items():
        if len(df) > 0:
            for idx, fila in df.iterrows():
                for col in df.columns:
                    if col.startswith('estrategia_') and not col.endswith(('_valor', '_descripcion')):
                        if col in fila and pd.notna(fila[col]):
                            datos_señales.append({
                                'Símbolo': symbol,
                                'Fecha_Hora': fila.get('datetime', 'N/A'),
                                'Estrategia': col.replace('estrategia_', ''),
                                'Señal': fila[col],
                                'Precio': fila.get('Close', 'N/A'),
                                'Fuerza': fila.get('fuerza_señal', 'N/A')
                            })
    
    return pd.DataFrame(datos_señales)

def generar_archivos_csv(resultados_trading, user_name, timestamp, estrategia, verbose=False):
    """
    Genera archivos CSV individuales por símbolo ordenados por fecha.
    """
    archivos_generados = []
    
    try:
        for symbol, df in resultados_trading.items():
            if len(df) > 0:
                # Crear copia para no modificar el original
                df_csv = df.copy()
                
                # Ordenar por fecha más reciente primero
                if 'datetime' in df_csv.columns:
                    df_csv = df_csv.sort_values('datetime', ascending=False)
                    
                    # Manejar timezone - convertir a string con timezone
                    if pd.api.types.is_datetime64_any_dtype(df_csv['datetime']):
                        # Si tiene timezone, convertir a string con timezone
                        if df_csv['datetime'].dt.tz is not None:
                            df_csv['datetime'] = df_csv['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S%z')
                        else:
                            # Si no tiene timezone, asumir UTC y añadir timezone
                            df_csv['datetime'] = df_csv['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S') + '+0000'
                
                #nombre_archivo = f"{user_name}_datos_{symbol}_{timestamp}.csv"
                nombre_archivo = f"{user_name}_datos__{symbol}_{estrategia}.csv"
                ruta_archivo = f"/app/tmp/{nombre_archivo}"
                
                df_csv.to_csv(ruta_archivo, index=False, encoding='utf-8')
                archivos_generados.append(ruta_archivo)
                
                if verbose:
                    print(f"      ✅ CSV generado: {symbol}")
        
        return archivos_generados
        
    except Exception as e:
        if verbose:
            print(f"      ❌ Error generando CSVs: {e}")
        return []

# =============================================================================
# PRIMERA PARTE: CONFIGURACIÓN DE PANELES
# =============================================================================

def configurar_paneles_graficos(symbol, df, estrategia, verbose=False):
    """
    Primera parte: Configura todos los paneles del gráfico con títulos, descripciones y métricas.
    Retorna una estructura con la configuración de cada panel.
    """
    try:
        if len(df) < 5:
            if verbose:
                print(f"        ⚠️ Datos insuficientes para {symbol}")
            return None
        
        # Ordenar por fecha ascendente para el gráfico
        df_plot = df.copy()
        if 'datetime' in df_plot.columns:
            df_plot = df_plot.sort_values('datetime', ascending=True)
        
        # Configuración de cada panel
        paneles_config = {
            'titulo_principal': f'Análisis Completo - {symbol} | Estrategia: {estrategia}',
            'paneles': [
                {
                    'id': 'velas',
                    'titulo': f'Velas Japonesas - {symbol}',
                    'descripcion': 'Gráfico principal de precios con velas japonesas, incluyendo indicadores de tendencia como Bandas Bollinger, Ichimoku Cloud y Parabolic SAR',
                    'tipo': 'velas_japonesas',
                    'metricas': [
                        'Open', 'High', 'Low', 'Close', 
                        'Bollinger_Upper', 'Bollinger_Lower',
                        'SAR', 'Ichimoku_Base', 'Ichimoku_Conversion', 
                        'Ichimoku_A', 'Ichimoku_B'
                    ],
                    'datos': df_plot,
                    'señales': True
                },
                {
                    'id': 'volumen',
                    'titulo': 'Volumen',
                    'descripcion': 'Volumen de trading con colores que indican tendencia alcista (verde) o bajista (roja)',
                    'tipo': 'volumen',
                    'metricas': ['Volume', 'Open', 'Close'],
                    'datos': df_plot
                },
                {
                    'id': 'momento',
                    'titulo': 'Indicadores de Momento (RSI, Estocástico, Williams %R)',
                    'descripcion': 'Indicadores de momentum que miden la velocidad y cambio de movimientos de precios',
                    'tipo': 'indicadores_momento',
                    'metricas': ['RSI', 'Stochastic_K', 'Stochastic_D', 'Williams_R'],
                    'datos': df_plot,
                    'lineas_referencia': [
                        {'y': 70, 'color': 'red', 'estilo': 'dash', 'descripcion': 'Sobrecompra RSI'},
                        {'y': 30, 'color': 'green', 'estilo': 'dash', 'descripcion': 'Sobreventa RSI'},
                        {'y': 80, 'color': 'red', 'estilo': 'dot', 'descripcion': 'Sobrecompra Estocástico'},
                        {'y': 20, 'color': 'green', 'estilo': 'dot', 'descripcion': 'Sobreventa Estocástico'}
                    ]
                },
                {
                    'id': 'macd',
                    'titulo': 'MACD',
                    'descripcion': 'Indicador de tendencia que muestra la relación entre dos medias móviles del precio',
                    'tipo': 'macd',
                    'metricas': ['MACD', 'MACD_signal', 'MACD_hist'],
                    'datos': df_plot
                },
                {
                    'id': 'tendencia',
                    'titulo': 'Indicadores de Tendencia (ADX, Fibonacci)',
                    'descripcion': 'Indicadores que miden la fuerza y dirección de la tendencia del mercado',
                    'tipo': 'indicadores_tendencia',
                    'metricas': ['ADX', 'Fibonacci_0', 'Fibonacci_23.6', 'Fibonacci_38.2', 'Fibonacci_61.8', 'Fibonacci_100'],
                    'datos': df_plot,
                    'lineas_referencia': [
                        {'y': 25, 'color': 'orange', 'estilo': 'dash', 'descripcion': 'Fuerza de tendencia ADX'}
                    ]
                },
                {
                    'id': 'fuerza',
                    'titulo': 'Fuerza de Señal',
                    'descripcion': 'Fuerza consolidada de todas las señales de trading, donde valores positivos indican tendencia alcista y negativos tendencia bajista',
                    'tipo': 'fuerza_señal',
                    'metricas': ['fuerza_señal'],
                    'datos': df_plot,
                    'lineas_referencia': [
                        {'y': 0.7, 'color': 'green', 'estilo': 'dash', 'descripcion': 'Compra Fuerte'},
                        {'y': 0.3, 'color': 'lightgreen', 'estilo': 'dash', 'descripcion': 'Compra'},
                        {'y': -0.3, 'color': 'lightcoral', 'estilo': 'dash', 'descripcion': 'Venta'},
                        {'y': -0.7, 'color': 'red', 'estilo': 'dash', 'descripcion': 'Venta Fuerte'},
                        {'y': 0, 'color': 'black', 'estilo': 'solid', 'descripcion': 'Neutral'}
                    ]
                }
            ],
            'filtros_comunes': {
                'rango_fechas': {
                    'desde': df_plot['datetime'].min() if 'datetime' in df_plot.columns else None,
                    'hasta': df_plot['datetime'].max() if 'datetime' in df_plot.columns else None
                },
                'indicadores_disponibles': list(df_plot.columns),
                'señales_disponibles': [col for col in df_plot.columns if col.startswith('estrategia_')]
            }
        }
        
        return paneles_config
        
    except Exception as e:
        if verbose:
            print(f"        ❌ Error configurando paneles para {symbol}: {e}")
        return None

# =============================================================================
# SEGUNDA PARTE: ARMADO DEL GRÁFICO CON DISTRIBUCIÓN DE PANELES
# =============================================================================

def armar_grafico_con_paneles(paneles_config, symbol, user_name, estrategia, timestamp, verbose=False):
    """
    Segunda parte: Arma el gráfico completo con la configuración de paneles,
    distribuyendo el espacio y agregando filtros agrupados.
    """
    try:
        if not paneles_config:
            return None
            
        # Crear figura con subplots usando la configuración
        num_paneles = len(paneles_config['paneles'])
        
        # Configurar alturas de paneles (en porcentaje)
        alturas_paneles = [0.4, 0.1, 0.15, 0.15, 0.1, 0.1]  # Mantener proporciones originales
        
        # Crear subplots
        fig = make_subplots(
            rows=num_paneles, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            subplot_titles=[panel['titulo'] for panel in paneles_config['paneles']],
            row_heights=alturas_paneles
        )
        
        # Procesar cada panel según su configuración
        for idx, panel in enumerate(paneles_config['paneles']):
            fila = idx + 1
            
            # Agregar el tipo de gráfico correspondiente
            if panel['tipo'] == 'velas_japonesas':
                agregar_velas_japonesas(fig, panel['datos'], symbol, verbose)
                if panel.get('señales', False):
                    agregar_señales_trading_mejoradas(fig, panel['datos'], verbose)
                    
            elif panel['tipo'] == 'volumen':
                agregar_volumen(fig, panel['datos'], verbose)
                
            elif panel['tipo'] == 'indicadores_momento':
                agregar_indicadores_momento(fig, panel['datos'], verbose)
                # Agregar líneas de referencia si existen
                for linea in panel.get('lineas_referencia', []):
                    fig.add_hline(
                        y=linea['y'], 
                        line_dash=linea['estilo'], 
                        line_color=linea['color'], 
                        row=fila, col=1
                    )
                    
            elif panel['tipo'] == 'macd':
                agregar_macd(fig, panel['datos'], verbose)
                
            elif panel['tipo'] == 'indicadores_tendencia':
                agregar_indicadores_tendencia(fig, panel['datos'], verbose)
                # Agregar líneas de referencia si existen
                for linea in panel.get('lineas_referencia', []):
                    fig.add_hline(
                        y=linea['y'], 
                        line_dash=linea['estilo'], 
                        line_color=linea['color'], 
                        row=fila, col=1
                    )
                    
            elif panel['tipo'] == 'fuerza_señal':
                agregar_fuerza_señal(fig, panel['datos'], verbose)
                # Agregar líneas de referencia si existen
                for linea in panel.get('lineas_referencia', []):
                    fig.add_hline(
                        y=linea['y'], 
                        line_dash=linea['estilo'], 
                        line_color=linea['color'], 
                        row=fila, col=1
                    )
        
        # AGREGAR PANEL DE FILTROS
        agregar_panel_filtros(fig, paneles_config['filtros_comunes'], num_paneles + 1)
        
        # Actualizar layout con márgenes del 2%
        fig.update_layout(
            title=paneles_config['titulo_principal'],
            height=1600,  # Aumentar altura para incluir filtros
            showlegend=True,
            xaxis_rangeslider_visible=False,
            margin=dict(l=20, r=20, t=80, b=100),  # 2% de margen aproximado
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Configurar ejes para cada panel
        configuraciones_ejes = {
            1: {'titulo_y': 'Precio'},
            2: {'titulo_y': 'Volumen'},
            3: {'titulo_y': 'Momento'},
            4: {'titulo_y': 'MACD'},
            5: {'titulo_y': 'Tendencia'},
            6: {'titulo_y': 'Fuerza'}
        }
        
        for fila, config in configuraciones_ejes.items():
            fig.update_yaxes(title_text=config['titulo_y'], row=fila, col=1)
        
        # Eje X solo en el último panel
        fig.update_xaxes(title_text='Fecha y Hora', row=num_paneles, col=1)
        
        #nombre_archivo = f"{user_name}_grafico_interactivo_{symbol}_{estrategia}_{timestamp}.html"
        nombre_archivo = f"{user_name}_grafico_interactivo_{symbol}_{estrategia}.html"
        ruta_archivo = f"/app/tmp/{nombre_archivo}"
        fig.write_html(ruta_archivo)
        
        if verbose:
            print(f"        ✅ Gráfico interactivo generado: {symbol}")
        
        return ruta_archivo
        
    except Exception as e:
        if verbose:
            print(f"        ❌ Error armando gráfico {symbol}: {e}")
        return None

def agregar_panel_filtros(fig, filtros_comunes, fila_filtros):
    """
    Agrega un panel unificado de filtros para todos los gráficos.
    """
    try:
        # Información de filtros disponibles
        desde = filtros_comunes['rango_fechas']['desde']
        hasta = filtros_comunes['rango_fechas']['hasta']
        
        # Formatear fechas para mostrar
        if desde and hasta:
            if hasattr(desde, 'strftime'):
                desde_str = desde.strftime('%Y-%m-%d %H:%M')
                hasta_str = hasta.strftime('%Y-%m-%d %H:%M')
            else:
                desde_str = str(desde)[:16]
                hasta_str = str(hasta)[:16]
        else:
            desde_str = "N/A"
            hasta_str = "N/A"
        
        # Agregar información de filtros como trazas invisibles para la leyenda
        fig.add_trace(
            go.Scatter(
                x=[None], y=[None],
                mode='markers',
                marker=dict(size=0),
                name='🎛️ PANEL DE FILTROS',
                showlegend=True,
                legendgroup='filtros'
            ),
            row=fila_filtros, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=[None], y=[None],
                mode='markers',
                marker=dict(size=0),
                name=f'📅 Rango: {desde_str} a {hasta_str}',
                showlegend=True,
                legendgroup='filtros'
            ),
            row=fila_filtros, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=[None], y=[None],
                mode='markers',
                marker=dict(size=0),
                name=f'📊 Indicadores: {len(filtros_comunes["indicadores_disponibles"])} disponibles',
                showlegend=True,
                legendgroup='filtros'
            ),
            row=fila_filtros, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=[None], y=[None],
                mode='markers',
                marker=dict(size=0),
                name=f'⚡ Señales: {len(filtros_comunes["señales_disponibles"])} estrategias',
                showlegend=True,
                legendgroup='filtros'
            ),
            row=fila_filtros, col=1
        )
        
        # Configurar el panel de filtros
        fig.update_xaxes(
            showticklabels=False, 
            showgrid=False, 
            zeroline=False,
            row=fila_filtros, 
            col=1
        )
        fig.update_yaxes(
            showticklabels=False, 
            showgrid=False, 
            zeroline=False,
            row=fila_filtros, 
            col=1
        )
        
    except Exception as e:
        print(f"Error agregando panel de filtros: {e}")

# =============================================================================
# FUNCIONES DE AGREGADO DE GRÁFICOS (MANTENIDAS)
# =============================================================================

def agregar_velas_japonesas(fig, df, symbol, verbose=False):
    """Agrega gráfico de velas japonesas al subplot."""
    try:
        # Gráfico de velas
        fig.add_trace(
            go.Candlestick(
                x=df['datetime'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name=f'Velas {symbol}'
            ),
            row=1, col=1
        )
        
        # Agregar Bandas de Bollinger si existen
        if all(col in df.columns for col in ['Bollinger_Upper', 'Bollinger_Lower']):
            fig.add_trace(
                go.Scatter(
                    x=df['datetime'],
                    y=df['Bollinger_Upper'],
                    name='Bollinger Upper',
                    line=dict(color=COLORES['bollinger_upper'], width=1)
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=df['datetime'],
                    y=df['Bollinger_Lower'],
                    name='Bollinger Lower',
                    line=dict(color=COLORES['bollinger_lower'], width=1),
                    fill='tonexty',
                    fillcolor=COLORES['bollinger_band']
                ),
                row=1, col=1
            )
        elif verbose:
            print(f"          ⚠️ Bandas de Bollinger no encontradas para {symbol}")
            
        # Agregar Parabolic SAR si existe
        if 'SAR' in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df['datetime'],
                    y=df['SAR'],
                    name='Parabolic SAR',
                    mode='markers',
                    marker=dict(
                        size=4,
                        color=COLORES['sar'],
                        symbol='circle'
                    )
                ),
                row=1, col=1
            )
        elif verbose:
            print(f"          ⚠️ Parabolic SAR no encontrado para {symbol}")
            
        # Agregar Ichimoku Cloud si existe
        if all(col in df.columns for col in ['Ichimoku_Base', 'Ichimoku_Conversion', 'Ichimoku_A', 'Ichimoku_B']):
            # Líneas de conversión y base
            fig.add_trace(
                go.Scatter(
                    x=df['datetime'],
                    y=df['Ichimoku_Conversion'],
                    name='Ichimoku Conversion',
                    line=dict(color=COLORES['ichimoku'], width=1, dash='dot')
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=df['datetime'],
                    y=df['Ichimoku_Base'],
                    name='Ichimoku Base',
                    line=dict(color=COLORES['ichimoku'], width=1, dash='dash')
                ),
                row=1, col=1
            )
            
            # Nube Ichimoku
            fig.add_trace(
                go.Scatter(
                    x=df['datetime'],
                    y=df['Ichimoku_A'],
                    name='Ichimoku A',
                    line=dict(color='rgba(0,0,0,0)')
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=df['datetime'],
                    y=df['Ichimoku_B'],
                    name='Ichimoku B',
                    line=dict(color='rgba(0,0,0,0)'),
                    fill='tonexty',
                    fillcolor='rgba(30, 144, 255, 0.2)'
                ),
                row=1, col=1
            )
        elif verbose:
            print(f"          ⚠️ Ichimoku Cloud no encontrado para {symbol}")
            
    except Exception as e:
        if verbose:
            print(f"          ❌ Error agregando velas: {e}")

def agregar_volumen(fig, df, verbose=False):
    """Agrega gráfico de volumen al subplot."""
    try:
        if 'Volume' in df.columns:
            # Crear colores para el volumen (verde para subida, rojo para bajada)
            colors = ['green' if close >= open_ else 'red' 
                     for close, open_ in zip(df['Close'], df['Open'])]
            
            fig.add_trace(
                go.Bar(
                    x=df['datetime'],
                    y=df['Volume'],
                    name='Volumen',
                    marker_color=colors,
                    opacity=0.7
                ),
                row=2, col=1
            )
            
        else:
            if verbose:
                print(f"          ⚠️ Volumen no encontrado")
                
    except Exception as e:
        if verbose:
            print(f"          ❌ Error agregando volumen: {e}")

def agregar_indicadores_momento(fig, df, verbose=False):
    """Agrega indicadores de momento al subplot."""
    try:
        # RSI
        if 'RSI' in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df['datetime'],
                    y=df['RSI'],
                    name='RSI',
                    line=dict(color='purple', width=1)
                ),
                row=3, col=1
            )
            
            # Líneas de sobrecompra y sobreventa
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
        elif verbose:
            print(f"          ⚠️ RSI no encontrado")
        
        # Estocástico
        if all(col in df.columns for col in ['Stochastic_K', 'Stochastic_D']):
            fig.add_trace(
                go.Scatter(
                    x=df['datetime'],
                    y=df['Stochastic_K'],
                    name='Stochastic %K',
                    line=dict(color=COLORES['stochastic'], width=1)
                ),
                row=3, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=df['datetime'],
                    y=df['Stochastic_D'],
                    name='Stochastic %D',
                    line=dict(color=COLORES['stochastic'], width=1, dash='dash')
                ),
                row=3, col=1
            )
            
            # Líneas de sobrecompra y sobreventa para Estocástico
            fig.add_hline(y=80, line_dash="dot", line_color="red", row=3, col=1)
            fig.add_hline(y=20, line_dash="dot", line_color="green", row=3, col=1)
        elif verbose:
            print(f"          ⚠️ Estocástico no encontrado")
        
        # Williams %R
        if 'Williams_R' in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df['datetime'],
                    y=df['Williams_R'],
                    name='Williams %R',
                    line=dict(color=COLORES['williams'], width=1)
                ),
                row=3, col=1
            )
        elif verbose:
            print(f"          ⚠️ Williams %R no encontrado")
            
    except Exception as e:
        if verbose:
            print(f"          ❌ Error agregando indicadores de momento: {e}")

def agregar_macd(fig, df, verbose=False):
    """Agrega MACD al subplot."""
    try:
        if all(col in df.columns for col in ['MACD', 'MACD_signal']):
            fig.add_trace(
                go.Scatter(
                    x=df['datetime'],
                    y=df['MACD'],
                    name='MACD',
                    line=dict(color='blue', width=1)
                ),
                row=4, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=df['datetime'],
                    y=df['MACD_signal'],
                    name='Señal MACD',
                    line=dict(color='red', width=1)
                ),
                row=4, col=1
            )
            
            # Histograma MACD
            if 'MACD_hist' in df.columns:
                colors_hist = ['green' if x >= 0 else 'red' for x in df['MACD_hist']]
                fig.add_trace(
                    go.Bar(
                        x=df['datetime'],
                        y=df['MACD_hist'],
                        name='Histograma MACD',
                        marker_color=colors_hist,
                        opacity=0.5
                    ),
                    row=4, col=1
                )
        elif verbose:
            print(f"          ⚠️ MACD no encontrado")
                
    except Exception as e:
        if verbose:
            print(f"          ❌ Error agregando MACD: {e}")

def agregar_indicadores_tendencia(fig, df, verbose=False):
    """Agrega indicadores de tendencia al subplot."""
    try:
        # ADX
        if 'ADX' in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df['datetime'],
                    y=df['ADX'],
                    name='ADX',
                    line=dict(color=COLORES['adx'], width=2)
                ),
                row=5, col=1
            )
            
            # Línea de referencia para ADX (25 típicamente)
            fig.add_hline(y=25, line_dash="dash", line_color="orange", row=5, col=1)
        elif verbose:
            print(f"          ⚠️ ADX no encontrado")
            
        # Fibonacci Retracement (simplificado - mostramos niveles clave)
        if all(col in df.columns for col in ['Fibonacci_0', 'Fibonacci_23.6', 'Fibonacci_38.2', 'Fibonacci_61.8', 'Fibonacci_100']):
            niveles_fib = ['0', '23.6', '38.2', '61.8', '100']
            for nivel in niveles_fib:
                col_name = f'Fibonacci_{nivel}'
                if col_name in df.columns:
                    fig.add_trace(
                        go.Scatter(
                            x=df['datetime'],
                            y=df[col_name],
                            name=f'Fib {nivel}%',
                            line=dict(color=COLORES['fibonacci'], width=1, dash='dot'),
                            opacity=0.7
                        ),
                        row=5, col=1
                    )
        elif verbose:
            print(f"          ⚠️ Fibonacci Retracement no encontrado")
            
    except Exception as e:
        if verbose:
            print(f"          ❌ Error agregando indicadores de tendencia: {e}")

def agregar_fuerza_señal(fig, df, verbose=False):
    """Agrega gráfico de fuerza de señal al subplot."""
    try:
        if 'fuerza_señal' in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df['datetime'],
                    y=df['fuerza_señal'],
                    name='Fuerza Señal',
                    line=dict(color='orange', width=2),
                    fill='tozeroy',
                    fillcolor='rgba(255,165,0,0.1)'
                ),
                row=6, col=1
            )
            
            # Líneas de referencia
            fig.add_hline(y=0.7, line_dash="dash", line_color="green", row=6, col=1)
            fig.add_hline(y=0.3, line_dash="dash", line_color="lightgreen", row=6, col=1)
            fig.add_hline(y=-0.3, line_dash="dash", line_color="lightcoral", row=6, col=1)
            fig.add_hline(y=-0.7, line_dash="dash", line_color="red", row=6, col=1)
            fig.add_hline(y=0, line_color="black", row=6, col=1)
            
        else:
            if verbose:
                print(f"          ⚠️ Fuerza de señal no encontrada")
            
    except Exception as e:
        if verbose:
            print(f"          ❌ Error agregando fuerza señal: {e}")

def agregar_señales_trading_mejoradas(fig, df, verbose=False):
    """Agrega señales de trading mejoradas con flechas y triángulos."""
    try:
        if 'estrategia_mayoritaria' in df.columns:
            # Filtrar solo las filas con señales relevantes
            señales_df = df[df['estrategia_mayoritaria'].notna()].copy()
            
            for _, row in señales_df.iterrows():
                señal = str(row['estrategia_mayoritaria'])
                fuerza = row.get('fuerza_señal', 0)
                precio = row['High'] * 1.02  # Mostrar ligeramente arriba del high
                
                # Determinar símbolo y tamaño basado en la fuerza
                if 'COMPRA_FUERTE' in señal or 'VENTA_FUERTE' in señal:
                    # Usar flechas para señales fuertes
                    simbolo = 'arrow-up' if 'COMPRA' in señal else 'arrow-down'
                    # Tamaño basado en fuerza (3x el tamaño base para 100% de fuerza)
                    tamaño_base = 15
                    tamaño = tamaño_base + (abs(fuerza) * 2 * tamaño_base) if pd.notna(fuerza) else tamaño_base * 2
                    color = 'green' if 'COMPRA' in señal else 'red'
                    texto = f"{señal}<br>Fuerza: {fuerza:.2f}"
                else:
                    # Usar triángulos para señales normales
                    simbolo = 'triangle-up' if 'COMPRA' in señal else 'triangle-down'
                    tamaño = 12
                    color = 'lightgreen' if 'COMPRA' in señal else 'lightcoral'
                    texto = f"{señal}<br>Fuerza: {fuerza:.2f}" if pd.notna(fuerza) else señal
                
                fig.add_trace(
                    go.Scatter(
                        x=[row['datetime']],
                        y=[precio],
                        mode='markers+text',
                        marker=dict(
                            symbol=simbolo,
                            size=tamaño,
                            color=color,
                            line=dict(width=2, color='black')
                        ),
                        text=[f" {señal.split('_')[0]}"],
                        textposition="top center",
                        name=señal,
                        hovertemplate=texto,
                        showlegend=False
                    ),
                    row=1, col=1
                )
                
        else:
            if verbose:
                print(f"          ⚠️ No se encontraron señales de trading")
                
    except Exception as e:
        if verbose:
            print(f"          ❌ Error agregando señales trading mejoradas: {e}")

# =============================================================================
# FUNCIÓN PRINCIPAL MODIFICADA
# =============================================================================

def generar_grafico_interactivo_individual(symbol, df, estrategia, user_name, timestamp, verbose=False):
    """
    Función principal modificada que utiliza las dos nuevas partes.
    """
    try:
        if len(df) < 5:
            if verbose:
                print(f"        ⚠️ Datos insuficientes para {symbol}")
            return None
        
        # PRIMERA PARTE: Configurar paneles
        paneles_config = configurar_paneles_graficos(symbol, df, estrategia, verbose)
        
        if not paneles_config:
            return None
        
        # SEGUNDA PARTE: Armar gráfico con paneles
        archivo = armar_grafico_con_paneles(paneles_config, symbol, user_name, estrategia, timestamp, verbose)
        
        return archivo
        
    except Exception as e:
        if verbose:
            print(f"        ❌ Error generando gráfico interactivo {symbol}: {e}")
        return None

# =============================================================================
# FUNCIÓN MAIN (OPCIONAL)
# =============================================================================

"""
# Función principal para uso externo
def main():
    #Función principal para ejecución independiente.
    import sys
    
    if len(sys.argv) < 4:
        print("Uso: python CreateReportExcelAndDashboard.py <resultados_trading> <estrategia> <user_name> [debug]")
        print("Ejemplo: python CreateReportExcelAndDashboard.py resultados.json mediano_plazo Juan true")
        sys.exit(1)
    
    # Aquí se cargarían los resultados_trading desde archivo JSON
    # Por ahora es un placeholder
    resultados_trading = {}
    estrategia = sys.argv[2]
    user_name = sys.argv[3]
    debug = len(sys.argv) > 4 and sys.argv[4].lower() in ['true', '1', 'yes', 'y']
    
    archivos = generar_reporte_excel_dashboard(resultados_trading, estrategia, user_name, debug)
    print(f"Archivos generados: {len(archivos)}")

if __name__ == "__main__":
    main()
"""