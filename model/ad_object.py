

class AdObject(object):

    id = 0
    score = 0
    rank = 0

    url = ""
    img_url = ""
    title = ""
    price = ""

    loaded = False

    def set_initial_data(self, id, rank, score):
        self.id = id
        self.rank = rank
        self.score = score

    def set_enriched_data(self, url, img_url, title, price):
        self.url = url
        self.img_url = img_url
        self.title = title
        self.price = price
        self.loaded = True

    def __repr__(self):
        return "({id}, {url}, {title})".format(id=self.id, url=self.url, title=self.title)

    def __str__(self):
        return "(id={id}, url={url}, title={title}, price={price}, img_url={img_url}, loaded={loaded})".format(id=self.id, url=self.url, title=self.title, price=self.price, img_url=self.img_url, loaded=self.loaded)

