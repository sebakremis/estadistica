# core/descriptive.py
import pandas as pd

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
    tabla['Frecuencia Relativa Acumulada (Hi)'] = tabla['Frecuencia Relativa (hi)'].cumsum()

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