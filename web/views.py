from flask import render_template, redirect, request, flash, url_for, jsonify
from web import app, mongo
from web.forms.consulta import Consulta
import web.consulta
import pandas as pd


@app.route('/')
def index():
    """
    Página de inicio
    """
    return render_template('index.html')


@app.route('/consulta', methods=('GET', 'POST'))
def consulta():
    """
    Formulario de consulta
    """
    columnas = web.consulta.todas_columnas()
    fuentes = web.consulta.todas_fuentes()
    form = Consulta(fuentes=fuentes, columnas=columnas)
    if form.validate_on_submit():
        datos = web.consulta.consulta(fuente=form.fuente.data,
                                      columna=form.columna_filtro.data,
                                      mostrar=form.columna_mostrar.data,
                                      comparador=form.comparador.data,
                                      valor=form.valor.data)
        if datos.empty:
            flash('No hay resultados.')
            return redirect(url_for('consulta'))
        return render_template('resultados-consulta.html',
                               datos=datos)
    return render_template('consulta.html', form=form)


@app.route('/api/actualiza_columnas/<fuente>')
def actualiza_columnas(fuente):
    """
    Obtiene todas las columnas de una fuente en formato json
    """
    columnas = web.consulta.columnas_coleccion(fuente)
    return jsonify(columnas)


@app.route('/consulta/descarga/<datos>')
def descarga(datos):
    """
    Muestra una cadena de texto
    """
    return datos
