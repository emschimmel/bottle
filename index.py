import os
from bottle import route, run, template, view, static_file, request, redirect, post, get
from data_frame import DataActions
from model.ad_object import AdObject
from model.config_object import FileName, State
import math

####################################
# Instances
####################################
df = DataActions()
state = State()

####################################
# State config
####################################
search_string = state.search_string
selected_item = state.selected_item
tenant = state.tenant

current_page = None
max_per_page = state.max_per_page
amount_pages = 1

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

@route('/static/img/<filename>', name='static')
def server_static(filename):
    return static_file(filename, root='./static/img')

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
    paged_output = [full_output[i:i + max_per_page] for i in range(0, len(full_output), max_per_page)]
    amount_pages = len(paged_output)

    if current_page is None:
        current_page = math.floor(full_output.index(selected_item)/max_per_page) if selected_item in full_output else 0
    print("full_output length {l}".format(l=len(full_output)))

    output = []
    if len(paged_output) > 0:
        output = paged_output[current_page]
        print("set selected_item")
        if selected_item is None:
            selected_item = output[0] if len(output)>0 else 0

    return output


def __page_bar_list():
    sub_set = set()
    sub_set.add(0)
    sub_set.add(amount_pages)
    sub_set.add(current_page)
    start = current_page-2 if current_page is not None and current_page-2 >0 else 1
    for e in range(start, start+5 if start+5 < amount_pages else amount_pages):
        sub_set.add(e)

    return list(sub_set)


def __process_original_file():
    global search_string

    df.restore()
    search_string = ""


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
        view['selectable_page_amounts'] = State.SELECTABLE_PAGE_AMOUNTS
        view['page_bar'] = __page_bar_list()
        view['current_page'] = current_page

        # ad pane
        selected_ad = df.get_ad_by_id(selected_item)
        view['selected_ad_complete'] = selected_ad.loaded
        view['selected_ad_error'] = selected_ad.error

        if selected_ad.loaded and not selected_ad.error:
            view['selected_item_pane_title'] = selected_ad.title
            view['selected_item_pane_id'] = selected_ad.id
            view['selected_item_pane_img_url'] = selected_ad.img_url
            view['selected_item_pane_url'] = selected_ad.url
            view['selected_item_pane_price'] = selected_ad.price
            recommendations = df.get_recommenders_by_parent_id(selected_item)
            view['not_loaded'] = len([not_loaded.loaded for not_loaded in recommendations if not not_loaded.loaded])>0
            #recommenders pane
            view['recommendations'] = recommendations

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


def __draw_config_controller():
    view = dict()
    view['tenant'] = tenant
    view['tenant_list'] = State.supported_tenants()
    view['search_string'] = search_string
    view['selected_item'] = selected_item
    view['current_page'] = current_page
    view['max_per_page'] = max_per_page
    view['selectable_page_amounts'] = State.SELECTABLE_PAGE_AMOUNTS
    view['amount_todo'] = df.amount_adds()
    view['amount_done'] = df.amount_enriched()
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
    global selected_item

    selected_item = None
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


@get('/config')
@view('config')
def config_control():
    return __draw_config_controller()


@post('/config')
@view('config')
def save_config():
    global tenant
    global search_string
    global selected_item
    global max_per_page

    tenant = request.forms.get('tenant')
    search_string = request.forms.get('search_string')
    selected_item = request.forms.get('selected_item')
    max_per_page = int(request.forms.get('max_per_page'))
    state.set_variables(tenant=tenant,
                        search_string=search_string,
                        selected_item=selected_item,
                        max_per_page=max_per_page)
    state.store_state()
    return __draw_config_controller()

@post('/_start_scrape')
def start_scrape():
    if request.forms.get('use_all'):
        df.start_all()
    else:
        print(request.forms)
        df.start_for_criteria(amount=request.forms.get('amount'),
                              start=request.forms.get('start'),
                              end=request.forms.get('end'))

@post('/original')
def reduse_original():
    df.reduce_uploaded_csv_data()
    return __draw_config_controller()


@get('/upload')
@view('upload')
def view_upload():
    view = dict()
    view['tenant_list'] = State.supported_tenants()
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
    state.tenant = tenant
    state.store_state()
    __process_original_file()
    print("yay, done")
    return redirect('/')


@post('/search')
def do_search():
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
