import os
from itertools import islice

from bottle import route, run, template, view, static_file, request, redirect, post, get

from actions.insert_actions import InsertActions
from actions.overview_actions import OverviewActions
from actions.scrapper_actions import ScrapperActions
from actions.elastic_actions import ElasticActions
from model.ad_object import AdObject
from model.state_config import FileName, State
import math

####################################
# Instances
####################################

overview_action = OverviewActions()
scrapper_action = ScrapperActions()
insert_action = InsertActions()
elastic_action = ElasticActions()

state = State()

####################################
# State config
####################################
search_string = state.search_string
filter_string = state.filter_string
selected_item = state.selected_item
selected_user_item = state.selected_user_item
tenant = state.tenant
offline_mode = state.offline_mode

current_page = None
max_per_page = state.max_per_page

insert_preference = State.insert_preference
input_options = ["CSV", "RAW", "FORM"]
limit = state.default_limit


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


####################################
# Private
####################################
def __call_restore():
    if State.system_mode == State.AD_LIST_MODE:
        print('starting the application in ad list ui mode')
        if os.path.exists(FileName.original_data_list_file_name()):
            overview_action.restore_add_list_data()
    elif State.system_mode == State.AD_RECOMMENDERS_MODE:
        print('starting the application in recommender ui mode')
        if os.path.exists(FileName.original_file_name()):
            overview_action.restore()
    elif State.system_mode == State.AD_USER_RECOM_MODE:
        print('starting the application in user recommender ui mode')
        if os.path.exists(FileName.original_user_recom_file_name()):
            overview_action.restore_user_recom_data()
        if os.path.exists(FileName.original_product_recom_file_name()):
            overview_action.restore_product_recom_data()


def __update_item_list():
    global selected_item
    global current_page
    if State.system_mode == State.AD_RECOMMENDERS_MODE:
        full_output = overview_action.ad_id_overview(search_string=search_string, filter_string=filter_string,
                                                     offline_mode=offline_mode)
    else:
        full_output = overview_action.ad_id_overview_user_recom(search_string=search_string,
                                                                filter_string=filter_string,
                                                                offline_mode=offline_mode)

    paged_output = [full_output[i:i + max_per_page] for i in range(0, len(full_output), max_per_page)]
    amount_pages = len(paged_output) - 1
    if current_page is None:
        current_page = math.floor(
            full_output.index(selected_item) / max_per_page) if selected_item in full_output else 0
    print("full_output length {l}".format(l=len(full_output)))
    output = []
    if len(paged_output) > 0:
        output = paged_output[current_page]
        if (selected_item not in output):
            selected_item = output[0] if len(output) > 0 else 0

    return output, amount_pages, current_page


def __page_bar_list(amount_pages, current_page):
    sub_set = set()
    sub_set.add(0)
    if amount_pages > 1:
        sub_set.add(amount_pages)
    sub_set.add(current_page)
    start = current_page - 2 if current_page is not None and current_page - 2 > 0 else 1
    for e in range(start, start + 5 if start + 5 < amount_pages else amount_pages):
        sub_set.add(e)
    return list(sorted(sub_set))


def __draw_index_list_mode(all=True):
    global current_page

    view = dict()
    if all:
        ad_list, amount_pages, current_page = overview_action.ad_list_for_page(search_string, filter_string,
                                                                               offline_mode, current_page, max_per_page)
        if len(ad_list) is 0:
            return __draw_index_search_data()
        # list pane
        view['item_list'] = ad_list

        # pagination
        view['max_per_page'] = max_per_page
        view['selectable_page_amounts'] = State.SELECTABLE_PAGE_AMOUNTS
        view['page_bar'] = __page_bar_list(amount_pages=amount_pages, current_page=current_page)
        view['current_page'] = current_page

    view['all_data'] = all

    # top pane
    view['tenant'] = tenant
    view['system_mode'] = State.system_mode
    view['filter_string'] = filter_string
    view['search_string'] = search_string
    view['offline_mode'] = offline_mode

    # fallback
    view['no_data'] = False
    view['no_search_data'] = False
    return view


