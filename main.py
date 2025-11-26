import pandas as pd
import streamlit as st

from core.utils import procesar_datos
from core.descriptive import crear_tabla_estadistica, calcular_metricas_principales
from core.visualization import crear_histograma

# Configuración de la página
st.set_page_config(layout="wide", page_title="Statboard", page_icon="📊")

def main():
    st.title("📊 StatBoard")
    st.write("Estadística Descriptiva")

    # --- Sidebar para entrada de datos ---
    with st.sidebar:
        st.header("Configuración de Datos")
        valores_default = "15 16 14 12 15 15 14 18 16 12 14 12 15 14 14 15 14 13 16 16 13 16 17 14 13 12 14 17 13 14 13 15 15 15 18 14 16 14 14 14 13 15 12 13 14 14 13 13 17 13"
        entrada_usuario = st.text_area(
            "Reemplaza con tus datos:",
            value=valores_default,
            height=200,
            help="Reemplaza los valores del ejemplo con números separados por espacios o comas."
        )
        st.caption("💡 **Tip:** Puedes copiar datos desde Excel/CSV y pegarlos en el cuadro.")

    # 1. Procesar los datos (Usando core/utils.py)
    serie_valores = procesar_datos(entrada_usuario)

    if serie_valores.empty:
        st.warning("👈 Ingresa datos numéricos en el menú lateral, luego presiona Ctrl+Enter para actualizar el tablero.")
        return

    st.write("## Distribución de Frecuencias")
    
    # 2. Crear Tabla Estadística (Usando core/descriptive.py)
    tabla_estadistica = crear_tabla_estadistica(serie_valores)

    st.dataframe(tabla_estadistica,
                 width='stretch',
                 column_config={
                    'Valores': st.column_config.NumberColumn(format="%.2f", width='medium'),
                    'Frecuencia Absoluta (fi)': st.column_config.NumberColumn(format="%d", width='medium'),
                    'Frecuencia Relativa (hi)': st.column_config.NumberColumn(format="%.2f", width='medium'),
                    'Porcentaje (pi)': st.column_config.NumberColumn(format="%.2f%%", width='medium'),
                    'Frecuencia Acumulada (Fi)': st.column_config.NumberColumn(format="%d", width='medium'),
                    'Frecuencia Relativa Acumulada (Hi)': st.column_config.NumberColumn(format="%.2f", width='medium'),
                 }
    )
    
    st.divider()
    
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Parámetros")
        
        # 3. Calcular Métricas (Usando core/descriptive.py)
        # Esto elimina el cálculo directo en el main
        metricas = calcular_metricas_principales(serie_valores)

        # Visualización de métricas
        kpi1, kpi2 = st.columns(2)
        kpi1.metric("Media", f"{metricas['media']:.2f}")
        kpi2.metric("Mediana", f"{metricas['mediana']:.2f}")
        
        kpi3, kpi4 = st.columns(2)
        kpi3.metric("Moda", metricas['moda'])
        kpi4.metric("N (Total)", metricas['n'])

        kpi5, kpi6 = st.columns(2)
        kpi5.metric("Varianza", f"{metricas['varianza']:.2f}")
        kpi6.metric("Desv. Estándar", f"{metricas['desviacion']:.2f}")
        
    with col2:
        # 4. Generar Gráfico (Usando core/visualization.py)
        # Pasamos la tabla estadística ya calculada
        grafico = crear_histograma(tabla_estadistica)
        st.altair_chart(grafico, width='stretch')

if __name__ == "__main__":
    main()
