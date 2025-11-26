# core/utils.py
import pandas as pd
import streamlit as st

@st.cache_data
def procesar_datos(cadena_valores: str) -> pd.Series:
    '''
    Procesa una cadena de valores separados por espacios o comas.
    Maneja errores si el usuario introduce texto no numérico.
    
    :param cadena_valores: Cadena con valores separados por espacios.
    :return: Serie de Pandas.
    '''
    try:
        if not cadena_valores.strip():
            return pd.Series(dtype=int)  # Retorna una Serie vacía si la cadena está vacía
        
        cadena_limpia = cadena_valores.replace(',', ' ')  # Reemplaza comas por espacios
        lista_valores = cadena_limpia.split()   
        lista_valores = [int(valor) for valor in lista_valores]  # Convierte a enteros
        return pd.Series(lista_valores)
    except ValueError:
        st.error("Error: Por favor, introduce solo números enteros separados por espacios o comas.")
        return pd.Series(dtype=int)