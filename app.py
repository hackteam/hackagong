#!/usr/bin/env python
from os import path

import bottle
from bottle import get
from bottle import route, static_file
from beaker.middleware import SessionMiddleware
import models
import controllers
import config

from models import db_session
from werkzeug.debug import DebuggedApplication
import warnings

def setup_app():
    #Add templates path -- more to come?
    bottle.TEMPLATE_PATH.insert(0, path.join(config.BASE_DIR, 'templates'))

    bottle.debug(True)

    models.db_init()

    #Change errors to warnings
    warnings.simplefilter('error')

    #Grab the app
    app = bottle.app()
    sess_app = SessionMiddleware(app, config.SESSION_OPTS)



    sess_app.catchall = False
    sess_app = DebuggedApplication(sess_app, evalex=True)

    return sess_app



application = setup_app()




if __name__ == '__main__':
    SERVER = getattr(bottle, 'WaitressServer', bottle.AutoServer)
    bottle.run(app=application, server=SERVER,host=config.BIND_TO_HOST, 
        port=config.BIND_TO_PORT, reloader=True, debug=True)



