from flask import render_template
from web import app, mongo
import pandas as pd


@app.route('/')
def index():
    """
    Página de inicio
    """
    return render_template('index.html')


@app.route('/consulta')
def renta_burgos():
    """
    Ejemplo de consulta
    """
    fuente = 'aeat_renta'
    filtro = {
        'Municipio': 'Burgos',
        'RENTA BRUTA MEDIA': {'$lte': 26}
    }
    cursor = mongo.db[fuente].find(filtro)
    df = pd.DataFrame.from_records(cursor, exclude=['_id'])
    return df.to_html()
