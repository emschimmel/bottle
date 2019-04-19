import pandas

from model.state_config import FileName


class DataFrameObject(object):

    uploaded_csv_data = pandas.DataFrame(columns=['ad_id', 'recommended_ad_id', 'rank', 'score'])
    uploaded_add_list_data = pandas.DataFrame(columns=['ad_id'])
    uploaded_user_recom_data = pandas.DataFrame(columns=['user','lot_id','rating','auction','number','lot','auction_name','title','interest_group','topcategoryid','topcategory','channel','timestamp'])
    enriched_data = pandas.DataFrame(columns=['ad_id', 'url', 'img_url', 'title', 'price', 'location', 'categories', 'loaded', 'error', 'expired', 'enriched_at', 'extra_data', 'extra_images'])
    enriched_data.sort_index(axis=0)

    @staticmethod
    def restore():
        DataFrameObject.uploaded_csv_data = pandas.read_csv(FileName.original_file_name(), dtype={'ad_id':str, 'recommended_ad_id':str})

    @classmethod
    def save_data(self):
        self.uploaded_csv_data.to_csv(FileName.original_file_name(), index=False)

    @staticmethod
    def restore_add_list_data():
        DataFrameObject.uploaded_add_list_data = pandas.read_csv(FileName.original_data_list_file_name(), dtype={'ad_id': str})

    @classmethod
    def save_add_list_data(self):
        self.uploaded_add_list_data.to_csv(FileName.original_data_list_file_name(), index=False)

    @staticmethod
    def restore_user_recom_data():
        DataFrameObject.uploaded_user_recom_data = pandas.read_csv(FileName.original_user_recom_file_name(), dtype={'user':int, 'lot_id':int, 'rating':float, 'auction':str, 'number':str, 'lot':str, 'auction_name':str, 'title':str, 'interest_group':str, 'topcategoryid':str, 'topcategory':str, 'channel':str}, parse_dates=['timestamp'])

    @classmethod
    def save_user_recom_data(self):
        DataFrameObject.uploaded_user_recom_data.to_csv(FileName.original_user_recom_file_name(), index=False)

    @staticmethod
    def load_enriched_data():
        DataFrameObject.enriched_data = pandas.read_csv(FileName.dump_file_name(), dtype={'ad_id':str, 'url':str, 'img_url':str, 'title':str, 'price':str, 'location':str, 'categories':object, 'loaded':bool, 'error':bool, 'expired':bool, 'enriched_at':str, 'extra_data':object, 'extra_images':object})

    @classmethod
    def save_enriched_data(self):
        self.enriched_data.to_csv(FileName.dump_file_name(), index=False)
