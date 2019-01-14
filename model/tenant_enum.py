from model.config_object import ConfigObject
from scrapper.enrich_data_dba import EnrichDataDBA
from scrapper.enrich_data_tweede_hands import EnrichDataTweedeHands
from scrapper.enrich_data_kijiji import EnrichDataKijiji
from scrapper.enrich_data_marktplaats import EnrichDataMarktplaats

from enum import Enum


class TenantEnum(Enum):
    TWEEDE_HANDS = ("2dehands", EnrichDataTweedeHands)
    MARKTPLAATS = ("Marktplaats", EnrichDataMarktplaats)
    KIJIJI = ("Kijiji", EnrichDataKijiji)
    DBA = ("Dba", EnrichDataDBA)

    def __init__(self, tenant, scrapper):
        self.tenant = tenant
        self.scrapper = scrapper


    def getScrapper(self):
        return self.scrapper

    def startForId(self, ad_id, url):
        return self.scrapper().start_for_id(ad_id=ad_id, url=url, tenant=self.tenant)

    def getName(self):
        return self.tenant


class TenantConfig(ConfigObject):

    def getTenantList(self):
        return [e.tenant for e in TenantEnum if getattr(ConfigObject, e.name)]

    def startForId(self, tenant, id):
        for e in TenantEnum:
            if e.tenant == tenant:
                return e.startForId(ad_id=id, url=getattr(ConfigObject, e.name+"_URL"))
        # return (e.startForId(id) for e in TenantEnum if e.tenant is tenant)