def __draw_index_user_recom_mode(all=True, ad_id=selected_item, user_id=selected_user_item):
    view = dict()
    view['all_data'] = all
    if all:
        ad_list, amount_pages, current_page = __update_item_list()
        ad_id = selected_item
        if len(ad_list) is 0:
            return __draw_index_search_data()
        # list pane
        view['selected_item'] = ad_id
        view['selected_user_item'] = user_id
        view['item_list'] = ad_list

        # pagination
        view['max_per_page'] = max_per_page
        view['selectable_page_amounts'] = State.SELECTABLE_PAGE_AMOUNTS
        view['page_bar'] = __page_bar_list(amount_pages=amount_pages, current_page=current_page)
        view['current_page'] = current_page
    view['item_user_list'] = overview_action.get_users_for_product_recommendations(ad_id=ad_id)
    # top pane
    view['tenant'] = tenant
    view['system_mode'] = State.system_mode
    view['filter_string'] = filter_string
    view['search_string'] = search_string
    view['offline_mode'] = offline_mode

    # ad pane
    selected_ad = overview_action.get_ad_by_id(ad_id)
    view['selected_ad_complete'] = selected_ad.loaded
    view['selected_ad_error'] = selected_ad.error
    if selected_ad.loaded and not selected_ad.error:
        view['selected_ad'] = selected_ad
        recommendations, product_ad_ids_to_load = overview_action.get_product_recommenders_for_initial_view(ad_id=ad_id,
                                                                                                            limit=limit)

        # if len(recommendations):
        #     recommendations = sorted(recommendations, key=lambda x: float(x.score), reverse=True)
        user_recommendations, user_ad_ids_to_load = overview_action.get_user_recommenders_for_initial_view(ad_id=ad_id,
                                                                                                           user_id=user_id,
                                                                                                           limit=limit)
        # if len(user_recommendations):
        #     user_recommendations = sorted(user_recommendations, key=lambda x: float(x.score), reverse=True)

        if len(product_ad_ids_to_load + user_ad_ids_to_load) > 0:
            scrapper_action.start_processes_for_list(product_ad_ids_to_load + user_ad_ids_to_load)

        # recommenders pane
        view['recommendations'] = recommendations
        view['user_recommendations'] = user_recommendations
        if len(product_ad_ids_to_load+user_ad_ids_to_load) > 0:
            scrapper_action.start_processes_for_list(product_ad_ids_to_load+user_ad_ids_to_load)
        view['not_loaded'] = len([not_loaded.loaded for not_loaded in
                                  recommendations[0:limit if limit is not False else len(recommendations)]+user_recommendations[0:limit if limit is not False else len(user_recommendations)] if
                                  not not_loaded.loaded]) > 0
    view['recommendations_limit'] = limit

    # fallback
    view['no_data'] = False
    view['no_search_data'] = False
    return view


def __draw_index_with_recommenders(all=True, ad_id=selected_item):
    view = dict()
    if all:
        ad_list, amount_pages, current_page = __update_item_list()
        ad_id = selected_item
        if len(ad_list) is 0:
            return __draw_index_search_data()
        # list pane
        view['selected_item'] = ad_id
        view['item_list'] = ad_list

        # pagination
        view['max_per_page'] = max_per_page
        view['selectable_page_amounts'] = State.SELECTABLE_PAGE_AMOUNTS
        view['page_bar'] = __page_bar_list(amount_pages=amount_pages, current_page=current_page)
        view['current_page'] = current_page

    view['all_data'] = all

    # top pane
    view['tenant'] = tenant
    view['system_mode'] = State.system_mode
    view['filter_string'] = filter_string
    view['search_string'] = search_string
    view['offline_mode'] = offline_mode

    # ad pane
    selected_ad = overview_action.get_ad_by_id(ad_id)
    view['selected_ad_complete'] = selected_ad.loaded
    view['selected_ad_error'] = selected_ad.error

    if selected_ad.loaded and not selected_ad.error:
        view['selected_ad'] = selected_ad
        recommendations, ad_ids_to_load = overview_action.get_recommenders_for_initial_view(ad_id=ad_id, limit=limit)
        if len(ad_ids_to_load) > 0:
            scrapper_action.start_processes_for_list(ad_ids_to_load)
        view['not_loaded'] = len([not_loaded.loaded for not_loaded in
                                  recommendations[0:limit if limit is not False else len(recommendations)] if
                                  not not_loaded.loaded]) > 0
        # recommenders pane
        view['recommendations'] = recommendations
    view['recommendations_limit'] = limit

    # fallback
    view['no_data'] = False
    view['no_search_data'] = False
    return view

