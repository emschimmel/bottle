import configparser
import ast


class ConfigObject(object):

    ad_recommenders = None
    config_file = "config/state_config.ini"
    parser = configparser.RawConfigParser()
    parser.read(config_file)
    CONFIG_PATH = "config"

    ####################################
    # Tenant config
    ####################################
    BVA = parser.getboolean('TenantConfig', 'enable_bva', fallback=True)
    MARKTPLAATS = parser.getboolean('TenantConfig', 'enable_marktplaats', fallback=False)
    KIJIJI = parser.getboolean('TenantConfig', 'enable_kijiji', fallback=False)
    TWEEDE_HANDS = parser.getboolean('TenantConfig', 'enable_tweedehands', fallback=False)
    DBA = parser.getboolean('TenantConfig', 'enable_dba', fallback=False)

    BVA_URL = parser.get('TenantConfig', 'url_bva', fallback="https://www.bva-auctions.com/nl/auction/lot/{auction_id}/{lot_id}")
    MARKTPLAATS_URL = parser.get('TenantConfig', 'url_marktplaats', fallback="http://marktplaats.nl/{id}")
    KIJIJI_URL = parser.get('TenantConfig', 'url_kijiji', fallback="https://www.kijiji.ca/v-view-details.html?adId={id}")
    TWEEDE_HANDS_URL = parser.get('TenantConfig', 'url_tweedehands', fallback="https://www.2dehands.be/{id}.html")
    DBA_URL = parser.get('TenantConfig', 'url_dba', fallback="https://www.dba.dk/id-{id}")

    ####################################
    # System config
    ####################################
    ORIGINAL_FILE_SUFFIX = parser.get('SystemConfig', 'original_file_suffix', fallback='original')
    ORIGINAL_AD_LIST_FILE_SUFFIX = parser.get('SystemConfig', 'original_ad_list_file_suffix', fallback='original_ad_list')
    ORIGINAL_USER_RECOM_FILE_SUFFIX = parser.get('SystemConfig', 'original_user_recom_file_suffix', fallback='original_user_recom')
    ORIGINAL_PRODUCT_RECOM_FILE_SUFFIX = parser.get('SystemConfig', 'original_product_recom_file_suffix', fallback='original_product_recom')
    PARSED_FILE_SUFFIX = parser.get('SystemConfig', 'parsed_file_suffix', fallback='dump')
    SELECTABLE_PAGE_AMOUNTS = ast.literal_eval(parser.get('SystemConfig', 'selectable_page_amounts', fallback="[10, 50, 100]"))
    MAX_WORKERS = parser.getint('SystemConfig', 'max_workers', fallback=10)
    SAVE_INTERVAL = parser.getint('SystemConfig', 'save_interval', fallback=5)
    AD_RECOMMENDERS_MODE = 'ad_recommenders'
    AD_LIST_MODE = 'ad_list_mode'
    AD_USER_RECOM_MODE = 'user_recom_mode'
    AVAILABLE_SYSTEM_MODES = [AD_RECOMMENDERS_MODE, AD_LIST_MODE, AD_USER_RECOM_MODE]

    ####################################
    # State config
    ####################################
    search_string = parser.get('UserConfig', 'search_string', fallback="")
    filter_string = parser.get('UserConfig', 'filter_string', fallback="")

    selected_item = parser.get('UserConfig', 'selected_item', fallback="0")
    selected_user_item = parser.get('UserConfig', 'selected_user_item', fallback="0")
    tenant = parser.get('UserConfig', 'tenant', fallback="Bva")
    system_mode = parser.get('UserConfig', 'system_mode', fallback=AD_USER_RECOM_MODE)

    max_per_page = parser.getint('UserConfig', 'max_per_page', fallback=50)
    offline_mode = parser.getboolean('UserConfig', 'offline_mode', fallback=False)

    insert_preference = parser.get('UserConfig', 'insert_preference', fallback="CSV")

    default_limit = parser.getint('UserConfig', 'default_limit', fallback=6)

    ####################################
    # ES connection settings
    ####################################
    ELASTIC_IP = parser.get('ElasticConfig', 'ip', fallback='127.0.0.1')
    ELASTIC_PORT = parser.getint('ElasticConfig', 'port', fallback=9200)