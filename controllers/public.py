import bottle
from bottle import get, post, view, static_file, request, response, route, abort
from config import BASE_DIR_STATIC, BASE_URL_PATH_RES
import forms
from models import db_session, User
from forms import form_filter
from utils import web_session, web_session_exists, existing_web_session, redirect, delete_web_session
import json

@get('/', template='landing.html')
def index():
    form = forms.LoginForm()
    ws = existing_web_session()
    if (ws and 'user_id' in ws):
        redirect('profile')
    return {
        'form':form,
        'message':'Your message would show up here.'
    }

@get('/profile',template="profile.html")
def lists():
    return {}

@get('/about',template="about.html")
def about():
	return {}

@get('/lists',template="todolists.html")
def todolists():
    return {}

@get('/logout')
def logout():
    delete_web_session()
    return "Logged Out"




@post('/submitLogin')
def doLogin():
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
        return "success"
        #return json.dumps({"output" : "success"})


    return "fail"
    #return json.dumps({
    #   'form':form,
    #   'message':'Username or password incorrect'
    #})


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




