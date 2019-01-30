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
    def start_for_id(self, ad_id, url, tenant):
        url = url.format(id=ad_id)
        # print("start for id {id} on url {url}".format(id=ad_id, url=url))

        response = requests.get(url)
        html = BeautifulSoup(response.content, "lxml")
        # print(html)
        object = AdObject()
        object.id = ad_id
        object.url = url
        object.set_enriched_moment()

        try:
            error = html.find('div', {"class": "error-404-background"})
            if error:
                print("Page returns a 404 for {url}".format(url=url))
                object.error = True
        except Exception:
            pass

        if not object.error:
            object.title, error = self.__get_title(html=html, id=ad_id)
            object.categories, error = self.__get_categories(html=html, id=ad_id)
            expired = None
            try:
                expired = html.find('div', {"data-component": "expired-view-item"})
            except Exception:
                print("error determining if the add is expired for {url}".format(url=url))
            if expired is None:
                object.price, error = self.__get_price(html=html, id=ad_id)
                object.img_url, error = self.__get_img(html, tenant, ad_id, object.title)
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
            section = html.find("div", {"class": "image-carousel-thumbs"})
            images_links = section.findChildren("img" , recursive=True)

            for index, image_tag in enumerate(images_links):
                img_from_site = image_tag.get('src')
                href_from_site = image_tag.get('data-enlarged-image-src').replace('[breakpointPlaceholder]', 'normal')

                img_url = "img/{tenant}/{id}_{index}.jpg".format(tenant=tenant, id=id, index=index)
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
            section = html.find("dl", {"class": "item-details-list"})
            keys = section.findChildren("dt" , recursive=True)
            values = section.findChildren("dd" , recursive=True)
            for index, key in enumerate(keys):
                value = values[index].getText().replace("\n            ", "")
                attributes.append([key.getText(), value])
            return attributes, False
        except Exception as e:
            print("extra attributes not found for {id}".format(id=id))
            print(e)
            return attributes, True

    @staticmethod
    def __get_location(html, id):
        try:
            location = html.find('span', {"class":"data-text ui-button-clean ui-link-info"}).getText()
            return location, False
        except Exception as e:
            print("location not found for {id}".format(id=id))
            print(e)
            return "", True

    @staticmethod
    def __get_categories(html, id):
        categories = list()
        try:
            json_text = html.find("script", text=re.compile("data-datalayer-content-json"))[
                'data-datalayer-content-json']
            json_data = loads(json_text)
            for key in sorted(json_data[0]['c'].keys()):
                if key is not 'c':
                    categories.append(json_data[0]['c'][key]['id'])
            return categories, False
        except Exception as e:
            print("categories not found for {id}".format(id=id))
            print(e)
            return categories, True

    @staticmethod
    def __get_price(html, id):
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
            print("price not found for {id}".format(id=id))
            print(e)
            return "", True

    @staticmethod
    def __get_title(html, id):
        try:
            title = html.find('meta', property="og:title")
            title = title["content"] if title else html.find('h1', itemprop="name").getText().strip()
            return title, False
        except Exception as e:
            print("title not found for {id}".format(id=id))
            print(e)
            return "", True

    @staticmethod
    def __get_img(html, tenant, ad_id, title):
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
                else:
                    return "/static/img/no_data.png", True
            except Exception as e:
                print("image not found for {id}".format(id=ad_id))
                print(e)
                return "/static/img/no_data.png", True
        return "/" + img_url, False

# EnrichDataTweedeHands().start_for_id(ad_id="4816171", url="https://www.2dehands.be/{id}.html", tenant="2dehands")
# EnrichDataTweedeHands().start_for_id(ad_id="478237791", url="https://www.2dehands.be/{id}.html", tenant="2dehands")
# EnrichDataTweedeHands().start_for_id(ad_id="471726179", url="https://www.2dehands.be/{id}.html", tenant="2dehands")
# EnrichDataTweedeHands().start_for_id(ad_id="482616171", url="https://www.2dehands.be/{id}.html", tenant="2dehands") # expired
# EnrichDataTweedeHands().start_for_id(ad_id="456307202", url="https://www.2dehands.be/{id}.html", tenant="2dehands")
# EnrichDataTweedeHands().start_for_id(ad_id="476958230", url="https://www.2dehands.be/{id}.html", tenant="2dehands") # no image
