import os
import re
from json import loads

from model.ad_object import AdObject
from bs4 import BeautifulSoup
import requests
import urllib.request as urllib
import certifi

# url = https://www.bva-auctions.com/nl/auction/lot/39555/12487239
class EnrichDataBVA():

    @classmethod
    def start_for_id(self, ad_id, url, tenant):
        # if '-' in url:
        #     url = url.format(id=ad_id.replace('-', '/'))
        # else:
        #     url = "https://www.bva-auctions.com/nl/auction/39555/"+ad_id
        response = requests.get(url)
        html = BeautifulSoup(response.content, "html.parser") # slowest parser
        # print(html)

        object = AdObject()
        object.id = ad_id
        object.url = url

        object.error = False
        object.title, error = self.__get_title(html, ad_id)
        object.img_url, error = self.__get_img(html, tenant, ad_id)
        # object.extra_images, error = self.__get_other_images(html=html, tenant=tenant, id=ad_id)
        object.loaded = True
        return object

    @staticmethod
    def __get_other_images(html, tenant, id):
        images = list()
        try:
            caroussel_small = html.find('div', {"class": "lot-thumbnails lot-thumbnails-contained"})
            print(caroussel_small)

            return images, False
        except Exception as e:
            print("extra images not found for {id}".format(id=id))
            print(e)
            return images, True

    @staticmethod
    def __get_title(html, id):
        try:
            title = html.find('meta', property="og:title").get("content")
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

# EnrichDataBVA().start_for_id(ad_id="39555/12487239", url="https://www.bva-auctions.com/nl/auction/lot/{id}", tenant="Bva")
