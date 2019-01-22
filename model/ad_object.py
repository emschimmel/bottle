from datetime import datetime

class AdObject(object):

    id = ""
    score = 0
    rank = 1

    url = ""
    img_url = "/static/img/no_data.png"
    title = ""
    price = ""
    location = ""

    loaded = False
    error = False
    expired = False

    categories = []

    enriched_at = datetime.now()

    def set_initial_data(self, id, rank, score):
        self.id = id
        self.rank = rank
        self.score = score

    def set_enriched_data(self, url, img_url, title, price, loaded, error, expired, categories, enriched_at, location):
        self.url = url
        self.img_url = img_url
        self.title = title
        self.price = price
        self.loaded = loaded
        self.error = error
        self.expired = expired
        self.categories = categories
        self.enriched_at = enriched_at
        self.location = location

    def get_enriched_moment(self):
        return self.enriched_at.strftime('%H:%M:%S %d-%m-%Y')

    def set_enriched_moment(self):
        self.enriched_at = datetime.now()

    def validate_for_csv(self):
        return self.rank and self.score and self.score

    def __repr__(self):
        return "({id}, {url}, {title})".format(id=self.id, url=self.url, title=self.title)

    def __str__(self):
        return "(id={id}, url={url}, title={title}, price={price}, img_url={img_url}, loaded={loaded}, error={error})".format(id=self.id, url=self.url, title=self.title, price=self.price, img_url=self.img_url, loaded=self.loaded, error=self.error)

