#!/usr/bin/env python
import bottle
from bottle import get, run

@get('/hello/<name>')
def index(name='World'):
    return bottle.template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=9091)