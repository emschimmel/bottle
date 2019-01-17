import os
from model.ad_object import AdObject
from bs4 import BeautifulSoup
import requests
import urllib.request as urllib
import certifi


class EnrichDataKijiji():

    @classmethod
    def start_for_id(self, ad_id, url, tenant):
        url = url.format(id=ad_id)
        print("start for id {id} on url {url}".format(id=ad_id, url=url))

        response = requests.get(url)
        html = BeautifulSoup(response.content, "lxml")
        object = AdObject()
        object.id = ad_id
        object.url = url

        try:
            error = html.find('body', {'id': 'Page404'})
            if error:
                print("Page returns a 404 for {url}".format(url=url))
                object.error = True
        except Exception:
            print("Page is availale")

        if not object.error:
            object.price, error = self.__get_price(html=html, id=ad_id)
            object.title, error = self.__get_title(html=html, id=ad_id)
            object.img_url, error = self.__get_img(html, tenant, ad_id)
        object.loaded = True
        return object

    @staticmethod
    def __get_price(html, id):
        try:
            price = html.find('span', itemProp="price").getText()
            return price, False
        except Exception as e:
            print("price not found for {id}".format(id=id))
            print(e)
            return "", True

    @staticmethod
    def __get_title(html, id):
        try:
            title = html.find('h1', {'class':"title-2323565163"}).getText()
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
            print(img_from_site)
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

# EnrichDataKijiji().start_for_id(ad_id="1369844148", url="https://www.kijiji.ca/v-view-details.html?adId={id}", tenant="Kijiji")
# EnrichDataKijiji().start_for_id(ad_id="1408605635", url="https://www.kijiji.ca/v-view-details.html?adId={id}", tenant="Kijiji")
# EnrichDataKijiji().start_for_id(ad_id="1406837982", url="https://www.kijiji.ca/v-view-details.html?adId={id}", tenant="Kijiji")
