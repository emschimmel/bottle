import os
from bottle import route, run, template, view, static_file, request, redirect, post, get
from data_frame import ParseCsv
from model.tenant_enum import TenantConfig
import model.ad_object

####################################
# Static config
####################################
CONFIG_PATH = "config"
ORIGIONAL_FILE_SUFFIX = "origional"
PARSED_FILE_SUFFIX = "dump"
FILE_NAME_DUMP = "{path}/{suffix}.json".format(path=CONFIG_PATH,
                                                   suffix=PARSED_FILE_SUFFIX)
FILE_NAME_ORIGINAL = "{path}/{suffix}.csv".format(path=CONFIG_PATH,
                                                   suffix=ORIGIONAL_FILE_SUFFIX)

####################################
# State config
####################################
SUPPORTED_TENANTS = TenantConfig().getTenantList()
overview_data = dict()
overview_data_filtered = dict()
search_string = ""
selected_item = 0
tenant = SUPPORTED_TENANTS[0]

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

    output = df.ad_id_overview(search_string)
    if not selected_item in output:
        selected_item = output[0]
    return output


def __process_origional_file():
    global search_string

    df.restore(FILE_NAME_ORIGINAL)
    search_string = ""
    # EnrichData(df).process(tenant)


def __draw_index():
    # maybe we need a beter check here
    if not os.path.exists(FILE_NAME_ORIGINAL):
        view = dict()
        view['tenant'] = tenant
        view['search_string'] = search_string
        view['no_data'] = True
        return view
    else:
        view = dict()
        # top pane
        view['tenant'] = tenant
        view['search_string'] = search_string
        # list pane
        view['item_list'] = __update_item_list()
        view['selected_item'] = selected_item

        # ad pane
        selected_ad = df.get_ad_by_id(tenant, selected_item)
        view['selected_ad_complete'] = selected_ad.loaded
        if selected_ad.loaded:
            view['selected_item_pane_title'] = selected_ad.title
            view['selected_item_pane_id'] = selected_ad.id
            view['selected_item_pane_img_url'] = selected_ad.img_url
            view['selected_item_pane_url'] = selected_ad.url
            view['selected_item_pane_price'] = selected_ad.price

            #recommenders pane
            view['recommendations'] = df.get_recommenders_by_parent_id(tenant, selected_item)
        #fallback
        view['no_data'] = False
        return view


####################################
# public routes
####################################
@get('/')
@view('index')
def main_page():
    return __draw_index()


@get('/_open_item/<ad_id:int>')
@view('index')
def open_item(ad_id):
    global selected_item

    selected_item = ad_id
    return __draw_index()


@get('/upload')
@view('upload')
def view_upload():
    view = dict()
    view['tenant_list'] = SUPPORTED_TENANTS
    return view


@post('/upload')
def do_upload():
    global tenant
    tenant = request.forms.get('tenant')
    upload = request.files.get('upload')
    # use_all = request.files.get('use_all')
    # start = request.files.get('start')
    # end = request.files.get('end')
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)
    upload.save(FILE_NAME_ORIGINAL, overwrite=True)

    __process_origional_file()
    print("yay, done")
    return redirect('/')


@post('/search')
def do_search():
    global overview_data
    global overview_data_filtered
    global search_string
    search_string = request.forms.get('search')

####################################
# On server start
####################################

if os.path.exists(FILE_NAME_DUMP):
    # df.restore(FILE_NAME_DUMP)
    df.load_enriched_data()
else:
    if os.path.exists(FILE_NAME_ORIGINAL):
        __process_origional_file()

run(host='localhost', port=8084)
