from os import path


LOCAL_HOST = '127.0.0.1'
BIND_TO_PORT = 9091

BIND_TO_HOST = LOCAL_HOST
PUBLIC_HOST = LOCAL_HOST + ':' + str(BIND_TO_PORT)
BASE_URL_PATH = '/'

BASE_DIR = path.abspath(path.dirname(__file__))
BASE_DIR_STATIC = path.join(BASE_DIR, 'static')

#URL paths
BASE_HOST_URL = 'http://' + PUBLIC_HOST
BASE_URL_PATH_RES = BASE_URL_PATH + 'static/'
FULL_BASE_URL = BASE_HOST_URL + BASE_URL_PATH

#Sessions path
SESSIONS_BASE_DIR = path.join(BASE_DIR, 'sessions')

#Session options
SESSION_OPTS = {
    'session.type': 'file',
    'session.data_dir': path.join(SESSIONS_BASE_DIR, 'sessions'),
    'session.cookie_expires': True,
    'session.timeout': 30*60,   # 30 minutes (in seconds)
    'session.key': 'ldt_session',
    'session.auto': True
}

BASE_DIR = path.abspath(path.dirname(__file__))
BASE_DIR_STATIC = path.join(BASE_DIR, 'static')