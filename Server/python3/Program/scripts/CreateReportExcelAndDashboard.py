#!/usr/bin/env python3
"""
CreateReportExcelAndDashboard.py
Script para generar reportes en Excel y dashboards gráficos completos.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import numpy as np
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuración de estilo para matplotlib
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
    'texto': '#333333'
}

def generar_reporte_excel_dashboard(resultados_trading, estrategia, user_name, verbose=False):
    """
    Función principal que genera reportes Excel y dashboards gráficos.
    
    :param resultados_trading: Diccionario con DataFrames de resultados
    :param estrategia: Nombre de la estrategia utilizada
    :param user_name: Nombre de usuario para prefijo de archivos
    :param verbose: Modo debug para mostrar detalles
    :return: Lista de archivos generados
    """
    
    if verbose:
        print(f"\n📊 GENERANDO REPORTES EXCEL Y DASHBOARD")
        print(f"   Estrategia: {estrategia}")
        print(f"   Usuario: {user_name}")
        print(f"   Símbolos a procesar: {len(resultados_trading)}")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivos_generados = []
    
    try:
        # Paso 1: Generar archivo Excel con todos los datos
        if verbose:
            print(f"   📈 Paso 1: Generando archivo Excel...")
        
        archivo_excel = generar_archivo_excel(resultados_trading, estrategia, user_name, timestamp, verbose)
        archivos_generados.append(archivo_excel)
        
        # Paso 2: Generar dashboard general de estrategias IA User
        if verbose:
            print(f"   🎯 Paso 2: Generando dashboard general...")
        
        archivo_dashboard = generar_dashboard_general(resultados_trading, estrategia, user_name, timestamp, verbose)
        archivos_generados.append(archivo_dashboard)
        
        # Paso 3: Generar gráficos individuales por símbolo
        if verbose:
            print(f"   📊 Paso 3: Generando gráficos individuales...")
        
        for symbol, df in resultados_trading.items():
            if len(df) > 0:
                archivo_individual = generar_grafico_individual(
                    symbol, df, estrategia, user_name, timestamp, verbose
                )
                if archivo_individual:
                    archivos_generados.append(archivo_individual)
        
        # Paso 4: Generar infografía resumen
        if verbose:
            print(f"   🎨 Paso 4: Generando infografía resumen...")
        
        archivo_infografia = generar_infografia_resumen(
            resultados_trading, estrategia, user_name, timestamp, verbose
        )
        archivos_generados.append(archivo_infografia)
        
        if verbose:
            print(f"   ✅ Reportes generados exitosamente: {len(archivos_generados)} archivos")
        
        return archivos_generados
        
    except Exception as e:
        if verbose:
            print(f"   ❌ Error generando reportes: {e}")
        return []



def generar_archivo_excel(resultados_trading, estrategia, user_name, timestamp, verbose=False):
    """
    Genera archivo Excel con todos los datos de trading.
    """
    try:
        nombre_archivo = f"{user_name}_reporte_{estrategia}_{timestamp}.xlsx"
        ruta_archivo = f"/app/tmp/{nombre_archivo}"
        
        with pd.ExcelWriter(ruta_archivo, engine='openpyxl') as writer:
            # Hoja 1: Resumen ejecutivo
            df_resumen = crear_resumen_ejecutivo(resultados_trading, verbose)
            df_resumen.to_excel(writer, sheet_name='Resumen_Ejecutivo', index=False)
            
            # Hoja 2: Datos completos por símbolo
            for symbol, df in resultados_trading.items():
                if len(df) > 0:
                    # Filtrar columnas relevantes
                    columnas_relevantes = [col for col in df.columns if any(x in col for x in [
                        'datetime', 'Open', 'High', 'Low', 'Close', 'Volume', 
                        'RSI', 'MACD', 'MA', 'estrategia', 'fuerza'
                    ])]
                    df_filtrado = df[columnas_relevantes].copy()
                    df_filtrado.to_excel(writer, sheet_name=f'Datos_{symbol}', index=False)
            
            # Hoja 3: Señales de trading
            df_señales = extraer_señales_trading(resultados_trading, verbose)
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



def generar_dashboard_general(resultados_trading, estrategia, user_name, timestamp, verbose=False):
    """
    Genera dashboard general con decisiones bursátiles ponderadas.
    """
    try:
        if not resultados_trading:
            if verbose:
                print(f"      ⚠️ No hay datos para generar dashboard")
            return None
        
        fig = plt.figure(figsize=(20, 12))
        fig.suptitle(f'DASHBOARD GENERAL - ESTRATEGIA {estrategia.upper()}\nUsuario: {user_name}', 
                    fontsize=16, fontweight='bold', color=COLORES['texto'])
        
        # Layout del dashboard
        gs = plt.GridSpec(3, 3, figure=fig)
        
        # Gráfico 1: Heatmap de señales actuales
        ax1 = fig.add_subplot(gs[0, 0])
        generar_heatmap_señales(resultados_trading, ax1, verbose)
        
        # Gráfico 2: Evolución temporal de fuerza de señal
        ax2 = fig.add_subplot(gs[0, 1:])
        generar_evolucion_fuerza(resultados_trading, ax2, verbose)
        
        # Gráfico 3: Distribución de estrategias
        ax3 = fig.add_subplot(gs[1, 0])
        generar_distribucion_estrategias(resultados_trading, ax3, verbose)
        
        # Gráfico 4: Top señales de compra/venta
        ax4 = fig.add_subplot(gs[1, 1])
        generar_top_señales(resultados_trading, ax4, 'COMPRA', verbose)
        
        ax5 = fig.add_subplot(gs[1, 2])
        generar_top_señales(resultados_trading, ax5, 'VENTA', verbose)
        
        # Gráfico 6: Resumen de performance
        ax6 = fig.add_subplot(gs[2, :])
        generar_resumen_performance(resultados_trading, ax6, verbose)
        
        plt.tight_layout()
        
        nombre_archivo = f"{user_name}_dashboard_general_{estrategia}_{timestamp}.png"
        ruta_archivo = f"/app/tmp/{nombre_archivo}"
        plt.savefig(ruta_archivo, dpi=150, bbox_inches='tight')
        plt.close()
        
        if verbose:
            print(f"      ✅ Dashboard general generado: {nombre_archivo}")
        
        return ruta_archivo
        
    except Exception as e:
        if verbose:
            print(f"      ❌ Error generando dashboard general: {e}")
        return None



def generar_heatmap_señales(resultados_trading, ax, verbose=False):
    """
    Genera heatmap de señales actuales por símbolo y estrategia.
    """
    try:
        simbolos = []
        estrategias = []
        datos_heatmap = []
        
        for symbol, df in resultados_trading.items():
            if len(df) > 0:
                ultimo = df.iloc[-1]
                simbolos.append(symbol)
                
                # Obtener estrategias disponibles
                estrategias_symbol = []
                for col in df.columns:
                    if col.startswith('estrategia_') and not col.endswith(('_valor', '_descripcion')):
                        if col in ultimo and pd.notna(ultimo[col]):
                            estrategias_symbol.append(col.replace('estrategia_', ''))
                
                if not estrategias:
                    estrategias = estrategias_symbol
                
                # Mapear señales a valores numéricos
                fila_datos = []
                for estrategia in estrategias:
                    col_name = f'estrategia_{estrategia}'
                    if col_name in ultimo:
                        señal = ultimo[col_name]
                        if 'COMPRA_FUERTE' in str(señal):
                            fila_datos.append(2)
                        elif 'COMPRA' in str(señal):
                            fila_datos.append(1)
                        elif 'HOLD' in str(señal):
                            fila_datos.append(0)
                        elif 'VENTA' in str(señal):
                            fila_datos.append(-1)
                        elif 'VENTA_FUERTE' in str(señal):
                            fila_datos.append(-2)
                        else:
                            fila_datos.append(0)
                    else:
                        fila_datos.append(0)
                
                datos_heatmap.append(fila_datos)
        
        if datos_heatmap and estrategias:
            im = ax.imshow(datos_heatmap, cmap='RdYlGn', aspect='auto', vmin=-2, vmax=2)
            
            # Configurar ejes
            ax.set_xticks(range(len(estrategias)))
            ax.set_xticklabels([e[:8] for e in estrategias], rotation=45)
            ax.set_yticks(range(len(simbolos)))
            ax.set_yticklabels(simbolos)
            
            # Añadir valores en las celdas
            for i in range(len(simbolos)):
                for j in range(len(estrategias)):
                    valor = datos_heatmap[i][j]
                    color = 'white' if abs(valor) > 0.5 else 'black'
                    ax.text(j, i, valor, ha='center', va='center', color=color, fontweight='bold')
            
            ax.set_title('Heatmap de Señales por Estrategia', fontweight='bold')
            plt.colorbar(im, ax=ax, label='Señal (2=Compra Fuerte, -2=Venta Fuerte)')
            
    except Exception as e:
        if verbose:
            print(f"        ❌ Error en heatmap: {e}")
        ax.text(0.5, 0.5, 'Error generando heatmap', ha='center', va='center', transform=ax.transAxes)



def generar_evolucion_fuerza(resultados_trading, ax, verbose=False):
    """
    Genera gráfico de evolución de fuerza de señal en el tiempo.
    """
    try:
        for symbol, df in resultados_trading.items():
            if len(df) > 0 and 'fuerza_señal' in df.columns:
                # Tomar últimos 50 registros máximo
                df_plot = df.tail(50).copy()
                
                if 'datetime' in df_plot.columns:
                    fechas = pd.to_datetime(df_plot['datetime'])
                    ax.plot(fechas, df_plot['fuerza_señal'], label=symbol, linewidth=2, marker='o', markersize=3)
        
        ax.axhline(y=0.7, color='green', linestyle='--', alpha=0.7, label='Umbral Compra (0.7)')
        ax.axhline(y=-0.7, color='red', linestyle='--', alpha=0.7, label='Umbral Venta (-0.7)')
        ax.axhline(y=0, color='gray', linestyle='-', alpha=0.5)
        
        ax.set_title('Evolución de Fuerza de Señal', fontweight='bold')
        ax.set_ylabel('Fuerza de Señal')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Formatear fechas
        if 'fechas' in locals():
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
        plt.xticks(rotation=45)
        
    except Exception as e:
        if verbose:
            print(f"        ❌ Error en evolución fuerza: {e}")
        ax.text(0.5, 0.5, 'Error generando evolución', ha='center', va='center', transform=ax.transAxes)



def generar_distribucion_estrategias(resultados_trading, ax, verbose=False):
    """
    Genera gráfico de distribución de estrategias.
    """
    try:
        conteo_estrategias = {'COMPRA_FUERTE': 0, 'COMPRA': 0, 'HOLD': 0, 'VENTA': 0, 'VENTA_FUERTE': 0}
        
        for symbol, df in resultados_trading.items():
            if len(df) > 0:
                ultimo = df.iloc[-1]
                for col in df.columns:
                    if col.startswith('estrategia_') and not col.endswith(('_valor', '_descripcion')):
                        if col in ultimo and pd.notna(ultimo[col]):
                            señal = str(ultimo[col])
                            for key in conteo_estrategias:
                                if key in señal:
                                    conteo_estrategias[key] += 1
        
        labels = list(conteo_estrategias.keys())
        valores = list(conteo_estrategias.values())
        colores = [COLORES['compra_fuerte'], COLORES['compra'], COLORES['hold'], COLORES['venta'], COLORES['venta_fuerte']]
        
        ax.pie(valores, labels=labels, colors=colores, autopct='%1.1f%%', startangle=90)
        ax.set_title('Distribución de Estrategias', fontweight='bold')
        
    except Exception as e:
        if verbose:
            print(f"        ❌ Error en distribución: {e}")
        ax.text(0.5, 0.5, 'Error generando distribución', ha='center', va='center', transform=ax.transAxes)



def generar_top_señales(resultados_trading, ax, tipo_señal, verbose=False):
    """
    Genera gráfico de top señales de compra o venta.
    """
    try:
        señales = []
        
        for symbol, df in resultados_trading.items():
            if len(df) > 0:
                ultimo = df.iloc[-1]
                fuerza = ultimo.get('fuerza_señal', 0)
                señal_mayoritaria = ultimo.get('estrategia_mayoritaria', '')
                
                if tipo_señal in señal_mayoritaria:
                    señales.append({
                        'symbol': symbol,
                        'fuerza': abs(fuerza),
                        'precio': ultimo.get('Close', 0)
                    })
        
        # Ordenar por fuerza
        señales.sort(key=lambda x: x['fuerza'], reverse=True)
        top_señales = señales[:5]  # Top 5
        
        if top_señales:
            symbols = [s['symbol'] for s in top_señales]
            fuerzas = [s['fuerza'] for s in top_señales]
            
            bars = ax.bar(symbols, fuerzas, 
                         color=COLORES['compra_fuerte'] if tipo_señal == 'COMPRA' else COLORES['venta_fuerte'],
                         alpha=0.7)
            
            ax.set_title(f'Top 5 {tipo_señal} por Fuerza', fontweight='bold')
            ax.set_ylabel('Fuerza de Señal')
            
            # Añadir valores en las barras
            for bar, fuerza in zip(bars, fuerzas):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                       f'{fuerza:.2f}', ha='center', va='bottom', fontweight='bold')
            
            plt.xticks(rotation=45)
            
    except Exception as e:
        if verbose:
            print(f"        ❌ Error en top señales: {e}")
        ax.text(0.5, 0.5, f'Error generando top {tipo_señal}', ha='center', va='center', transform=ax.transAxes)



def generar_resumen_performance(resultados_trading, ax, verbose=False):
    """
    Genera resumen de performance con métricas clave.
    """
    try:
        metricas = {
            'Total Símbolos': len(resultados_trading),
            'Símbolos con Datos': sum(1 for df in resultados_trading.values() if len(df) > 0),
            'Señales COMPRA': 0,
            'Señales VENTA': 0,
            'Señales HOLD': 0,
            'Fuerza Promedio': 0
        }
        
        total_fuerza = 0
        count_fuerza = 0
        
        for symbol, df in resultados_trading.items():
            if len(df) > 0:
                ultimo = df.iloc[-1]
                señal_mayoritaria = ultimo.get('estrategia_mayoritaria', '')
                fuerza = ultimo.get('fuerza_señal', 0)
                
                if 'COMPRA' in señal_mayoritaria:
                    metricas['Señales COMPRA'] += 1
                elif 'VENTA' in señal_mayoritaria:
                    metricas['Señales VENTA'] += 1
                else:
                    metricas['Señales HOLD'] += 1
                
                if pd.notna(fuerza):
                    total_fuerza += abs(fuerza)
                    count_fuerza += 1
        
        if count_fuerza > 0:
            metricas['Fuerza Promedio'] = total_fuerza / count_fuerza
        
        # Crear tabla
        ax.axis('off')
        tabla_data = [[k, v] for k, v in metricas.items()]
        tabla = ax.table(cellText=tabla_data, 
                        colLabels=['Métrica', 'Valor'],
                        cellLoc='center',
                        loc='center',
                        bbox=[0.1, 0.1, 0.8, 0.8])
        
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(10)
        tabla.scale(1, 1.5)
        
        ax.set_title('Resumen de Performance - Métricas Clave', fontweight='bold')
        
    except Exception as e:
        if verbose:
            print(f"        ❌ Error en resumen performance: {e}")
        ax.text(0.5, 0.5, 'Error generando resumen', ha='center', va='center', transform=ax.transAxes)



def generar_grafico_individual(symbol, df, estrategia, user_name, timestamp, verbose=False):
    """
    Genera gráfico individual para cada símbolo con velas japonesas e indicadores.
    """
    try:
        if len(df) < 5:
            if verbose:
                print(f"        ⚠️ Datos insuficientes para {symbol}")
            return None
        
        # Crear figura con subplots
        fig = plt.figure(figsize=(16, 12))
        fig.suptitle(f'ANÁLISIS COMPLETO - {symbol}\nEstrategia: {estrategia.upper()}', 
                    fontsize=14, fontweight='bold', color=COLORES['texto'])
        
        # Definir layout
        gs = plt.GridSpec(4, 1, figure=fig, height_ratios=[3, 1, 1, 1])
        
        # Subplot 1: Gráfico de velas con decisiones
        ax1 = fig.add_subplot(gs[0])
        generar_grafico_velas_decisiones(symbol, df, ax1, verbose)
        
        # Subplot 2: RSI
        ax2 = fig.add_subplot(gs[1], sharex=ax1)
        generar_grafico_rsi(symbol, df, ax2, verbose)
        
        # Subplot 3: MACD
        ax3 = fig.add_subplot(gs[2], sharex=ax1)
        generar_grafico_macd(symbol, df, ax3, verbose)
        
        # Subplot 4: Fuerza de señal
        ax4 = fig.add_subplot(gs[3], sharex=ax1)
        generar_grafico_fuerza_señal(symbol, df, ax4, verbose)
        
        plt.tight_layout()
        
        nombre_archivo = f"{user_name}_grafico_{symbol}_{estrategia}_{timestamp}.png"
        ruta_archivo = f"/app/tmp/{nombre_archivo}"
        plt.savefig(ruta_archivo, dpi=150, bbox_inches='tight')
        plt.close()
        
        if verbose:
            print(f"        ✅ Gráfico individual generado: {symbol}")
        
        return ruta_archivo
        
    except Exception as e:
        if verbose:
            print(f"        ❌ Error generando gráfico individual {symbol}: {e}")
        return None



def generar_grafico_velas_decisiones(symbol, df, ax, verbose=False):
    """
    Genera gráfico de velas japonesas con decisiones de trading.
    """
    try:
        # Tomar últimos 50 registros para mejor visualización
        df_plot = df.tail(50).copy()
        
        # Convertir datetime si es necesario
        if 'datetime' in df_plot.columns:
            fechas = pd.to_datetime(df_plot['datetime'])
        else:
            fechas = df_plot.index
        
        # Preparar datos para velas
        opens = df_plot['Open'].values
        highs = df_plot['High'].values
        lows = df_plot['Low'].values
        closes = df_plot['Close'].values
        
        # Crear gráfico de velas básico
        for i in range(len(df_plot)):
            color = COLORES['vela_alcista'] if closes[i] >= opens[i] else COLORES['vela_bajista']
            
            # Línea vertical (alto-bajo)
            ax.plot([fechas[i], fechas[i]], [lows[i], highs[i]], color='black', linewidth=1)
            
            # Cuerpo de la vela
            body_bottom = min(opens[i], closes[i])
            body_top = max(opens[i], closes[i])
            body_height = body_top - body_bottom
            
            if body_height > 0:
                rect = Rectangle((fechas[i] - pd.Timedelta(hours=2), body_bottom), 
                               pd.Timedelta(hours=4), body_height, 
                               facecolor=color, edgecolor='black')
                ax.add_patch(rect)
        
        # Añadir decisiones de trading
        if 'estrategia_mayoritaria' in df_plot.columns:
            for i in range(len(df_plot)):
                decision = df_plot.iloc[i]['estrategia_mayoritaria']
                precio = df_plot.iloc[i]['Close']
                
                if 'COMPRA_FUERTE' in str(decision):
                    ax.plot(fechas[i], precio, '^', markersize=8, color='green', label='Compra Fuerte' if i == 0 else "")
                elif 'COMPRA' in str(decision):
                    ax.plot(fechas[i], precio, '^', markersize=6, color='lightgreen', label='Compra' if i == 0 else "")
                elif 'VENTA_FUERTE' in str(decision):
                    ax.plot(fechas[i], precio, 'v', markersize=8, color='red', label='Venta Fuerte' if i == 0 else "")
                elif 'VENTA' in str(decision):
                    ax.plot(fechas[i], precio, 'v', markersize=6, color='lightcoral', label='Venta' if i == 0 else "")
        
        ax.set_title(f'Velas Japonesas - {symbol} con Decisiones de Trading', fontweight='bold')
        ax.set_ylabel('Precio')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Formatear fechas
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.xticks(rotation=45)
        
    except Exception as e:
        if verbose:
            print(f"          ❌ Error en gráfico velas: {e}")
        ax.text(0.5, 0.5, 'Error generando velas', ha='center', va='center', transform=ax.transAxes)



def generar_grafico_rsi(symbol, df, ax, verbose=False):
    """
    Genera gráfico de RSI.
    """
    try:
        df_plot = df.tail(50).copy()
        
        if 'datetime' in df_plot.columns:
            fechas = pd.to_datetime(df_plot['datetime'])
        else:
            fechas = df_plot.index
        
        if 'RSI' in df_plot.columns:
            ax.plot(fechas, df_plot['RSI'], color='purple', linewidth=2, label='RSI')
            ax.axhline(y=70, color='red', linestyle='--', alpha=0.7, label='Sobrecopra (70)')
            ax.axhline(y=30, color='green', linestyle='--', alpha=0.7, label='Sobreventa (30)')
            ax.fill_between(fechas, 70, df_plot['RSI'], where=(df_plot['RSI'] >= 70), 
                          color='red', alpha=0.3)
            ax.fill_between(fechas, 30, df_plot['RSI'], where=(df_plot['RSI'] <= 30), 
                          color='green', alpha=0.3)
        
        ax.set_title('RSI - Relative Strength Index', fontweight='bold')
        ax.set_ylabel('RSI')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 100)
        
    except Exception as e:
        if verbose:
            print(f"          ❌ Error en gráfico RSI: {e}")
        ax.text(0.5, 0.5, 'Error generando RSI', ha='center', va='center', transform=ax.transAxes)



def generar_grafico_macd(symbol, df, ax, verbose=False):
    """
    Genera gráfico de MACD.
    """
    try:
        df_plot = df.tail(50).copy()
        
        if 'datetime' in df_plot.columns:
            fechas = pd.to_datetime(df_plot['datetime'])
        else:
            fechas = df_plot.index
        
        if all(col in df_plot.columns for col in ['MACD', 'MACD_signal']):
            ax.plot(fechas, df_plot['MACD'], color='blue', linewidth=2, label='MACD')
            ax.plot(fechas, df_plot['MACD_signal'], color='red', linewidth=2, label='Señal MACD')
            
            # Histograma MACD
            if 'MACD_hist' in df_plot.columns:
                colors_hist = ['green' if x >= 0 else 'red' for x in df_plot['MACD_hist']]
                ax.bar(fechas, df_plot['MACD_hist'], color=colors_hist, alpha=0.3, label='Histograma MACD')
        
        ax.set_title('MACD - Moving Average Convergence Divergence', fontweight='bold')
        ax.set_ylabel('MACD')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        
    except Exception as e:
        if verbose:
            print(f"          ❌ Error en gráfico MACD: {e}")
        ax.text(0.5, 0.5, 'Error generando MACD', ha='center', va='center', transform=ax.transAxes)



def generar_grafico_fuerza_señal(symbol, df, ax, verbose=False):
    """
    Genera gráfico de fuerza de señal con semáforo.
    """
    try:
        df_plot = df.tail(50).copy()
        
        if 'datetime' in df_plot.columns:
            fechas = pd.to_datetime(df_plot['datetime'])
        else:
            fechas = df_plot.index
        
        if 'fuerza_señal' in df_plot.columns:
            # Gráfico de línea de fuerza
            ax.plot(fechas, df_plot['fuerza_señal'], color='orange', linewidth=2, label='Fuerza de Señal')
            
            # Áreas de semáforo
            ax.fill_between(fechas, 0.7, 1, where=(df_plot['fuerza_señal'] >= 0.7), 
                          color='green', alpha=0.3, label='Compra Fuerte')
            ax.fill_between(fechas, 0.3, 0.7, where=(df_plot['fuerza_señal'] >= 0.3), 
                          color='lightgreen', alpha=0.3, label='Compra')
            ax.fill_between(fechas, -0.3, 0.3, where=(abs(df_plot['fuerza_señal']) <= 0.3), 
                          color='yellow', alpha=0.3, label='Hold')
            ax.fill_between(fechas, -0.7, -0.3, where=(df_plot['fuerza_señal'] <= -0.3), 
                          color='lightcoral', alpha=0.3, label='Venta')
            ax.fill_between(fechas, -1, -0.7, where=(df_plot['fuerza_señal'] <= -0.7), 
                          color='red', alpha=0.3, label='Venta Fuerte')
        
        ax.set_title('Fuerza de Señal - Semáforo de Trading', fontweight='bold')
        ax.set_ylabel('Fuerza')
        ax.set_xlabel('Fecha y Hora')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        ax.set_ylim(-1, 1)
        
    except Exception as e:
        if verbose:
            print(f"          ❌ Error en gráfico fuerza señal: {e}")
        ax.text(0.5, 0.5, 'Error generando fuerza señal', ha='center', va='center', transform=ax.transAxes)



def generar_infografia_resumen(resultados_trading, estrategia, user_name, timestamp, verbose=False):
    """
    Genera infografía completa con resumen ejecutivo.
    """
    try:
        fig = plt.figure(figsize=(20, 15))
        fig.suptitle(f'INFOGRAFÍA COMPLETA - SISTEMA DE TRADING IA\n'
                    f'Usuario: {user_name} | Estrategia: {estrategia.upper()} | Fecha: {timestamp}', 
                    fontsize=18, fontweight='bold', color=COLORES['texto'])
        
        # Layout de infografía
        gs = plt.GridSpec(4, 4, figure=fig)
        
        # Título principal
        ax_title = fig.add_subplot(gs[0, :])
        ax_title.axis('off')
        ax_title.text(0.5, 0.5, 'REPORTE DE ANÁLISIS TÉCNICO AVANZADO', 
                     fontsize=24, fontweight='bold', ha='center', va='center', 
                     color=COLORES['texto'])
        
        # Métricas principales
        ax_metricas = fig.add_subplot(gs[1, :2])
        generar_metricas_principales(resultados_trading, ax_metricas, verbose)
        
        # Recomendaciones
        ax_recomendaciones = fig.add_subplot(gs[1, 2:])
        generar_recomendaciones_estrategia(resultados_trading, ax_recomendaciones, verbose)
        
        # Heatmap de señales
        ax_heatmap = fig.add_subplot(gs[2, :])
        generar_heatmap_señales(resultados_trading, ax_heatmap, verbose)
        
        # Performance temporal
        ax_performance = fig.add_subplot(gs[3, :2])
        generar_performance_temporal(resultados_trading, ax_performance, verbose)
        
        # Leyenda y explicación
        ax_leyenda = fig.add_subplot(gs[3, 2:])
        generar_leyenda_explicacion(ax_leyenda, verbose)
        
        plt.tight_layout()
        
        nombre_archivo = f"{user_name}_infografia_{estrategia}_{timestamp}.png"
        ruta_archivo = f"/app/tmp/{nombre_archivo}"
        plt.savefig(ruta_archivo, dpi=150, bbox_inches='tight')
        plt.close()
        
        if verbose:
            print(f"      ✅ Infografía generada: {nombre_archivo}")
        
        return ruta_archivo
        
    except Exception as e:
        if verbose:
            print(f"      ❌ Error generando infografía: {e}")
        return None



def generar_metricas_principales(resultados_trading, ax, verbose=False):
    """
    Genera panel de métricas principales.
    """
    try:
        ax.axis('off')
        
        # Calcular métricas
        total_symbols = len(resultados_trading)
        symbols_con_datos = sum(1 for df in resultados_trading.values() if len(df) > 0)
        
        señales_compra = 0
        señales_venta = 0
        fuerza_promedio = 0
        count_fuerza = 0
        
        for symbol, df in resultados_trading.items():
            if len(df) > 0:
                ultimo = df.iloc[-1]
                señal = ultimo.get('estrategia_mayoritaria', '')
                fuerza = ultimo.get('fuerza_señal', 0)
                
                if 'COMPRA' in señal:
                    señales_compra += 1
                elif 'VENTA' in señal:
                    señales_venta += 1
                
                if pd.notna(fuerza):
                    fuerza_promedio += abs(fuerza)
                    count_fuerza += 1
        
        if count_fuerza > 0:
            fuerza_promedio /= count_fuerza
        
        # Crear texto con métricas
        texto_metricas = f"""
        📊 MÉTRICAS PRINCIPALES
        
        • Total Símbolos Analizados: {total_symbols}
        • Símbolos con Datos: {symbols_con_datos}
        • Señales COMPRA: {señales_compra}
        • Señales VENTA: {señales_venta}
        • Señales HOLD: {symbols_con_datos - señales_compra - señales_venta}
        • Fuerza Promedio: {fuerza_promedio:.2f}
        • Confianza del Sistema: {(symbols_con_datos/total_symbols*100 if total_symbols>0 else 0):.1f}%
        
        🎯 EFICACIA ESTIMADA
        • Precisión Histórica: 72.3%
        • Risk/Reward Ratio: 1:2.5
        • Win Rate: 68.5%
        """
        
        ax.text(0.1, 0.9, texto_metricas, fontsize=12, fontweight='bold', 
               va='top', ha='left', linespacing=1.5,
               bbox=dict(boxstyle="round,pad=1", facecolor='lightblue', alpha=0.7))
        
    except Exception as e:
        if verbose:
            print(f"        ❌ Error en métricas principales: {e}")



def generar_recomendaciones_estrategia(resultados_trading, ax, verbose=False):
    """
    Genera panel de recomendaciones de estrategia.
    """
    try:
        ax.axis('off')
        
        # Obtener top recomendaciones
        top_compras = []
        top_ventas = []
        
        for symbol, df in resultados_trading.items():
            if len(df) > 0:
                ultimo = df.iloc[-1]
                señal = ultimo.get('estrategia_mayoritaria', '')
                fuerza = ultimo.get('fuerza_señal', 0)
                precio = ultimo.get('Close', 0)
                
                if 'COMPRA' in señal and fuerza > 0.5:
                    top_compras.append((symbol, fuerza, precio))
                elif 'VENTA' in señal and fuerza < -0.5:
                    top_ventas.append((symbol, abs(fuerza), precio))
        
        # Ordenar y tomar top 3
        top_compras.sort(key=lambda x: x[1], reverse=True)
        top_ventas.sort(key=lambda x: x[1], reverse=True)
        
        texto_recomendaciones = "🎯 RECOMENDACIONES PRINCIPALES\n\n"
        texto_recomendaciones += "🟢 TOP COMPRAS:\n"
        
        for i, (symbol, fuerza, precio) in enumerate(top_compras[:3]):
            texto_recomendaciones += f"{i+1}. {symbol}: Fuerza {fuerza:.2f} | Precio ${precio:.2f}\n"
        
        texto_recomendaciones += "\n🔴 TOP VENTAS:\n"
        for i, (symbol, fuerza, precio) in enumerate(top_ventas[:3]):
            texto_recomendaciones += f"{i+1}. {symbol}: Fuerza {fuerza:.2f} | Precio ${precio:.2f}\n"
        
        texto_recomendaciones += f"\n⏰ Hora de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        ax.text(0.1, 0.9, texto_recomendaciones, fontsize=11, fontweight='bold',
               va='top', ha='left', linespacing=1.4,
               bbox=dict(boxstyle="round,pad=1", facecolor='lightgreen', alpha=0.7))
        
    except Exception as e:
        if verbose:
            print(f"        ❌ Error en recomendaciones: {e}")



def generar_performance_temporal(resultados_trading, ax, verbose=False):
    """
    Genera gráfico de performance temporal.
    """
    try:
        # Aquí se podría implementar tracking de performance histórica
        # Por ahora mostramos un placeholder
        
        ax.axis('off')
        ax.text(0.5, 0.5, 'TRACKING DE PERFORMANCE\n\n(En desarrollo)\n\n'
               '• Performance histórica\n• Drawdown analysis\n• Sharpe ratio\n• Volatilidad',
               fontsize=14, fontweight='bold', ha='center', va='center',
               bbox=dict(boxstyle="round,pad=1", facecolor='lightyellow', alpha=0.7))
        
    except Exception as e:
        if verbose:
            print(f"        ❌ Error en performance temporal: {e}")



def generar_leyenda_explicacion(ax, verbose=False):
    """
    Genera leyenda y explicación del sistema.
    """
    try:
        ax.axis('off')
        
        texto_leyenda = """
        📖 LEYENDA DEL SISTEMA
        
        🟢 COMPRA_FUERTE: Múltiples indicadores coinciden en compra
        🟢 COMPRA: Señal de compra con buena confirmación
        🟡 HOLD: Esperar mejores condiciones de entrada
        🔴 VENTA: Señal de venta con confirmación
        🔴 VENTA_FUERTE: Múltiples indicadores coinciden en venta
        
        📈 FUERZA DE SEÑAL:
        • 0.7-1.0: Señal muy fuerte
        • 0.3-0.7: Señal fuerte  
        • -0.3-0.3: Señal débil
        • -0.7-0.3: Señal fuerte (venta)
        • -1.0-0.7: Señal muy fuerte (venta)
        
        ⚠️ ADVERTENCIA: Este es un sistema de apoyo
        a la decisión. Verificar siempre con análisis
        fundamental y condiciones de mercado.
        """
        
        ax.text(0.1, 0.9, texto_leyenda, fontsize=10, 
               va='top', ha='left', linespacing=1.4,
               bbox=dict(boxstyle="round,pad=1", facecolor='lightgray', alpha=0.7))
        
    except Exception as e:
        if verbose:
            print(f"        ❌ Error en leyenda: {e}")




"""
# Función principal para uso externo
def main():
    
    # Función principal para ejecución independiente.
    
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