def __draw_index_with_recommenders_and_users(all=True, ad_id=selected_item, user_id=selected_user_item):
    view = dict()
    if all:
        ad_list, amount_pages, current_page = __update_item_list()
        ad_id = selected_item
        if len(ad_list) is 0:
            return __draw_index_search_data()
        # list pane
        view['selected_item'] = ad_id
        view['item_list'] = ad_list

        # pagination
        view['max_per_page'] = max_per_page
        view['selectable_page_amounts'] = State.SELECTABLE_PAGE_AMOUNTS
        view['page_bar'] = __page_bar_list(amount_pages=amount_pages, current_page=current_page)
        view['current_page'] = current_page
    view['item_user_list'] = overview_action.get_users_for_product_recommendations(ad_id=ad_id)
    view['selected_user_item'] = selected_user_item
    view['all_data'] = all

    # top pane
    view['tenant'] = tenant
    view['system_mode'] = State.system_mode
    view['filter_string'] = filter_string
    view['search_string'] = search_string
    view['offline_mode'] = offline_mode

    # ad pane
    selected_ad = overview_action.get_ad_by_id(ad_id)
    view['selected_ad_complete'] = selected_ad.loaded
    view['selected_ad_error'] = selected_ad.error

    if selected_ad.loaded and not selected_ad.error:
        view['selected_ad'] = selected_ad
        recommendations, product_ad_ids_to_load = overview_action.get_product_recommenders_for_initial_view(ad_id=ad_id,
                                                                                                            limit=limit)
        user_recommendations, user_ad_ids_to_load = overview_action.get_user_recommenders_for_initial_view(ad_id=ad_id,
                                                                                                           user_id=user_id,
                                                                                                           limit=limit)

        if len(product_ad_ids_to_load + user_ad_ids_to_load) > 0:
            scrapper_action.start_processes_for_list(product_ad_ids_to_load + user_ad_ids_to_load)

        # recommenders pane
        view['recommendations'] = recommendations
        view['user_recommendations'] = user_recommendations
        if len(product_ad_ids_to_load+user_ad_ids_to_load) > 0:
            scrapper_action.start_processes_for_list(product_ad_ids_to_load+user_ad_ids_to_load)
        view['not_loaded'] = len([not_loaded.loaded for not_loaded in
                                  recommendations[0:limit if limit is not False else len(recommendations)]+user_recommendations[0:limit if limit is not False else len(user_recommendations)] if
                                  not not_loaded.loaded]) > 0
    view['recommendations_limit'] = limit

    # fallback
    view['no_data'] = False
    view['no_search_data'] = False
    return view


def __draw_index(all=True, ad_id=selected_item, user_id=selected_user_item):
    if State.system_mode == State.AD_RECOMMENDERS_MODE and os.path.exists(FileName.original_file_name()):
        return __draw_index_with_recommenders(all=all, ad_id=ad_id)
    if State.system_mode == State.AD_LIST_MODE and os.path.exists(FileName.original_data_list_file_name()):
        return __draw_index_list_mode(all=all)
    if State.system_mode == State.AD_USER_RECOM_MODE and os.path.exists(FileName.original_product_recom_file_name()):
        return __draw_index_user_recom_mode(all=all, ad_id=ad_id, user_id=selected_user_item)
    return __draw_index_no_data()


def __draw_index_no_data():
    view = dict()
    view['tenant'] = tenant
    view['search_string'] = search_string
    view['filter_string'] = filter_string
    view['no_data'] = True
    view['no_search_data'] = False
    view['all_data'] = True
    view['offline_mode'] = offline_mode
    return view


def __draw_index_search_data():
    view = dict()
    view['tenant'] = tenant
    view['search_string'] = search_string
    view['filter_string'] = filter_string
    view['no_data'] = False
    view['no_search_data'] = True
    view['all_data'] = True
    view['offline_mode'] = offline_mode
    return view


