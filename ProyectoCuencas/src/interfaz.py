import streamlit as st
import matplotlib.pyplot as plt
from src.geocodificador import obtener_coordenadas
from src.mapa import mostrar_mapa_dibujable
from src.morfometria import calcular_parametros
from src.exportacion import exportar_shapefile_zip, exportar_excel

def ejecutar_interfaz():
    st.set_page_config(layout="wide")

    # Fondo estilizado
    st.markdown(
        """
        <style>
        body {
            background-color: #f5f9ff;
        }
        .stApp {
            background: linear-gradient(to bottom right, #f5f9ff, #dceeff);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("🗺️ Delimitación de Cuencas y Análisis Morfométrico")
    st.markdown("Busca una ciudad o ingresa coordenadas, dibuja una cuenca y descarga sus parámetros.")

    lugar = st.text_input("🔍 Buscar ciudad (ejemplo: Medellín, Colombia)")
    if lugar:
        coords = obtener_coordenadas(lugar)
        if coords:
            st.success(f"📍 Coordenadas encontradas: {coords}")
        else:
            st.error("❌ No se encontraron coordenadas para ese lugar.")
            coords = [4.6, -74.1]
    else:
        coords = [4.6, -74.1]

    with st.expander("📌 O ingresa coordenadas manuales"):
        lat = st.number_input("Latitud", value=coords[0], format="%.6f")
        lon = st.number_input("Longitud", value=coords[1], format="%.6f")
        usar_coords = st.checkbox("Usar estas coordenadas en lugar de la ciudad")

    if usar_coords:
        coords = [lat, lon]

    st.markdown("### 🗺️ Dibuja tu cuenca hidrológica en el mapa")
    geojson_data = mostrar_mapa_dibujable(coords)

    if geojson_data:
        st.markdown("---")
        st.markdown("### 📐 Parámetros Morfométricos Calculados")

        gdf, resultados = calcular_parametros(geojson_data)

        st.dataframe(resultados)

        # GRÁFICO DE BARRAS
        st.markdown("### 📊 Visualización de Parámetros Morfométricos")
        datos_graficar = resultados.drop(columns=["Centroide X", "Centroide Y"])
        fig, ax = plt.subplots(figsize=(10, 4))
        datos_graficar.T.plot(kind='bar', legend=False, ax=ax)
        ax.set_ylabel("Valor")
        ax.set_title("Parámetros Morfométricos")
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)

        col1, col2 = st.columns(2)
        with col1:
            shp_zip = exportar_shapefile_zip(gdf)
            st.download_button(
                label="⬇️ Descargar Shapefile (.zip)",
                data=shp_zip,
                file_name="cuenca_shapefile.zip",
                mime="application/zip"
            )
        with col2:
            excel_file = exportar_excel(resultados)
            st.download_button(
                label="⬇️ Descargar Excel (.xlsx)",
                data=excel_file,
                file_name="parametros_morfometricos.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
