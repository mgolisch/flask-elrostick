from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired


class OutletForm(Form):
        name = StringField('name',validators=[DataRequired()])
        channel = StringField('channel',validators=[DataRequired()])
        unit = StringField('unit',validators=[DataRequired()])
        submit = SubmitField()
