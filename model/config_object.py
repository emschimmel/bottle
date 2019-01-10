from model.tenant_enum import TenantConfig
import configparser
import ast


class ConfigObject(object):
    config_file = "config/state_config.ini"
    parser = configparser.RawConfigParser()
    parser.read(config_file)

    CONFIG_PATH = "config"
    ORIGINAL_FILE_SUFFIX = parser.get('SystemConfig', 'original_file_suffix', fallback='original')
    PARSED_FILE_SUFFIX = parser.get('SystemConfig', 'parsed_file_suffix', fallback='dump')
    SELECTABLE_PAGE_AMOUNTS = ast.literal_eval(parser.get('SystemConfig', 'selectable_page_amounts', fallback="[10, 50, 100]"))
    MAX_WORKERS = parser.getint('SystemConfig', 'max_workers', fallback=10)

    ####################################
    # State config
    ####################################
    search_string = parser.get('UserConfig', 'search_string', fallback="")
    selected_item = parser.get('UserConfig', 'selected_item', fallback="0")
    tenant = parser.get('UserConfig', 'tenant', fallback=TenantConfig().getTenantList()[0]) # "2dehands"

    max_per_page = parser.getint('UserConfig', 'max_per_page', fallback=50)
    offline_mode = parser.getboolean('UserConfig', 'offline_mode', fallback=False)


class FileName(ConfigObject):

    @staticmethod
    def config_path():
        return ConfigObject.CONFIG_PATH

    @staticmethod
    def dump_file_name():
        return "{path}/{suffix}-{tenant}.json".format(path=ConfigObject.CONFIG_PATH, suffix=ConfigObject.PARSED_FILE_SUFFIX, tenant=ConfigObject.tenant)

    @staticmethod
    def original_file_name():
        return "{path}/{suffix}.csv".format(path=ConfigObject.CONFIG_PATH, suffix=ConfigObject.ORIGINAL_FILE_SUFFIX)


class State(ConfigObject):

    @staticmethod
    def supported_tenants():
        return TenantConfig().getTenantList()

    @staticmethod
    def saved_config():
        return ConfigObject

    def set_variables(self, tenant, search_string, selected_item, max_per_page, offline_mode):
        ConfigObject.tenant = tenant
        ConfigObject.search_string = search_string
        ConfigObject.selected_item = selected_item
        ConfigObject.max_per_page = max_per_page
        ConfigObject.offline_mode = offline_mode

    # store state
    def store_state(self):
        parser = configparser.RawConfigParser()
        parser.add_section('UserConfig')
        parser.set('UserConfig', 'tenant', ConfigObject.tenant)
        parser.set('UserConfig', 'search_string', ConfigObject.search_string)
        parser.set('UserConfig', 'selected_item', ConfigObject.selected_item)
        parser.set('UserConfig', 'max_per_page', ConfigObject.max_per_page)
        parser.set('UserConfig', 'offline_mode', ConfigObject.offline_mode)
        parser.add_section('SystemConfig')
        parser.set('SystemConfig', 'original_file_suffix', ConfigObject.ORIGINAL_FILE_SUFFIX)
        parser.set('SystemConfig', 'parsed_file_suffix', ConfigObject.PARSED_FILE_SUFFIX)
        parser.set('SystemConfig', 'selectable_page_amounts', ConfigObject.SELECTABLE_PAGE_AMOUNTS)
        parser.set('SystemConfig', 'max_workers', ConfigObject.MAX_WORKERS)

        with open(ConfigObject.config_file, 'w') as file:
            # json.dump(self.config, file)
            parser.write(file)
