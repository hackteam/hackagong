import bottle
from bottle import get, post, view, static_file, request, response, route, abort
from config import BASE_DIR_STATIC, BASE_URL_PATH_RES
from utils import redirect, existing_web_session
from controllers.common import logged_in_only
from models import Task, User, db_session
import forms

@get('/home',template='home.html')
def home():
	'''User overview page'''
	form = forms.AddTask()
	ws = existing_web_session()

	raise
	return {
		'ws':ws,
		'form':form
	}

@post('/addtask',template='home.html')
@logged_in_only
def add_task():
	'''Add task for the current user'''

	ws = existing_web_session()
	dbs = db_session(close=True)
	form = forms.AddTask()
	post = request.POST.decode()
	
	name = post['task']
	desc = post['description']
	task = Task(name=name,description=desc,creator=ws['user_id'],reviewer=ws['user_id'])


	dbs.add(task)

	try:
		dbs.commit()
	except:
		return {
			'form':form,
			'ws':ws,
			'message':'Something went wrong'
		}

	return {
		'form':form,
		'ws':ws,
		'message':'Task created'
	}