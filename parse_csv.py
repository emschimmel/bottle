import csv

from model.ad_object import AdObject

class ParseCsv():
    def parse(self, tenant, file_name):
        output = dict()

        with open(file_name, "rb") as file:
            reader = csv.reader(file, delimiter="\t")
            for i, line in enumerate(reader):
                if i>0:
                    csv_row = line.split()
                    parent = AdObject().set_parent_data(csv_row[0])
                    child = AdObject().set_initial_data(csv_row[1], csv_row[2], csv_row[3])

                    if parent in output:
                        output[parent] += child
                    else:
                        output = dict(output, **dict({parent, [child]}))
                else:
                    print(line)
        return output