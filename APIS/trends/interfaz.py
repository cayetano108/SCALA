import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import time
from PIL import Image  # Necesario para cargar imágenes en Streamlit
import os

# Inicialización de pytrends
pytrends = TrendReq(hl='es-ES', tz=60)

# Título de la app
st.title('Google Trends - Análisis Personalizado')

# Definir las opciones para los parámetros
busquedas = st.text_input("Palabras clave (separadas por comas)", "viaje,vacaciones,hoteles")
categoria = st.selectbox(
    "Categoría de búsqueda", 
    options=[0, 67, 44, 16, 71],  # Algunas categorías predefinidas relacionadas con turismo
    format_func=lambda x: {
        0: "Todas las Categorías",
        67: "Turismo",
        44: "Comida y Bebida",
        16: "Arte y Entretenimiento",
        71: "Viajes"
    }.get(x)
)
periodo = st.selectbox(
    "Periodo de Tiempo", 
    options=['today 1-m', 'today 3-m', 'today 12-m', 'today 5-y', 'now 1-H', 'now 1-d'],
    format_func=lambda x: {
        'today 1-m': "Últimos 30 días",
        'today 3-m': "Últimos 90 días",
        'today 12-m': "Últimos 12 meses",
        'today 5-y': "Últimos 5 años",
        'now 1-H': "Última hora",
        'now 1-d': "Últimas 24 horas"
    }.get(x)
)
region = st.selectbox(
    "Región", 
    options=['', 'ES', 'ES-CN', 'US', 'FR', 'DE'],
    format_func=lambda x: {
        '': "Mundial",
        'ES': "España",
        'ES-CN': "Islas Canarias (España)",
        'US': "Estados Unidos",
        'FR': "Francia",
        'DE': "Alemania"
    }.get(x)
)
servicio = st.selectbox(
    "Servicio de Google", 
    options=['', 'images', 'news', 'youtube', 'froogle'],
    format_func=lambda x: {
        '': "Búsqueda Web",
        'images': "Imágenes",
        'news': "Noticias",
        'youtube': "YouTube",
        'froogle': "Shopping"
    }.get(x)
)

# Convertir la lista de palabras clave
palabras_clave = [kw.strip() for kw in busquedas.split(",")]

# Botón para ejecutar la consulta
if st.button("Obtener Tendencias"):
    try:
        # Pausa para no exceder el límite de peticiones
        time.sleep(5)
        
        # Construir la consulta a Google Trends
        pytrends.build_payload(palabras_clave, cat=categoria, timeframe=periodo, geo=region, gprop=servicio)
        
        # Obtener el interés a lo largo del tiempo
        interest_over_time_df = pytrends.interest_over_time()
        
        # Verificar si hay datos
        if not interest_over_time_df.empty:

            # texto que ponga tendencias encontradas!!!!
            st.write("Tendencias encontradas!!!!")
            current_directory = os.path.dirname(__file__)  # Obtener el directorio actual del script
            image_path = os.path.join(current_directory, "foto.png")  # Ruta absoluta de la imagen
            
            # Cargar la imagen si existe
            if os.path.exists(image_path):
                image = Image.open(image_path)
                st.image(image, caption="Análisis de tendencias")
            else:
                st.warning(f"No se encontró la imagen en la ruta: {image_path}")
            st.image(image, caption="Análisis de tendencias")  # Mostrar la imagen
            
            st.write("Resultados de la tendencia de búsqueda:")
            st.dataframe(interest_over_time_df)
            
            # Obtener el interés por subregiones
            st.write("Resultados de la tendencia por subregiones:")
            interest_by_region_df = pytrends.interest_by_region(resolution='REGION')
            if not interest_by_region_df.empty:
                st.dataframe(interest_by_region_df)
            else:
                st.write("No se encontraron datos para las subregiones.")
        else:
            st.write("No se encontraron datos para los parámetros seleccionados.")
    except Exception as e:
        st.error(f"Error al obtener datos de Google Trends: {e}")
