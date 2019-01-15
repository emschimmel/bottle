import configparser

from model.config_object import ConfigObject
from model.tenant_enum import TenantConfig


class FileName(ConfigObject):

    @staticmethod
    def config_path():
        return ConfigObject.CONFIG_PATH

    @staticmethod
    def dump_file_name():
        return "{path}/{suffix}-{tenant}.json".format(path=ConfigObject.CONFIG_PATH,
                                                      suffix=ConfigObject.PARSED_FILE_SUFFIX,
                                                      tenant=ConfigObject.tenant)

    @staticmethod
    def original_file_name():
        return "{path}/{suffix}.csv".format(path=ConfigObject.CONFIG_PATH,
                                            suffix=ConfigObject.ORIGINAL_FILE_SUFFIX)


class State(ConfigObject):

    @staticmethod
    def supported_tenants():
        return TenantConfig().getTenantList()

    @staticmethod
    def saved_config():
        return ConfigObject

    @staticmethod
    def set_variables(tenant, search_string, selected_item, max_per_page, offline_mode):
        ConfigObject.tenant = tenant
        ConfigObject.search_string = search_string
        ConfigObject.selected_item = selected_item
        ConfigObject.max_per_page = max_per_page
        ConfigObject.offline_mode = offline_mode

    @staticmethod
    def store_state():
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