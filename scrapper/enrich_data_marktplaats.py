import os
from model.ad_object import AdObject
from bs4 import BeautifulSoup
import requests
import urllib.request as urllib
import certifi


class EnrichDataMarktplaats():

    @staticmethod
    def start_for_id(ad_id, tenant):
        url = "http://marktplaats.nl/adId={id}".format(id=ad_id)
        print("start for id {id} on url {url}".format(id=ad_id, url=url))

        response = requests.get(url)
        html = BeautifulSoup(response.content, "xml")
        object = AdObject()

        return object