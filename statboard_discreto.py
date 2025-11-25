import pandas as pd
import streamlit as st
import altair as alt

# Configuración de la página
st.set_page_config(layout="wide", page_title="Estadística Descriptiva")

def crear_tabla_estadistica(valores: pd.Series) -> pd.DataFrame:
    '''
    Crea una tabla estadística a partir de valores discretos.
    
    :param valores: Serie de Pandas con los valores discretos
    :return: DataFrame de la tabla estadística
    '''    
    # Calcular Frecuencia Absoluta (fi)
    tabla=valores.value_counts().sort_index().to_frame(name='Frecuencia Absoluta (fi)') # Convertir a DataFrame y ordenar por índice

    # Calcular Frecuencia Relativa (hi)
    n=len(valores)
    tabla['Frecuencia Relativa (hi)']=tabla['Frecuencia Absoluta (fi)']/n

    # Calcular Porcentaje (pi)
    tabla['Porcentaje (pi)']=tabla['Frecuencia Relativa (hi)']*100

    # Calcular Frecuencia Acumulada (Fi)
    tabla['Frecuencia Acumulada (Fi)']=tabla['Frecuencia Absoluta (fi)'].cumsum()

    # Calcular Frecuencia Relativa Acumulada (Hi)
    tabla['Frecuencia Relativa Acumulada (Hi)']=tabla['Frecuencia Relativa (hi)'].cumsum()

    tabla.index.name='Valores' # Nombrar el índice   
    return tabla.round(4) # Redondear a 4 decimales

# Ejemplo de uso a partir de una cadena de valores
valores="12 13 12 12 13 14 13 13 13 12 13 14 13 15 14 13 13 13 14 14 14 15 12 15 14 15 15 16 14 16 12 14 14 14 18 15 16 16 13 15 16 14 15 17 15 16 18 16 16 16 12 14 13 13 16 13 12 13 13 13 14 15 15 13 14 17 17 13 14 14 14 14 17 15 13 14 13 14 15 17 13 14 13 14 14 14 16 17 14 14 15 15 18 13 16 15 13 12 17 17"
lista_valores=valores.split()
lista_valores=[int(edad) for edad in lista_valores] # Convertir a enteros
serie_valores=pd.Series(lista_valores) # Crear Serie de Pandas

def main():
    st.title("Estadística Descriptiva de Valores Discretos")
    st.divider() # Línea divisoria   
    st.write("## Tabla de Distribución de Frecuencias")
    tabla_estadistica = crear_tabla_estadistica(serie_valores)

    st.dataframe(tabla_estadistica,
                 width='stretch',
                 column_config={
                    'Valores': st.column_config.NumberColumn(format="%d",width='medium'),
                    'Frecuencia Absoluta (fi)': st.column_config.NumberColumn(format="%d",width='medium'),
                    'Frecuencia Relativa (hi)': st.column_config.NumberColumn(format="%.2f",width='medium'),
                    'Porcentaje (pi)': st.column_config.NumberColumn(format="%.2f%%",width='medium'),
                    'Frecuencia Acumulada (Fi)': st.column_config.NumberColumn(format="%d",width='medium'),
                    'Frecuencia Relativa Acumulada (Hi)': st.column_config.NumberColumn(format="%.2f",width='medium'),
                    }
    )
    st.divider()
    col1,col2= st.columns([1,2]) # Dos columnas, la segunda el doble de ancha que la primera
    with col1:
        st.subheader("Parámetros")
        
        # Cálculos
        media = serie_valores.mean()
        mediana = serie_valores.median()
        desviacion = serie_valores.std()
        varianza = serie_valores.var()
        
        # Manejo robusto de la Moda
        moda_series = serie_valores.mode()
        moda_str = ", ".join(map(str, moda_series.tolist())) # Si hay varias, las muestra todas: "13, 14"

        # Visualización tipo Dashboard
        kpi1, kpi2 = st.columns(2)
        kpi1.metric("Media", f"{media:.2f}")
        kpi2.metric("Mediana", f"{mediana:.2f}")
        
        kpi3, kpi4 = st.columns(2)
        kpi3.metric("Moda", moda_str)
        kpi4.metric("N (Total)", len(serie_valores))

        kpi5, kpi6 = st.columns(2)
        kpi5.metric("Varianza", f"{varianza:.2f}")
        kpi6.metric("Desv. Estándar", f"{desviacion:.2f}")
        
    with col2:
        datos_grafico=tabla_estadistica.reset_index() # Reiniciar el índice para Altair
        grafico=alt.Chart(datos_grafico).mark_bar(size=40).encode(
            # Eje X: Usamos la columna 'Valores' y forzamos el angulo a 0 para mejor legibilidad
            # Agregamos ':O' después de 'Valores' (O de Ordinal) para tratar los valores como categóricos
            x=alt.X('Valores:O', axis=alt.Axis(labelAngle=0),title='Valores'),
            # Eje Y: Usamos la Frecuencia Absoluta
            y=alt.Y('Frecuencia Absoluta (fi)', title='Frecuencia Absoluta'),
            tooltip=['Valores', 'Frecuencia Absoluta (fi)'] # Información al pasar el ratón
        ).properties(
            height=400,
            title='Histograma'
        )
        st.altair_chart(grafico)

if __name__ == "__main__":
    main()