def __draw_config_controller():
    view = dict()
    view['tenant'] = tenant
    view['tenant_list'] = State.supported_tenants()
    view['application_modes'] = State.AVAILABLE_SYSTEM_MODES
    view['system_mode'] = State.system_mode
    view['selected_item'] = selected_item
    view['selected_user_item'] = selected_user_item
    view['search_string'] = search_string
    view['current_page'] = current_page
    view['max_per_page'] = max_per_page
    view['selectable_page_amounts'] = State.SELECTABLE_PAGE_AMOUNTS
    view['offline_mode'] = offline_mode
    view['input_options'] = input_options
    view['insert_preference'] = insert_preference
    view['default_limit'] = State.default_limit
    return view


def __draw_scrape_controller():
    view = dict()
    view['tenant'] = tenant
    print(State.system_mode)
    if State.system_mode == State.AD_RECOMMENDERS_MODE:
        view['amount_todo'] = scrapper_action.amount_adds()
        view['amount_done'] = scrapper_action.amount_enriched()
    elif State.system_mode == State.AD_LIST_MODE:
        view['amount_todo'] = scrapper_action.amount_adds_for_list()
        view['amount_done'] = scrapper_action.amount_enriched_for_list()
    elif State.system_mode == State.AD_USER_RECOM_MODE:
        view['amount_todo'] = scrapper_action.amount_adds_for_user_mode()
        view['amount_done'] = scrapper_action.amount_enriched_for_user_mode()
    else:
        view['amount_todo'] = 0
        view['amount_done'] = 0
    return view


def __draw_insert_controller():
    view = dict()
    view['tenant_list'] = State.supported_tenants()
    view['tenant'] = State.tenant
    view['application_modes'] = State.AVAILABLE_SYSTEM_MODES
    view['system_mode'] = State.system_mode
    view['insert_tenant'] = insert_tenant
    view['insert_ad_id'] = insert_ad_id
    view['insert_rows'] = rows
    view['insert_preference'] = insert_preference
    return view


####################################
# public routes
####################################

####################################
# Overview
####################################
@get('/')
@view('index')
def main_page():
    return __draw_index()


@get('/_open_item/<ad_id>')
@view('index')
def open_item(ad_id):
    global selected_user_item
    global selected_item
    global limit

    limit = state.default_limit
    selected_item = int(ad_id)
    selected_user_item = 0
    return redirect('/')


@get('/_open_item_for_user/<user_id>/<all>')
@view('index')
def open_item(user_id, all):
    global selected_user_item
    global limit

    limit = state.default_limit
    selected_user_item = int(user_id)
    if all == "False":
        return redirect('/share/'+str(selected_item))
    else:
        return redirect('/')



@get('/_show_all')
@get('/_show_more/<prefered_limit:int>')
@view('index')
def open_item(prefered_limit=False):
    global limit

    limit = prefered_limit
    return redirect('/')


@get('/_page/<page:int>')
@view('index')
def open_page(page):
    global current_page
    global selected_item
    global limit

    limit = state.default_limit
    selected_item = None
    current_page = page
    return redirect('/')


@get('/_search/<search_phrase>')
@get('/_search/')
def search(search_phrase=""):
    global search_string
    global current_page
    global limit

    limit = state.default_limit
    current_page = 0
    search_string = search_phrase


@get('/_filter/<filter_phrase>')
@get('/_filter/')
def search(filter_phrase=""):
    global filter_string
    global current_page
    global limit

    limit = state.default_limit
    current_page = 0
    filter_string = filter_phrase


@get('/_amount_per_page/<amount:int>')
def change_amount_per_page(amount):
    global max_per_page
    global current_page

    current_page = 0
    max_per_page = amount


@get('/_reload/<ad_id>')
@get('/share/_reload/<ad_id>')
def reload(ad_id):
    global limit

    limit = state.default_limit
    if State.system_mode == State.AD_RECOMMENDERS_MODE:
        overview_action.reload(ad_id)
    elif State.system_mode == State.AD_LIST_MODE:
        overview_action.reload_list_item(ad_id)
    elif State.system_mode == State.AD_USER_RECOM_MODE:
        overview_action.reload_list_item(ad_id)


