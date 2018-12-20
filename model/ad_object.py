

class AdObject(object):

    id = 0
    score = 0
    rank = 0

    url = ""
    img_url = ""
    title = ""
    price = ""

    def set_initial_data(self, id, rank, score):
        self.id = id
        self.rank = rank
        self.score = score

    # def __repr__(self):
    #     return "({id}, {url}, {title})".format(id=self.id, url=self.url, title=self.title)
    #
    # def __str__(self):
    #     return "({id}, {url}, {title})".format(id=self.id, url=self.url, title=self.title)


class RecommandationObject(object):
    addObject = AdObject()
    recommondations = []

    def set_parent_data(self, id):
        self.addObject.id = id

    def add_recommondation(self, recommandation):
        self.recommondations.append(recommandation)
