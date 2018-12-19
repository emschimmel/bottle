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

@route('/main')
@view('main_field')
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

@route('/_click_tile')
def click_tile():
    hx = request.params.get('hx', 0, type=int)
    hy = request.params.get('hy', 0, type=int)
    suggested_moves = []
    print(hx)
    print(hy)
    if hx != hy:
        diffInX = hx > hy
        diffxy = math.floor(hx/(hx-hy)) if diffInX else math.floor(hy/(hy-hx))

    lowestx = curr_x if curr_x < hx else hx
    lowesty = curr_y if curr_y < hy else hy

    highestx = hx if hx > curr_x else curr_x
    highesty = hy if hy > curr_y else curr_y
    for x in range(lowestx, highestx):
        suggested_moves.append((x, lowesty))
        if x%2 ==0:
            suggested_moves.append((x+1, lowesty))

        if lowesty<highesty:
            lowesty = lowesty+1
    if lowesty != highesty:
        for y in range(lowesty, highesty):
            suggested_moves.append((hx, y))


    return json.dumps({'result': suggested_moves})


run(host='localhost', port=8083)