@get('/share/<ad_id>')
@view('index')
def share(ad_id):
    if State.system_mode == State.AD_USER_RECOM_MODE:
        return __draw_index_with_recommenders_and_users(all=False, ad_id=ad_id, user_id=selected_user_item)
    return __draw_index_with_recommenders(all=False, ad_id=ad_id)



####################################
# Config
####################################
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
    global offline_mode
    global insert_preference

    tenant = request.forms.get('tenant')
    system_mode = request.forms.get('application_mode')
    search_string = request.forms.get('search_string')
    selected_item = request.forms.get('selected_item')
    selected_user_item = request.forms.get('selected_user_item')
    offline_mode = True if request.forms.get('offline_mode') else False
    insert_preference = request.forms.get('insert_preference')
    default_limit = request.forms.get('default_limit')

    State.default_limit = default_limit
    State.tenant = tenant

    max_per_page = int(request.forms.get('max_per_page'))
    state.set_variables(tenant=tenant,
                        system_mode=system_mode,
                        search_string=search_string,
                        selected_item=selected_item,
                        selected_user_item=selected_user_item,
                        max_per_page=max_per_page,
                        offline_mode=offline_mode,
                        insert_preference=insert_preference,
                        default_limit=default_limit)
    state.store_state()
    return __draw_config_controller()


####################################
# Scrape
####################################
@get('/scrape')
@view('scrape')
def config_control():
    return __draw_scrape_controller()


@post('/_start_scrape')
def start_scrape():
    if State.system_mode == State.AD_RECOMMENDERS_MODE:
        if request.forms.get('use_all'):
            scrapper_action.start_all()
        else:
            scrapper_action.start_for_criteria(amount=request.forms.get('amount'),
                                               start=request.forms.get('start'),
                                               end=request.forms.get('end'))
    elif State.system_mode == State.AD_LIST_MODE:
        if request.forms.get('use_all'):
            scrapper_action.start_all_for_list()
        else:
            scrapper_action.start_for_criteria_for_list(amount=request.forms.get('amount'),
                                                        start=request.forms.get('start'),
                                                        end=request.forms.get('end'))
    elif State.system_mode == State.AD_USER_RECOM_MODE:
        if request.forms.get('use_all'):
            scrapper_action.start_all_for_user_recom()
        else:
            scrapper_action.start_for_criteria_for_user_recom(amount=request.forms.get('amount'),
                                                              start=request.forms.get('start'),
                                                              end=request.forms.get('end'))


####################################
# Insert
####################################
rows = [AdObject()]
insert_ad_id = ""
insert_tenant = State.tenant
insert_system_mode = State.system_mode


@get('/insert')
@view('insert')
def view_insert():
    return __draw_insert_controller()


@get('/upload')
@get('/_switch_input_format/<perference>')
def switch_input_format(perference=state.insert_preference):
    global insert_preference

    insert_preference = perference
    redirect("/insert")


@post('/_add_insert_row')
def add_insert_row():
    global rows

    __set_insert_form_data()

    new_row = AdObject()
    new_row.rank = len(rows) + 1
    rows.insert(len(rows), new_row)


@post('/_remove_insert_row/<row_id:int>')
def remove_insert_row(row_id):
    global rows

    __set_insert_form_data()

    del rows[row_id]
    for index, row in enumerate(rows):
        row.rank = index + 1


def __set_insert_form_data():
    global insert_ad_id
    global insert_tenant
    global insert_system_mode
    global rows

    for key in request.forms.keys():
        if key == 'ad_id':
            insert_ad_id = request.forms.get('ad_id')
        elif key == 'tenant':
            insert_tenant = request.forms.get('tenant')
        elif key == 'application_mode':
            insert_system_mode = request.forms.get('application_mode')
        else:
            key_for_row, rank = key.split('_', 1)
            setattr(rows[int(rank)], key_for_row, request.forms.get(key))


