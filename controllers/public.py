import bottle
from bottle import get, post, view, static_file, request, response, route, abort
from config import BASE_DIR_STATIC, BASE_URL_PATH_RES
import forms
from models import db_session, User
from forms import form_filter
from utils import web_session, web_session_exists, existing_web_session, redirect

@get('/', template='index.html')
def index():
    form = forms.LoginForm()
    ws = existing_web_session()
    return {
    	'form':form,
    	'message':'Your message would show up here.'
    }

@post('/',template='index.html')
def index_post():
	'''Login'''

	post = request.POST.decode()

	form = forms.LoginForm(post)
	dbs = db_session(close=True)

	username = post['username'].strip()
	password = post['password']
	user = dbs.query(User).filter(User.username == username).first()


	if user and user.password == password:
		ws = web_session()
		ws['username'] = username
		ws['user_id'] = user.id
		relative_redirect('home')


	return {
		'form':form,
		'message':'Username or password incorrect'
	}


@get('/register',template='register.html')
def register():
	form = forms.RegisterForm()

	return {
		'form':form
	}

@post('/register',template='register.html')
def register_post():

	post = request.POST.decode()

	form = forms.RegisterForm(post)

	dbs = db_session(close=True)


	#Check if username exists
	username = post['username'].strip()
	user = dbs.query(User).filter(User.username == username).first()


	if user:
		return {
			'error':'Username already in use',
			'form':form
		}


	fd = form_filter(form.data, [
        'username',
        'password'
    ])

	user = User(**fd)

	dbs.add(user)

	try:
		dbs.commit()
	except:
		return {
			'form':form,
			'error':'You broke me :('
		}


	else:
		return {
			'message':'Account created! Huzzah'
		}




