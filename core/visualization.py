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

def crear_boxplot(metricas: dict, tabla_estadistica: pd.DataFrame):
    """
    Crea un boxplot usando métricas pre-calculadas y detecta outliers
    basándose en la columna 'Valores' (ya sea clase o marca de clase).
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # -----------------------------------------------------
    # 1. Configurar la Caja (Usando tus métricas interpoladas)
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
           boxprops=dict(facecolor='#ADD8E6', color='blue'), # Azul claro
           medianprops=dict(color='red', linewidth=2))
    
    # -----------------------------------------------------
    # 2. Detectar y Graficar Outliers usando columna 'Valores'
    # -----------------------------------------------------
    col_valores = 'Valores' 
    
    # Filtramos filas donde el valor (o marca de clase) escapa de los bigotes
    # NOTA: Usamos .copy() para evitar warnings de pandas
    outliers_df = tabla_estadistica[
        (tabla_estadistica[col_valores] < limite_inferior) | 
        (tabla_estadistica[col_valores] > limite_superior)
    ].copy()
    lista_outliers = outliers_df[col_valores].tolist() # Lista de valores atípicos para retorno
    
    if not outliers_df.empty:
        # Obtenemos los valores a graficar
        valores_y = outliers_df[col_valores].values
        
        # Coordenada X fija (1) porque solo hay un boxplot
        valores_x = [1] * len(valores_y)
        
        # Graficamos los puntos rojos
        ax.scatter(valores_x, valores_y, 
                   color='red', 
                   marker='o', 
                   s=60, 
                   zorder=5, 
                   label='Outliers')
        
        # Agregar etiquetas de texto al lado del punto
        for val in valores_y:
            ax.text(1.02, val, f' {val}', verticalalignment='center', fontsize=8)

    # -----------------------------------------------------
    # 3. Estética
    # -----------------------------------------------------
    ax.set_title('Diagrama de Caja (Boxplot)', fontsize=16)
    ax.set_ylabel('Valores / Marcas de Clase')
    ax.legend(loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.6, axis='y')
    
    return fig, lista_outliers
