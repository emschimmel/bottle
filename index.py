import math
from bottle import route, run, template, view, static_file, request
import json

curr_x = 0
curr_y = 0

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/js/<filename>')
def server_static(filename):
    return static_file(filename, root='./static/js')

@route('/css/<filename>')
def server_static(filename):
    return static_file(filename, root='./static/css')

@route('/')
@view('index')
def main_field():
    stats = dict()
    stats['value1'] = 100
    stats['value2'] = 100
    stats['value3'] = 100
    stats['value4'] = 100
    stats['value5'] = 100
    stats['curr_x'] = curr_x
    stats['curr_y'] = curr_y
    stats['request'] = request
    return stats



run(host='localhost', port=8083)
