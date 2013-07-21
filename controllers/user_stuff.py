import bottle
from bottle import get, post, view, static_file, request, response, route, abort
import config
from config import BASE_DIR_STATIC, BASE_URL_PATH_RES, BASE_DIR
from utils import redirect, existing_web_session
from controllers.common import logged_in_only
from models import Task, User, db_session, Todo
import forms
import uuid
import os
import json
import cgi

@get('/profile',template="profile.html")
def profile():
    '''Show profile overview page'''

    ws = existing_web_session()
    
    return {
        'ws':ws
    }

@get('/lists',template="todolists.html")
@logged_in_only
def todolists():
    '''Show all todo lists'''
    dbs = db_session(close=True)
    ws = existing_web_session()

    form = forms.AddTodo()

    todo_lists = dbs.query(Todo).filter(Todo.owner_id == ws['user_id']).all()

    if not todo_lists:
        return {
            'form':form,
            'ws':ws,
            'message':'You don\'t have any lists yet :('
        }

    return {
        'form':form,
        'todo_lists':todo_lists,
        'ws':ws
    }

@post('/lists', template="todolists.html")
@logged_in_only
def todolists_post():
    '''Process add new list request'''
    ws = existing_web_session()
    dbs = db_session(close=True)
    post = request.POST.decode()
    form = forms.AddTodo()

    todo_name = cgi.escape(post['todo_list'])

    todo = Todo(owner_id=ws['user_id'], name=todo_name)

    dbs.add(todo)

    try:
        dbs.commit()
    except:
        dbs.rollback()
        return "-1"
    
    return json.dumps(todo.get_details())







@get('/addtask/<list_id>',template="addtask.html")
@logged_in_only
def addTask(list_id):
    '''Show a specific list'''

    ws = existing_web_session()
    dbs = db_session(close=True)
    attrs = {}



    tasks = dbs.query(Task).filter(Task.user_created_id == ws['user_id'], Task.todo_list_id == list_id).all()
    if tasks:
        for count,task in enumerate(tasks):
            attrs[count] = {'task_id':task.id}
            task.date_created = task.date_created.strftime("%Y-%m-%d %H:%M:%S")


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

    task_name = cgi.escape(post['task'])

    task = Task(name=task_name,description='',todo_list_id=list_id, creator=ws['user_id'],reviewer=ws['user_id'])


    dbs.add(task)

    try:
        dbs.commit()
    except:
        dbs.rollback()
        return "-1"

    #tasks = dbs.query(Task).filter(Task.user_created_id == ws['user_id']).all()

    return json.dumps(task.get_details())

@get('/upload',template='upload.html')
@logged_in_only
def upload():
    ws = existing_web_session()


    form = forms.UploadForm()

    return {
        'ws':ws,
        'form':form
    }

@post('/upload',template='upload.html')
@logged_in_only
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
