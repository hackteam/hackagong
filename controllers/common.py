import functools
import bottle
from bottle import get, view, static_file, request, response, route, abort
from config import BASE_DIR_STATIC, BASE_URL_PATH_RES, VIDEO_PATH
from utils import existing_web_session, web_session_exists, redirect
import os


def logged_in_only(f):
    ''' Only allow logged in users to access this page '''
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        redir = False
        if web_session_exists():
            ws = existing_web_session()
            if 'user_id' not in ws:
                redir = True
        else:
            redir = True

        if redir:
            redirect()
            
        return f(*args, **kwargs)
    return decorated

@get('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root=BASE_DIR_STATIC)


@route('/video/<filename>')
@logged_in_only
def watch(filename):
    return static_file(filename, root=os.path.join(VIDEO_PATH,'completed'))

