import ast
from datetime import datetime

from dateutil import parser


class AdObject(object):

    id = ""
    score = 0
    rank = 1

    url = ""
    img_url = "/static/img/no_data.png"
    title = ""
    price = ""
    location = ""

    categories = []

    loaded = False
    error = False
    expired = False

    enriched_at = datetime.now()

    extra_images = []
    extra_data = []

    def set_initial_data(self, id, rank, score):
        self.id = id
        self.rank = rank
        self.score = score

    # def set_enriched_data(self, url, img_url, title, price, loaded, error, expired, location):
    def set_enriched_data(self, url, img_url, title, price, loaded, error, expired, categories, enriched_at, location, extra_images=list(), extra_data=list()):
        self.url = url
        self.img_url = img_url
        self.title = title
        self.price = price
        self.loaded = loaded
        self.error = error
        self.expired = expired
        self.categories = categories
        if isinstance(categories, str):
            self.categories = ast.literal_eval(categories)
        self.enriched_at = enriched_at
        if isinstance(enriched_at, str):
            self.enriched_at = parser.parse(enriched_at)
        self.location = location
        self.extra_images = extra_images
        self.extra_data = extra_data

    def get_enriched_moment(self):
        return self.enriched_at.strftime('%H:%M:%S %d-%m-%Y')
        # return self.enriched_at

    def set_enriched_moment(self):
        self.enriched_at = datetime.now()

    def validate_for_csv(self):
        return self.rank and self.score and self.score

    def enriched_panda_row(self):
        # return [self.id, self.url, self.img_url, self.title, self.price, self.location, self.loaded, self.error, self.expired]
        return [self.id, self.url, self.img_url, self.title, self.price, self.location, self.categories, self.loaded, self.error, self.expired, self.enriched_at]

    def __repr__(self):
        return "({id}, {url}, {title})".format(id=self.id, url=self.url, title=self.title)

    def __str__(self):
        return "(id={id}, url={url}, title={title}, price={price}, img_url={img_url}, loaded={loaded}, error={error})".format(id=self.id, url=self.url, title=self.title, price=self.price, img_url=self.img_url, loaded=self.loaded, error=self.error)

