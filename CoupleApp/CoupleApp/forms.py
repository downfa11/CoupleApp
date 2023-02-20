from models import Myuser
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo



class CoupleForm(FlaskForm):
    hashcode=StringField('hashcode',validators=[DataRequired()])