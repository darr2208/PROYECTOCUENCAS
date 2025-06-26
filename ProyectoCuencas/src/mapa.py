import folium
from streamlit_folium import st_folium
from folium.plugins import Draw

def mostrar_mapa_dibujable(coordenadas):
    m = folium.Map(location=coordenadas, zoom_start=13, tiles="OpenStreetMap")

    draw = Draw(
        export=False,
        draw_options={
            "polyline": False,
            "rectangle": False,
            "circle": False,
            "marker": False,
            "circlemarker": False,
            "polygon": {
                "shapeOptions": {
                    "color": "#ff66cc",
                    "fillColor": "#ffe6f0",
                    "fillOpacity": 0.5
                }
            }
        },
        edit_options={"edit": True}
    )
    draw.add_to(m)

    st_data = st_folium(m, width=900, height=600, returned_objects=["last_active_drawing"])

    if st_data and "last_active_drawing" in st_data and st_data["last_active_drawing"]:
        geom = st_data["last_active_drawing"]["geometry"]
        coords = geom["coordinates"][0]

        if len(coords) == 5:
            lat = coords[0][1]
            lon = coords[0][0]
            folium.Marker(
                location=[lat, lon],
                popup="📍 Punto de interés",
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(m)

            st_folium(m, width=900, height=600)

        return st_data["last_active_drawing"]

    return None
