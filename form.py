from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import SubmitField, FileField, StringField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class ImageForm(FlaskForm):
    image = FileField(validators=[FileRequired(),FileAllowed(['jpg','jpeg', 'png'], 'Images only!')])
    submit = SubmitField('Submit')

class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    comments = TextAreaField('What do you want to tell me?', validators=[DataRequired()])
    submit = SubmitField('Submit')
