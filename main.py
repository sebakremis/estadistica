import pandas as pd
import streamlit as st
from core.utils import procesar_datos
from core.descriptive import crear_tabla_estadistica, calcular_metricas_principales, calcular_metricas_agrupadas
from core.visualization import crear_histograma, crear_boxplot
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
        # Procesar la serie original desde la entrada del usuario
        serie_original = procesar_datos(entrada_usuario)
        
        if serie_original.empty:
            st.warning("👈 Ingresa datos numéricos en el menú lateral...")
            return

        # Inicializamos variables para el flujo
        tabla_estadistica = pd.DataFrame()
        
        # Lógica bifurcada: Discretos vs Continuos
        if tipo_datos == "Por Intervalos":
            # A. Generamos la tabla de intervalos (Límites, Marca de Clase, fi)
            tabla_estadistica = crear_intervalos(serie_original, criterio_intervalos)
            
            
            # B. Calculamos las columnas estadísticas DIRECTAMENTE aquí
            # (Evitamos reconstruir la serie y perder filas vacías)
            total_n = tabla_estadistica['Frecuencia Absoluta (fi)'].sum()
            
            tabla_estadistica['Frecuencia Relativa (hi)'] = tabla_estadistica['Frecuencia Absoluta (fi)'] / total_n
            tabla_estadistica['Porcentaje (pi)'] = tabla_estadistica['Frecuencia Relativa (hi)']
            tabla_estadistica['Frecuencia Acumulada (Fi)'] = tabla_estadistica['Frecuencia Absoluta (fi)'].cumsum()
            tabla_estadistica['Frecuencia Rel Acumulada (Hi)'] = tabla_estadistica['Frecuencia Relativa (hi)'].cumsum()
            
            # C. Asignamos la columna 'Valores' para compatibilidad con el gráfico (usamos Marca de Clase)
            tabla_estadistica['Valores'] = tabla_estadistica['Marca de Clase']
            # D. Calculamos métricas usando interpolación para datos agrupados
            metricas= calcular_metricas_agrupadas(tabla_estadistica)

        else: 
            # Metricas para valores discretos
            tabla_estadistica = crear_tabla_estadistica(serie_original)
            metricas = calcular_metricas_principales(serie_original)

            # Aseguramos que la columna 'Valores' exista para compatibilidad con gráficos
            tabla_estadistica = tabla_estadistica.reset_index()
            col_indice = tabla_estadistica.columns[0]
            tabla_estadistica.rename(columns={col_indice: 'Valores'}, inplace=True)


        st.write("## Distribución de Frecuencias")

        # --- Visualización de la tabla estadística ---
        # Configuración de columnas común
        config_columnas = {
            'Frecuencia Absoluta (fi)': st.column_config.NumberColumn(format="%d", width='small'),
            'Frecuencia Relativa (hi)': st.column_config.NumberColumn(format="%.4f", width='small'),
            'Porcentaje (pi)': st.column_config.NumberColumn(format="%.2f%%", width='small'),
            'Frecuencia Acumulada (Fi)': st.column_config.NumberColumn(format="%d", width='small'),
            'Frecuencia Rel Acumulada (Hi)': st.column_config.NumberColumn(format="%.4f", width='small'),
        }

        if tipo_datos == "Por Intervalos":
            # Crear columna 'intervalos'
            tabla_estadistica['Intervalos'] = tabla_estadistica.apply(
                lambda row: f"[ {row['Límite Inferior']:.2f} , {row['Límite Superior']:.2f} )", axis=1
            )
            # Añadimos columnas específicas de intervalos a la config
            config_columnas.update({
                'Intervalos': st.column_config.TextColumn("Intervalos", width='small'),
                'Valores': st.column_config.NumberColumn("Marca de Clase", format="%.2f", width='small')                
            })
            
            # Orden de columnas preferido para visualización
            columnas_ordenadas = ['Intervalos', 'Valores', 
                                'Frecuencia Absoluta (fi)', 'Frecuencia Relativa (hi)', 
                                'Porcentaje (pi)', 'Frecuencia Acumulada (Fi)', 
                                'Frecuencia Rel Acumulada (Hi)']
            
            st.dataframe(tabla_estadistica[columnas_ordenadas], 
                         hide_index=True, 
                         column_config=config_columnas,
                         width='stretch')            

        else:
            # Configuración para Discretos
            # Aseguramos que 'Valores' se muestre primero si lo deseamos, o dejamos el índice
            config_columnas['Valores'] = st.column_config.NumberColumn("Valor (xi)", format="%.2f", width='small')
            
            # Reordenamos para que 'Valores' aparezca primero
            cols = ['Valores'] + [c for c in tabla_estadistica.columns if c != 'Valores']
            
            st.dataframe(tabla_estadistica[cols], 
                         width='stretch', 
                         hide_index=True, # Ocultamos índice porque ya tenemos la columna 'Valores'
                         column_config=config_columnas)
            
        # Mostrar cantidad de clases / intervalos
        st.write(f"* **Número de Clases / Intervalos:** {len(tabla_estadistica)}")
        st.write(f"* **Número Total de Datos (N):** {metricas['n']}")
        
        st.divider()
        
        col1, col2 = st.columns([1, 2])

        with col1:
            # Visualización de métricas
            st.write("### Medidas de Posición")
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            kpi1.metric("Min", f"{metricas['minimo']:.2f}")
            kpi2.metric("Q1", f"{metricas['Q1']:.2f}")
            kpi3.metric("Q3", f"{metricas['Q3']:.2f}")
            kpi4.metric("Max", f"{metricas['maximo']:.2f}")            
            
            st.write("### Medidas de Tendencia Central")
            kpi5, kpi6, kpi7 = st.columns(3)
            kpi5.metric("Media", f"{metricas['media']:.2f}")
            kpi6.metric("Mediana", f"{metricas['mediana']:.2f}")
            kpi7.metric("Moda", metricas['moda'])
            
            st.write("### Medidas de Dispersión")
            kpi8, kpi9, kpi10 = st.columns(3)           
            kpi8.metric("Varianza", f"{metricas['varianza']:.2f}")
            kpi9.metric("Desv. Estándar", f"{metricas['desviacion']:.2f}")
            kpi10.metric("Coef. de Variación", f"{metricas['coef_variacion']:.2f}%")
            kpi11, kpi12, kpi13 = st.columns(3)
            kpi11.metric("Rango", f"{metricas['rango']:.2f}")
            kpi12.metric("Rango Intercuartílico", f"{metricas['rango_intercuartilico']:.2f}")
            kpi13= st.empty()  # Espacio vacío para mantener la cuadrícula
            
        with col2:
            # Generar Gráfico
            st.write("### Histograma")
            grafico = crear_histograma(tabla_estadistica)
            st.plotly_chart(grafico)

        # --- Valores atípicos ---
        st.divider()
        st.subheader("Valores Atípicos")
        diagrama_de_cajas, valores_atipicos = crear_boxplot(metricas, tabla_estadistica)

        def _render_advertencia_atipicos_():
            '''
            Renderiza una advertencia sobre valores atípicos.
            '''
            st.write("#### Atención:")
            st.markdown("""
            Los valores atípicos son observaciones que se encuentran significativamente alejadas del resto de los datos. 
            Estos pueden influir en los resultados estadísticos y deben ser analizados cuidadosamente.
            """)

        col1,col2 = st.columns(2)
        with col1:
            if len(valores_atipicos) == 0:
                st.write("No se detectaron valores atipicos")
            elif len(valores_atipicos) == 1:
                st.write("Se detectó 1 valor atípico:")
                st.write(f"- {valores_atipicos[0]}")
                _render_advertencia_atipicos_()
            else:
                st.write(f"Se dectectaron {len(valores_atipicos)} valores atípicos:")
                st.write(", ".join([str(v) for v in valores_atipicos]))                    
                _render_advertencia_atipicos_()
        with col2:
            # Diagrama de caja para valores atípicos
            
            st.pyplot(diagrama_de_cajas)

        # --- Creditos ---
        st.divider()
        st.markdown(
            "🔗 [Ver código fuente en GitHub](https://github.com/sebakremis/StatBoard)",
            unsafe_allow_html=True
        )
        st.markdown("👤 Desarrollado por Sebastian Kremis")

if __name__ == "__main__":
    main()
