#!/usr/bin/env python
from os import path

import bottle
from bottle import get
from beaker.middleware import SessionMiddleware
import models
import controllers
import config

from werkzeug.debug import DebuggedApplication
import warnings

def setup_app():
    #Add templates path -- more to come?
    bottle.TEMPLATE_PATH.insert(0, path.join(config.BASE_DIR, 'templates'))

    bottle.debug(True)
    
    #Change errors to warnings
    warnings.simplefilter('error')

    #Grab the app
    app = bottle.app()


    app.catchall = False
    app = DebuggedApplication(app, evalex=True)

    return app



application = setup_app()


@get('/hello/<name>')
def index(name='World'):
    x = 11

    raise 

if __name__ == '__main__':
    SERVER = getattr(bottle, 'WaitressServer', bottle.AutoServer)
    bottle.run(app=application, server=SERVER,host=config.BIND_TO_HOST, 
        port=config.BIND_TO_PORT, reloader=True, debug=True)



