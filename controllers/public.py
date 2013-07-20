import bottle
from bottle import get, post, view, static_file, request, response, route, abort
from config import BASE_DIR_STATIC, BASE_URL_PATH_RES
import forms
from models import db_session, User

from utils import web_session, web_session_exists, existing_web_session

@get('/', template='index.html')
def index():
    form = forms.LoginForm()
    ws = existing_web_session()
    raise
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
		return {
			'form':form,
			'message':'Successfully logged in'
		}



	return {
		'form':form,
		'message':'Username or password incorrect'
	}

@get('/register',template='register.html')
def register():


	form = forms.RegisterForm()