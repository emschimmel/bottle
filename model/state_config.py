import configparser

from model.config_object import ConfigObject
from model.tenant_enum import TenantConfig


class FileName(ConfigObject):

    @staticmethod
    def config_path():
        return ConfigObject.CONFIG_PATH

    @staticmethod
    def dump_file_name():
        return "{path}/{suffix}-{tenant}.csv".format(path=ConfigObject.CONFIG_PATH,
                                                      suffix=ConfigObject.PARSED_FILE_SUFFIX,
                                                      tenant=ConfigObject.tenant)

    @staticmethod
    def original_file_name():
        return "{path}/{suffix}.csv".format(path=ConfigObject.CONFIG_PATH,
                                            suffix=ConfigObject.ORIGINAL_FILE_SUFFIX)

    @staticmethod
    def original_data_list_file_name():
        return "{path}/{suffix}.csv".format(path=ConfigObject.CONFIG_PATH,
                                            suffix=ConfigObject.ORIGINAL_AD_LIST_FILE_SUFFIX)


class State(ConfigObject):



    @staticmethod
    def supported_tenants():
        return TenantConfig().getTenantList()

    @staticmethod
    def saved_config():
        return ConfigObject

    @staticmethod
    def set_variables(tenant, system_mode, search_string, selected_item, max_per_page, offline_mode, insert_preference, default_limit):
        ConfigObject.tenant = tenant
        ConfigObject.system_mode = system_mode
        ConfigObject.search_string = search_string
        ConfigObject.selected_item = selected_item
        ConfigObject.max_per_page = max_per_page
        ConfigObject.offline_mode = offline_mode
        ConfigObject.insert_preference = insert_preference
        ConfigObject.default_limit = default_limit

    @staticmethod
    def store_state():
        parser = configparser.RawConfigParser()
        parser.add_section('ElasticConfig')
        parser.set('ElasticConfig', 'ip', ConfigObject.ELASTIC_IP)
        parser.set('ElasticConfig', 'port', ConfigObject.ELASTIC_PORT)
        parser.add_section('UserConfig')
        parser.set('UserConfig', 'system_mode', ConfigObject.system_mode)
        parser.set('UserConfig', 'tenant', ConfigObject.tenant)
        parser.set('UserConfig', 'search_string', ConfigObject.search_string)
        parser.set('UserConfig', 'filter_string', ConfigObject.filter_string)
        parser.set('UserConfig', 'selected_item', ConfigObject.selected_item)
        parser.set('UserConfig', 'max_per_page', ConfigObject.max_per_page)
        parser.set('UserConfig', 'offline_mode', ConfigObject.offline_mode)
        parser.set('UserConfig', 'insert_preference', ConfigObject.insert_preference)
        parser.set('UserConfig', 'default_limit', ConfigObject.default_limit)
        parser.add_section('SystemConfig')
        parser.set('SystemConfig', 'original_file_suffix', ConfigObject.ORIGINAL_FILE_SUFFIX)
        parser.set('SystemConfig', 'original_ad_list_file_suffix', ConfigObject.ORIGINAL_AD_LIST_FILE_SUFFIX)
        parser.set('SystemConfig', 'parsed_file_suffix', ConfigObject.PARSED_FILE_SUFFIX)
        parser.set('SystemConfig', 'selectable_page_amounts', ConfigObject.SELECTABLE_PAGE_AMOUNTS)
        parser.set('SystemConfig', 'max_workers', ConfigObject.MAX_WORKERS)
        parser.set('SystemConfig', 'save_interval', ConfigObject.SAVE_INTERVAL)
        parser.add_section('TenantConfig')
        parser.set('TenantConfig', 'enable_dba', ConfigObject.DBA)
        parser.set('TenantConfig', 'enable_tweedehands', ConfigObject.TWEEDE_HANDS)
        parser.set('TenantConfig', 'enable_marktplaats', ConfigObject.MARKTPLAATS)
        parser.set('TenantConfig', 'enable_kijiji', ConfigObject.KIJIJI)
        parser.set('TenantConfig', 'url_dba', ConfigObject.DBA_URL)
        parser.set('TenantConfig', 'url_tweedehands', ConfigObject.TWEEDE_HANDS_URL)
        parser.set('TenantConfig', 'url_marktplaats', ConfigObject.MARKTPLAATS_URL)
        parser.set('TenantConfig', 'url_kijiji', ConfigObject.KIJIJI_URL)

        with open(ConfigObject.config_file, 'w') as file:
            # json.dump(self.config, file)
            parser.write(file)

    @classmethod
    def store_filled_state(self, tenant="", system_mode=False, selected_item="", search_string="", filter_string=""):
        ConfigObject.tenant = tenant
        if system_mode:
            ConfigObject.system_mode = system_mode
        ConfigObject.selected_item = selected_item
        ConfigObject.search_string = search_string
        ConfigObject.filter_string = filter_string
        self.store_state()
