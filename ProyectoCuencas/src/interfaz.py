import streamlit as st
from src.mapa import mostrar_mapa_dibujable
from src.geocodificador import obtener_coordenadas
from src.morfometria import calcular_parametros
from src.exportacion import exportar_shapefile_zip, exportar_excel
import pandas as pd

def ejecutar_interfaz():
    st.set_page_config(page_title="Delimitación de Cuencas", layout="wide", page_icon="🌎")
    st.markdown(
        """
        <style>
            body {
                background-color: #eaf2fb;
            }
            .stApp {
                background-color: #eaf2fb;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("🌍 Delimitación de Cuencas y Análisis Morfométrico")
    st.markdown("Busca una ciudad o ingresa coordenadas, dibuja una cuenca y descarga sus parámetros.")

    # Campo para búsqueda por ciudad
    with st.expander("🔎 Buscar ciudad (ejemplo: Medellín, Colombia)"):
        ciudad = st.text_input("")

    coordenadas = None
    if ciudad:
        coordenadas = obtener_coordenadas(ciudad)
        if coordenadas:
            st.success(f"Coordenadas encontradas: {coordenadas}")
        else:
            st.error("No se encontraron coordenadas para esa ciudad.")

    # Campo para ingreso manual
    with st.expander("📍 O ingresa coordenadas manuales"):
        col1, col2 = st.columns(2)
        with col1:
            lat = st.number_input("Latitud", format="%.6f")
        with col2:
            lon = st.number_input("Longitud", format="%.6f")

        if lat != 0.0 or lon != 0.0:
            coordenadas = [lat, lon]

    # Mostrar mapa
    st.subheader("🗺️ Dibuja tu cuenca hidrológica en el mapa")
    if coordenadas:
        geom = mostrar_mapa_dibujable(coordenadas)
    else:
        st.info("Esperando coordenadas para mostrar el mapa...")
        return

    resultados = None
    if geom:
        resultados = calcular_parametros_morfometricos(geom)

    # Mostrar resultados si existen
    if resultados is not None and not resultados.empty:
        st.subheader("📊 Resultados del análisis morfométrico")
        datos_graficar = resultados.drop(columns=["Centroide X", "Centroide Y"])
        st.dataframe(datos_graficar)

        # Descarga de archivos
        col1, col2 = st.columns(2)
        with col1:
            excel = exportar_excel(resultados)
            st.download_button("📥 Descargar Excel", data=excel, file_name="resultados_cuenca.xlsx")
        with col2:
            shapefile_zip = exportar_shapefile_zip(geom)
            st.download_button("📥 Descargar Shapefile (.zip)", data=shapefile_zip, file_name="cuenca_shapefile.zip")
    else:
        st.warning("Dibuja una cuenca para ver los resultados y habilitar las descargas.")
