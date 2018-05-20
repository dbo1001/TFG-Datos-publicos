from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, SelectMultipleField, FieldList, IntegerField
from wtforms.validators import Optional


class Consulta(FlaskForm):
    """
    Formulario para la consulta de datos
    """
    comparadores = [('$eq', '='), ('$ne', '!='), ('$lt', '<'), ('$lte', '<='), ('$gt', '>'), ('$gte', '>=')]
    join_choices = [('inner', 'inner'), ('outer', 'outer'), ('left', 'left'), ('right', 'right')]
    entradas = 1

    fuente = FieldList(SelectField('Fuente de datos', choices=[]), min_entries=entradas)
    columna_filtro = FieldList(SelectField('Columna', choices=[]), min_entries=entradas)
    columna_mostrar = SelectMultipleField('Columnas a mostrar', choices=[], id="select_mostrar")
    comparador = FieldList(SelectField('Comparador', choices=comparadores,
                                       validators=[Optional()]), min_entries=entradas)
    valor = FieldList(StringField('Valor'), min_entries=entradas)
    mostrar = IntegerField('Filas a mostrar', default=1000)
    columna_calculada = StringField('Columna calculada')
    join = SelectField('Join', choices=join_choices)
    submit = SubmitField('Consultar')

    def __init__(self, fuentes, columnas, *args, **kwargs):
        super().__init__(*args, **kwargs)
        valores = [(col, col) for col in columnas]
        fuentes = [(fuente, fuente) for fuente in fuentes]
        # Posibles columnas
        self.columna_mostrar.choices = valores
        for i in range(self.entradas):
            self.columna_filtro[i].choices = valores
            self.fuente[i].choices = fuentes
