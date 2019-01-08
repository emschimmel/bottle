import os
from bottle import route, run, template, view, static_file, request, redirect, post, get
from data_frame import ParseCsv
from model.ad_object import AdObject
from model.config_object import FileName, SystemConfig
import math

####################################
# State config
####################################
overview_data = dict()
search_string = ""
selected_item = 0
tenant = SystemConfig.supported_tenants()[0]

current_page = 0
amount_pages = 1
max_per_page = 50

####################################
# Datasource instance
####################################
df = ParseCsv()


####################################
# Static loaders
####################################
@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)


@route('/js/<filename>', name='static')
def server_static(filename):
    return static_file(filename, root='./static/js')


@route('/css/<filename>', name='static')
def server_static(filename):
    return static_file(filename, root='./static/css')

@route('/img/<subdir>/<filename>', name='static')
def server_static(subdir, filename):
    return static_file(filename, root='./img/{subdir}'.format(subdir=subdir))


# components to fill:
# - item_list
# - selected_item
# - related_items
####################################
# Private
####################################
def __update_item_list():
    global selected_item
    global amount_pages
    global current_page

    full_output = df.ad_id_overview(search_string)
    print("full_output length {l}".format(l=len(full_output)))

    paged_output = [full_output[i:i + max_per_page] for i in range(0, len(full_output), max_per_page)]
    amount_pages = math.ceil(len(paged_output) / max_per_page)
    if amount_pages < current_page:
        current_page = 0

    output = []
    if len(paged_output) > 0:
        output = paged_output[current_page]
        if selected_item not in output:
            print("set selected_item")
            selected_item = output[0] if len(output)>0 else 0

    return output


def __page_bar_list():
    sub_set = set()
    sub_set.add(0)
    sub_set.add(amount_pages)
    sub_set.add(current_page)
    start = current_page-2 if current_page-2 >0 else 1
    for e in range(start, start+5 if start+5 < amount_pages else amount_pages):
        sub_set.add(e)

    return list(sub_set)


def __process_original_file():
    global search_string

    df.restore(FileName.original_file_name())
    search_string = ""
    # EnrichData(df).process(tenant)


def __draw_index():
    # maybe we need a beter check here
    if os.path.exists(FileName.original_file_name()):
        ad_list = __update_item_list()
        if len(ad_list) is 0:
            return __draw_index_search_data()
        view = dict()
        # top pane
        view['tenant'] = tenant
        view['search_string'] = search_string

        # list pane
        view['item_list'] = ad_list
        view['selected_item'] = selected_item

        # pagination
        view['max_per_page'] = max_per_page
        view['selectable_page_amounts'] = SystemConfig.selectable_amounts()
        view['page_bar'] = __page_bar_list()
        view['current_page'] = current_page

        # ad pane
        selected_ad = df.get_ad_by_id(tenant, selected_item)
        view['selected_ad_complete'] = selected_ad.loaded
        view['selected_ad_error'] = selected_ad.error

        if selected_ad.loaded and not selected_ad.error:
            view['selected_item_pane_title'] = selected_ad.title
            view['selected_item_pane_id'] = selected_ad.id
            view['selected_item_pane_img_url'] = selected_ad.img_url
            view['selected_item_pane_url'] = selected_ad.url
            view['selected_item_pane_price'] = selected_ad.price

            #recommenders pane
            view['recommendations'] = df.get_recommenders_by_parent_id(tenant, selected_item)

        #fallback
        view['no_data'] = False
        view['no_search_data'] = False
        return view
    return __draw_index_no_data()


def __draw_index_no_data():
    view = dict()
    view['tenant'] = tenant
    view['search_string'] = search_string
    view['no_data'] = True
    view['no_search_data'] = False
    return view


def __draw_index_search_data():
    view = dict()
    view['tenant'] = tenant
    view['search_string'] = search_string
    view['no_data'] = False
    view['no_search_data'] = True
    return view


####################################
# public routes
####################################
@get('/')
@view('index')
def main_page():
    return __draw_index()


@get('/_open_item/<ad_id>')
@view('index')
def open_item(ad_id):
    global selected_item

    selected_item = ad_id
    return redirect('/')


@get('/_page/<page:int>')
@view('index')
def open_page(page):
    global current_page

    current_page = page
    return redirect('/')


@get('/_search/<search_phrase>')
@get('/_search/')
def search(search_phrase=""):
    print(search_phrase)
    global search_string
    global current_page

    current_page = 0
    search_string = search_phrase


@get('/_amount_per_page/<amount:int>')
def change_amount_per_page(amount):
    global max_per_page
    global current_page

    current_page = 0
    max_per_page = amount


@get('/upload')
@view('upload')
def view_upload():
    view = dict()
    view['tenant_list'] = SystemConfig.supported_tenants()
    return view


@post('/upload')
def do_upload():
    global tenant
    tenant = request.forms.get('tenant')
    upload = request.files.get('upload')
    # use_all = request.files.get('use_all')
    # start = request.files.get('start')
    # end = request.files.get('end')
    if not os.path.exists(FileName.config_path()):
        os.makedirs(FileName.config_path())
    upload.save(FileName.original_file_name(), overwrite=True)

    __process_original_file()
    print("yay, done")
    return redirect('/')


@post('/search')
def do_search():
    global overview_data
    global search_string
    search_string = request.forms.get('search')

####################################
# On server start
####################################

if os.path.exists(FileName.dump_file_name()):
    df.load_enriched_data()
if os.path.exists(FileName.original_file_name()):
    __process_original_file()

run(host='localhost', port=8084)
