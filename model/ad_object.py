

class AdObject(object):

    id = ""
    score = 0
    other_field = 0

    url = ""
    img_url = ""
    title = ""
    description = ""
    price = ""

    def set_parent_data(self, id):
        self.id = id

    def set_initial_data(self, id, other_field, score):
        self.id = id
        self.other_field = other_field
        self.score = score