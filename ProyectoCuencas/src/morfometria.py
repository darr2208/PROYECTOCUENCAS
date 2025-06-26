import geopandas as gpd
import pandas as pd
from shapely.geometry import shape
from math import pi, sqrt

def calcular_parametros(geojson_data):
    geometry = shape(geojson_data['geometry'])
    gdf = gpd.GeoDataFrame(index=[0], geometry=[geometry], crs="EPSG:4326")
    gdf_utm = gdf.to_crs(gdf.estimate_utm_crs())

    area_m2 = gdf_utm.geometry.area.iloc[0]
    perimetro_m = gdf_utm.geometry.length.iloc[0]
    centroide = gdf_utm.geometry.centroid.iloc[0]

    area_km2 = area_m2 / 1e6
    perimetro_km = perimetro_m / 1000

    longitud_cuenca_km = perimetro_km / 2
    diametro_equivalente_km = sqrt((4 * area_km2) / pi)
    coef_compacidad = perimetro_km / (2 * sqrt(pi * area_km2)) if area_km2 > 0 else 0
    razon_elongacion = (2 * sqrt(area_km2 / pi)) / longitud_cuenca_km if longitud_cuenca_km > 0 else 0
    indice_forma = area_km2 / (longitud_cuenca_km ** 2) if longitud_cuenca_km > 0 else 0

    resultados = {
        "Área (km²)": round(area_km2, 2),
        "Perímetro (km)": round(perimetro_km, 2),
        "Centroide X": round(centroide.x, 2),
        "Centroide Y": round(centroide.y, 2),
        "Longitud de cuenca (km)": round(longitud_cuenca_km, 2),
        "Diámetro equivalente (km)": round(diametro_equivalente_km, 2),
        "Coef. de Compacidad": round(coef_compacidad, 4),
        "Razón de Elongación": round(razon_elongacion, 4),
        "Índice de Forma": round(indice_forma, 6)
    }

    return gdf, resultados
