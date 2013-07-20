from bottle import MultiDict
from wtforms.form import BaseForm
from wtforms import Form, BooleanField, TextField, PasswordField, \
    HiddenField, SelectField, TextAreaField, FieldList, FormField, FileField
from wtforms.validators import Required, Length


class LoginForm(Form):
	username = TextField(u'User name:',
        [Required(), Length(min=2, max=30)])
	password = PasswordField(u'Password:',
		[Required(), Length(min=2, max=30)])
