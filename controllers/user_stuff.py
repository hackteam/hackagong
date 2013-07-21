import bottle
from bottle import get, post, view, static_file, request, response, route, abort
import config
from config import BASE_DIR_STATIC, BASE_URL_PATH_RES, BASE_DIR
from utils import redirect, existing_web_session
from controllers.common import logged_in_only
from models import Task, User, db_session, Todo, VideoReward, ImageReward
import forms
import uuid
import os
import json
import cgi

import shlex
from subprocess import check_call, check_output, Popen
from subprocess import PIPE, STDOUT


import datetime

@get('/reward/video/<video_id>',template='watch_video.html')
def watch_vid(video_id):
    ws = existing_web_session()

    return {
        'ws':ws,
        'video_id':video_id
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


    list_obj = dbs.query(Todo).filter(Todo.id==list_id).all()
    if not list_obj:
        return {
            'message':'This is not the list you are looking for.',
            'ws':ws
        }


    tasks = dbs.query(Task).filter(Task.user_created_id == ws['user_id'], Task.todo_list_id == list_id, Task.date_completed == None).all()

    if tasks:
        for count,task in enumerate(tasks):
            attrs[count] = {'task_id':task.id}
            task.date_created = task.date_created.strftime("%Y-%m-%d %H:%M:%S")
    form = forms.AddTask()
    return {
        'list_id':list_id,
        'list_name':list_obj.pop().name,
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

    if not dbs.query(Todo).filter(Todo.id==list_id).all():
        return {
            'message':'This is not the list you are looking for.',
            'ws':ws
        }

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
    dbs = db_session(close=True)

    vid_types = ('.mp4','.wmv','.mov','.m4v')
    img_types = ('.jpg','.png','.gif')


    new_file = post['uploaded_file']

    #Check for upload pressed with no file selected.
    if not new_file:
        return {
            "message":"No file was selected. Please try again.",
            "ws":ws,
            'form':form
        }


    name,ext = os.path.splitext(new_file.filename)



    name = str(uuid.uuid4())


    if ext in vid_types:
        OUTPUT_PATH = config.VIDEO_PATH
    elif ext in img_types:
        OUTPUT_PATH = config.IMAGE_PATH

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

    #Check extension and decide on tpye of reward to create
    if ext in vid_types:
        encode = encode_video(name+ext)
        reward = VideoReward(name='New Video Reward!', owner_id=ws['user_id'])
        reward.set_reward_values(media_url=name)

    elif ext in img_types:
        reward = ImageReward(name='New Image Reward!', owner_id=ws['user_id'])
        reward.set_reward_values(media_url=name+ext)

    else:
        return {
            'message':'Invalid format :(',
            'ws':ws
        }

    dbs.add(reward)

    try:
        dbs.commit()
    except:
        return {
            'ws':ws,
            'message':'Something went wrong :('
        }


    return {
        'message':'File saved successfully',
        'ws':ws,
        'form':form
    }


def encode_video(filename):
    ws = existing_web_session()
    dest = os.path.join(config.VIDEO_PATH,'completed/')
    vid = config.VIDEO_PATH+"/"+filename

    if not os.path.exists(dest):
        os.makedirs(dest)

    name,ext = os.path.splitext(filename)


    dest=dest+name

    encode_mp4 = 'ffmpeg -i "%s" -vcodec libx264 -movflags faststart "%s.mp4"' % (vid,dest)
    encode_mp4 = shlex.split(encode_mp4)


    encode_webm = 'ffmpeg -i "%s" -vcodec libvpx -codec:a libvorbis -f webm "%s.webm"' %(vid,dest)
    encode_webm = shlex.split(encode_webm)


    try:
        call = check_call(encode_mp4, stderr=STDOUT)
        call = check_call(encode_webm, stderr=STDOUT)
    except:
        return False

    else:
        return True

@get('/profile',template="profile.html")
@logged_in_only
def profile():
    ws = existing_web_session()
    dbs = db_session(close=True)

    num_lists = len(dbs.query(Todo).filter(
        Todo.owner_id == ws['user_id']).all())

    num_tasks = len(dbs.query(Task).filter(
        Task.user_created_id == ws['user_id']).all())

    return {
        'ws':ws,
        'num_lists':num_lists,
        'num_tasks': num_tasks,
        'num_perks': 2}

@get('/perks',template='perks.html')
@logged_in_only
def view_perks():
    ws = existing_web_session()
    dbs = db_session(close=True)


    return {
        'ws':ws
    }

@post('/finishtask/<task_id>')
@logged_in_only
def finish_task(task_id):
    '''Finish task for the current user'''

    dbs = db_session(close=True)
    post = request.POST.decode()

    dbs.query(Task).filter_by(id = post['task_id']).update({"date_completed": datetime.datetime.now()})

    try:
        dbs.commit()
    except:
        dbs.rollback()
        return "-1"
    return 'success'
