import os
from json import loads

from model.ad_object import AdObject
from bs4 import BeautifulSoup
import requests
import urllib.request as urllib
import certifi
import re


class EnrichDataTweedeHands():

    @staticmethod
    def start_for_id(ad_id, tenant):
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
                object.loaded = True
                object.error = True
        except Exception:
            print("Page is availale")

        if not object.error:
            try:
                json_text = html.find("script", text=re.compile("data-datalayer-content-json"))['data-datalayer-content-json']
                json_data = loads(json_text)
                price = json_data[0]['a']['prc']['amt']
                if not price:
                    price = html.find('span', itemprop="price").getText().strip()
                object.price = price
                object.loaded = True
            except Exception as e:
                print("price not found")
                print(e)

            title = False
            try:
                title = html.find('meta', property="og:title")
                title = title["content"] if title else html.find('h1', itemprop="name").getText().strip()
                object.title = title
                object.loaded = True
            except Exception as e:
                print("title not found")
                print(e)

            if title:
                imgUrl = "img/{tenant}/{id}.jpg".format(tenant=tenant, id=ad_id)
                if not os.path.exists(imgUrl):
                    try:
                        imgFromSite = html.find('meta', property="og:image")
                        imgFromSite = imgFromSite["content"] if imgFromSite else html.find('img', alt=title)['src']
                        if not imgFromSite.endswith('.svg'):
                            IMG_PATH = "img/{tenant}".format(tenant=tenant)
                            if not os.path.exists(IMG_PATH):
                                os.makedirs(IMG_PATH)
                            with urllib.urlopen(imgFromSite, cafile=certifi.where()) as response, open(imgUrl, 'wb') as out_file:
                                data = response.read()  # a `bytes` object
                                out_file.write(data)
                                object.img_url = "/"+imgUrl
                        object.loaded = True
                    except Exception as e:
                        object.img_url = ""
                        print("image not found")
                        print(e)
                    pass
                else:
                    object.loaded = True
                    object.img_url = "/"+imgUrl
        return object
#
EnrichDataTweedeHands().start_for_id(ad_id="478237791", tenant="2dehands")
# EnrichDataTweedeHands().start_for_id(ad_id="471726179", tenant="2dehands")