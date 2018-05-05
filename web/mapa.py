import folium
import json


COORDENADAS = [40, -3]
ZOOM = 3.5


def agrupa_df(df, metodo):
    """
    Agrupa un dataframe utilizando como función
    el método pasado como paráemtro (string).
    """
    columna = df.columns.values[0]
    group = df.groupby(columna)
    # Función por la que agrupar
    func = getattr(group, metodo, None)
    if func:
        df = func()
    return df.reset_index()


def visualiza_mapa(df, columna, metodo):
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

    df = df[['Codigo Provincia', columna]]
    df = agrupa_df(df, metodo)

    mapa.choropleth(geo_data=geo_data,
                    data=df,
                    columns=['Codigo Provincia', columna],
                    key_on='feature.properties.cod_prov',
                    legend_name=columna,
                    highlight=True,
                    # threshold_scale=[100, 200, 300, 500, 1000, 5000],
                    fill_color='OrRd')

    return mapa
