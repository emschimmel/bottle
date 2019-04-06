import pandas


class DataPreperation():

    json_file = "sample.json"

    @classmethod
    def read_from_json(self):
        large_data = pandas.read_json(self.json_file)
        outer_hits = large_data['hits'].astype(list)
        inner_hits = outer_hits['hits']
        parsed_data_list = []
        data_for_spark = []
        ### line
        # for item in inner_hits[10]['_source']:
            # print(item)
            # print(type(item))
            # print(inner_hits[10]['_source']['contexts_com_snowplowanalytics_snowplow_web_page_1'])
            # print(inner_hits[10]['_source']['unstruct_event_com_bvaauctions_lot_view_1'])

        ### line end
        for hit in inner_hits:

            rate = 1
            event_name = hit['_source']['event_name']
            user_id = hit['_source']['user_id']
            event_subtype = "no_ref"
            product = ""
            combined_key = ""
            categoryId = ""
            title = ""

            if hit['_source']['refr_urlpath']:
                event_subtype = "ref_with_auction"
                url_string_parts = hit['_source']['refr_urlpath'].split('/')
                product = url_string_parts[-1] if url_string_parts[-1].isdigit() else ""
                auction_id = url_string_parts[-2] if url_string_parts[-2].isdigit() else ""
                combined_key = product
                if auction_id is not "":
                    event_subtype = "ref_with_lot"
                    combined_key = auction_id+"-"+combined_key

            if 'unstruct_event_com_bvaauctions_lot_view_1' in hit['_source']:
                custom_data = hit['_source']['unstruct_event_com_bvaauctions_lot_view_1']
                rate = 1
                if 'lotTitle' in custom_data:
                    title = custom_data['lotTitle']
                if 'categoryId' in custom_data:
                    categoryId = custom_data['categoryId']
                if 'lotId' in custom_data:
                    product = custom_data['lotId']
                if 'favorite' in custom_data:
                    favorite = custom_data['favorite']
                    if favorite:
                        rate = 2
                if 'bidded' in custom_data:
                    bidded = custom_data['bidded']
                    if bidded:
                        rate = 3

            elif 'user_id' in hit['_source']:
                if hit['_source']['user_id'] is not None:
                    user_id = hit['_source']['user_id']
            parsed_data_list.append([user_id, combined_key, rate, event_name, event_subtype, categoryId , title ])
            if user_id and product:
                data_for_spark.append([user_id, product, rate])
            # else:
            #     print(hit)
        pandas.DataFrame(data_for_spark, columns=['user', 'product', 'rank']).to_csv("test_data.csv", index=False)



if __name__ == '__main__':
    DataPreperation().read_from_json()