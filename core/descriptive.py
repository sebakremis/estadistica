# core/descriptive.py
import pandas as pd
import numpy as np

def crear_tabla_estadistica(valores: pd.Series) -> pd.DataFrame:
    '''
    Crea una tabla estadística a partir de valores numéricos.
    Calcula frecuencias absolutas, relativas, acumuladas y porcentajes.
    '''    
    # Calcular Frecuencia Absoluta (fi)
    tabla = valores.value_counts().sort_index().to_frame(name='Frecuencia Absoluta (fi)')

    # Calcular Frecuencia Relativa (hi)
    n = len(valores)
    tabla['Frecuencia Relativa (hi)'] = tabla['Frecuencia Absoluta (fi)'] / n

    # Calcular Porcentaje (pi)
    tabla['Porcentaje (pi)'] = tabla['Frecuencia Relativa (hi)'] * 100

    # Calcular Frecuencia Acumulada (Fi)
    tabla['Frecuencia Acumulada (Fi)'] = tabla['Frecuencia Absoluta (fi)'].cumsum()

    # Calcular Frecuencia Relativa Acumulada (Hi)
    tabla['Frecuencia Rel Acumulada (Hi)'] = tabla['Frecuencia Relativa (hi)'].cumsum()

    tabla.index.name = 'Valores'
    return tabla.round(4)

def calcular_metricas_principales(serie_valores: pd.Series) -> dict:
    '''
    Calcula las métricas descriptivas principales (Media, Mediana, Moda, etc.)
    y las retorna en un diccionario para fácil acceso.
    '''
    moda_series = serie_valores.mode()
    moda_str = ", ".join(map(str, moda_series.tolist()))
    desvio_estandar = serie_valores.std()
    media = serie_valores.mean()

    return {
        "media": media,
        "mediana": serie_valores.median(),
        "desviacion": desvio_estandar,
        "varianza": serie_valores.var(),
        "moda": moda_str,
        "n": len(serie_valores),
        "coef_variacion": (serie_valores.std() / serie_valores.mean()) * 100 if serie_valores.mean() != 0 else 0,
        "rango": serie_valores.max() - serie_valores.min()
    }

def calcular_metricas_agrupadas(df_intervalos: pd.DataFrame) -> dict:
    """
    Calcula métricas estadísticas precisas para datos agrupados en intervalos
    usando fórmulas de interpolación para Mediana y Moda.
    """
    # 1. Preparación de datos
    # Reseteamos el índice para asegurarnos de poder acceder a filas anterior/siguiente por posición (0, 1, 2...)
    df = df_intervalos.reset_index(drop=True)
    
    # Nombres de columnas abreviados para facilitar lectura del código
    col_fi = 'Frecuencia Absoluta (fi)'
    col_Fi = 'Frecuencia Acumulada (Fi)'
    col_mc = 'Marca de Clase'
    col_li = 'Límite Inferior'
    col_ls = 'Límite Superior'
    
    N = df[col_fi].sum()
    
    # ---------------------------------------------------------
    # 2. MEDIA (Ponderada)
    # Fórmula: Sum(xi * fi) / N
    # ---------------------------------------------------------
    suma_ponderada = (df[col_fi] * df[col_mc]).sum()
    media = suma_ponderada / N
    
    # ---------------------------------------------------------
    # 3. MEDIANA (Interpolada)
    # Fórmula: Li + ((N/2 - F_ant) / fi) * amplitud
    # ---------------------------------------------------------
    posicion_mediana = N / 2
    
    # Buscamos la primera fila donde la Frecuencia Acumulada supera a N/2
    fila_mediana = df[df[col_Fi] >= posicion_mediana].iloc[0]
    idx_mediana = df[df[col_Fi] >= posicion_mediana].index[0]
    
    # Datos del intervalo mediano
    Li = fila_mediana[col_li]
    fi_mediana = fila_mediana[col_fi]
    amplitud = fila_mediana[col_ls] - Li
    
    # Frecuencia acumulada anterior (Fi-1)
    # Si es el primer intervalo, la acumulada anterior es 0
    Fi_anterior = df.at[idx_mediana - 1, col_Fi] if idx_mediana > 0 else 0
    
    mediana = Li + ((posicion_mediana - Fi_anterior) / fi_mediana) * amplitud
    
    # ---------------------------------------------------------
    # 4. MODA (Interpolada)
    # Fórmula: Li + (d1 / (d1 + d2)) * amplitud
    # Donde d1 = fi - fi_anterior  y  d2 = fi - fi_siguiente
    # ---------------------------------------------------------
    # Encontramos el índice con la mayor frecuencia
    idx_moda = df[col_fi].idxmax()
    fila_moda = df.loc[idx_moda]
    
    Li_moda = fila_moda[col_li]
    fi_moda = fila_moda[col_fi]
    amplitud_moda = fila_moda[col_ls] - Li_moda
    
    # Frecuencias vecinas (Manejando bordes si la moda está en el primer o último intervalo)
    fi_prev = df.at[idx_moda - 1, col_fi] if idx_moda > 0 else 0
    fi_next = df.at[idx_moda + 1, col_fi] if idx_moda < (len(df) - 1) else 0
    
    d1 = fi_moda - fi_prev
    d2 = fi_moda - fi_next
    
    # Evitar división por cero si d1+d2 es 0 (caso raro donde todos los fi son iguales)
    if (d1 + d2) == 0:
        moda = fila_moda[col_mc] # Fallback a marca de clase
    else:
        moda = Li_moda + (d1 / (d1 + d2)) * amplitud_moda
    
    # Redondeamos la moda a 2 decimales
    moda = round(moda, 2)

    # ---------------------------------------------------------
    # 5. VARIANZA Y DESVIACIÓN
    # ---------------------------------------------------------
    # Varianza Ponderada: Sum(fi * (xi - media)^2) / (N - 1)
    suma_cuadrados = (df[col_fi] * (df[col_mc] - media)**2).sum()
    varianza = suma_cuadrados / (N - 1) if N > 1 else 0
    desviacion = np.sqrt(varianza)
    
    # Coeficiente de Variación
    cv = (desviacion / media) * 100 if media != 0 else 0
    
    # Rango Total
    rango = df[col_ls].max() - df[col_li].min()

    return {
        "media": media,
        "mediana": mediana,
        "moda": moda,
        "n": N,
        "varianza": varianza,
        "desviacion": desviacion,
        "coef_variacion": cv,
        "rango": rango
    }
    