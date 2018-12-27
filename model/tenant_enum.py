
from enum import Enum

class TenantEnum(Enum):
    TWEEDE_HANDS = ("2dehands", "https://www.2dehands.be/{id}.html")
    MARKTPLAATS = ("Marktplaats", "http://marktplaats.nl/adId={id}")
    KIJIJI = ("Kijiji", "https://www.kijiji.ca/v-view-details.html?adId={id}")

    def __init__(self, tenant, url):
        self.tenant = tenant
        self.url = url

    def getUrl(self, id):
        return self.url.format(id=id)

class TenantConfig():

    def getTenantList(self):
        return [e.tenant for e in TenantEnum]

    def getTenantUrl(self, tenant, id):
        return [e.getUrl(id) for e in TenantEnum if e.tenant is tenant][0]




