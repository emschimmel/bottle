import os

from bottle import route, run, template, view, static_file, request, redirect, post, get
import json
from parse_csv import ParseCsv
from enrich_data import EnrichData
import model.ad_object

# static_configs
CONFIG_PATH = "config"
ORIGIONAL_FILE_SUFFIX = "origional"
PARSED_FILE_SUFFIX = "dump"
SUPPORTED_TENANTS = ["marktplaats", "2dehands"]

overview_data = dict()
overview_data_filtered = dict()
search_string = ""
selected_index = 0

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

# components to fill:
# - item_list
# - selected_item
# - related_items

def __item_list_item(ad_object, selected):
    return '<a href="#" class="list-group-item list-group-item-action list-group-item-secondary p-2 {selected}">(id)</a>'.format(id=ad_object, selected="active" if selected else "")

def __update_item_list():
    global overview_data_filtered
    global selected_index

    if selected_index>len(overview_data_filtered):
        selected_index = 0
    output = []
    for index, item in enumerate(overview_data_filtered.keys()):
        output.append(__item_list_item(item, selected_index==index))
    return output

def __process_origional_file(tenant, file_name_origional):
    global overview_data
    global overview_data_filtered

    global search_string
    global selected_index

    overview_data = ParseCsv().parse(file_name_origional)

    search_string = ""
    selected_index = 0

    # for key, recommendations in overview_data.items():
    #     enriched_parent = EnrichData().process(tenant, key)
    #     for index, item in enumerate(recommendations):
    #         enriched_item = EnrichData().process(tenant, item)
    #         recommendations[index] = enriched_item
    #     overview_data[enriched_parent] = recommendations
    # overview_data_filtered = overview_data

    file_name_dump = "{path}/{suffix}.json".format(path=CONFIG_PATH,
                                                   suffix=PARSED_FILE_SUFFIX)
    print(overview_data)
    with open(file_name_dump, 'w') as file:
        file.write(json.dumps(overview_data))


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
        else:
            # todo: fix the static tenant
            tenant = "2dehands"
            file_name_origional = "{path}/{suffix}.json".format(path=CONFIG_PATH,
                                                           suffix=ORIGIONAL_FILE_SUFFIX)
            if os.path.exists(file_name_dump):
                __process_origional_file(tenant, file_name_origional)
        overview_data_filtered = overview_data
    view = dict()
    # TBD
    # view['request'] = request
    view['item_list'] = __update_item_list()
    # view['item_list'] = "bnbll"
    return view

@get('/upload')
@view('upload')
def view_upload():
    view = dict()
    view['tenant_list'] = SUPPORTED_TENANTS
    return view

@post('/upload')
def do_upload():
    tenant = request.forms.get('tenant')
    upload = request.files.get('upload')
    # use_all = request.files.get('use_all')
    # start = request.files.get('start')
    # end = request.files.get('end')
    file_name_origional = "{path}/{suffix}.csv".format(path=CONFIG_PATH,
                                                       suffix=ORIGIONAL_FILE_SUFFIX)
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)
    upload.save(file_name_origional, overwrite=True)

    __process_origional_file(tenant, file_name_origional)
    print("yay, done")
    return redirect('/')

@post('/search')
def do_search():
    global overview_data
    global overview_data_filtered
    global search_string
    search_string = request.forms.get('search')


run(host='localhost', port=8084)
