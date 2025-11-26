# core/visualization.py
import pandas as pd
import plotly.express as px

def crear_histograma(tabla_estadistica: pd.DataFrame):
    datos = tabla_estadistica.reset_index()
    datos['Valores'] = datos['Valores'].astype(str)

    fig = px.bar(
        datos,
        x='Valores',
        y='Frecuencia Absoluta (fi)',
        title='Histograma de Frecuencias',
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
    )

    fig.update_traces(marker_line_color='white', marker_line_width=1)

    return fig


