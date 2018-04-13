from flask import abort, render_template, redirect, request, flash, url_for, jsonify, make_response
from web import app
from web.forms.consulta import Consulta
import web.consulta


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
    cookies_descarga = request.cookies.get('descarga')
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
        # Descarga los datos
        if cookies_descarga:
            return descarga_consulta(datos, cookies_descarga)
        return render_template('resultados-consulta.html',
                               datos=datos)
    return render_template('consulta.html', form=form)


@app.route('/api/fuente/<fuente>')
def actualiza_columnas(fuente):
    """
    Obtiene todas las columnas de una fuente en formato json
    """
    columnas = web.consulta.columnas_coleccion(fuente)
    descripcion = web.consulta.descripcion_fuente(fuente)
    return jsonify({
        'columnas': columnas,
        'descripcion': descripcion
    })


def descarga_consulta(datos, formato):
    """
    Descarga un dataframe en el formato especificado
    """
    if formato == 'csv':
        contenido = datos.to_csv()
    elif formato == 'json':
        contenido = datos.to_json()
    else:
        return abort(403)
    resp = make_response(contenido)
    resp.headers['Content-type'] = 'text/{}'.format(formato)
    resp.headers["Content-Disposition"] = 'attachment; filename=consulta.{}'.format(formato)
    resp.set_cookie('descarga', '')
    return resp
