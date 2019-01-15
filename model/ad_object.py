

class AdObject(object):

    id = 0
    score = 0
    rank = 0

    url = ""
    img_url = ""
    title = ""
    price = ""

    loaded = False
    error = False
    expired = False

    l1 = ""
    l2 = ""

    def set_initial_data(self, id, rank, score):
        self.id = id
        self.rank = rank
        self.score = score

    def set_enriched_data(self, url, img_url, title, price, loaded, error, expired, l1, l2):
        self.url = url
        self.img_url = img_url
        self.title = title
        self.price = price
        self.loaded = loaded
        self.error = error
        self.expired = expired
        self.l1 = l1
        self.l2 = l2

    def __repr__(self):
        return "({id}, {url}, {title})".format(id=self.id, url=self.url, title=self.title)

    def __str__(self):
        return "(id={id}, url={url}, title={title}, price={price}, img_url={img_url}, loaded={loaded}, error={error})".format(id=self.id, url=self.url, title=self.title, price=self.price, img_url=self.img_url, loaded=self.loaded, error=self.error)

