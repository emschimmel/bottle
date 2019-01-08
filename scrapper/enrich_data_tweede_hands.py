import os
from json import loads

from model.ad_object import AdObject
from bs4 import BeautifulSoup
import requests
import urllib.request as urllib
import certifi
import re


class EnrichDataTweedeHands():

    @classmethod
    def start_for_id(self, ad_id, tenant):
        url = "https://www.2dehands.be/{id}.html".format(id=ad_id)
        print("start for id {id} on url {url}".format(id=ad_id, url=url))

        response = requests.get(url)
        html = BeautifulSoup(response.content, "xml")
        object = AdObject()
        object.id = ad_id
        object.url = url

        try:
            error = html.find('div', {"class": "error-404-background"})
            if error:
                print("Page returns a 404")
                object.error = True
        except Exception:
            print("Page is availale")

        if not object.error:
            object.price, error = self.get_price(html=html)
            object.title, error = self.get_title(html=html)
            object.img_url, error = self.get_img(html, tenant, ad_id, object.title)
        object.loaded = True
        return object

    @staticmethod
    def get_price(html):
        try:
            json_text = html.find("script", text=re.compile("data-datalayer-content-json"))[
                'data-datalayer-content-json']
            json_data = loads(json_text)
            price = json_data[0]['a']['prc']['amt']
            if not price:
                price = json_data[0]['a']['prc']['t']
            if not price:
                price = html.find('span', itemprop="price").getText().strip()
            return price, False
        except Exception as e:
            print("price not found")
            print(e)
            return "", True

    @staticmethod
    def get_title(html):
        try:
            title = html.find('meta', property="og:title")
            title = title["content"] if title else html.find('h1', itemprop="name").getText().strip()
            return title, False
        except Exception as e:
            print("title not found")
            print(e)
            return "", True

    @staticmethod
    def get_img(html, tenant, ad_id, title):
        img_url = "img/{tenant}/{id}.jpg".format(tenant=tenant, id=ad_id)
        if not os.path.exists(img_url):
            try:
                img_from_site = html.find('meta', property="og:image")
                img_from_site = img_from_site["content"] if img_from_site else html.find('img', alt=title)['src']
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
                return "", True
        return "/" + img_url, False

# EnrichDataTweedeHands().start_for_id(ad_id="478237791", tenant="2dehands")
# EnrichDataTweedeHands().start_for_id(ad_id="471726179", tenant="2dehands")