from bottle import MultiDict
from wtforms.form import BaseForm
from wtforms import Form, BooleanField, TextField, PasswordField, \
    HiddenField, SelectField, TextAreaField, FieldList, FormField, FileField
from wtforms.validators import Required, Length


def form_filter(form, keys, strip=True):
    ''' Pull out only specific names/keys (from WTForm).
        Optionally strips leading/trailing spaces from strings.
    '''
    if strip:
        def process(val):
            if hasattr(val, 'strip'):
                return val.strip()
            elif isinstance(val, list):
                return [v.strip() for v in val if hasattr(v, 'strip')]
            return val
    else:
        def process(val):
            return val
    d = {}
    for key in keys:
        form_val = form.get(key, None)
        d[key] = process(form_val)
    return d

class LoginForm(Form):
	username = TextField(u'User name:',
        [Required(), Length(min=2, max=30)])

	password = PasswordField(u'Password:',
		[Required(), Length(min=2, max=30)])



class RegisterForm(Form):
	username = TextField(u'User name:',
        [Required(), Length(min=2, max=30)])
	password = PasswordField(u'Password:',
		[Required()])

class AddTask(Form):
    task = TextField()

class UploadForm(Form):
    uploaded_file = FileField(u'Upload your video: ',
        [Required()])
