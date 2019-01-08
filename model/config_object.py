from model.tenant_enum import TenantConfig


class ConfigObject(object):


    SUPPORTED_TENANTS = TenantConfig().getTenantList()
    CONFIG_PATH = "config"
    ORIGINAL_FILE_SUFFIX = "original"
    PARSED_FILE_SUFFIX = "dump"
    STATE_FILE_SUFFIX = "state"
    SELECTABLE_PAGE_AMOUNTS = [10, 50, 100]

    ####################################
    # State config
    ####################################
    overview_data = dict()
    search_string = ""
    selected_item = 0
    tenant = SUPPORTED_TENANTS[0] # "2dehands"

    current_page = 0
    max_per_page = 50


class FileName():

    @staticmethod
    def config_path():
        return ConfigObject.CONFIG_PATH

    @staticmethod
    def dump_file_name():
        return "{path}/{suffix}.json".format(path=ConfigObject.CONFIG_PATH, suffix=ConfigObject.PARSED_FILE_SUFFIX)

    @staticmethod
    def state_file_name():
        return "{path}/{suffix}.json".format(path=ConfigObject.CONFIG_PATH, suffix=ConfigObject.STATE_FILE_SUFFIX)

    @staticmethod
    def original_file_name():
        return "{path}/{suffix}.csv".format(path=ConfigObject.CONFIG_PATH, suffix=ConfigObject.ORIGINAL_FILE_SUFFIX)


class SystemConfig():

    @staticmethod
    def supported_tenants():
        return ConfigObject.SUPPORTED_TENANTS

    @ staticmethod
    def selectable_amounts():
        return ConfigObject.SELECTABLE_PAGE_AMOUNTS


class State():

    @staticmethod
    def saved_config():
        return ConfigObject

    # load state

    # store state