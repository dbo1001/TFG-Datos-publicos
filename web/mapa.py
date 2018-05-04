import folium
import json


COORDENADAS = [40, -3]
ZOOM = 3.5


def visualiza_mapa(df, columna):
    """
    Guarda un mapa con el código de provincia y la columna
    del argumento de un dataframe.
    """
    # Crea el mapa
    mapa = folium.Map(COORDENADAS,
                      zoom_start=ZOOM,
                      tiles='cartodbpositron')

    geo_json = 'web/geojson/provincias.geojson'
    geo_data = json.load(open(geo_json, encoding='utf-8'))

    mapa.choropleth(geo_data=geo_data,
                    data=df,
                    columns=['Codigo Provincia', columna],
                    key_on='feature.properties.cod_prov',
                    # threshold_scale=[100, 200, 300, 500, 1000, 5000],
                    fill_color='BuPu')

    mapa.save('web/static/_mapa.html')
