# core/visualization.py
import altair as alt
import pandas as pd

def crear_histograma(tabla_estadistica: pd.DataFrame) -> alt.Chart:
    '''
    Genera un gráfico de barras (histograma) usando Altair basado en la tabla de frecuencias.
    '''
    datos_grafico = tabla_estadistica.reset_index() # Reiniciar el índice para Altair
    
    grafico = alt.Chart(datos_grafico).mark_bar(size=40).encode(
        # Eje X: Usamos la columna 'Valores' como Ordinal (:O)
        x=alt.X('Valores:O', axis=alt.Axis(labelAngle=0), title='Valores'),
        # Eje Y: Usamos la Frecuencia Absoluta
        y=alt.Y('Frecuencia Absoluta (fi)', title='Frecuencia Absoluta'),
        tooltip=['Valores', 'Frecuencia Absoluta (fi)']
    ).properties(
        height=400,
        title='Histograma de Frecuencias'
    )
    
    return grafico