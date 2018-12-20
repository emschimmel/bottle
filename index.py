import os

from bottle import route, run, template, view, static_file, request
import json
from parse_csv import ParseCsv

# static_configs
CONFIG_PATH = "config"
ORIGIONAL_FILE_SUFFIX = "origional"
PARSED_FILE_SUFFIX = "dump"
overview_data = dict()
overview_data_filtered = dict()
search_string = ""

# Hello world test
@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/js/<filename>', name='static')
def server_static(filename):
    return static_file(filename, root='./static/js')

@route('/css/<filename>', name='static')
def server_static(filename):
    return static_file(filename, root='./static/css')

@route('/')
@view('index')
def main_page():
    global overview_data
    global overview_data_filtered

    if not overview_data_filtered:
        file_name_dump = "{path}/{suffix}.json".format(path=CONFIG_PATH,
                                                       suffix=PARSED_FILE_SUFFIX)
        if os.path.exists(file_name_dump):
            with open(file_name_dump, 'r') as file:
                overview_data = json.load(file)

        overview_data_filtered = overview_data
    stats = dict()
    # TBD
    # stats['request'] = request
    return stats

@route('/upload', method='POST')
def do_upload():
    global overview_data
    global overview_data_filtered
    global search_string

    tenant = request.forms.get('tenant')
    upload = request.files.get('upload')
    file_name_origional = "{path}/{suffix}.csv".format(path=CONFIG_PATH,
                                                       suffix=ORIGIONAL_FILE_SUFFIX)
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)
    upload.save(file_name_origional, overwrite=True)
    overview_data = ParseCsv().parse(tenant, file_name_origional)
    search_string = ""
    overview_data_filtered = overview_data

    file_name_dump = "{path}/{suffix}.json".format(path=CONFIG_PATH,
                                                  suffix=PARSED_FILE_SUFFIX)

    with open(file_name_dump, 'w') as file:
        json.dump(overview_data, file)

    return "File saved"

@route('/upload', method='POST')
def do_search():
    global overview_data
    global overview_data_filtered
    global search_string
    search_string = request.forms.get('search')


# components to fill:
# - item_list
# - selected_item
# - related_items


run(host='localhost', port=8084)
