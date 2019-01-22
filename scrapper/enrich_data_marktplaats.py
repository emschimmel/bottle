import os
import re
from json import loads

from model.ad_object import AdObject
from bs4 import BeautifulSoup
import requests
import urllib.request as urllib
import certifi


class EnrichDataMarktplaats():

    @classmethod
    def start_for_id(self, ad_id, url, tenant):
        url = url.format(id=ad_id)
        print("start for id {id} on url {url}".format(id=ad_id, url=url))

        response = requests.get(url)
        html = BeautifulSoup(response.content, "lxml")
        # print(html)
        object = AdObject()
        object.id = ad_id
        object.url = url

        try:
            error = html.find('body', {'data-ga-page-view-url': '/404'})
            if error:
                print("Page returns a 404 for {url}".format(url=url))
                object.error = True
        except Exception:
            pass
        if not object.error:
            expired = None
            try:
                expired = html.find('div', {"class": "expired-state-label"})
            except Exception:
                print("error determining if the add is expired for {url}".format(url=url))
            object.title, error = self.__get_title(html=html, id=ad_id)
            object.categories, error = self.__get_categories(html=html, id=ad_id)
            if expired is None:
                object.price, error = self.__get_price(html=html, id=ad_id)
                object.img_url, error = self.__get_img(html, tenant, ad_id)
            else:
                object.expired = True
        object.loaded = True
        print(object)
        print(object.categories)
        return object

    @staticmethod
    def __get_categories(html, id):
        categories = list()
        try:

            json_text = html.find("script", text=re.compile("dataLayer = (.*?)")).getText()
            json_text = json_text.strip().replace('dataLayer = [', '').replace('];', '')

            json_data = loads(json_text)
            for key in sorted(json_data['c'].keys()):
                if key is not 'c':
                    categories.append(json_data['c'][key]['n'])
            return categories, False
        except Exception as e:
            print("categories not found for {id}".format(id=id))
            print(e)
            return categories, True

    @staticmethod
    def __get_price(html, id):
        try:
            price = html.find('span', {'class': 'price '}).getText()
            # price = html.find('meta', name="twitter:data1").get("content")
            return price, False
        except Exception as e:
            print("price not found for {id}".format(id=id))
            print(e)
            return "", True

    @staticmethod
    def __get_title(html, id):
        try:
            title = html.find('h1', {'class':'title', 'id':'title'})
            if title is not None:
                title = title.getText()
            else:
                title = html.find('span', {'class':'mp-listing-title'}).getText()
            print(title)
            # title = html.find('meta', name="twitter:title").get("content")
            return title, False
        except Exception as e:
            print("title not found for {id}".format(id=id))
            print(e)
            return "", True

    @staticmethod
    def __get_img(html, tenant, id):
        img_url = "img/{tenant}/{id}.jpg".format(tenant=tenant, id=id)
        try:
            img_from_site = html.find('meta', property="og:image").get("content")
            if not img_from_site.endswith('.svg'):
                img_path = "img/{tenant}".format(tenant=tenant)
                if not os.path.exists(img_path):
                    os.makedirs(img_path)
                with urllib.urlopen(img_from_site, cafile=certifi.where()) as response, open(img_url, 'wb') as out_file:
                    data = response.read()  # a `bytes` object
                    out_file.write(data)
        except Exception as e:
            print("image not found for {id}".format(id=id))
            print(e)
            return "static/img/no_data.png", True
        return "/" + img_url, False



# EnrichDataMarktplaats().start_for_id(ad_id="a1262510063", url="http://marktplaats.nl/{id}", tenant="Marktplaats")
# EnrichDataMarktplaats().start_for_id(ad_id="m1362515546", url="http://marktplaats.nl/{id}", tenant="Marktplaats")
# EnrichDataMarktplaats().start_for_id(ad_id="m1399515546", url="http://marktplaats.nl/{id}", tenant="Marktplaats") # 404
# EnrichDataMarktplaats().start_for_id(ad_id="m1351796175", url="http://marktplaats.nl/{id}", tenant="Marktplaats") # expired
