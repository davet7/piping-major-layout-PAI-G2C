from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class PiperackArea(FlaskForm):
    ancho = IntegerField('Ancho', validators=[DataRequired()])
    largo = IntegerField('Largo',validators=[DataRequired()])
    submit1 = SubmitField('Ingresar')


class PiperackP(FlaskForm):    
    ancho = IntegerField('Ancho Area', validators=[DataRequired()])
    largo = IntegerField('Largo Area',validators=[DataRequired()])
    anchoP =IntegerField('Ancho Piperack',validators=[DataRequired()])    
    largoP =IntegerField('Largo Piperack',validators=[DataRequired()])
    altoP =IntegerField('Alto Pirerack',validators=[DataRequired()])
    seccionesP =IntegerField('Secciones')
    submit2 = SubmitField('Ingresar')


class Equipos(FlaskForm):
    nombreEquipo = StringField('Nombre del Equipo', validators=[DataRequired()])
    tag = StringField('TAG',validators=[DataRequired()])
    coorX =IntegerField('Coordenada en X',validators=[DataRequired()])
    coorY =IntegerField('Coordenada en Y',validators=[DataRequired()])
    coorZ =IntegerField('Coordenada en Z',validators=[DataRequired()])
    tipoEquipo = StringField('Tipo de equipo',validators=[DataRequired()])
    submit3 = SubmitField('Ingresar')

class Lineas(FlaskForm):
    numLinea = StringField('Número de Linea', validators=[DataRequired()])
    tagLinea = StringField('TAG',validators=[DataRequired()])
    equipo1 =IntegerField('Equipo 1',validators=[DataRequired()])
    equipo2 =IntegerField('Equipo 2',validators=[DataRequired()])
    diametro =IntegerField('Diametro',validators=[DataRequired()])    
    submit4 = SubmitField('Ingresar')

