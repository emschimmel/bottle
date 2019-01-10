import os
from model.ad_object import AdObject
from bs4 import BeautifulSoup
import requests
import urllib.request as urllib
import certifi


class EnrichDataMarktplaats():

    @classmethod
    def start_for_id(self, ad_id, tenant):
        url = "http://marktplaats.nl/{id}".format(id=ad_id)
        print("start for id {id} on url {url}".format(id=ad_id, url=url))

        response = requests.get(url)
        html = BeautifulSoup(response.content, "xml")
        print(html)
        object = AdObject()
        object.id = ad_id
        object.url = url

        try:
            error = html.find('body', {'data-ga-page-view-url': '/404'})
            if error:
                print("Page returns a 404")
                object.error = True
        except Exception:
            print("Page is availale")

        if not object.error:
            object.price, error = self.__get_price(html=html)
            object.title, error = self.__get_title(html=html)
            object.img_url, error = self.__get_img(html, tenant, ad_id)
        object.loaded = True
        return object

    @staticmethod
    def __get_price(html):
        try:
            price = html.find('meta', property="twitter:data1")
            return price, False
        except:
            return "", True

    @staticmethod
    def __get_title(html):
        try:
            title = html.find('meta', property="twitter:title")
            return title, False
        except:
            return "", True

    @staticmethod
    def __get_img(html, tenant, id):
        img_url = "img/{tenant}/{id}.jpg".format(tenant=tenant, id=id)
        try:
            img_from_site = html.find('meta', property="twitter:image")
            if not img_from_site.endswith('.svg'):
                img_path = "img/{tenant}".format(tenant=tenant)
                if not os.path.exists(img_path):
                    os.makedirs(img_path)
                with urllib.urlopen(img_from_site, cafile=certifi.where()) as response, open(img_url, 'wb') as out_file:
                    data = response.read()  # a `bytes` object
                    out_file.write(data)
        except Exception as e:
            print("image not found")
            print(e)
            return "static/img/no_data.png", True
        return "/" + img_url, False



# EnrichDataMarktplaats().start_for_id(ad_id="a1262510063", tenant="marktplaats")
# EnrichDataMarktplaats().start_for_id(ad_id="m1362515546", tenant="marktplaats")
# EnrichDataMarktplaats().start_for_id(ad_id="m1399515546", tenant="marktplaats")