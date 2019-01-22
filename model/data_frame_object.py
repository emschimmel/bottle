import pickle
import pandas

from model.state_config import FileName

class DataFrameObject(object):

    uploaded_csv_data = pandas.DataFrame(columns=['ad_id', 'recommended_ad_id', 'rank', 'score'])
    enriched_data = dict()
    # enriched_data = pandas.DataFrame()

    @staticmethod
    def restore():
        DataFrameObject.uploaded_csv_data = pandas.read_csv(FileName.original_file_name(), dtype={'ad_id':str, 'recommended_ad_id':str})

    @staticmethod
    def save_data():
        DataFrameObject.uploaded_csv_data.to_csv(FileName.original_file_name(), index=False)
        DataFrameObject.uploaded_csv_data = pandas.read_csv(FileName.original_file_name(), dtype={'ad_id':str, 'recommended_ad_id':str})

    @staticmethod
    def load_enriched_data():
        with open(FileName.dump_file_name(), 'rb') as f:
            DataFrameObject.enriched_data = pickle.load(f)

    @staticmethod
    def save_enriched_data():
        with open(FileName.dump_file_name(), 'wb') as f:
            pickle.dump(DataFrameObject.enriched_data, f, protocol=pickle.HIGHEST_PROTOCOL)