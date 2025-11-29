# 📊 StatBoard: Herramienta de Estadística Descriptiva con Python

Este repositorio aloja **StatBoard**, una aplicación interactiva de Estadística Descriptiva desarrollada con **Python** y **Streamlit** durante mis estudios del Master Data Science, Big Data & Business Analytics en la Universidad Complutense de Madrid.

---

## 🎯 Descripción General
StatBoard permite analizar datos **discretos** y **continuos** desde una única interfaz.  

---

## ✨ Características Principales
- **Procesamiento de Datos:** Entrada manual o pegado directo desde Excel/CSV.  
- **Tablas Estadísticas Automáticas:** cálculo de frecuencias absolutas ($f_i$), relativas ($h_i$), acumuladas ($F_i, H_i$) y porcentajes. Permite exportar los datos a un fichero CSV. 
- **Métricas Clave:** Media, Mediana, Moda, Varianza y Desviación Estándar.  
- **Visualización Interactiva:** histogramas y gráficos dinámicos para distribución de frecuencias.  
- **Selector de Modo:** opción para trabajar con datos **discretos** o **por intervalos** en la misma aplicación.
- **Detección de Valores Atípicos:** se grafica un Diagrama de Cajas y se localizan valores atípicos, cuando los mismos se encuentren fuera de los limites de los bigotes (1.5 IQR).

---

## 🚀 Ejecución

### 🔹 Versión desplegada en Streamlit Cloud
StatBoard está disponible en línea y **no requiere instalaciones**.  
Accede directamente desde tu navegador:

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://statboard.streamlit.app)

---

### 🔹 Ejecución local
Si prefieres ejecutar la aplicación en tu entorno local:

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/sebakremis/StatBoard.git
   cd StatBoard
   ```
2. **Instalar dependencias**
  ```bash
   pip install -r requirements.txt
   ```
3. **Ejecutar la aplicación**
  ```bash
  streamlit run main.py
  ```

---

## 🧭 Próximos Pasos

* Agregar polígono de frecuencias y métricas al histograma.
* Realizar test unitario para el cálculo de métricas principales y agrupadas.

## 🛠️ Librerías Utilizadas

* `Streamlit`
* `Pandas`
* `Plotly`
* `Numpy`
* `Matplotlib`

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
Siéntete libre de usarlo y modificarlo para propósitos académicos o profesionales.

