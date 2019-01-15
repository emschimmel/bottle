import requests
from bs4 import BeautifulSoup

from model.ad_object import AdObject


class EnrichDataDBA():

    @classmethod
    def start_for_id(self, ad_id, url, tenant):
        # there is no current way to get the right id's to use

        url = url.format(id=ad_id)
        response = requests.get(url)
        html = BeautifulSoup(response.content, "html.parser") # slowest parser
        print(html)

        object = AdObject()
        object.id = ad_id
        object.url = url

        object.error = True
        object.loaded = True
        return object

# EnrichDataDBA().start_for_id(ad_id="a1262510063", url="https://www.dba.dk/id-{id}", tenant="Dba")
