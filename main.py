import pandas as pd
import streamlit as st
from core.utils import procesar_datos
from core.descriptive import crear_tabla_estadistica, calcular_metricas_principales
from core.visualization import crear_histograma
from core.intervals import crear_intervalos

# --- Ocultar mensaje "Press Ctrl+Enter en st.text_area()" ---
st.markdown("""
    <style>
    /* Hide the specific element that shows the input instructions */
    div[data-testid="InputInstructions"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Configuración de la página
st.set_page_config(layout="wide", page_title="Statboard", page_icon="📊")

def main():
    st.title("📊 StatBoard")
    st.write("Estadística Descriptiva")

    # --- Sidebar para entrada de datos ---
    with st.sidebar:
        st.header("Configuración de Datos")
        # Seleccionar datos discretos o por intervalos
        tipo_datos= st.radio("Tipo de Datos:", ("Discretos", "Por Intervalos"))

        # Si es continuo con intervalos, definir criterio de intervalos  
        if tipo_datos == "Por Intervalos":
            # Ingresar criterio de intervalos, opcionalmente número de intervalos
            criterio_intervalos = st.selectbox("Criterio de Intervalos:", 
                                              ("Raíz cuadrada", "Regla de Sturges", "Regla de Scott", "Número Personalizado"))
            if criterio_intervalos == "Número Personalizado":
                num_intervalos = st.number_input("Número de Intervalos:", min_value=1, value=5, step=1)
                criterio_intervalos = str(num_intervalos)
                          

        with st.form("form_datos"):
            valores_default = "50 42 61 55 48 50 39 52 58 45 53 49 50 44 65 51 47 56 40 54 48 59 43 50 55 52 46 53 49 57 41 62 48 50 54 45 58 51 38 52 49 47 55 60 44 53 50 46 59 52 48 54 42 57 49 51 35 63 47 55 50 43 58 52 46 49 53 66 45 54 50 48 56 42 51 59 47 37 53 55 49 44 60 52 46 50 58 41 54 48 64 53 47 55 50 45 51 57 43 52"
            entrada_usuario = st.text_area(
                "Datos:",
                value=valores_default,
                height=200,
                help="Reemplaza con tus datos, ingresando o pegando números separados por espacios o comas."
            )
            enviar = st.form_submit_button("Actualizar")

    # --- Procesar Datos ---
    if enviar:
        # 1. Obtenemos los datos ORIGINALES (sin agrupar)
        # Mantenemos esta serie pura para calcular métricas exactas (Media, Mediana, etc.)
        serie_original = procesar_datos(entrada_usuario)
        
        if serie_original.empty:
            st.warning("👈 Ingresa datos numéricos en el menú lateral...")
            return

        # Inicializamos variables para el flujo
        tabla_estadistica = pd.DataFrame()
        
        # 2. Lógica bifurcada: Discretos vs Continuos
        if tipo_datos == "Por Intervalos":
            # A. Generamos la tabla de intervalos (Límites, Marca de Clase, fi)
            tabla_estadistica = crear_intervalos(serie_original, criterio_intervalos)
            
            # B. Calculamos las columnas estadísticas DIRECTAMENTE aquí
            # (Evitamos reconstruir la serie y perder filas vacías)
            total_n = tabla_estadistica['Frecuencia Absoluta (fi)'].sum()
            
            tabla_estadistica['Frecuencia Relativa (hi)'] = tabla_estadistica['Frecuencia Absoluta (fi)'] / total_n
            tabla_estadistica['Porcentaje (pi)'] = tabla_estadistica['Frecuencia Relativa (hi)']
            tabla_estadistica['Frecuencia Acumulada (Fi)'] = tabla_estadistica['Frecuencia Absoluta (fi)'].cumsum()
            tabla_estadistica['Frecuencia Relativa Acumulada (Hi)'] = tabla_estadistica['Frecuencia Relativa (hi)'].cumsum()
            
            # C. Asignamos la columna 'Valores' para compatibilidad con el gráfico (usamos Marca de Clase)
            tabla_estadistica['Valores'] = tabla_estadistica['Marca de Clase']

            # Nota: Para las métricas, decidimos si usar los datos exactos o agrupados.
            # Lo profesional es usar los datos exactos (serie_original).
            serie_para_metricas = serie_original

        else: # Discretos
            # Para discretos, usamos la función existente
            tabla_estadistica = crear_tabla_estadistica(serie_original)
            serie_para_metricas = serie_original

        st.write("## Distribución de Frecuencias")

        # 3. Visualización de la Tabla
        # Configuración de columnas común
        config_columnas = {
            'Frecuencia Absoluta (fi)': st.column_config.NumberColumn(format="%d", width='small'),
            'Frecuencia Relativa (hi)': st.column_config.NumberColumn(format="%.4f", width='small'),
            'Porcentaje (pi)': st.column_config.NumberColumn(format="%.2f%%", width='small'),
            'Frecuencia Acumulada (Fi)': st.column_config.NumberColumn(format="%d", width='small'),
            'Frecuencia Relativa Acumulada (Hi)': st.column_config.NumberColumn(format="%.4f", width='small'),
        }

        if tipo_datos == "Por Intervalos":
            # Añadimos columnas específicas de intervalos a la config
            config_columnas.update({
                'Límite Inferior': st.column_config.NumberColumn(format="%.2f", width='small'),
                'Límite Superior': st.column_config.NumberColumn(format="%.2f", width='small'),
                'Valores': st.column_config.NumberColumn("Marca de Clase", format="%.2f", width='small'),
                # Ocultamos la columna original 'Marca de Clase' si ya la mostramos como 'Valores'

            })
            
            # Orden de columnas preferido para visualización
            columnas_ordenadas = ['Límite Inferior', 'Límite Superior', 'Valores', 
                                'Frecuencia Absoluta (fi)', 'Frecuencia Relativa (hi)', 
                                'Porcentaje (pi)', 'Frecuencia Acumulada (Fi)', 
                                'Frecuencia Relativa Acumulada (Hi)']
            
            st.dataframe(tabla_estadistica[columnas_ordenadas], 
                         hide_index=True, 
                         column_config=config_columnas,
                         width='stretch')
            

        else:
            # Configuración para Discretos
            config_columnas['Valores'] = st.column_config.NumberColumn(format="%.2f", width='small')
            st.dataframe(tabla_estadistica, 
                         width='stretch', 
                         column_config=config_columnas)
            
        # Mostrar cantidad de clases / intervalos
        st.write(f"**Número de Clases / Intervalos:** {len(tabla_estadistica)}")
        
        st.divider()
        
        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("Parámetros")
            # Calculamos métricas sobre la serie (Original o Agrupada según tu preferencia)
            metricas = calcular_metricas_principales(serie_para_metricas)

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
            # Generar Gráfico
            grafico = crear_histograma(tabla_estadistica)
            st.plotly_chart(grafico)
        # --- Creditos ---
        st.divider()
        st.markdown(
            "🔗 [Ver código fuente en GitHub](https://github.com/sebakremis/StatBoard)",
            unsafe_allow_html=True
        )
        st.markdown("👤 Desarrollado por Sebastian Kremis")

if __name__ == "__main__":
    main()
