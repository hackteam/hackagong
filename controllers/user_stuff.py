import bottle
from bottle import get, post, view, static_file, request, response, route, abort
import config
from config import BASE_DIR_STATIC, BASE_URL_PATH_RES, BASE_DIR
from utils import redirect, existing_web_session
from controllers.common import logged_in_only
from models import Task, User, db_session
import forms
import uuid
import os



@get('/addtask/<list_id>',template="addtask.html")
@logged_in_only
def addTask(list_id):

	ws = existing_web_session()
	ws['user_id'] = 1
	dbs = db_session(close=True)
	attrs = {}


	tasks = dbs.query(Task).filter(Task.user_created_id == ws['user_id']).all()
	if tasks:
		for count,task in enumerate(tasks):
			attrs[count] = {'task_id':task.id}


	form = forms.AddTask()

	return {
		'list_id':list_id,
		'tasks':tasks,
		'attrs':attrs,
		'form':form,
		'ws':ws
	}

@post('/addtask/<list_id>',template='addtask.html')
@logged_in_only
def add_task(list_id):
	'''Add task for the current user'''

	ws = existing_web_session()
	dbs = db_session(close=True)
	form = forms.AddTask()
	post = request.POST.decode()
	


	task = Task(name=post['task'],description='',creator=ws['user_id'],reviewer=ws['user_id'])


	dbs.add(task)

	try:
		dbs.commit()
	except:
		dbs.rollback()
		return {
			'list_id':list_id,
			'form':form,
			'ws':ws,
			'message':'Something went wrong',
			'tasks':tasks
		}

	tasks = dbs.query(Task).filter(Task.user_created_id == ws['user_id']).all()

	return {
		'list_id':list_id,
		'form':form,
		'ws':ws,
		'message':'Task created',
		'tasks':tasks
	}


@get('/upload',template='upload.html')
def upload():
	ws = existing_web_session()


	form = forms.UploadForm()

	return {
		'ws':ws,
		'form':form
	}

@post('/upload',template='upload.html')
def upload_video():
	post = request.POST.decode()
	ws = existing_web_session()
	form = forms.UploadForm()

	new_file = post['uploaded_file']
    
	name,ext = os.path.splitext(new_file.filename)

    
	#Check for upload pressed with no file selected.
	if not new_file:
		return {
		    "message":"No file was selected. Please try again.",
		    "ws":ws,
		    'form':form
		}


    
	name = str(uuid.uuid4())


	OUTPUT_PATH = os.path.join(config.BASE_DIR,'vids')

	if not os.path.exists(OUTPUT_PATH):
		os.makedirs(OUTPUT_PATH)

	chunk_size = 68000
	raw = ''
	if new_file.file:
		while True:
			chunk = new_file.file.read(chunk_size)
			if not chunk:
				break
			raw+=chunk


	with open(OUTPUT_PATH+'/'+name+ext, 'w') as f:
		f.write(raw) 

	return {
    	'message':'File saved successfully',
    	'ws':ws,
    	'form':form
    }