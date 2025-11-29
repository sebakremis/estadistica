# core/visualization.py
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

def crear_histograma(tabla_estadistica: pd.DataFrame):
    datos = tabla_estadistica.reset_index()
    datos['Valores'] = datos['Valores'].astype(str)

    fig = px.bar(
        datos,
        x='Valores',
        y='Frecuencia Absoluta (fi)'
    )

    # Eliminar espacios entre barras
    fig.update_layout(
        bargap=0,
        bargroupgap=0,
        xaxis=dict(
            categoryorder='array',
            categoryarray=list(datos['Valores'])
        ),
        yaxis_title='Frecuencia Absoluta',
        xaxis_title='Valores',
        height=600
    )

    fig.update_traces(marker_line_color='white', marker_line_width=1)

    return fig

def crear_boxplot(metricas: dict, serie_original: pd.Series):
    """
    Crea un boxplot usando métricas pre-calculadas y detecta outliers
    basándose en la SERIE ORIGINAL de datos.
    
    Args:
        metricas (dict): Diccionario con Q1, Q3, IQR, Mediana.
        serie_original (pd.Series): La serie de datos crudos (numéricos).
        
    Returns:
        fig: Figura de matplotlib.
        outliers_series: Serie de pandas con los valores atípicos detectados.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # -----------------------------------------------------
    # 1. Configurar la Caja (Usando métricas calculadas)
    # -----------------------------------------------------
    iqr = metricas['rango_intercuartilico']
    q1 = metricas['Q1']
    q3 = metricas['Q3']
    mediana = metricas['mediana']
    
    # Límites de Tukey (Bigotes)
    limite_inferior = q1 - (1.5 * iqr)
    limite_superior = q3 + (1.5 * iqr)
    
    stats = [{
        'med': mediana,
        'q1': q1,
        'q3': q3,
        'whislo': limite_inferior, 
        'whishi': limite_superior,
        'label': 'Distribución'
    }]
    
    # Dibujamos la caja base (sin outliers automáticos)
    ax.bxp(stats, showfliers=False, patch_artist=True, 
           boxprops=dict(facecolor='#ADD8E6', edgecolor='blue'), # Azul claro
           medianprops=dict(color='red', linewidth=2))
    
    # -----------------------------------------------------
    # 2. Detectar y Graficar Outliers usando la SERIE ORIGINAL
    # -----------------------------------------------------
    
    # Filtramos directamente sobre la serie de datos crudos
    outliers_series = serie_original[
        (serie_original < limite_inferior) | 
        (serie_original > limite_superior)
    ].copy()
    
    if not outliers_series.empty:
        # Obtenemos los valores a graficar
        valores_y = outliers_series.values
        
        # Coordenada X fija (1) porque solo hay un boxplot centrado ahí
        valores_x = [1] * len(valores_y)
        
        # Graficamos los puntos rojos
        ax.scatter(valores_x, valores_y, 
                   color='red', 
                   marker='o', 
                   s=60, 
                   zorder=5, 
                   label='Outliers')
        
        # Agregar etiquetas de texto al lado del punto
        # Usamos un set para no superponer textos si hay valores repetidos
        valores_unicos_outliers = sorted(list(set(valores_y)))
        for val in valores_unicos_outliers:
             ax.text(1.02, val, f' {val:.2f}', verticalalignment='center', fontsize=8)

    # -----------------------------------------------------
    # 3. Estética
    # -----------------------------------------------------
    ax.set_title('Diagrama de Caja (Boxplot)', fontsize=16)
    ax.set_ylabel('Valores de la Serie')
    
    # Solo mostramos leyenda si hubo outliers
    if not outliers_series.empty:
        ax.legend(loc='upper right')
        
    ax.grid(True, linestyle='--', alpha=0.6, axis='y')

    # Convertir la serie de outliers a lista y eliminar duplicados
    lista_outliers = outliers_series.drop_duplicates().sort_values().to_list()   
    
    # Retornamos la serie para que el main pueda mostrarla en tabla
    return fig, lista_outliers
