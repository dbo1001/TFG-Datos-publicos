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


def visualiza_mapa(df, columna_valores, territorio, metodo):
    """
    Guarda un mapa con el código de provincia y la columna
    del argumento de un dataframe.
    """
    # Crea el mapa
    mapa = folium.Map(COORDENADAS,
                      zoom_start=ZOOM,
                      tiles='cartodbpositron')

    geo_json = 'web/geojson/{}.geojson'.format(territorio)
    file = open(geo_json, encoding='utf-8')
    geo_data = json.load(file)
    file.close()

    columna_codigo = 'Codigo {}'.format(
        'Municipio' if territorio == 'municipios' else 'Provincia')

    df = df[[columna_codigo, columna_valores]]
    df = agrupa_df(df, metodo)

    # Añade el maoa coroplético encima del mapa de España
    mapa.choropleth(geo_data=geo_data,
                    data=df,
                    columns=[columna_codigo, columna_valores],
                    key_on='feature.properties.codigo',
                    legend_name=columna_valores,
                    line_opacity=0.2,
                    fill_opacity=0.6,
                    highlight=True,
                    fill_color='OrRd')

    return mapa
