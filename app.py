import streamlit as st
import pandas as pd
import time
import requests
import xml.etree.ElementTree as Xet

# Función para obtener la información de un anime desde la API
def obtener_info_anime(id_anime):
    url = f'https://api.jikan.moe/v4/anime/{id_anime}'
    response = requests.get(url)
    data = response.json() if response.status_code == 200 else None
    info = {'name': data['data']['title_english'],
            'score': data['data']['score']}
    return info

# Función para procesar el archivo XML y obtener la lista de nombres de anime
def obtener_id_anime_desde_xml(archivo_xml):
    root = Xet.parse(archivo_xml).getroot()
    animelist = []
    for nodo in root.iter('anime'):
        for elemento in nodo.iter('series_animedb_id'):
            animelist.append(elemento.text)
    return animelist

# Función para realizar el análisis de datos y mostrar los resultados
def analizar_datos(df):
    # Borramos la tabla existente
    st.subheader('Información recolectada:')
    # Creamos la tabla con los datos actualizados
    st.write(df)

# Configuración de la aplicación Streamlit
st.title('Análisis de Datos de Anime')

# Interfaz para cargar el archivo XML
archivo_xml = st.file_uploader('Cargar archivo XML', type=['xml'])

# DataFrame para almacenar la información recolectada
df = pd.DataFrame(columns=['id_anime','Nombre', 'Puntuación'])  # Modifica según los datos que desees recolectar
tabla_resultados = st.empty()

if archivo_xml is not None:
    # Obtener los nombres de los animes desde el archivo XML
    ids_anime = obtener_id_anime_desde_xml(archivo_xml)

    # DataFrame para almacenar la información recolectada
    df = pd.DataFrame(columns=['id_anime', 'Nombre', 'Puntuación'])  # DataFrame vacío

    # Proceso de recolección de información
    st.subheader('Proceso de recolección de información:')
    with st.spinner('Recopilando información...'):
        for id_anime in ids_anime:
            # Obtener información del anime desde la API
            info_anime = obtener_info_anime(id_anime)
            if info_anime is not None:
                # Agregar la información al DataFrame
                df.loc[len(df)] = {'id_anime': id_anime, 'Nombre': info_anime['name'], 'Puntuación': info_anime['score']}
                
                # Mostrar los resultados parciales
                tabla_resultados.table(df)

                # Esperar 1 segundo antes de la siguiente solicitud a la API
                time.sleep(1)

    # Mostrar resultados finales
    st.success('Proceso completado. Información recopilada:')
    analizar_datos(df)
