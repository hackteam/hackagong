import bottle
from bottle import get, view, static_file, request, response, route, abort
from config import BASE_DIR_STATIC



@get(['/static/:filename#.*#', r'/:filename#favicon\.ico#'])
def static_files(filename):
    ''' Route for styles and images '''
    return static_file(filename, root=BASE_DIR_STATIC)