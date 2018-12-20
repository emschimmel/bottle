import csv

from model.ad_object import AdObject, RecommandationObject

class ParseCsv():
    def parse(self, file_name):
        output = dict()

        with open(file_name, newline='') as file:
            reader = csv.DictReader(file)
            count = 0
            for line in reader:

                child = AdObject()
                child.set_initial_data(line['recommended_ad_id'], line['rank'], line['score'])

                if not line['ad_id'] in output.keys():
                    parent = RecommandationObject()
                    parent.set_parent_data(line['ad_id'])
                    output[line['ad_id']] = parent

                output[line['ad_id']] = output[line['ad_id']].add_recommondation(child)

                count = count+1
                if count > 1000:
                    break
        return output