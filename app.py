#!/usr/bin/env python
from os import path

import bottle
from bottle import get
from beaker.middleware import SessionMiddleware
import models
import controllers
import config

def setup_app():
	#Add templates path -- more to come?
	bottle.TEMPLATE_PATH.insert(0, path.join(config.BASE_DIR, 'templates'))

	bottle.debug(True)

	#Grab the app
	app = bottle.app()

	#Session control stuff
	sess_app = SessionMiddleware(app, config.SESSION_OPTS)


	return sess_app



application = setup_app()


@get('/hello/<name>')
def index(name='World'):
    return bottle.template('<b>Hello {{name}}</b>!!', name=name)

if __name__ == '__main__':
	bottle.run(host='localhost', port=9091, reloader=True)