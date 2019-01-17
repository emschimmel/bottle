import configparser
import ast


class ConfigObject(object):
    config_file = "config/state_config.ini"
    parser = configparser.RawConfigParser()
    parser.read(config_file)
    CONFIG_PATH = "config"

    ####################################
    # Tenant config
    ####################################
    MARKTPLAATS = parser.getboolean('TenantConfig', 'enable_marktplaats', fallback=True)
    KIJIJI = parser.getboolean('TenantConfig', 'enable_kijiji', fallback=True)
    TWEEDE_HANDS = parser.getboolean('TenantConfig', 'enable_tweedehands', fallback=True)
    DBA = parser.getboolean('TenantConfig', 'enable_dba', fallback=False)

    MARKTPLAATS_URL = parser.get('TenantConfig', 'url_marktplaats', fallback="http://marktplaats.nl/{id}")
    KIJIJI_URL = parser.get('TenantConfig', 'url_kijiji', fallback="https://www.kijiji.ca/v-view-details.html?adId={id}")
    TWEEDE_HANDS_URL = parser.get('TenantConfig', 'url_tweedehands', fallback="https://www.2dehands.be/{id}.html")
    DBA_URL = parser.get('TenantConfig', 'url_dba', fallback="https://www.dba.dk/id-{id}")

    ####################################
    # System config
    ####################################
    ORIGINAL_FILE_SUFFIX = parser.get('SystemConfig', 'original_file_suffix', fallback='original')
    PARSED_FILE_SUFFIX = parser.get('SystemConfig', 'parsed_file_suffix', fallback='dump')
    SELECTABLE_PAGE_AMOUNTS = ast.literal_eval(parser.get('SystemConfig', 'selectable_page_amounts', fallback="[10, 50, 100]"))
    MAX_WORKERS = parser.getint('SystemConfig', 'max_workers', fallback=10)
    SAVE_INTERVAL = parser.getint('SystemConfig', 'save_interval', fallback=20)

    ####################################
    # State config
    ####################################
    search_string = parser.get('UserConfig', 'search_string', fallback="")
    filter_string = parser.get('UserConfig', 'filter_string', fallback="")

    selected_item = parser.get('UserConfig', 'selected_item', fallback="0")
    tenant = parser.get('UserConfig', 'tenant', fallback="2dehands")

    max_per_page = parser.getint('UserConfig', 'max_per_page', fallback=50)
    offline_mode = parser.getboolean('UserConfig', 'offline_mode', fallback=False)

    insert_preference = parser.get('UserConfig', 'insert_preference', fallback="CSV")
