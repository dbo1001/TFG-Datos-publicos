from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import Optional


class Consulta(FlaskForm):
    """
    Formulario para la consulta de datos
    """
    comparadores = [('$eq', '='), ('$ne', '!='), ('$lt', '<'), ('$lte', '<='), ('$gt', '>'), ('$gte', '>=')]

    fuente = SelectField('Fuente de datos', choices=[], id='select_fuente')
    columna_filtro = SelectField('Columna', choices=[], id='select_columna')
    columna_mostrar = SelectMultipleField('Columnas a mostrar', choices=[], id="select_mostrar")
    comparador = SelectField('Comparador', choices=comparadores, validators=[Optional()], id='select_comparador')
    valor = StringField('Valor', id='select_valor')

    submit = SubmitField('Consultar')

    def __init__(self, fuentes, columnas, *args, **kwargs):
        super().__init__(*args, **kwargs)
        valores = [(col, col) for col in columnas]
        fuentes = [(fuente, fuente) for fuente in fuentes]
        # Posibles columnas
        self.columna_filtro.choices = valores
        self.columna_mostrar.choices = valores
        self.fuente.choices = fuentes