@post('/insert')
def do_insert():
    global rows
    global tenant
    global insert_ad_id
    global insert_system_mode

    __set_insert_form_data()

    for row in rows:
        if not row.validate_for_csv():
            rows.remove(row)
    if insert_system_mode == State.AD_RECOMMENDERS_MODE:
        insert_action.insert_single_row_with_recommendations(insert_ad_id, rows)
    elif insert_system_mode == State.AD_LIST_MODE:
        insert_action.insert_single_row_add_list(insert_ad_id)
    elif insert_system_mode == State.AD_USER_RECOM_MODE:
        insert_action.insert_single_row_user_recommendations(insert_ad_id, rows)
    tenant = insert_tenant
    selected_item = insert_ad_id
    insert_ad_id = ""
    rows = [AdObject()]

    state.tenant = tenant
    state.system_mode = insert_system_mode
    state.store_filled_state(tenant=tenant, system_mode=insert_system_mode)
    return redirect('/_open_item/' + selected_item)


@post('/insert_raw')
def do_insert_raw():
    global tenant
    global limit

    limit = state.default_limit
    tenant = request.forms.get('tenant')
    system_mode = request.forms.get('application_mode')
    raw_collection = [l.replace('\r', '').replace(' ', '') for l in request.forms.get('input_raw').split("\n") if l]
    if system_mode == State.AD_RECOMMENDERS_MODE:
        insert_action.insert_multi_row_with_recommendations(raw_collection)
    elif insert_system_mode == State.AD_LIST_MODE:
        insert_action.insert_multi_row_add_list(raw_collection)
    elif insert_system_mode == State.AD_USER_RECOM_MODE:
        insert_action.insert_multi_row_product_recom_list(raw_collection)
        raw_user_collection = [l.replace('\r', '').replace(' ', '') for l in
                               request.forms.get('input_raw_user').split("\n") if l]
        insert_action.insert_multi_row_user_recom_list(raw_user_collection)
    state.tenant = tenant
    state.system_mode = system_mode
    state.store_filled_state(tenant=tenant, system_mode=system_mode)
    return redirect('/')


@post('/upload')
def do_upload():
    global tenant
    global search_string
    global filter_string
    global current_page
    global limit

    limit = state.default_limit
    tenant = request.forms.get('tenant')
    system_mode = request.forms.get('application_mode')
    upload = request.files.get('upload')

    filename = FileName.original_file_name()
    if system_mode == State.AD_LIST_MODE:
        filename = FileName.original_data_list_file_name()
    elif system_mode == State.AD_USER_RECOM_MODE:
        upload_user_file = request.files.get('upload_user_file')
        user_filename = FileName.original_user_recom_file_name()
        __store_file(user_filename, upload_user_file)
        filename = FileName.original_product_recom_file_name()

    __store_file(upload, filename)
    current_page = 0
    state.tenant = tenant
    state.system_mode = system_mode
    state.store_filled_state(tenant=tenant, system_mode=system_mode)

    __call_restore()
    print("yay, done")
    return redirect('/')


def __store_file(upload, filename):
    if not os.path.exists(FileName.config_path()):
        os.makedirs(FileName.config_path())
    if request.forms.get('use_all'):
        upload.save(filename, overwrite=True)
    else:
        temp_file_name = filename + "_temp"
        upload.save(temp_file_name, overwrite=True)
        start = int(request.forms.get('start'))
        end = int(request.forms.get('end'))
        # TODO: check if this isn't to specific
        lines = ["ad_id,recommended_ad_id,rank,score\n"]
        with open(temp_file_name, 'r') as open_file:
            lines.extend(line for line in islice(open_file, start, end))

        with open(filename, 'w') as open_file:
            open_file.write(''.join(lines))

        os.remove(temp_file_name)


####################################
# Insert into Elasticsearch
####################################
@route('/elastic')
def elastic():
    elastic_action.start_import()
    return template('<b>Started importing</b>')


####################################
# On server start
####################################
if __name__ == '__main__':
    if os.path.exists(FileName.dump_file_name()):
        print('loading scrapped data for tenant {tenant}'.format(tenant=State.tenant))
        overview_action.load_enriched_data()
    __call_restore()

    # signal.signal(signal.SIGTERM, scrapper_action.stop_processes())
    # signal.signal(signal.SIGINT, scrapper_action.stop_processes())
    # signal.signal(signal.SIGQUIT, scrapper_action.stop_processes())
    run(host='localhost', port=8084)
