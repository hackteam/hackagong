import bottle
from bottle import get, view, static_file, request, response, route, abort
from config import BASE_DIR_STATIC, BASE_URL_PATH_RES


@get('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root=BASE_DIR_STATIC)
