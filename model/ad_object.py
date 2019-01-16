

class AdObject(object):

    id = ""
    score = 0
    rank = 1

    url = ""
    img_url = "/static/img/no_data.png"
    title = ""
    price = ""

    loaded = False
    error = False
    expired = False

    categories = []

    def set_initial_data(self, id, rank, score):
        self.id = id
        self.rank = rank
        self.score = score

    def set_enriched_data(self, url, img_url, title, price, loaded, error, expired, categories):
        self.url = url
        self.img_url = img_url
        self.title = title
        self.price = price
        self.loaded = loaded
        self.error = error
        self.expired = expired
        self.categories = categories

    def validate_for_csv(self):
        return self.rank and self.score and self.score

    def __repr__(self):
        return "({id}, {url}, {title})".format(id=self.id, url=self.url, title=self.title)

    def __str__(self):
        return "(id={id}, url={url}, title={title}, price={price}, img_url={img_url}, loaded={loaded}, error={error})".format(id=self.id, url=self.url, title=self.title, price=self.price, img_url=self.img_url, loaded=self.loaded, error=self.error)

