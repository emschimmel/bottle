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
                object.location, error = self.__get_location(html=html, id=ad_id)
                object.extra_data, error = self.__get_as_much_attributes_possible(html=html, id=ad_id)
                object.extra_images, error = self.__get_other_images(html=html, tenant=tenant, id=ad_id)
            else:
                object.expired = True

        object.loaded = True
        return object

    @staticmethod
    def __get_other_images(html, tenant, id):
        images = list()
        try:
            caroussel_small = html.find('div', id="vip-carousel").get("data-images-s")
            caroussel_small = caroussel_small.replace('//', '').split('&')
            caroussel_xl = html.find('div', id="vip-carousel").get("data-images-xl")
            caroussel_xl = caroussel_xl.replace('//', '').split('&')
            for index, item in enumerate(caroussel_small):
                img_url = "img/{tenant}/{id}_{index}.jpg".format(tenant=tenant, id=id, index=index)
                img_from_site = "http://{item}".format(item=item)
                href_from_site = caroussel_xl[index]
                img_path = "img/{tenant}".format(tenant=tenant)
                if not os.path.exists(img_path):
                    os.makedirs(img_path)
                with urllib.urlopen(img_from_site, cafile=certifi.where()) as response, open(img_url, 'wb') as out_file:
                    data = response.read()  # a `bytes` object
                    out_file.write(data)
                images.append(["/" + img_url, href_from_site])
            return images, False
        except Exception as e:
            print("extra images not found for {id}".format(id=id))
            print(e)
            return images, True

    @staticmethod
    def __get_as_much_attributes_possible(html, id):
        attributes = list()
        try:
            json_text = html.find("script", text=re.compile("dataLayer = (.*?)")).getText()
            json_text = json_text.strip().replace('dataLayer = [', '').replace('];', '')

            json_data = loads(json_text)
            for key in json_data['a']['attr'].keys():
                value = json_data['a']['attr'][key]
                value = str(value).replace('[', '').replace(']', '').replace("'", '')
                attributes.append([key, value])
            return attributes, False
        except Exception as e:
            print("extra attributes not found for {id}".format(id=id))
            print(e)
            return attributes, True

    @staticmethod
    def __get_location(html, id):
        try:
            location = html.find('meta', {"name":"twitter:label2"}).get("content")
            return location, False
        except Exception as e:
            print("location not found for {id}".format(id=id))
            print(e)
            return "", True

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
            price = html.find('span', {'class': 'price '})
            if price is not None:
                price = price.getText()
            else:
                price = html.find('meta', {'name':'twitter:data1'}).get("content")
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
